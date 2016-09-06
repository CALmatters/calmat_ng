Overview
========

Calmatters NG is the next gen version of calmatters.org.   It is compmrised of the following main parts

1.  Python 3/Django 9  (pip freeze # for all Python dependencies andversions)
2.  PostgreSQL 9.5
3.  html5, css3, jQuery/JS various
4.  Live:  Nginx, uwsgi

The Django admin uses Django Admin Tools to add functionality.   Extended CMS management is added by customizing the admin.
The first version of the project leveraged Mezzanine.  This new version doesn't use Mezzanine, but some elements were
lifted and added to this project.

The front end is stand post/response with some, but very little javascript async comms back to the server.  
jQuery is used mostly for dynamic frontend code



Development Workflow
====================

*  Developers install a working environment to run the project, including cloning the source
git@github.com:idmloco/calmat_ng.git
(Note, SSH public key needs to be installed in github account.)
*  To begin work on an issue, the developer pulls from the
git repo
*  Once the issue is resolved, the dev can push commits to master
*  The dev or admin can then pull from the master branch on the Landing Path system (code staging)
*  The admin needs to collect the static files and/or restart the python environment
$ ./manage.py collectstatic --noinput
$ sudo service uwsgi restart
*  At this point, product owners and stakeholders can view the changes on http://landingpath.calmatters.org/
*  Once the changes are reviewed, and approved, the admin can merge the changes to production
*  The admin logs into the production system, and resets the production branch to match master
(The assuption is that anything on master can safely be in production, and that that production should hold no special state.)
$  git checkout <production_branch>
$  git reset --hard master


DEV Environment
===============

In a nutshell, you'll need to install Python3, and PostgresSQL 9.5.  Then use virtualenv to build a Python3 environment.
clone the project, and make sure the environment is activated, in order to install the dependencies.  
Use pip install -r requirements.txt

Once the Python library support is installed, copy the local_settings.py.example file to create your own local_settings.py
file.  In here, you need to configure access to your DB.  Now is a good time to create a database in your PostgresSQL 
system.   You can then put the database name and any other auth information in the DATABASES section.  Make sure all the
STRIPE AND MAILCHIMP lines are commented out, or removed for a local enviroment, unless you want to work on those functions.

Once the DB is created, install the DB tables: ./manage.py migrate
You'll also need a superuser:  ./manage.py createsuperuser

At this point, try starting the application:  ./manage.py runserver
http://localhost:8000/
http://localhost:8000/admin




