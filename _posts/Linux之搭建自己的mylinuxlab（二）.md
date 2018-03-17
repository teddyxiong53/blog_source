---
title: Linux之搭建自己的mylinuxlab（二）
date: 2018-03-16 16:04:12
tags:
	- Linux

---



现在还是改为直接从kernel启动的方式。

这样启动就没有什么问题。把Makefile调整好。马上就可以正常启动。

```
boot:
	qemu-system-arm -M vexpress-a9 \
	-smp 1 -kernel $(KERNEL_DIR)/arch/arm/boot/zImage \
	 -nographic  -initrd $(ROOT_DIR)/ramfs.gz -dtb $(KERNEL_DIR)/arch/arm/boot/dts/vexpress-v2p-ca9.dtb
```

现在仍然是没有ram0的设备。

但是不影响启动到shell。

我的init脚本写得很简单。

```
#!/bin/sh

bb=/bin/busybox
echo "build root filesystem"

$bb --install -s

echo "mount proc and sys"
$bb mount -t proc proc /proc
$bb mount -t sys sys /sys

echo "mount dev tmpfs"
$bb mount -t tmpfs dev /dev

$bb mount -t devpts devpts /dev/pts


$bb mdev -s

echo "drop to shell"
$bb sh 

exit 0
```



还是从/linuxrc进行启动吧。

配置一下qemu的启动命令。

我加append，总是出错。

我直接/init是一个指向busybox的软链接得了。

靠inittab里调用到/etc/init.d/rcS。

在rcS里加挂载等操作。



# 加入挂载nfs的功能

服务器的配置方法参考我自己的《Ubuntu之允许挂载nfs》。

板端挂载路径。

```
mount -t nfs -o tcp,nolock 192.168.0.1:/home/teddy/work/mylinuxlab/nfs  /mnt
```

这个需要配置服务器的tap0网卡地址，配置板端网卡地址。加入到脚本里。

让make boot的时候，自动配置好。



后续的开发都放在/home/teddy/work/mylinuxlab/nfs路径下，无论是应用还是模块。



