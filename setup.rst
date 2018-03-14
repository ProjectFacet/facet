Setup
=====

In order to run Facet locally, here are instructions for how to structure your setup.

Development Environment
-----------------------

Prerequisites:

- Python 2.7 (currently people use 2.7.10)

- PostgreSQL 9.4

Go into the repo root and

  ``virtualenv-2.7 venv`` or ``virtualenv venv``

and then ::

  source venv/bin/activate
  pip install -r requirements/local.txt

  # create postgresql user "facet" which will own the database
  createuser -P facet

If you get error(s) from the pip install such as::

  Could not find a version that satisfies the requirement django-watson==1.2.0#egg=watson...
  No matching distribution found for django-watson==1.2.0#egg=watson...

Then your virtual environment may have a buggy version of pip. Try "upgrading" pip to a good version::

  pip install -U pip==8.1.1

Enter a password, and then::

  # create postgresql database "facet", owned by postgresql user "facet"
  createdb -O facet facet

  # run Django's "migrate" command, which will run newer migrations than initial
  python project/manage.py migrate

This will give you a superuser account, "admin", with the password "admin".

Ongoing Setup
+++++++++++++

As changes are made to the model, you'll want to migrate your database.
You can keep up with this with::

  python project/manage.py migrate

To update the search engine indexes::

  python project/manage.py buildwatson

To launch a development webserver::

  python project/manage.py runserver
