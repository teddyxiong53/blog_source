---
title: nginx（1）
date: 2018-08-11 22:14:44
tags:
	- 网络

---



下载安装，用windows版本。

http://nginx.org/en/download.html

不大，才1.4M。

解压后的目录结构。

```
├─conf
├─contrib
│  ├─unicode2nginx
│  └─vim
│      ├─ftdetect
│      ├─ftplugin
│      ├─indent
│      └─syntax
├─docs
├─html
├─logs
└─temp
```

为了方便使用，我们写一个startup.bat文件。跟nginx.exe文件放在同一个目录下。

```
@echo off
nginx -s stop

nginx -t -c conf/nginx.conf

nginx -v

nginx -c conf/nginx.conf
```

因为我的windows默认把80端口给了IIS服务器。所以要先修改一下nginx.conf文件，把端口改成8080。然后访问。

http://localhost:8080/

可以看到页面了。

现在我们看看如何配置一个反向代理器。



反向代理最大的用途就是做负载均衡。



nginx属于典型的微内核设计。内核非常简洁和优雅。同时也有很好的扩展性。



# windows下配置php在nginx

1、下载php。

https://windows.php.net/downloads/releases/archives/php-5.2.16-nts-Win32-VC6-x86.zip

nginx下的php是以fastcgi的方式运行的。所以我们下载的是非线程安全的nts的包。

2、另外还需要RunHiddenConsole。

http://redmine.lighttpd.net/attachments/660/RunHiddenConsole.zip

这个文件很小，只有2K。

3、解压php的压缩包。

我把内容放在D:\work\nginx\php5这个目录下。

把php.ini-recommend改名为php.ini。

修改内容：

```
1、把extension_dir修改为绝对路径
extension_dir ="D:\work\nginx\php5"
2、打开extension的php_mysql.dll和php_mysqli.dll的分号注释。
3、把libmysql.dll拷贝到c:\windows目录下去。
```

做完上面这些步骤，php就可以支持mysql了。

接下来，我们就让php跟nginx结合。

我们找到这一行：

```
;cgi.fix_pathinfo=1
```

把分号去掉，这个是打开cgi的。

接下来要在nginx.conf里进行设置。

我把网站的根目录指定为D:\work\nginx\www。

我们新建一个脚本，就叫startup-php.bat。写入：

```
@echo off
D:/work/nginx/php5/php-cgi.exe -b 127.0.0.1:9000 -c D:/work/nginx/php5/php.ini
```

但是我这个运行，怎么都跑不起来。

问题在于，指定网站的根目录不能在nginx目录之外，我把目录改回到默认的html目录，就正常了。

我开发就这么做。



后面发现有语法错误的时候，直接就是提示页面找不到，这样对于开发定位问题是很麻烦的。

是要在php.ini里，把这一行修改 如下：

```
display_errors = On
```

默认是off的，所以看不到错误信息。

## 升级到最新版本的php

我上面的搭建，都是安装教程来的。所以用了5.2的版本，这个版本太旧了一点。

我另外下载了这个版本。

php-7.0.31-nts-Win32-VC14-x64

放在这里：D:\work\nginx\php7



nginx的配置

用nginx -V查看。Ubuntu下安装的，默认配置是这样：

````
configure arguments: 
--with-cc-opt='-g -O2 -fPIE -fstack-protector-strong -Wformat -Werror=format-security -Wdate-time -D_FORTIFY_SOURCE=2' 
--with-ld-opt='-Wl,-Bsymbolic-functions -fPIE -pie -Wl,-z,relro -Wl,-z,now' 
--prefix=/usr/share/nginx 
--conf-path=/etc/nginx/nginx.conf 
--http-log-path=/var/log/nginx/access.log 
--error-log-path=/var/log/nginx/error.log 
--lock-path=/var/lock/nginx.lock 
--pid-path=/run/nginx.pid 
--http-client-body-temp-path=/var/lib/nginx/body 
--http-fastcgi-temp-path=/var/lib/nginx/fastcgi 
--http-proxy-temp-path=/var/lib/nginx/proxy 
--http-scgi-temp-path=/var/lib/nginx/scgi 
--http-uwsgi-temp-path=/var/lib/nginx/uwsgi 
--with-debug 
--with-pcre-jit 
--with-ipv6 
--with-http_ssl_module 
--with-http_stub_status_module 
--with-http_realip_module 
--with-http_auth_request_module 
--with-http_addition_module 
--with-http_dav_module 
--with-http_geoip_module 
--with-http_gunzip_module 
--with-http_gzip_static_module 
--with-http_image_filter_module 
--with-http_v2_module 
--with-http_sub_module 
--with-http_xslt_module 
--with-stream 
--with-stream_ssl_module
--with-mail 
--with-mail_ssl_module 
--with-threads

````



# 参考资料

官网文档

http://www.nginx.cn/doc/

nginx简易教程

https://www.cnblogs.com/jingmoxukong/p/5945200.html

Nginx模块开发入门

https://www.cnblogs.com/leoo2sk/archive/2011/04/19/nginx-module-develop-guide.html

windows下配置nginx+php环境

https://www.cnblogs.com/yiwd/p/3679308.html