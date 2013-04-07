#!/bin/sh

sudo -u postgres dropdb howmuch
sudo -u postgres createdb howmuch
python manage.py syncdb --settings howmuch.localsettings
python categories_setup.py
python manage.py runserver --settings howmuch.localsettings
