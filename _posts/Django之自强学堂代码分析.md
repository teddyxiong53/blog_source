---
title: Django之自强学堂代码分析
date: 2018-07-24 22:30:02
tags:
	- Python

---



先下载代码。在我的虚拟机里部署跑起来先。

我在一个新安装的Ubuntu里，16.04, 64位版本。

添加一个admin用户。

home目录是/home/admin。

把zqxt的源代码放在/home/admin目录下。



https的太麻烦了。我把https的干掉。

去掉nginx.conf里https相关内容。得到这个样子。

```
user  admin;
worker_processes  2;

#error_log  logs/error.log;
#error_log  logs/error.log  notice;
#error_log  logs/error.log  info;

#pid        logs/nginx.pid;


events {
    worker_connections  1024;
}

# load modules compiled as Dynamic Shared Object (DSO)
#
#dso {
#    load ngx_http_fastcgi_module.so;
#    load ngx_http_rewrite_module.so;
#}

http {
    include       mime.types;
    default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    #access_log  logs/access.log  main;
    access_log /var/log/nginx/access.log;
    error_log /var/log/nginx/error.log;
    sendfile        on;
    #tcp_nopush     on;

    #keepalive_timeout  0;
    keepalive_timeout  65;

    gzip  on;

    server {
        listen       80;
        server_name  _;
        charset utf-8;
        #rewrite ^(.*)$  https://$host$1 permanent;
		
		location /favicon.ico {
           alias /home/admin/zqxt/static/favicon.ico;
       }

       location ~ ^/(media|static)/ {
           root /home/admin/zqxt;
           expires 30d;
           access_log   off;
       }

       location ~* \.(htm|js|css|jpe?g|png|gif|zip|rar|txt|xml|xsl)$ {
           root /home/admin/zqxt;
           access_log   off;
           expires      30d;
       }

       location / {
           uwsgi_pass  unix:///home/admin/zqxt.sock;
           include uwsgi_params;
       }
    }


}
```



重启nginx。

这时候访问，会得到502的错误。

肯定是uwsgi_pass这一块的配置还没有好。

nginx和uwsgi都是文本服务器，nginx负责静态内容，而uwsgi负责Python这样的动态内容。

二者配合，一起提供web服务。

uwsgi实现了多个协议，如wsgi协议，http协议。

请求和响应的流程如下：

```
request > nginx > uwsgi > django > uwsgi > nginx > response
```



uwsgi的ini文件，已经提供了。是zqxt.ini这个文件。

所以我先启动uwsgi。

```
sudo uwsgi --ini /home/admin/zqxt/zqxt.ini &
```

我修改如下：

```
[uwsgi]
basedir = /home/admin
chdir = %(basedir)/zqxt
venv = %(basedir)/.envs/zqxt/

;http-socket = 127.0.0.1:7001
socket = /home/admin/zqxt.sock
wsgi-file = zqxt/wsgi.py

chmod-socket = 660
;chown-socket=nobody:nobody
;uid=nobody
;gid=nobody

process = 2
threads = 4
master = true
vacuum = true

buffer-size = 65535
;stats = 0.0.0.0:5000
```



启动报错。

```
Set PythonHome to /home/admin/.envs/zqxt/
ImportError: No module named site
VACUUM: unix socket /home/admin/zqxt.sock removed.
```

是因为这里要一个venv，名字叫zqxt的。所以我需要先生成这样一个虚拟环境。

我们需要先安装virtualenv，再安装virtualenvwrapper。

在/home/admin目录下新建一个.envs的目录。

然后在.bashrc里加入下面的语句：

```
export WORKON_HOME=$HOME/.envs
source /usr/local/bin/virtualenvwrapper.sh
```

然后source .bashrc。

```
admin@ubuntu:~$ source .bashrc
virtualenvwrapper.user_scripts creating /home/admin/.envs/premkproject
virtualenvwrapper.user_scripts creating /home/admin/.envs/postmkproject
virtualenvwrapper.user_scripts creating /home/admin/.envs/initialize
virtualenvwrapper.user_scripts creating /home/admin/.envs/premkvirtualenv
virtualenvwrapper.user_scripts creating /home/admin/.envs/postmkvirtualenv
virtualenvwrapper.user_scripts creating /home/admin/.envs/prermvirtualenv
virtualenvwrapper.user_scripts creating /home/admin/.envs/postrmvirtualenv
virtualenvwrapper.user_scripts creating /home/admin/.envs/predeactivate
virtualenvwrapper.user_scripts creating /home/admin/.envs/postdeactivate
virtualenvwrapper.user_scripts creating /home/admin/.envs/preactivate
virtualenvwrapper.user_scripts creating /home/admin/.envs/postactivate
virtualenvwrapper.user_scripts creating /home/admin/.envs/get_env_details
```

然后创建一个虚拟环境，名字叫zqxt。

创建会失败。我看是因为我的~/.pip/pip.conf导致的。我先把这个文件改个名字。

```
mkvirtualenv zqxt
```

这样成功了。

我再把~/.pip/pip.conf 改回来。

然后安装需要的文件。在虚拟环境下。

```
(zqxt) admin@ubuntu:~$ pip install -r ./zqxt/requirements.txt
(zqxt) admin@ubuntu:~$ 
```

但是失败了。

```
EnvironmentError: mysql_config not found
```



先安装mysql。

```
sudo apt-get install mysql-server
```

安装中间需要输入root密码两次。

然后配置mysql。

```
sudo mysql_secure_installation
```

一直回车就好了。



然后安装：

```
sudo apt-get install libmysqlclient-dev
```

然后继续

```
pip install -r ./zqxt/requirements.txt
```

这次安装就成功了。



现在再启动uwsgi。没有报错了。

但是访问，还是提示报错502。

查看错误日志。

```
2018/07/31 23:15:04 [crit] 29611#29611: *1 connect() to unix:///home/admin/zqxt.sock failed (13: Permission denied) while connecting to upstream, client: 192.168.211.1, server: _, request: "GET / HTTP/1.1", upstream: "uwsgi://unix:///home/admin/zqxt.sock:", host: "192.168.211.10"
2018/07/31 23:16:05 [crit] 29611#29611: *6 connect() to unix:///home/admin/zqxt.sock failed (13: Permission denied) while connecting to upstream, client: 127.0.0.1, server: _, request: "GET / HTTP/1.1", upstream: "uwsgi://unix:///home/admin/zqxt.sock:", host: "localhost"
```

参考网上的，把sock文件的权限 改成666，还是不行。

我再安装网上的，把nginx.conf里的user改成root。

再试。还是报错。

```
1 upstream prematurely closed connection while reading response header from upstream,
```

这篇文章讲到了跟我类似的问题。

https://blog.csdn.net/libing1991_/article/details/48049227



# 参考资料

1、跨过Nginx上基于uWSGI部署Django项目的坑

https://www.cnblogs.com/qingspace/p/6838747.html

2、mysql-python安装时EnvironmentError: mysql_config not found

https://www.cnblogs.com/xiazh/archive/2012/12/12/2814289.html

3、Ubuntu 16.04 上安装 MySQL 5.7 教程

https://www.linuxidc.com/Linux/2017-05/143864.htm

4、nginx 502错误 failed (13: Permission denied)

https://blog.csdn.net/liangpz521/article/details/40112013