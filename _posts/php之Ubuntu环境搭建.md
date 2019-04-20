---
title: php之Ubuntu环境搭建
date: 2019-04-20 10:09:25
tags:
	- php

---

1

安装mysql

```
sudo apt-get install mysql-server
```

安装apache

```
sudo apt-get install apache2
```

安装php

```
sudo apt-get install php
```

安装apache和php的连接

```
sudo apt-get install libapache2-mod-php
```

安装phpmyadmin

```
sudo apt-get install phpmyadmin
```

安装mysql-client

```
sudo apt-get install mysql-client
```



在/var/www/html目录下，写一个test.php文件，内容如下：

```
<?php
	phpinfo();
?>
```

然后访问http://localhost/test.php

看到php信息则正常。



指定apache的根目录。

然后需要做的就是修改php.ini文件，打开错误日志。

然后及可以进行开发调试了。



参考资料

1、

https://segmentfault.com/a/1190000010258086