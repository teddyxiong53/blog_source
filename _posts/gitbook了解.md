---
title: gitbook了解
date: 2019-01-15 13:28:59
tags:
	- gitbook
---



gitbook是基于nodejs的命令行工具。

通过git和markdown来编写电子书。

安装：

```
npm install -g gitbook-cli
```

创建testbook。

```
hlxiong@hlxiong-VirtualBox:~/work/test/gitbook$ gitbook init testbook
warn: no summary file in this book 
info: create README.md 
info: create SUMMARY.md 
info: initialization is finished 
hlxiong@hlxiong-VirtualBox:~/work/test/gitbook$ tree
.
└── testbook
    ├── README.md
    └── SUMMARY.md
```

summary是书籍的排版和目录。

然后执行：

```
gitbook serve
```

这样是在本地起了一个服务器。你访问ip:4000就可以看到了。



添加新的章节。

新建a.md、b.md、c.md这3个文件。

修改summary.md如下：

```
# Summary

* [A](a.md)
* [B](b.md)
* [C](c.md)
```

添加层级关系。

```
* [A](a.md)
	* [A1](a1.md)
	* [A2](a2.md)
```

新建.gitignore文件。

```
.*
!.gitignore
_book
node_modules
```



发布书籍

有这些方式：

```
私有
github
gitbook
```



现在自己打算用gitbook来翻译一本python数据结构的书。当然这本书已经有中文版本，我相当于是自己写一本笔记。

排版尽量严格。怎样来做呢？

字体。

插图。

```
gitbook init python_data_structure
```



# 用docker搭建写书环境

我当前在笔记本上搭建，有点问题。为了节省时间，快速解决这个问题。

所以我打算用docker来搭建。





参考资料

1、Gitbook学习笔记

https://skyao.io/learning-gitbook/

2、

http://tinylab.org/docker-quick-start-docker-gitbook-writing-a-book/