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

Install Solr
---------------------

For install Solr you need use:

curl -O http://apache.mirrors.tds.net/lucene/solr/3.5.0/apache-solr-3.5.0.tgz
tar xvzf apache-solr-3.5.0.tgz
cd apache-solr-3.5.0
cd example
java -jar start.jar

for more info visit http://django-haystack.readthedocs.org/en/latest/installing_search_engines.html
