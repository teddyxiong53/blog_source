---
title: linux man命令使用总结
date: 2016-12-23 20:50:53
tags:
	- linux
---
有时候会碰到这种问题，例如sysctl这个东西，既是函数，也是命令。你如果直接用man sysctl，其实看到的命令的帮助信息。如果想要看到sysctl这个函数的帮助信息，应该怎么办呢？
可以用`man 2 sysctl `。这样看到的就是函数sysctl的信息了。
为什么会这样呢？其实是跟man的内容组织方式有关系。man手册分成了9个不同的section。依次如下：

```
1 - commands
2 - system calls
3 - library calls
4 - special files
5 - file formats and convertions
6 - games for linux
7 - macro packages and conventions
8 - system management commands
9 - 其他
```
解释一下, 
1是普通的命令
2是系统调用,如open,write之类的(通过这个，至少可以很方便的查到调用这个函数，需要加什么头文件)
3是库函数,如printf,fread
4是特殊文件,也就是/dev下的各种设备文件
5是指文件的格式,比如passwd, 就会说明这个文件中各个字段的含义
6是给游戏留的,由各个游戏自己定义
7是附件还有一些变量,比如向environ这种全局变量在这里就有说明
8是系统管理用的命令,这些命令只能由root使用,如ifconfig
