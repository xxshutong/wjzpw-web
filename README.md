WJZPW - WEB PROJECT
==========================

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
	$ psql -> CREATE ROLE wjzpw WITH LOGIN CREATEDB ENCRYPTED PASSWORD 'wjzpw' #创建用户
	$ su root
	$ ./wjzpw/manage.py syncdb -> no
	$ ./wjzpw/manage.py migrate
	$ python ./wjzpw/manage.py loaddata ./wjzpw/web/fixtures/*

11.初始化环境变量

    $ export <ENV_NAME>=<ENV_VALUE>
	
可用的环境变量有
	
	* DEBUG=true
	* DB_USERNAME=wjzpw
 	* DB_PASSWORD=wjzpw
	* HOME_URL=http://localhost:8000/
	* EMAIL_HOST_USERNAME=ipswitcher001@gmail.com
	* EMAIL_HOST_PASSWORD=###

12.复制第三方静态文件

    $ ./wjzpw/manage.py collectstatic

13.运行吴江-招聘网
	
	$ foreman start -p 80
	

部署中需要注意的问题
----------
**Note:** 后台管理默认的管理账户用户名和密码是admin/asdf

**Note:** 如果运行后出现decoder zip not available的问题可以试试以下命令:

    $ sudo apt-get build-dep python-imaging

**Note:** 如果要重启postgresql可杀掉进程后执行一下语句

    $ /usr/lib/postgresql/9.1/bin/postgres -D /var/lib/postgresql/9.1/main -c config_file=/etc/postgresql/9.1/main/postgresql.conf

**Note:** 如果无法上传图片可参考如下解决办法

    http://crazysky.iteye.com/admin/blogs/1303821

更新
----------

    $ git pull origin master
    $ ./wjzpw/manage.py migrate
    $ $ ./wjzpw/manage.py collectstatic


迁徙
----------
    git clone->restore database->restore uploaded images->set environment