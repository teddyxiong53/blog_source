---
title: Linux之mount相关用法
date: 2019-07-30 13:50:19
tags:
	- Linux

---

--

# bind

bind是mount的一种特殊用法。

基本格式是：

```
mount --bind olddir newdir
```

作用是：

```
把一个分区的一个目录，挂载到另外一个目录。
```

例如chroot后，希望可以访问/dev目录。

```
mount --bind /dev $chrootdir/dev
```

我们希望/dev对chroot只读。

```
mount -o remount,ro,bind /dev $chrootdir/dev
```



在嵌入式里的用途，主要是用来解决在只读分区里进行修改操作的问题。

```
cp /ro_part/1.txt /rw_part/1.txt
mount --bind /rw_part/1.txt /ro_part/1.txt
```

这样对/rw_part/1.txt的修改就可以反映到/ro_part/1.txt里。



# mount的选项

现在看linux的开机过程，各种切换rootfs的操作。

对mount使用较多。

所以需要把mount的选项都研究一下。

基本命令：

```
mount -t type device dir
```

# mount -n --move 

`mount -n --move` 是一个 Linux 命令，用于在文件系统中**移动挂载点而不进行卸载和重新挂载。**

具体而言，`mount -n --move` 命令的语法如下：

```
mount -n --move <source> <target>
```

其中，`<source>` 是要移动的挂载点的源路径，`<target>` 是要移动到的目标路径。

该命令的作用是将指定的源路径挂载点移动到目标路径上，而无需进行卸载和重新挂载操作。**这对于动态更改文件系统的挂载点位置很有用，尤其是在某些场景下需要保持文件系统挂载状态不变的情况下。**

需要注意的是，`mount -n --move` 命令需要以超级用户（root）权限执行。

# 参考资料

1、bind mount 的用法

https://xionchen.github.io/2016/08/25/linux-bind-mount/

2、mount --bind 的妙用

https://blog.csdn.net/gerryzhu/article/details/42525563