---
title: 用busybox制作根文件系统
date: 2016-12-12 23:51:15
tags:
	- busybox
---
前面我们用qemu制作了一个最简单的linux系统，但是文件系统其实并不够完善，所以现在把完整的busybox根文件系统做一遍。

# 1. 编译
busybox的编译，可以用`make help`来看看有什么目标可用。再快速看一遍顶层的makefile。
一条比较全的make命令可以是这样：
`make ARCH=arm CROSS_COMPILE=arm-linux-guneabihf- V=1 C=1 O=/dir/`
V=1表示用verbose模式来编译，就是会详细地把每条命令的内容打印出来，适合调试或者分析make过程。
C=1表示打开检查功能。
O表示指定输出路径。
我们先就用这个`make ARCH=arm CROSS_COMPILE=arm-linux-guneabihf-`编译。
然后用`make ARCH=arm CROSS_COMPILE=arm-linux-guneabihf- install`来产生一个根文件的基本框架。
这条命令在当前目录下的_install目录下生成文件系统目录。
```
teddy@teddy-ubuntu:~/work/qemu/busybox/busybox-1.25.1/_install$ ls -l
总用量 12
drwxrwxr-x 2 teddy teddy 4096 12月 12 23:11 bin
lrwxrwxrwx 1 teddy teddy   11 12月 12 23:11 linuxrc -> bin/busybox
drwxrwxr-x 2 teddy teddy 4096 12月 12 23:11 sbin
drwxrwxr-x 4 teddy teddy 4096 12月 12 23:11 usr
```
linuxrc这个是软连接，连接到/bin/busybox。
如果我们把这个目录直接制作成根文件系统去用的话，运行会得到这个结果：
```
[    1.564883] No filesystem could mount root, tried:  ext2 cramfs minix romfs
[    1.565804] Kernel panic - not syncing: VFS: Unable to mount root fs on unknown-block(1,0)
[    1.567656] CPU: 0 PID: 1 Comm: swapper Not tainted 4.4.34 #4
```
说明文件系统里还少东西。

# 2. 手动建立目录和文件
## 2.1 新建目录
新建一个rootfs目录，把_install目录下的内容都拷贝到这个目录下。
在rootfs目录下新建etc、dev、lib、tmp、var目录。
var目录下新建run和log目录。
现在的目录结构如下：
```
teddy@teddy-ubuntu:~/work/qemu/rootfs$ tree -d
.
├── bin
├── dev
├── lib
├── sbin
├── tmp
├── usr
│   ├── bin
│   └── sbin
└── var
    ├── log
    └── run
```
## 2.2 拷贝必要的配置文件
busybox给了一个examples目录，下面的bootfloppy是我们可以参考的。
我们把下面的etc目录内容整个拷贝到我们新建的etc目录下。
```
teddy@teddy-ubuntu:~/work/qemu/rootfs$ cp ../busybox/busybox-1.25.1/examples/bootfloppy/etc/* etc/ -rf
teddy@teddy-ubuntu:~/work/qemu/rootfs/etc$ tree
.
├── fstab
├── init.d
│   └── rcS
├── inittab
└── profile

1 directory, 4 files
```
我们在生成busybox的时候，默认是选择了它的init功能的，init也是一个指向busybox的软链接。
busybox的init做了这些事情：
1. 初始化控制台
2. 解析/etc/inittab文件，如果没有这个文件，那么busybox会执行默认的一些操作。
3. 执行初始化脚本，例如/etc/init.d/rcS

busybox给的examples里的inittab内容是这样的：
```
::sysinit:/etc/init.d/rcS
::respawn:-/bin/sh
tty2::askfirst:-/bin/sh
::ctrlaltdel:/bin/umount -a -r
```
指定了初始化脚本是`/etc/init.d/rcS`。
`::respawn:-/bin/sh`这一句表示当你在shell执行exit后，要做什么。这样配置的话，会直接再启动一个shell。
如果你想要在exit后，弹出一个登陆提示，则改成这样：`::respawn:-/bin/login`
`tty2::askfirst:-/bin/sh`这句表示在启动linux后，要按一下回车才能进入。
`::ctrlaltdel:/bin/umount -a -r`这句表示你按了ctrlaltdel键，会产生把所有文件系统umount的动作。
我们当前把inittab保持默认，因为用起来合理。
下面我们看rcS这个脚本。默认就是挂载所有的文件系统，需要根据fstab的内容来做。
我们可以在rcS脚本后面加入自己想加的内容。暂时不加。
```
#! /bin/sh

/bin/mount -a
```


## 2.3 创建设备文件
把bootfloppy下的mkdevs.sh拷贝到rootfs目录下并执行。
```
teddy@teddy-ubuntu:~/work/qemu/rootfs$ cp ../busybox/busybox-1.25.1/examples/bootfloppy/mkdevs.sh ./
teddy@teddy-ubuntu:~/work/qemu/rootfs$ sudo ./mkdevs.sh dev
teddy@teddy-ubuntu:~/work/qemu/rootfs/dev$ ls
console  hdb   loop0  loop4  mem   ram0  ram4  ram8    tty0  tty4  tty8     vcs0  vcs4  vcs8   vcsa1  vcsa5  vcsa9
core     hdc   loop1  loop5  null  ram1  ram5  ram9    tty1  tty5  tty9     vcs1  vcs5  vcs9   vcsa2  vcsa6  zero
full     hdd   loop2  loop6  port  ram2  ram6  random  tty2  tty6  urandom  vcs2  vcs6  vcsa   vcsa3  vcsa7
hda      kmem  loop3  loop7  ram   ram3  ram7  tty     tty3  tty7  vcs      vcs3  vcs7  vcsa0  vcsa4  vcsa8
```
这样就在dev目录下生成了一些设备文件。
mknod相当于touch，只不过mknod生成的文件是设备文件。而touch出来的文件是普通文件。





