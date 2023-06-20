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

# findmnt命令

这个命令比mount命令查看挂载情况要详细。

# mount函数分析

回忆一下，注册file_system_type的时候我们主要提供两个成员给内核，

一个是文件系统的名字，

一个是mount这个文件系统的方法（其它参数也很重要，但重点就是这两个）。

名字就是一个id，唯一标记一个文件系统，并方便内核在需要时根据它找到这个文件系统的file_system_type。

mount方法在挂载这个文件系统时使用的，在需要挂载一个文件系统时通过name找到这个文件系统的file_system_type实例，然后使用这个实例中挂载的方法(mount函数)，进行挂载。

```
/*
 * These are the fs-independent mount-flags: up to 32 flags are supported
 */
#define MS_RDONLY        1         /* 对应-o ro/rw */
#define MS_NOSUID        2         /* 对应-o suid/nosuid */
#define MS_NODEV         4         /*  对应-o suid/nosuid */
#define MS_NOEXEC        8         /* 对应-o exec/noexec */
#define MS_SYNCHRONOUS  16         /* 对应-o sync/async */
#define MS_REMOUNT      32         /* 对应-o remount，告诉mount这是一次remount操作 */
#define MS_MANDLOCK     64         /* 对应-o mand/nomand */
#define MS_DIRSYNC      128        /* 对应-o dirsync */
#define MS_NOATIME      1024       /* 对应-o atime/noatime */
#define MS_NODIRATIME   2048       /* 对应-o diratime/nodiratime */
#define MS_BIND         4096       /* 对应-B/--bind选项，告诉mount这是一次bind操作 */
#define MS_MOVE         8192       /* 对应-M/--move，告诉mount这是一次move操作 */
#define MS_REC          16384      /* rec是recursive的意思，这个flag一般不单独出现，都是伴随这其它flag，表示递归的进行操作 */
#define MS_VERBOSE      32768      /* 对应-v/--verbose */
#define MS_SILENT       32768      /* 对应-o silent/loud */
#define MS_POSIXACL     (1<<16)    /* 让VFS不应用umask，如NFS */
#define MS_UNBINDABLE   (1<<17)    /* 对应--make-unbindable */
#define MS_PRIVATE      (1<<18)    /* 对应--make-private */
#define MS_SLAVE        (1<<19)    /* 对应--make-slave */
#define MS_SHARED       (1<<20)    /* 对应--make-shared */
#define MS_RELATIME     (1<<21)    /* 对应-o relatime/norelatime */
#define MS_KERNMOUNT    (1<<22)    /* 这个一般不在应用层使用，一般内核挂载的文件系统如sysfs使用，表示使用kern_mount()进行挂载 */
#define MS_I_VERSION    (1<<23)    /* 对应-o iversion/noiversion */
#define MS_STRICTATIME  (1<<24)    /* 对应-o strictatime/nostrictatime */
 
/* 下面这几个flags都是内核内部使用的，它们的含义我只是通过简单的查看代码逻辑暂时猜测的 */
#define MS_NOSEC        (1<<28)    /* 有些文件系统不支持suid，security xattr等安全标记 */
#define MS_BORN         (1<<29)    /* 表示内存superblock已经创建完成 */
#define MS_ACTIVE       (1<<30)    /* 表示内存superblock正处于活动状态 */
#define MS_NOUSER       (1<<31)    /* 表示文件系统不能被应用层挂载使用，只能被内核使用，如rootfs */
 
/*
 * Superblock flags that can be altered by MS_REMOUNT
 */
#define MS_RMT_MASK     (MS_RDONLY|MS_SYNCHRONOUS|MS_MANDLOCK|MS_I_VERSION)  // 可以在remount是改变的flags
 
/*
 * Old magic mount flag and mask
 */
#define MS_MGC_VAL 0xC0ED0000      /* 过去使用的magic，现在基本被忽略了 */
#define MS_MGC_MSK 0xffff0000      /* 过去使用的flag的的mask */
```

从上面可以看出，flags基本上是options中通用的那些，也就是说基本是面向所有文件系统通用的，当然还有一些是内核使用的。这些flags大部分都在VFS层被解析使用。

而data呢，把options中通用的去掉，剩下的就是每个文件系统各自支持的挂载选项。

让我们来看个例子：

我们选取一个与flags对应的option，如nodev。在从xfs中选取一个特定的option，如noquota。然后用strace跟踪一下mount的过程，执行
strace mount /dev/loop0 /mnt/test -o noquota,nodev

在接近最后的位置我们可以看到mount系统调用：

mount("/dev/loop0", "/mnt/test", "xfs", MS_MGC_VAL|MS_NODEV, "noquota") = 0

果然，nodev被解释为flag，noquota被当作了mount data。



struct mount代表着一个mount实例，

其中struct vfsmount定义的mnt成员是它最核心的部分。

过去没有stuct mount，mount和vfsmount的成员都在vfsmount里，

现在linux将vfsmount改作mount结构体，并将mount中mnt_root, mnt_sb, mnt_flags成员移到vfsmount结构体中了。

这样使得vfsmount的内容更加精简，在很多情况下只需要传递vfsmount而已。

来看一下这两个结构体：

到此mount就可能做5种mount操作（remount, bind, chang type, move和new mount）之一。

我们以do_new_mount为例继续分析，do_new_mount属于最常见的情况，挂载一个新的文件系统。



# 参考资料

1、bind mount 的用法

https://xionchen.github.io/2016/08/25/linux-bind-mount/

2、mount --bind 的妙用

https://blog.csdn.net/gerryzhu/article/details/42525563

3、这个系列文章

https://blog.csdn.net/ZR_Lang/article/details/40002285