---
title: php之命令行使用
date: 2020-12-25 11:08:30
tags:
- php
---

1

查看帮助：

```
php --help
```

交互运行：

```
php -a
```

执行脚本

```
php -f test.php
```

test.php内容：

```
<?php
echo "hello php"
?>
```

查看ini配置文件的情况

```
php --ini
```

在我的云服务器上

```
ubuntu@VM-0-17-ubuntu:~$ php --ini
Configuration File (php.ini) Path: /www/server/php/80/etc
Loaded Configuration File:         /www/server/php/80/etc/php.ini
Scan for additional .ini files in: (none)
Additional .ini files parsed:      (none)
```

查看命令行手册

```
php --rf xx
```

xx是函数名，

![image-20201225111322916](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201225111322916.png)





参考资料

1、

https://www.jb51.net/article/71215.htm