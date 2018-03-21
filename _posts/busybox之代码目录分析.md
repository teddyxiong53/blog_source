---
title: busybox之代码目录分析
date: 2017-10-02 11:07:48
tags:
	- busybox

---



# 1. 先看reamde

可以得到如下信息：

1、安装说明是在INSTALL文件里。

2、busybox的简介：

1）busybox是把很多的精简版本的unix基础工具打包到一个小的可执行程序里了。

2）基础工具包有：

bzip2

coreutils：

dhcp：

diffutils：

e2fsprogs：

file

findutils：

gawk：

grep：

inetutils：

less：

modutils：

net-tools：

procps：

sed：

shadow：

sysklogd：

sysvinit：

tar：

util-linux：

vim：

busybox里的实现，去掉了一些复杂的选项的实现。

busybox里的代码充分考虑了资源限制，无论是程序大小还是运行时占用内存都进行了优化。busybox让构建嵌入式系统变得容易。



# 2. 看.config文件

这个文件分为这个几大块。

1、通用配置。

2、编译配置。

3、调试配置。

4、安装配置。

5、库配置。

6、applet配置。

7、各种utils命令选配。



# 3. 看Makefile





