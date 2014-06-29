#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = u'twmht'
SITENAME = u'技術筆記'
SITEURL = 'http://twmht.github.io/blog'

TIMEZONE = 'Asia/Taipei'

DEFAULT_LANG = u'en'
DEFAULT_DATE = 'fs'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
THEME = 'pelican-theme/pelican-fresh'
GOOGLE_CUSTOM_SEARCH = '011100128719699788018:4mb0t5kqbse'


# Blogroll
LINKS =  (('Pelican', 'http://getpelican.com/'),
          ('pygments', 'http://pygments.org/docs/lexers/'),
          ('Jinja2', 'http://jinja.pocoo.org/'),
          ('Author', 'http://twmht.github.io'),
          ('Luckycat','http://luckycat.kshs.kh.edu.tw/'),
          ('Markdown','http://warpedvisions.org/projects/markdown-cheat-sheet.md'))

# Social widget
SOCIAL = (('Github', 'https://github.com/twmht'),
          ('Facebook', 'https://www.facebook.com/profile.php?id=1793746917'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
RELATIVE_URLS = True
ARTICLE_URL = 'posts/{date:%Y}/{date:%m}/{category}/{slug}.html'
ARTICLE_SAVE_AS = 'posts/{date:%Y}/{date:%m}/{category}/{slug}.html'
STATIC_PATHS = ['images', 'pdf']
#FILES_TO_COPY = ( ('extra/favicon.ico', 'favicon.ico'),)
