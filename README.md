DIGIDO - METAVERSE PROJECT
==========================

THE STACK
---------
* Django application
* Runs on heroku cedar stack
* Backed by Postgresql database

PREREQUISITE
------------
These instructions are for Mac OSX only. sudo where necessary.
* Install HomeBrew

    > /usr/bin/ruby -e "$(curl -fsSL https://raw.github.com/gist/323731)"

* Install Git

    > brew install git

* Install Postgresql

    > brew install postgresql
    > initdb /usr/local/var/postgres
    > mkdir -p ~/Library/LaunchAgents
    > cp /usr/local/Cellar/postgresql/9.1.1/org.postgresql.postgres.plist ~/Library/LaunchAgents/
    > launchctl load -w ~/Library/LaunchAgents/org.postgresql.postgres.plist
    > createdb metaverse

* gem install heroku
* gem install foreman
* python


QUICK START
-----------
1. Get repository access from Alan.
2. git clone <see repo url>
3. cd digido
4. ./setup.sh
5. source .ve/bin/activate
6. createdb metaverse
7. cd webverse
8. manage.py syncdb
9. manage.py migrate
10. To start the server, you must run it from within the digido directory.
    Otherwise the TEMPLATE_DIR will not be found. This is to stay consistent
    with how it'd run within Heroku which puts the app in different directory.

        > foreman start

        or

        > python metaverse/manage.py runserver

11. Load admin user

    >python metaverse/manage.py loaddata admin_users
    

**Note:** Default user name and password are admin/asdf

KEY LINKS
---------
* Learn about [Django on Heroku](http://devcenter.heroku.com/articles/django)
* Admin portal for metaverse is at http://localhost:5000/admin **Note** that port might be different check logs


DEPLOYMENT
----------
* Make sure you have access to the heroku app.
* Add the heroku remote:

    > git remote add heroku <heroku git url>

* Push your code up:

    > git push heroku master

* View your app:

    > heroku open

