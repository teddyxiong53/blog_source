---
title: busybox的启动过程
date: 2017-05-02 19:10:19
tags:

	- busybox

---

# 1. busybox的默认的启动过程

从kernel到busybox的调用过程，按文件分析大致如下：

```
kernel里调用init.c
	init.c里通过解析/etc/inittab里的内容，得到对getty.c里的getty的调用
	getty调用到login.c。
	login.c调用了sh进行登陆。
	最后进入到ash.c里的cmdloop循环，一直等待命令输入。
	
```



# 2. 自己另外实现init程序

启动可以不走busybox自己的init.c里的init_main。这个init也只是一个C语言的实现版本。init可以任意实现。
但是用脚本写的init，谁来实现内容解析的呢？
在解析init脚本的时候也调用了一次。

```
xhl -- lbb_main 

xhl -- ash_main 

#

THis is a init script for initrd/initramfs

Author: wengpingbo@gmail.com

Date: 2016-12-19 22:34:33 CST

#

build root filesystem...

xhl -- lbb_main 

input: AT Raw Set 2 keyboard as /devices/fpga:06/serio0/input/input0

/proc dir not exist, create it...

xhl -- lbb_main 



```

再进一步加打印，可以看到最前面的打印是这样：

```
xhl -- lbb_main 

argv[0]:/bin/sh 

argv[1]:/init 

xhl -- ash_main 

```


为什么可以解析到/bin/sh这样来调用init文件呢？应该就是靠脚本文件开头的`!#/bin/sh`。

`busybox sh`，这样调用到的才是最后的shell界面。
在kernel的代码里。

```


ramdisk_execute_command = "/init";

run_init_process(ramdisk_execute_command); 这样来调用到的。

```

