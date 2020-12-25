---
title: php之fpm
date: 2019-04-20 11:57:25
tags:
	- php

---



fpm是Fastcgi Progress Manager的缩写。

PHP-FPM是一个PHP FastCGI的管理器，

它实际上就是PHP源代码的补丁，

**旨在将FastCGI进程管理引进到PHP软件包中，**

我们必须将其patch到PHP源代码中，然后再行编译才能使用。

而现在我们可以在PHP 5.3.2及更新版本中直接开启并使用即可，

**因为PHP从该版本已经将其收入到软件包中，所以其不再是补丁包的存在了。**



# CGI

CGI可以用任何一种语言编写，只要这种语言具有标准输入、输出和环境变量。

# FastCGI

FastCGI是一个常驻型的CGI，

它可以一直执行，只要激活后，不会每次都要花费时间去fork一次（这是CGI最为人诟病的fork-and-execute模式）。

它还支持分布式的运算，即 FastCGI 程序可以在网站服务器以外的主机上执行并且接受来自其它网站服务器来的请求。



FastCGI是语言无关的、可伸缩架构的CGI开放扩展，

其主要行为是将CGI解释器进程保持在内存中并因此获得较高的性能。

我们知道，CGI解释器的反复加载是CGI性能低下的主要原因，

如果CGI解释器保存在内存中并接受FastCGI进程管理器调度，

那么就可以提供良好的性能、伸缩性等。



## 优点：

1. FastCGI具有语言无关性；

2. FastCGI独立于核心web服务器运行，提供了一个比API更安全的环境。APIs把应用程序的代码与核心的web服务器链接在一起，这意味着在一个错误的API的应用程序可能会损坏其他应用程序或核心服务器。而恶意的API的应用程序代码甚至可以窃取另一个应用程序或核心服务器的密钥；

3. FastCGI技术目前支持语言有：C/C++、Java、Perl、Tcl、Python、SmallTalk、Ruby等。相关模块在Apache, ISS, Lighttpd等流行的服务器上也是可用的；

4. FastCGI不依赖于任何Web服务器的内部架构，因此即使服务器技术的变化, FastCGI依然稳定不变；



## 缺点：

因为是多进程，所以比CGI多线程消耗更多的服务器内存，

PHP-CGI解释器每进程消耗7至25兆内存，将这个数字乘以50或100就是很大的内存数。

Nginx 0.8.46+PHP 5.2.14(FastCGI)服务器在3万并发连接下，

开启的10个Nginx进程消耗150M内存（15M*10=150M），*

*开启的64个php-cgi进程消耗1280M内存（20M*64=1280M），加上系统自身消耗的内存，总共消耗不到2GB内存。

如果服务器内存较小，完全可以只开启25个php-cgi进程，这样php-cgi消耗的总内存数才500M。

上面的数据摘自Nginx 0.8.x + PHP 5.2.13(FastCGI)搭建胜过Apache十倍的Web服务器(第6版)。



参考资料

1、PHP-FPM配置及使用总结

https://blog.csdn.net/why_2012_gogo/article/details/51112477