---
title: git原理分析
date: 2021-03-19 10:42:41
tags:
	- git

---

--

这个是网页游戏性质的git教程，对于理解非常有好处。

https://git.mo.mk/

pro git，这个电子书很好。

https://www.progit.cn/



git的配置信息

C:\Program Files\Git\etc\gitconfig：系统级的

`C:\Users\hanliang.xiong\.gitconfig`: 用户级的

.git/config ：项目级的

范围越小的，优先级越高。



首先要弄明白一点，

从根本上来讲 Git 是一个内容寻址（content-addressable）文件系统，

并在此之上提供了一个版本控制系统的用户界面。 

早期的 Git（主要是 1.5 之前的版本）的用户界面要比现在复杂的多，

因为它更侧重于作为一个文件系统，

而不是一个打磨过的版本控制系统。

 不时会有一些陈词滥调抱怨早期那个晦涩复杂的 Git 用户界面；

不过最近几年来，它已经被改进到不输于任何其他版本控制系统地清晰易用了。



本书主要涵盖了 `checkout`、`branch`、`remote` 等约 30 个 Git 的子命令。

 然而，由于 Git 最初是一套面向版本控制系统的工具集，

而不是一个完整的、用户友好的版本控制系统，

 所以它还包含了一部分用于完成底层工作的子命令。

 这些命令被设计成能以 UNIX 命令行的风格连接在一起，

抑或藉由脚本调用，来完成工作。 

这部分命令一般被称作“底层（plumbing）”命令，

而那些更友好的命令则被称作“上层（porcelain）”命令。



你或许已经注意到了，本书前九章专注于探讨上层命令。 

然而在本章中，我们将主要面对底层命令。 

因为，底层命令得以让你窥探 Git 内部的工作机制，

也有助于说明 Git 是如何完成工作的，以及它为何如此运作。

 多数底层命令并不面向最终用户：

它们更适合作为新工具的组件和自定义脚本的组成部分。

.git目录下是这样

```
$ ls -F1
config
description
HEAD
hooks/
info/
objects/
refs/
```

`description` 文件仅供 GitWeb 程序使用，我们无需关心。 

`config` 文件包含项目特有的配置选项。

 `info` 目录包含一个全局性排除（global exclude）文件， 用以放置那些不希望被记录在 `.gitignore` 文件中的忽略模式（ignored patterns）。

 `hooks` 目录包含客户端或服务端的钩子脚本（hook scripts）， 在 [Git 钩子](https://git-scm.com/book/zh/v2/ch00/_git_hooks) 中这部分话题已被详细探讨过。



剩下的四个条目很重要：

`HEAD` 文件、

（尚待创建的）`index` 文件，

和 `objects` 目录、

`refs` 目录。

 它们都是 Git 的核心组成部分。

 `objects` 目录存储所有数据内容；

`refs` 目录存储指向数据（分支、远程仓库和标签等）的提交对象的指针；

 `HEAD` 文件指向目前被检出的分支；

`index` 文件保存暂存区信息。 我们将详细地逐一检视这四部分，来理解 Git 是如何运转的。



Git 是一个内容寻址文件系统，听起来很酷。

但这是什么意思呢？ 

这意味着，Git 的核心部分是一个简单的键值对数据库（key-value data store）。 

**你可以向 Git 仓库中插入任意类型的内容，它会返回一个唯一的键，通过该键可以在任意时刻再次取回该内容。**





# 参考资料

1、

https://git-scm.com/book/zh/v2/Git-%E5%86%85%E9%83%A8%E5%8E%9F%E7%90%86-%E5%BA%95%E5%B1%82%E5%91%BD%E4%BB%A4%E4%B8%8E%E4%B8%8A%E5%B1%82%E5%91%BD%E4%BB%A4#ch10-git-internals

2、git源码剖析-init-db

https://blog.csdn.net/sayhello_world/article/details/82877647