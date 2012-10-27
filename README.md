WJZPW - WEB PROJECT
==========================

THE STACK
---------
* Django application
* Runs on heroku cedar stack
* Backed by Postgresql database

PREREQUISITE
------------
These instructions are for Ubuntu only. sudo where necessary.
* Install Git
    > sudo apt-get install git-core
    > Configure for your github account in local machine, refer to https://help.github.com/articles/set-up-git

* Install Postgresql
    > sudo apt-get install postgresql
    > sudo passwd postgres(Change password for postgres)
    > sudo -u postgres psql
    > alter user postgres with password 'postgres'

* Install ruby gems(Version must be bigger than 1.3.5)
    > sudo apt-get install ruby
    > http://rubyforge.org/frs/?group_id=126(Download the latest version)
    > sudo ruby setup.rb
    > sudo apt-get install rubygems

* gem install foreman(2.6.1)
    Download 2.6.1 manually(http://rubygems.org/downloads/foreman-0.26.1.gem)
    > wget http://rubygems.org/downloads/foreman-0.26.1.gem
    > sudo gem install foreman-0.26.1.gem

* python

* Install virtualenv
    > sudo apt-get install python-setuptools
    > sudo easy_install virtualenv


QUICK START
-----------
1. Get repository access from xxshutong@gmail.com.
2. git clone git@github.com:xxshutong/wjzpw-web.git
3. cd wjzpw-web
4. sudo apt-get install libpq-dev python-dev
5. ./setup.sh
6. source .ve/bin/activate
7. createdb wjzpw
8. ./wjzpw/manage.py syncdb
9. ./wjzpw/manage.py migrate
10. To start the server, you must run it from within the wjzpw-web directory.
    Otherwise the TEMPLATE_DIR will not be found. This is to stay consistent
    with how it'd run within Heroku which puts the app in different directory.

        > foreman start

        or

        > python wjzpw/manage.py runserver

11. Load initialized data

    >python ./wjzpw/manage.py loaddata ./wjzpw/web/fixtures/*
    

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

