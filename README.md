WJZPW - WEB PROJECT
==========================

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
    

部署(阿里云)
----------
1.确保数据盘已经挂载

* http://help.aliyun.com/manual?spm=0.0.0.115.AVOKFx&helpId=271

2.安装git

	$ sudo apt-get install git-core
	
3.配置git

* https://help.github.com/articles/set-up-git#platform-linux
* https://help.github.com/articles/generating-ssh-keys

4.安装Postgresql

	$ sudo apt-get install postgresql
	$ sudo passwd postgres #设置postgres账户密码
	$ sudo -u postgres psql #联合下一步修改postgres账户密码
	$ alter user postgres with password 'postgres'
	
5.安装ruby gems(版本号必须高于1.3.5)

	$ sudo apt-get install ruby #安装ruby
	$ 下载最新版本 [ruby gems](http://rubyforge.org/frs/?group_id=126)
	$ sudo ruby setup.rb
	$ sudo apt-get install rubygems
	
6.安装foreman(2.6.1)

	$ wget http://rubygems.org/downloads/foreman-0.26.1.gem
	$ sudo gem install foreman-0.26.1.gem

7.安装virtualenv

	$ sudo apt-get install python-setuptools
	$ sudo easy_install virtualenv

8.安装python

	$ sudo apt-get install libpq-dev python-dev

9.下载并初始化吴江-招聘网项目

	$ git clone git@github.com:xxshutong/wjzpw-web.git
	$ cd wjzpw-web
	$ ./setup.sh
	$ source .ve/bin/activate
	$ su postgres
	$ createdb wjzpw
	$ su root
	$ ./wjzpw/manage.py syncdb
	
	
**Note:** 后台管理默认的管理账户用户名和密码是admin/asdf

更新
----------
迁徙
----------
