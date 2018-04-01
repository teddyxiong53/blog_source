---
title: Linux之overlayfs
date: 2018-03-31 15:18:07
tags:
	- Linux

---



# 什么是overlayfs

overlay的字母含义是覆盖的意思。

overlayfs就是覆盖的文件系统。

它体现的是一种层次关系。

实现简单，性能较好。

特点是：

1、上下合并。

2、同名覆盖。

3、写时拷贝。



docker的底层就用到了overlayfs的机制。

# Ubuntu下的使用

1、这样进行插入对应的模块。

```
teddy@teddy-ubuntu:~/work/mylinuxlab/kernel/linux-stable$ lsmod |grep overlay
teddy@teddy-ubuntu:~/work/mylinuxlab/kernel/linux-stable$ sudo modprobe overlay
teddy@teddy-ubuntu:~/work/mylinuxlab/kernel/linux-stable$ lsmod |grep overlay
overlay                49152  0
```

2、建立一个简单的目录结构，下面的文件分布是这样的。

新建一个overlayfs的目录，下面内容是这样。

```
$tree
.
├── lower
│   └── l1.txt
├── merged
├── upper
│   └── u2.txt
└── work
```

3、挂载。

```
sudo mount -t overlay overlay -olowerdir=./lower,upperdir=./upper,workdir=./work ./merged
```

查看mount的情况：

```
overlay on /home/teddy/work/test/overlayfs/merged type overlay (rw,relatime,lowerdir=./lower,upperdir=./upper,workdir=./work)
```

4、测试。

看看上下合并如何工作。

在挂载之前，merged目录是空的。现在我们到merged里去看看。

```
$tree
.
├── lower
│   └── l1.txt
├── merged
│   ├── l1.txt
│   └── u2.txt
├── upper
│   └── u2.txt
└── work
    └── work [error opening dir]
```

所以上下合并，就是把upperdir和lowerdir的合并到merged目录下。

看看什么是同名覆盖。

我们在merged目录下修改l1.txt文件。

如何到lower目录里去看，lower下的l1.txt还是没有变化。

但是看道upper目录下多了一个l1.txt，内容跟merged下面的一样。

而且，其实就是对应了磁盘上同一个文件。inode号是一样的。

我们现在在merged目录下，删除l1.txt文件。再看。

到upper目录里看，文件变成了一个大小为0的字符设备，谁都没有权限的。overlayfs用这种方式来标记文件的删除。

```
$cd ../upper/
$ls -l
total 0
c--------- 1 root  root  0, 0 3月  31 15:33 l1.txt
```



# 参考资料

1、overlayfs简介

https://www.tuicool.com/articles/6ri2Ej7

2、

https://wenku.baidu.com/view/2c82473ca32d7375a41780ab.html