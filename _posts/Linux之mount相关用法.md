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



# 参考资料

1、bind mount 的用法

https://xionchen.github.io/2016/08/25/linux-bind-mount/

2、mount --bind 的妙用

https://blog.csdn.net/gerryzhu/article/details/42525563