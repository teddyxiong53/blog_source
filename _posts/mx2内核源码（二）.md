---
title: mx2内核源码（二）
date: 2018-03-28 12:10:44
tags:
	- Linux内核

---



现在用adb连接到mx2上。我当前已经是获取了root权限的。

adb shell

然后su。就可以切换到root用户。

查看挂载的文件系统情况。

```
root@mx2:/ # mount
rootfs / rootfs ro,relatime 0 0
tmpfs /dev tmpfs rw,nosuid,relatime,mode=755 0 0
devpts /dev/pts devpts rw,relatime,mode=600 0 0
proc /proc proc rw,relatime 0 0
sysfs /sys sysfs rw,relatime 0 0
none /acct cgroup rw,relatime,cpuacct 0 0
none /sys/fs/cgroup tmpfs rw,relatime,mode=750,gid=1000 0 0
tmpfs /mnt/asec tmpfs rw,relatime,mode=755,gid=1000 0 0
tmpfs /mnt/obb tmpfs rw,relatime,mode=755,gid=1000 0 0
none /dev/cpuctl cgroup rw,relatime,cpu 0 0
/dev/block/mmcblk0p2 /system ext4 rw,relatime,barrier=1,data=ordered 0 0
/dev/block/mmcblk0p1 /data ext4 rw,nosuid,nodev,noatime,barrier=1,nomblk_io_submit,data=ordered,noauto_da_alloc 0 0
/dev/block/mmcblk0p3 /custom ext4 rw,nosuid,nodev,noatime,barrier=1,nomblk_io_submit,data=ordered,noauto_da_alloc 0 0
/dev/block/mmcblk0p4 /cache ext4 rw,nosuid,nodev,noatime,barrier=1,data=ordered 0 0
/dev/fuse /mnt/shell/emulated fuse rw,nosuid,nodev,relatime,user_id=1023,group_id=1023,default_permissions,allow_other 0 0
```

当前只能看到4个分区。1到4，分区0估计是bootloader分区。

里面内置的工具不是busybox，是toolbox。

```
-rwxr-xr-x root     shell     9827993 2015-12-21 18:44 smbd
-rwxr-xr-x root     shell     7201113 2015-12-21 18:44 smbpasswd
lrwxr-xr-x root     shell             2015-12-21 18:44 smd -> toolbox
lrwxr-xr-x root     shell             2015-12-21 18:44 start -> toolbox
lrwxr-xr-x root     shell             2015-12-21 18:44 stop -> toolbox
```

