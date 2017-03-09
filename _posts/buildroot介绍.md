---
title: buildroot介绍
date: 2017-03-06 20:12:16
tags:
	- Linux
	- buildroot
---
搭建嵌入式Linux，总是要下载编译uboot、kernel、busybox这些组件，分别编译，显得比较繁琐，有没有办法精简这个过程呢？有的。就是我们现在要介绍的buildroot。

官网地址是：`https://buildroot.org/`。可以在官网上下载手册进行学习。
下面列出的就是我从手册总结的内容。


# 1. 关于buildroot
1. buildroot是一个用来简化和自动化构建一个完整的嵌入式Linux系统，使用交叉编译工具链。
2. buildroot可以生成交叉编译工具链，根文件系统，内核镜像和bootloader。
3. 支持多种处理器及其变种。

# 2. 需要的软件环境
就是需要安装各种开发用的工具，我都已经安装好了的。略过。

# 3. 获取buildroot
每3个月发布一个版本，2月、5月、8月和11月。版本以年和月来命名，格式是YYYY.MM。
官网下载就可以了。一个包也就是5M左右。

# 4. 编译方法
你以普通用户身份进行编译就可以了，不需要root权限。
就在buildroot代码目录下，用make menuconfig可以进行配置。

待续。




