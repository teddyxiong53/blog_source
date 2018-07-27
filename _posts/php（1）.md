---
title: php（1）
date: 2018-07-26 22:28:03
tags:
	- php

---



以前一直没有去了解php这种语言。现在觉得有必要了解一下。

概念就不管先。

先在Ubuntu下搭建php的环境。



1、先安装Apache。

```
sudo apt-get install apache2
```

2、安装php。

```
sudo apt-get install php7.0
```

这样则是安装好了。

```
teddy@ubuntu:~$ php -v
PHP 7.0.30-0ubuntu0.16.04.1 (cli) ( NTS )
Copyright (c) 1997-2017 The PHP Group
Zend Engine v3.0.0, Copyright (c) 1998-2017 Zend Technologies
    with Zend OPcache v7.0.30-0ubuntu0.16.04.1, Copyright (c) 1999-2017, by Zend Technologies
```

3、给Apache安装php插件。

```
sudo apt-get install libapache2-mod-php7.0
```

4、验证是否运行正常。

在/var/www/html目录下。新建一个test.php文件。

```

```



# 参考资料

1、ubuntu搭建php开发环境记录

https://www.cnblogs.com/impy/p/8040684.html

