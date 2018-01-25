---
title: scons（二）rt-thread的scons脚本分析
date: 2018-01-24 17:51:21
tags:
	- scons
	- rt-thread

---



从bsp/qemu-vexpress-a9/SConstruct文件开始看。

1、import rtconfig。就是当前目录的配置。配置了gcc等工具。

2、查看是否有RTT_ROOT这个环境变量。如果没有，就往外退两层，用这个目录。

3、把tools目录加入到sys.path里，然后from building import * 。

4、定义TARGET为rtthread.elf。

5、用Environment构造一个env，把上面的内容放进去。

6、调用PrepareBuilding。

7、调用DoBuilding。



