---
title: thinkphp（1）
date: 2018-08-15 22:43:27
tags:
	- php

---



都说thinkPHP是学习php入门经常用到的一个框架。

我就学习一下这个。



先看看环境如何搭建。

先要安装wampsever。这个是法国人写的。官网是法语的。

http://www.wampserver.com/

我直接在这里下载，看更新时间是2018年，应该足够新了。是3.0版本。

http://dl.pconline.com.cn/download/52877.html

看完整的名字是这样的。

apache版本是2.4 。

mysql版本是5.7.9 。

php版本有5.6和7.0 这2个版本。

```
wampserver3_x64_apache2.4.17_mysql5.7.9_php5.6.16_php7.0.0.exe
```

安装路径我们设定为：d:\wamp64

安装过程中，提示你设置要选择的浏览器和文本编辑器，我设置为chrome和notepad++。

安装完成后，双击运行就好了。

你可以右键wampsever，tools，check state of service。看看服务启动是否正常。

然后访问http://locahost可以看到就说明正常了。

点击页面里的phpmyadmin，进入到管理界面。

用户名为root，密码为空。

进去后，点击用户账户，进去修改root的密码。



# 参考资料

1、windows下本地thinkphp环境搭建

https://blog.csdn.net/via927/article/details/51419156