---
title: dpkg和apt-get关系
date: 2019-07-06 16:01:37
tags:
	- Linux
---



一般dpkg用来安装网上下载下来的deb包。

apt-get用来从仓库安装软件。

dpkg不会解决依赖问题。apt-get会解决依赖问题。

**可以这么理解，apt-get是对dpkg的封装。**

dpkg是绕过了apt-get的依赖管理。其实不是很安全的做法。

apt-get安装软件时，下载的文件，会缓存在/var/cache/apt/archives。都是deb文件。



aptitude

这个跟apt-get类似，功能没有apt-get，**但是在安装卸载软件这个功能上，比apt-get要强大。**

而且卸载的时候，卸载得更为干净。



下面这个命令，可以查看minidlna所有的相关的文件。

```
sudo dpkg -L minidlna 
```



参考资料

1、linux之apt与dpkg安装包管理工具的区别

https://blog.csdn.net/baidu_28149499/article/details/56307190

2、Ubuntu(Debian)的aptitude与apt-get的区别和联系

https://blog.csdn.net/u010670794/article/details/42520209