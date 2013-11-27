#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random
import pprint
import datetime
import smtplib
from email.header import Header
from email.mime.text import MIMEText
import time


try:
    import settings
except ImportError:
    raise ImportError("Error: you must provide a settings.py file")


def send_mail(present_from, present_to):

    people_from = people_to = None
    # retrieve people_from and people_to
    for people in settings.PEOPLE.values():
        if people[0] == present_from:
            people_from = people
        elif people[0] == present_to:
            people_to = people

    assert people_from is not None
    assert people_to is not None
    assert people_to != people_from

    subject = settings.MAIL_SUBJECT.format(datetime.datetime.now().year)
    body = settings.MAIL_BODY.format(people_from=people_from[1], people_to=people_to[1])

    mail_from = settings.MAIL_FROM.format(email=settings.EMAIL_HOST_USER)  # prevents spams
    mail_to = people_from[2] if not settings.DEBUG else settings.DEBUG_MAIL

    msg = MIMEText(body, _charset="UTF-8")
    msg['Subject'] = Header(subject, charset="UTF-8")
    msg['From'] = mail_from

    if settings.DEBUG:
        print "="*50
        print subject
        print body
        print ""

    print "Send email to {}".format(mail_to)
    server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
    if settings.EMAIL_USE_TLS:
        server.ehlo()
        server.starttls()
        server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    server.sendmail(mail_from, mail_to, msg.as_string())
    server.quit()
    time.sleep(4)  # prevents spams


def random_presents():
    winners = {}
    # brutal, not the good way to solve problem. TODO: changes method
    for number, people in settings.PEOPLE.items():
        slug = people[0]
        present_found = False
        cycle = 0
        while not present_found:
            cycle += 1
            if cycle > 1000:
                raise RuntimeError('Too many cycles for {} (already found: {}'.format(slug, winners))

            try_for = settings.PEOPLE[random.randint(1, len(settings.PEOPLE))][0]
            if try_for not in settings.CONSTRAINTS[slug] and try_for != slug and try_for not in set(winners.values()):
                present_found = True
                winners[slug] = try_for

    # checks:
    assert set(winners.values()) != 10

    return winners

if __name__ == '__main__':
    winners = random_presents()
    if settings.DEBUG:
        pprint.pprint(winners)
    if settings.LOG:
        with open('{}_generated.log'.format(datetime.datetime.now().year), mode='w+') as outfile:
            outfile.write(pprint.pformat(winners))

    for key, value in winners.items():
        send_mail(key, value)
