
GROUP_NAME = 'Your Family Name'

PEOPLE = [
    (
        ('Couple First Name 1', 'Couple First Name 2'),
        ('email 1', 'email 2')
    ),
    (
        ('Single First Name 3', ),
        ('email 3', )
    ),
]

MAIL_SUBJECT = "Christmas {group_name} {year}"
MAIL_BODY = (
    "This year, {people_from}, you will give {people_to} a present.\n"
    "\n"
    "-- \n"
    "Santa Claus\n"
)
MAIL_FROM = 'your-email'
MAIL_FROM_NAME = 'Santa Claus'


def make_mail_body(people_from, people_to):
    """
    :param people_from: tuple ('First Name 1', ...)
    :param people_to: tuple ('First Name A', ...)
    :return: str
    """

    if len(people_from[0]) == 1:
        people_from_str = people_from[0]
    else:
        people_from_str = "{} and {}".format(*people_from)

    if len(people_to[0]) == 1:
        people_to_str = people_to[0]
    else:
        people_to_str = "{} and {}".format(*people_to)

    return MAIL_BODY.format(
        people_from=people_from_str,
        people_to=people_to_str
    )
