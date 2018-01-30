---
title: busybox之inittab分析
date: 2018-01-30 09:02:29
tags:
	- busybox
	- inittab

---



inittab每一行的格式是：

```
id : runlevel_ignored : action: command
```

#四个元素解释

##id

一般可以留空。

这个行的格式，跟linux发行版里的sysvinit是一样的。但是id的具体含义在busybox这里不一样了。

（说明：sysvinit太老了。目前linux发行版都不用这个了，所以我在我的系统里都没有找到这个inittab文件）

busybox里的id代表是ttyXXX。

##runlevel_ignored

busybox留空。不管就是了。



## action

这个值得好好分析一下。

busybox里的action分为8种。依次是：

1、sysinit。系统启动的时候调用。

2、respawn。当对应的command终止执行的时候，重新启动该command。

3、askfirst。跟respawn类似，主要用途是减少系统上终端的占用数量。会让init在控制台上显示“Please press Enter to active this console”。等用户按了Enter键，才会重启对应的command。

4、wait。告诉init必须要等到这个command执行完了才能往下走。

5、once。对应的command只执行一次，而且init不会等。

6、ctrlaltdel。当用户按下ctrl+alt+del键的时候，执行对应的command。

7、shutdown。当系统关机的时候，执行对应的command。

8、restart。当然init重新启动时，执行对应的command。这个command一般就是init自己。



一份典型的inittab内容分析。

```
::sysinit:/bin/mount -t proc proc /proc
::sysinit:/bin/mount -o remount,rw /
::sysinit:/bin/mkdir -p /dev/pts
::sysinit:/bin/mkdir -p /dev/shm
::sysinit:/bin/mount -a
::sysinit:/bin/hostname -F /etc/hostname
::sysinit:/etc/init.d/rcS

console::respawn:/sbin/getty -L console 0 vt100

::shutdown:/etc/init.d/rcK
::shutdown:/sbin/swapoff -a
::shutdown:/bin/umount -a -r
```

这个会要求输入用户名和密码的。用户名是root，密码是空。



##respawn分析

如果相应的进程还不存在，那么init就启动这个进程，然后init进程不会等这个进程结束，init会继续扫描分析inittab里的内容。

如果对应的进程是dead状态的时候，init就会restart这个进程。

如果进程已经存在，init就忽略这一条继续。

