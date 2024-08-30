---
title: x-cmd命令行工具使用
date: 2024-08-18 15:06:11
tags:
	- 命令行

---

--

在B站刷视频，发现x-cmd这个工具，看起来很不错。

https://cn.x-cmd.com/pkg/

安装：

```
eval "$(curl https://get.x-cmd.com)"
```

基本使用：

查看环境：

```
x env ls
```

安装nodejs

```
x env use node
```

这样就会下载安装到个人目录下。不需要管理员权限。

X-cmd 作者已经集成了不少新的常用命令。

例如procs这个命令，是一个现代化的ps命令。

使用：

```
x procs
```

第一次使用，会自动下载安装。后面就可以直接用了。

对于一切的系统命令，你都可以加上x的前缀。

例如：ls、ps，都会得到不一样的体验。

```
x ls
x ps
```

实际上是去找了对应的现代化替换版本。

例如x du就是找的dust。

发现这些命令行工具很多都是用go语言写的。

go语言很适合写命令行工具。

从x-cmd的使用也可以了解到很多的实用小工具。



# 模块

模块不是个package。

而是x-cmd内部的东西。

例如下面这个，就可以很方便地查看本机的所有ip，非常直观。

```
x ip
```



# 进行各种编程语言环境的实验

## zig

# git工具

## gitui

```
x env use gitui
```

安装好之后，直接gitui就可以。使用确实非常方便。

# python版本

```
x env use python
```

这样安装一个本地的python。默认是下载安装了3.10的。

是安装在x-cmd的目录下的。



# x-cmd团队编译的go模块

列举在这里：

https://go.x-cmd.com/

可以从这里看到不少实用的模块。

# x-cmd团队编译的zig模块

