---
title: Linux之switch_root
date: 2023-03-13 13:37:33
tags:
	- Linux

---



switch_root 命令  

除了基于initramfs的系统（如第四节的mini linux），

通常initramfs都是为安装最终的根文件系统做准备工作，

它的最后一步需要安装最终的根文件系统，

然后切换到新根文件系统上去。



以往 的基于ramdisk 的initrd 使用pivot_root命令切换到新的根文件系统，

然后卸载ramdisk。

**但是initramfs是rootfs，**

**而rootfs既不能 pivot_root，也不能umount。**



为了从initramfs中切换到新根文件系统，需要作如下处理： 

（1）删除rootfs的全部内容，释放空间 
find -xdev / -exec rm '{}' ';' 

（2）安装新的根文件系统，并切换 
cd /newmount; mount --move . /; chroot . 

（3）把stdin/stdout/stderr 附加到新的/dev/console，然后执行新文件系统的init程序 



上述步骤比较麻烦，而且要解决一个重要的问题：

第一步删除rootfs的所有内容也删除了所有的命令，

那么后续如何再使用这些命令完成其他步骤？

busybox的解决方案是，

提供了switch_root命令，完成全部的处理过程，使用起来非常方便。 

switch_root命令的格式是：

```
switch_root [-c /dev/console] NEW_ROOT NEW_INIT [ARGUMENTS_TO_INIT]  
```

其中NEW_ROOT是实际的根文件系统的挂载目录，

执行switch_root命令前需要挂载到系统中；

NEW_INIT是实际根文件系统的init程序的路径，一般是/sbin/init；

 -c /dev/console是可选参数，用于重定向实际的根文件系统的设备文件，一般情况我们不会使用；

而 ARGUMENTS_TO_INIT则是传递给实际的根文件系统的init程序的参数，也是可选的。  



需要特别注意的是：switch_root命令必须由PID=1的进程调用，也就是必须由initramfs的init程序直接调用，不能由init派生的其他进程调用，否则会出错，提示： 

switch_root: not rootfs  

也是同样的原因，init脚本调用switch_root命令必须用exec命令调用，否则也会出错，提示： 

switch_root: not rootfs 



# pivot_root和switch_root区别

我看我们的脚本里还有这个。

那么这个的执行是在switch_root之后。

```
./etc/overlaymount:3:        pivot_root $1 $1$2 && {
```

这一层是为了其他的用途。

为了实现overlay。

```
do_overlay_mount() { #<overlay dir>
        mkdir -p $1/upper $1/work
        fopivot $1/upper $1/work /rom 1
}
```

```
do_overlay_mount /data/overlay
```



# 参考资料

1、

https://blog.csdn.net/lbaihao/article/details/51839481