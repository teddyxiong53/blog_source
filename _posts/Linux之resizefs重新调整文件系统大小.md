---
title: Linux之resizefs重新调整文件系统大小
date: 2020-03-18 14:57:11
tags:
	- Linux
---

1

在嵌入式开发里，可以看到resizefs的行为，这样可以让最后面的data分区自动使用所有的剩余磁盘空间。

这个是怎么做到的呢？

原理是什么？



resize2fs命令

这个命令用来增大或者缩小未加载的ext文件系统的大小。

如果文件系统处于mount状态，那么只能增大。



当前是在init.d/S21mountall.sh脚本里

```
case "$1" in
  start|"")
    RESIZE_LOG=/tmp/resizefs.log
    CHECK_LOG=/tmp/checkfs.log
    MOUNT_LOG=/tmp/mountfs.log

    SYS_BASE_FSTYPES="proc,devpts,tmpfs,sysfs,debugfs,pstore"

    # Mount /tmp firstly to save logs
    mountpoint -q /tmp || mount -t tmpfs tmpfs /tmp

    if is_recovery;then  # recovery，不进行文件系统操作，只挂载基本的ramfs。
        # Only mount basic file systems for recovery
        mountall $SYS_BASE_FSTYPES 2>&1 | tee $MOUNT_LOG
        echo Log saved to $MOUNT_LOG
    else # 这个是正常的启动。
        resizeall 2>&1 | tee $RESIZE_LOG
        echo Log saved to $RESIZE_LOG
        checkall 2>&1 | tee $CHECK_LOG
        echo Log saved to $CHECK_LOG
        mountall 2>&1 | tee $MOUNT_LOG
        echo Log saved to $MOUNT_LOG
    fi
    ;;
  restart|reload|force-reload)
    echo "Error: argument '$1' not supported" >&2
    exit 3
    ;;
  stop|status)
    # No-op
    ;;
  *)
    echo "Usage: [start|stop]" >&2
    exit 3
    ;;
esac
```



/tmp/resizefs.log

```
# cat /tmp/resizefs.log
Will now resize all file systems
Resizing /dev/rkflash0p6 / ext2...
dumpe2fs 1.43.9 (8-Feb-2018)
dumpe2fs: Bad magic number in super-block while trying to open /dev/rkflash0p6
Wrong fs type!
Resizing /dev/rkflash0p3 /misc emmc...
Resizing /dev/rkflash0p8 /oem squashfs...
Resizing /dev/rkflash0p9 /userdata ext2...
dumpe2fs 1.43.9 (8-Feb-2018)
Already resized
```

/tmp/checkfs.log

```
# cat /tmp/checkfs.log
Will now check all file systems
Create /var/.skip_fsck to skip the check
This might take awhile if it didn't shutdown properly!
fsck 1.43.9 (8-Feb-2018)
e2fsck 1.43.9 (8-Feb-2018)
userdata was not cleanly unmounted, check forced.
Pass 1: Checking inodes, blocks, and sizes
Pass 2: Checking directory structure
Pass 3: Checking directory connectivity
Pass 4: Checking reference counts
Pass 5: Checking group summary information
userdata: 36/35280 files (8.3% non-contiguous), 36158/140780 blocks
```

/tmp/mountfs.log

```
# cat /tmp/mountfs.log
Will now mount all file systems
mount: /misc: mount point does not exist.
```



这个代码是检查/tmp下面当前是不是已经挂载了，如果没有，进行挂载操作。

```
# Mount /tmp firstly to save logs
	mountpoint -q /tmp || mount -t tmpfs tmpfs /tmp
```

判断当前是不是处于recovery模式。是靠挂载在根上的设备节点号来判断的。

```
is_recovery()
{
	# Recovery's rootfs is ramfs
	mountpoint -d /|grep -wq 0:1
}
```



调整所有的设备分区大小，是先读取fstab里的内容来的。

```
resizeall()
{
	echo "Will now resize all file systems"
	while read LINE;do
		do_resize $LINE
	done < /etc/fstab
}
```



misc是一个裸分区。类型是emmc（还有这种类型）

```
Resizing /dev/rkflash0p6 / ext2...
Resizing /dev/rkflash0p3 /misc emmc...
Resizing /dev/rkflash0p8 /userdata ext2...
```

虽然有这些打印，但是只有ext、ntfs、fat支持调整。



```
dumpe2fs 1.43.9 (8-Feb-2018)
dumpe2fs: Bad magic number in super-block while trying to open /dev/rkflash0p6
Wrong fs type!
```

# dumpe2fs 命令

这个命令是把ext2/3/4文件系统的信息dump出来。

命令格式：

```
dumpe2fs [options] device
```

打印device上的superblock和block group信息。

一般我们用-h选项，这样打印出来的东西没有那么多，可读性好。



参考资料

1、

https://man.linuxde.net/resize2fs