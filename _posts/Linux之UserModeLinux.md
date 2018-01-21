---
title: Linux之UserModeLinux
date: 2018-01-19 12:34:29
tags:
	- Linux 

---



#概念

1、UserModeLinux是指在用户态运行的linux内核。把内核当成一个应用来跑。

2、可以把kernel当成一个普通的应用来进行gdb调试。

3、有限制就是不能涉及底层。硬件相关的东西不能通过这个来调试。

4、调度算法、vfs这些都是可以调试的。

# 环境搭建

我在Ubuntu16.04上进行操作。

1、下载kernel内核代码。我是之前有一份树莓派的linux-rpi-4.4.y.zip代码，就拿来直接用。看网上说linux2.6以上的版本才行。我现在用的是4.4的。

2、配置、编译。

```
make ARCH=um defconfig
make ARCH=um -j256
```

这个ARCH指定为um的。编译几分钟完成。没有出现错误。

编译后，在当前目录生产了一个叫linux的可执行文件。我们执行一下看看。

```
teddy@teddy-ubuntu:~/work/uml/linux-rpi-4.4.y$ ls -lh ./linux 
-rwxrwxr-x 2 teddy teddy 42M 1月  19 14:17 ./linux
teddy@teddy-ubuntu:~/work/uml/linux-rpi-4.4.y$ 
```

执行后报错并生成coredump文件。还需要做一些其他的工作。

为了后续使用上方便，我们把linux这个文件放到/usr/local/bin目录下。

```
sudo cp ./linux /usr/local/bin
```



3、需要生成一个rootfs。简单起见，到网上下载一个。谷歌搜索关键词：rootfs image download  uml。

http://fs.devloop.org.uk/ 这个网站上有，我们选择64位的Ubuntu的文件系统。下载是几十兆，解压后 是1个G。

解压后的名字是Ubuntu-TrustyTahr-AMD64-root_fs。为了使用方便，我们改名为rootfs。

4、用gdb调试。

```
 gdb linux ./rootfs
 (gdb) b start_kernel
```







