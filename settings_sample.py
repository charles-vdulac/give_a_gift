#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = True
DEBUG_MAIL = u'debug_mail@yopmail.com'  # In order to test mails.
LOG = False

# define people list (slug, name, email)
PEOPLE = {
    1: ('marie', u'FIRST_NAME LAST_NAME', 'marie_mail@yopmail.com'),
    2: ('charles', u'FIRST_NAME LAST_NAME', 'charles_mail@yopmail.com'),
    3: ('simon', u'FIRST_NAME LAST_NAME', 'simon_mail@yopmail.com'),
}

# define constraints: left slug can not offer presents to right slugs.
CONSTRAINTS = {
    'marie': ['charles'],
    'charles': ['marie'],
    'simon': [],
}

# email provider
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'XXXX'
EMAIL_HOST_PASSWORD = 'XXXXX'
EMAIL_USE_TLS = True

# MAILS CONTENT
MAIL_SUBJECT = u"Cadeau de noël {year}"  # include year (eg. 2013)
MAIL_BODY = u"Cette année, {people_from}, tu fais un cadeau à {people_to}.\n" \
            u"Mais chut !! Personne ne le sait.\n" \
            u"\n-- \nLe logiciel Papa Noël"
MAIL_FROM = u"Le logiciel Papa Noël <{email}>"
