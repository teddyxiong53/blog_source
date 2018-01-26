---
title: alpine（二）安装WordPress
date: 2018-01-26 15:36:12
tags:
	- alpine
	- WordPress

---



官方描述在这里：https://wiki.alpinelinux.org/wiki/WordPress

# 安装

1、安装需要的软件包：

```
apk add lighttpd \
php5-common php5-iconv php5-json php5-gd php5-curl php5-xml php5-pgsql php5-imap \
php5-cgi fcgi php5-pdo php5-pdo_pgsql php5-soap php5-xmlrpc php5-posix php5-mcrypt \
php5-gettext php5-ldap php5-ctype php5-dom
```

看看Lighttpd安装过程的打印：

```
vm-alpine-0:~# apk add lighttpd 
(1/13) Installing libbz2 (1.0.6-r6)
(2/13) Installing libev (4.24-r0)
(3/13) Installing libffi (3.2.1-r4)
(4/13) Installing libintl (0.19.8.1-r1)
(5/13) Installing libmount (2.31-r0)
(6/13) Installing pcre (8.41-r1)
(7/13) Installing glib (2.54.2-r0)
(8/13) Installing gamin (0.1.10-r10)
(9/13) Installing db (5.3.28-r0)
(10/13) Installing libsasl (2.1.26-r11)
(11/13) Installing libldap (2.4.45-r3)
(12/13) Installing lua5.3-libs (5.3.4-r2)
(13/13) Installing lighttpd (1.4.48-r0)
Executing lighttpd-1.4.48-r0.pre-install
Executing busybox-1.27.2-r7.trigger
Executing glib-2.54.2-r0.trigger
OK: 340 MiB in 55 packages
```

安装php相关的都是失败的。我到官方的仓库下查看，都是没有php相关的东西的。

我选择修改仓库配置文件，把community的也打开。

```
vm-alpine-0:~# apk update
fetch http://dl-cdn.alpinelinux.org/alpine/v3.7/main/x86/APKINDEX.tar.gz
fetch http://dl-cdn.alpinelinux.org/alpine/v3.7/community/x86/APKINDEX.tar.gz
v3.7.0-56-g2e8e7a0d34 [http://dl-cdn.alpinelinux.org/alpine/v3.7/main]
v3.7.0-58-g26701b74f8 [http://dl-cdn.alpinelinux.org/alpine/v3.7/community]
OK: 8970 distinct packages available
```

这样就可以找到php5相关的东西了。

# 配置Lighttpd

1、配置文件在/etc/lighttpd/lighttpd.conf

2、把`include "mod_fastcgi.conf"`这一行打开。

3、编辑mode_fastcgi.con文件。把这个文件里的/usr/bin/php-cgi改成/usr/bin/php-cgi5。

4、启动Lighttpd服务，并且添加到开机启动项里。

```
rc-service start lighttpd start 
rc-update add lighttpd default
```

5、安装其他的软件。

```
apk add wget php5-mysql mysql mysql-client php5-zlib
```

6、重启Lighttpd服务。

```
/etc/init.d/lighttpd restart
```

# 安装配置WordPress

1、下载。https://cn.wordpress.org/txt-download/ 网站在这里。下载tar.gz文件。

2、新建`/usr/share/webapps`目录。解压在这个目录下，得到wordpress目录。内容大概30M左右。

3、把webapp目录给lighttpd用户。

```
chown -R lighttpd /usr/share/webapps
```

4、建立一个软链接。

```
ln -s /usr/share/webapps/wordpress /var/www/localhost/htdocs/wordpress
```

5、配置mysql。

```
mysql_install_db --user=mysql
/etc/init.d/mariadb start && rc-update add mariadb default
mysqladmin -u root password 'password'
```

6、创建WordPress数据库

```
mysql -u root -p
```

下面的操作是在mysql下面做：

```
create database wordpress;
grant all privileges on wordpress.* to 'root'@'192.168.190.132' identified by '123456'; #123456是你设置的密码。
flush privileges;
exit;
```



7、配置WordPress。

在pc上打开浏览器，通过http://xx.xx/wordpress 地址访问你的网站。

然后就是一个输入界面，要输入：

用户名：wordpress。

密码：就是上面是123456

碰到问题，总是提示表名前缀不能为空。

网上找到一个解决办法，就是直接在/usr/share/webapps/wordpress/wp-config.php里写入（通过wp-sample-config.php改）：

```
define('DB_NAME', 'wordpress');

/** MySQL数据库用户名 */
define('DB_USER', 'root');

/** MySQL数据库密码 */
define('DB_PASSWORD', '123456');

/** MySQL主机 */
define('DB_HOST', '192.168.190.132');
```

然后重启Lighttpd。

```
service lighttpd restart
```

在访问，就顺利进入到wordpress的安装界面了。

然后就是配置一些信息，

登录名我用teddyxiong53.

密码用我最弱的那个密码。勾选允许弱密码。

邮箱用1073167306@qq.com。不允许搜索引擎收录。

管理目录是：http://192.168.190.132/wordpress/wp-admin/

# WordPress使用

1、默认进来有一篇示例文章，叫《世界，您好》默认还有一个评论在。

2、尝试去添加一篇文章，发现编辑功能比较弱。我习惯用markdown。到管理界面搜索插件。网上看了下，说Jetpack是比较好的插件。安装试用一下。

安装失败，因为这个只能在公共的网站上用。我的是内网的。

下载单独的Markdown插件，可以用。我可以从typora拷贝粘贴进去。











