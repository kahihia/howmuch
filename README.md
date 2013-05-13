howmuch
=======

Code by Howmuch project; Buyer puts the price, Supplier adapts

Buy and Sell Upside



Sample localsettings
--------------------

To customize the settings use another module called localsetting.py
and use: `$VENV/bin/python manage.py runserver  --settings howmuch.localsettings`

`localsettings.py` example:

    from howmuch.settings import *
    import dj_database_url
    DEBUG = True
    TEMPLATE_DEBUG = DEBUG
    DATABASES = {'default':
    	               dj_database_url.config(
              	      default='postgres://joe:@localhost:5432/howmuch')
	        }
