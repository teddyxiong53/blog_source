---
title: Linux内核之ramfs和tmpfs区别
date: 2018-03-14 21:55:08
tags:
	- Linux内核

---



ramfs和tmpfs都是在内存里的文件系统。

如果一个进程的瓶颈是硬盘的读写，可以考虑使用内存文件系统来做。

ramfs和tmpfs的比较：

1、当达到空间上限时，tmpfs会报错。ramfs可以继续写。

2、tmpfs固定大小，ramfs不固定大小。

3、tmpfs会使用swap分区，而ramfs不会。

看看我的树莓派上有哪些tmpfs和ramfs。

```
pi@raspberrypi:/boot$ mount | grep -E "(tmpfs|ramfs)"
devtmpfs on /dev type devtmpfs (rw,relatime,size=470128k,nr_inodes=117532,mode=755)
tmpfs on /dev/shm type tmpfs (rw,nosuid,nodev)
tmpfs on /run type tmpfs (rw,nosuid,nodev,mode=755)
tmpfs on /run/lock type tmpfs (rw,nosuid,nodev,noexec,relatime,size=5120k)
tmpfs on /sys/fs/cgroup type tmpfs (ro,nosuid,nodev,noexec,mode=755)
```

没有ramfs。

创建tmpfs和ramfs。

```
root@raspberrypi:~# mount -t tmpfs -o size=20m tmpfs /mnt/tmpfs
root@raspberrypi:~# mount -t ramfs -o size=20m ramfs /mnt/ramfs
```

查看：

```
tmpfs on /mnt/tmpfs type tmpfs (rw,relatime,size=20480k)
ramfs on /mnt/ramfs type ramfs (rw,relatime)
```



# 参考文章

1、

https://www.baidu.com/link?url=qPAW_hF8G037bluTJqQ7dnHMyg-DRfFHQS79mY5tAUXX5eKH8ba3vKIWFr1KpVUk9fBhr2ktzBmHiZlHh5Vura&wd=&eqid=ea13e8fc0000ca42000000035aa929a4

2、

http://blog.csdn.net/awkwardgirl/article/details/23832311

3、

http://blog.csdn.net/wonder4/article/details/44877427

