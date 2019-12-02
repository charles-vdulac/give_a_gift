#!/usr/bin/env python3
import datetime
import json
import logging
import os
import random
import smtplib
import time
from collections import namedtuple
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import requests
from clize import run


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()


# See sample_settings.py file.
# This declaration is here for code inspection.
settings = namedtuple(
    "settings",
    (
        "PEOPLE",
        "GROUP_NAME",
        "MAIL_SUBJECT",
        "MAIL_BODY",
        "MAIL_FROM",
        "MAIL_FROM_NAME",
        "make_mail_body",
    ),
)


def prepare_email(present_from, present_to):
    people_from = people_to = None
    # Retrieve people_from and people_to
    for people in settings.PEOPLE:
        if people[0] == present_from:
            people_from = people
        elif people[0] == present_to:
            people_to = people

    assert people_from is not None
    assert people_to is not None
    assert people_to != people_from

    body = settings.make_mail_body(people_from[0], people_to[0])

    subject = settings.MAIL_SUBJECT.format(
        year=datetime.datetime.now().year, group_name=settings.GROUP_NAME
    )

    from_email = settings.MAIL_FROM
    from_mail_name = settings.MAIL_FROM_NAME
    to_emails = people_from[1]

    logger.debug("=" * 50)
    logger.debug(f"from_email={from_email}")
    logger.debug(f"from_mail_name={from_mail_name}")
    logger.debug(f"to_emails={to_emails}")
    logger.debug(f"subject={subject}")
    logger.debug(f"Body={body}")

    return {
        "from_email": from_email,
        "from_mail_name": from_mail_name,
        "subject": subject,
        "to_emails": to_emails,
        "body": body,
    }


def send_via_gmail(from_email, from_mail_name, subject, to_emails, body):
    """
    Hacking Gmail Security

    In a nutshell, google is not allowing you to log in via smtp lib because
    it has flagged this sort of login as 'less secure', so what you have to
    do is go to this link while you're logged in to your google account, and
    allow the access:

    1. Allow less secure apps: ON. (https://myaccount.google.com/lesssecureapps)
    2. Display Unlock Captcha. (https://accounts.google.com/DisplayUnlockCaptcha)
    3. Enable IMAP Access (https://mail.google.com/mail/#settings/fwdandpop)

    Requires GMAIL_USER and GMAIL_PASSWORD env variables
    """

    logger.info(f"Sending email to {to_emails} via Gmail...")

    if not os.environ.get("GMAIL_PASSWORD"):
        os.environ["GMAIL_PASSWORD"] = input("What's your password? ")

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(user=os.environ["GMAIL_USER"], password=os.environ["GMAIL_PASSWORD"])

    for to_email in to_emails:

        msg = MIMEMultipart()
        msg["From"] = f"{from_mail_name} <{from_email}>"
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body))

        server.sendmail(from_email, to_email, msg.as_string())

        time.sleep(random.randint(1, 5))

        logger.info(f"Email sent to {to_email}")

    server.close()
    time.sleep(random.randint(1, 5))


def send_mail(**kwargs):
    """
    Send email via the right provider
    """
    if "GMAIL_USER" in os.environ:
        send_via_gmail(**kwargs)
    else:
        logger.error("Missing environment variables to be able to send emails.")


def backup(winners):

    backup_file = "{}_{}_results.json".format(
        datetime.datetime.now().year, settings.GROUP_NAME.lower().replace(" ", "-")
    )

    def t_str(data):
        return "{} and {}".format(*data) if len(data) == 2 else data[0]

    logger.info(f"Backupping results to {backup_file} file...")

    if os.path.isfile(backup_file):
        raise RuntimeError(f"File {backup_file} already exist")

    with open(backup_file, mode="w") as outfile:
        outfile.write(json.dumps({t_str(k): t_str(v) for k, v in winners.items()}))


def load_backup(year):

    backup_file = "{}_{}_results.json".format(
        year, settings.GROUP_NAME.lower().replace(" ", "-")
    )
    if not os.path.isfile(backup_file):
        return {}

    logger.info(f"Loading {backup_file} file...")

    def f_str(data):
        items = data.replace(" et ", " and ").split(" and ")
        return (items[0], items[1]) if len(items) == 2 else (items[0],)

    with open(backup_file, mode="r") as outfile:
        return {f_str(k): f_str(v) for k, v in json.loads(outfile.read()).items()}


def solve():
    """
    Solve the constraints.
    Inputs:
        - settings.PEOPLE
        - last year results

    :return: dict {people_from_tuple: people_to_tuple}
    """

    winners = {}

    last_year = load_backup(datetime.datetime.now().year - 1)

    for index, people in enumerate(settings.PEOPLE):
        # Brutal, not the good way to solve problem.

        present_from = people[0]
        present_found = False
        cycle = 0
        while not present_found:

            cycle += 1
            if cycle > 1000:
                raise RuntimeError(
                    f"Unable to find a solution for {present_from} (already found: "
                    f"{winners}"
                )

            rand = random.randint(0, len(settings.PEOPLE) - 1)
            present_to = settings.PEOPLE[rand][0]

            if rand == index:
                continue

            if present_to in winners.values():
                continue

            if last_year and last_year.get(people[0]) == present_to:
                continue

            present_found = True
            winners[present_from] = present_to

    assert set(winners.values()) != 10

    logger.info("The solver found a solution.")
    logger.debug(f"winners={winners}")

    return winners


def main(apply=False):

    winners = solve()

    if apply:
        backup(winners)
    else:
        logger.info("Do not backup results")

    for present_from, present_to in winners.items():

        kwargs = prepare_email(present_from, present_to)

        if not apply:
            logger.info(f"Do not sent any email to {present_from}")
            continue

        send_mail(**kwargs)


def local_handler(settings_file, *, apply=False, verbose=False):
    """
    Random drawing in a group to designate who will receive a gift.

    :param settings_file: settings file to load
    :param apply: Send emails to recipients
    :param verbose: Increase output verbosity
    """

    global settings

    settings = __import__(settings_file.split(".py")[0])
    for item in settings.PEOPLE:
        assert isinstance(item[0], tuple)
        assert isinstance(item[1], tuple)

    logger.setLevel(level=logging.DEBUG if verbose else logging.INFO)

    main(apply=apply)


if __name__ == "__main__":
    run(local_handler)
