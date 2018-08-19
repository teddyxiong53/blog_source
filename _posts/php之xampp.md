---
title: php之xampp
date: 2018-08-19 10:09:51
tags:
	- php

---



想要用zend studio调试，但是wamp下面总是弄不出来，我换xampp看看。

https://www.apachefriends.org/zh_cn/download.html

从这里下载最新的版本。只有32位版本。



xampp和wamp对比

wamp只能在windows上用。

xampp功能更加强大一些。

操作界面也更加人性化。



到这里下载xdebug的对应版本。

https://xdebug.org/download.php

我当前用的是这个。

https://xdebug.org/files/php_xdebug-2.6.1-7.2-vc15.dll



配置。

```
[xdebug]
zend_extension ="d:\xampp\php\ext\php_xdebug-2.6.1-7.2-vc15.dll"
xdebug.remote_enable = true
xdebug.remote_handler="dbgp"
xdebug.remote_host="127.0.0.1"
xdebug.remote_port=9001
xdebug.profiler_enable = 1
xdebug.profiler_output_dir ="d:\xampp\tmp"
```

然后zend studio这边，按照教程配置就好了。

关键的关键，就是不要直接debug as，而是要debug configure，然后新建一个调试设置。



现在我把emlog的代码，拷贝到zend studio里新建的一个php local项目里。

访问emlog，提示不支持mysql。

xampp默认的mysql没有密码。

我登陆去改密码，还是不行。

```
λ .\bin\mysql.exe -u root
ERROR 1045 (28000): Access denied for user 'root'@'localhost' (using password: NO)
D:\xampp\mysql
λ
```



先开一个窗口。

```
bin\mysqld --skip-grant-tables
```

再开一个窗口。

```
mysql -u root -p
提示密码，直接回车。

```



xampp里mysql启动不了，因为我系统里默认安装了一个mysql。现在把我系统里的mysql卸载，现在就可以在xampp面板里启动mysql了。



用这个代码，测试mysql数据库的连通性是好的。

```
<?PHP
$conn=mysqli_connect("localhost","root","040253");
if($conn){
    echo"ok";
}else{
    echo"error";
}
?>
```

也是坑爹。

wamp那边是php切换不到7.0版本，xampp是不能连接数据库。

从这里下载更新的高版本。

http://www.downza.cn/soft/30324.html

# 参考资料

1、Xampp + Zend Studio 开启Xdebug调试功能

https://blog.csdn.net/buyaore_wo/article/details/69787358

2、windows下mysql初始密码设置

https://www.cnblogs.com/dongzhuangdian/p/5620771.html

