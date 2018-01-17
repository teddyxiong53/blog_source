---
title: Python之Django学习（四）部署到nginx
date: 2018-01-16 17:34:43
tags:
	- python
	- nginx
---





1、安装nginx。`sudo apt-get install nginx`。

2、启动nginx试一下。sudo nginx。如果有错误，解决错误。

3、安装uwsgi。`sudo pip install uwsgi`

4、写一个test.py文件。用来测试uwsgi工作是否支持。文件如下：

```
def application(env, start_response):
	start_response("200 OK", [("Content-Type", "text/html")])
	return "hello"

```

测试命令：`uwsgi --http :8001 --wsgi-file test.py`。然后在浏览器就可以访问了。

5、进行uwsgi配置。

在/etc目录下，新建一个uwsgi.ini文件。这个位置可以修改。我的工程是放在/home/pi/work/django/zqxt_study/blog_admin目录下。

```
[uwsgi]
socket = /home/pi/work/django/zqxt_study/blog_admin/web.sock
chdir = /home/pi/work/django/zqxt_study/blog_admin
wsgi-file = blog_admin/wsgi.py
touch-reload = /home/pi/work/django/zqxt_study/blog_admin/reload
processes = 2
threads = 4
chmod-socket = 664
chown-socket = pi:www-data
vacuum = true
```

我们要理解一下nginx和uwsgi的关系：nginx相当于服务器，uwsgi相当于服务器里的一个程序。

nginx拿到request，交给uwsgi处理得到内容，然后nginx再把内容返回给用户。

uwsgi目前只支持到Python2.7版本。

6、配置nginx。

先在/etc/nginx/sites-available/目录下新建一个文件。就叫myweb.conf。

里面内容如下：

```
server {
    listen 80 default_server;
    #not set server_name, so you can use ip to visit this web directly.
    server_name _;
    #server_name www.myweb.com;
    client_max_body_size 75M;
    location /static {
        alias /home/pi/work/django/zqxt_study/blog_admin/static;
    }
    location / {
        uwsgi_pass  unix:///home/pi/work/django/zqxt_study/blog_admin/web.sock;
        include /etc/nginx/uwsgi_params;
    }
}

```

然后建立一个软链接到/etc/nginx/sites-enabled目录下，这样就相当于把网站使能了。另外把default的那个删掉。以免干扰。

```
sudo ln -s /etc/nginx/sites-available/myweb.conf /etc/nginx/sites-enabled/myweb.conf
```



7、启动运行。

```
sudo uwsgi --ini /etc/uwsgi.ini &
sudo nginx
```

然后运行测试就好了。





