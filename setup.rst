Setup
=====

Development Environment
-----------------------

Prerequisites:

- Python 2.7 (currently people use 2.7.10)

- PostgreSQL 9.4 (set up to bypass password requirements when connecting locally, as our
  :py:data:`frodo.settings.base.DATABASES` entry does not include password. This is
  the standard setup from OSX's Postgres.app)

Go into the repo root and

  ``virtualenv-2.7 venv`` or ``virtualenv venv``  

and then ::

  source venv/bin/activate
  pip install -r requirements/local.txt

  # create postgresql user "frodo" which will own the database
  createuser -P frodo

If you get error(s) from the pip install such as::

  Could not find a version that satisfies the requirement django-watson==1.2.0#egg=watson...
  No matching distribution found for django-watson==1.2.0#egg=watson...

Then your virtual environment may have a buggy version of pip. Try "upgrading" pip to a good version::

  pip install -U pip==8.1.1

Enter a password, and then::

  # create postgresql database "frodo", owned by postgresql user "frodo"
  createdb -O frodo frodo

  # Import data
  psql frodo < initial.sql

  # run Django's "migrate" command, which will run newer migrations than initial
  python project/manage.py migrate

This will give you a superuser account, "admin", with the password "admin".

Ongoing Setup
+++++++++++++

As changes are made to the model, you'll want to migrate your database.
You can keep up with this with::

  python project/manage.py migrate

To load initial data::

  python project/manage.py loaddata curriculum sis auth

To update the search engine indexes::

  python project/manage.py buildwatson

To launch a development webserver::

  python project/manage.py runserver

Links to Curriculum
+++++++++++++++++++

Frodo checks for the presence of the curriculum materials on-disk before showing links
for things like slides, handouts, demo ZIP files, etc. On the production server, it knows
to look for the real location of these. On your development environment, you can either
ignore this feature (in which case it won't show you links) or you can make sure you have
a local directory with the curriculum. (This is nice, but optional).

Set an environment variable in your frodo directory called `CURRICULUM_DIR`.

Set it equal to where the
`Hackbright Curriculum <https://github.com/hackbrightacademy/fellowship>`_ directory is on *your* machine.::

  export CURRICULUM_DIR='/path/to/your/fellowship/curriculum'


If you don't have access to the Hackbright fellowship curriculum, then sorry, your
links will never work. But they won't break stuff, either!

Deployment Setup
----------------

Prerequisites:

- Python 2.7 (currently people use 2.7.10)

- PostgreSQL 9.4

Go into the repo root and::

  virtualenv-2.7 venv
  source venv/bin/activate
  pip install -r requirements.txt
  createuser -P frodo

Enter a password, and then::

  createdb -O frodo frodo
  python project/manage.py migrate
  python project/manage.py createsuperuser

Enter superuser info username and password.

Copy development's `project/env-production.py` to `project/env.py`. This file contains
sensitive information, so it will never be in version control. (If you need this file,
you'll need to get it from an existing deployment server or ask Joel; it's not in Git).

Then set up the stuff for our proxy/edge servers::

  sudo ln -s $(pwd)/conf/nginx/*-production.conf /etc/nginx/sites-enabled/
  sudo ln -s $(pwd)/conf/uwsgi/*.ini /etc/uwsgi/apps-enabled/
  sudo /etc/init.d/uwsgi restart
  sudo /etc/init.d/nginx reload
  ./up

Ongoing Support
+++++++++++++++

The `up` script does everything needed to pull a new version of the app and
update the development environment (and if additional steps are added, **please add
them to this**):

.. literalinclude:: up
    :language: bash




