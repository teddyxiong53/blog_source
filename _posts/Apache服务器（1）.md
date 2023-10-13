---
title: Apache服务器（1）
date: 2018-08-11 22:55:33
tags:
	- 服务器
---



--

# 修改根目录

因为默认是指向了/var/www/html，这个目录修改不方便，所以希望指向我的开发目录。

配置都是在/etc/apache2目录下，修改site-enabled里的000-default.conf文件就好了。

apache的配置文件都是xml写的。

改这一行：

```
DocumentRoot /var/www/html
```

改成：

```
DocumentRoot /home/hlxiong/work/test/easyui
```

还要改apache2.conf文件。增加这个。

```
<Directory /home/hlxiong/work/test/easyui>
    Options Indexes FollowSymLinks
    AllowOverride None
    Require all granted
</Directory>
```

改了然后重启。

```
sudo /etc/init.d/apache2 restart
```







# 参考资料

1、Ubuntu Apache 根目录的更改方法

https://blog.csdn.net/fengguowuhen7871/article/details/8843241