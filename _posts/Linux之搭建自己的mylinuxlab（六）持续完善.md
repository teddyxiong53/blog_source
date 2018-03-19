---
title: Linux之搭建自己的mylinuxlab（六）持续完善
date: 2018-03-18 21:25:34
tags:
	- Linux

---



#从initramfs转到SD卡的rootfs

我试了一下给qemu加上-sd，是正常的。

我在qemu里对加载进来的SD卡进行写入也是正常的。所以现在可以用SD卡来带文件系统启动看看。

1、生成一个SD卡镜像文件。先不用多大，给64M就行。

```
dd if=/dev/zero of=./sd.img bs=1M count=64
格式化为ext2的。
sudo mkfs.ext2 ./sd.img
```

2、修改rootfs里的init为这样的脚本内容。

```
#!/bin/sh

bb=/bin/busybox
echo "build root filesystem"


if [ ! -d /sys ];then
  echo "/sys dir not exist, create it..."
  $BUSYBOX mkdir /sys
fi

echo "mount proc and sys"
$bb mount -t proc proc /proc
$bb mount -t sysfs sysfs /sys

echo "mount dev tmpfs"
$bb mount -t tmpfs dev /dev

if [ ! -d /dev/pts ];then
  echo "/dev/pts dir not exist, create it..."
  $BUSYBOX mkdir /dev/pts
fi
$bb mount -t devpts devpts /dev/pts


$bb mdev -s

echo "begin switch root to sd card " >> /dev/kmsg

$bb mkdir /newroot

if [ ! -b "/dev/mmcblk0" ]; then
    echo "can't find /dev/mmcblk0, now use the initramfs" >> /dev/kmsg
    echo "drop to shell" >> /dev/kmsg
    $bb sh 
else
    $bb mount /dev/mmcblk0 /newroot
    if [  $? -eq 0 ]; then
        echo "mount rootfs successfully" >> /dev/kmsg
    else
        echo "mount rootfs failed" >> /dev/kmsg
        $bb sh
    fi
fi 
echo "now begin to change to newroot" >> /dev/kmsg
echo "should clean something firstly" >> /dev/kmsg

$bb umount -f /proc
$bb umount -f /sys
$bb umount -f /dev/pts
$bb umount -f /dev

echo "enter new root " >> /dev/kmsg

exec $bb switch_root -c /dev/console /newroot /init

if [  $? -ne 0 ]; then
    echo "enter new root failed, now drop to shell" >> /dev/kmsg
    $bb mount -t proc proc /proc
    $bb sh
fi

exit 0

```

3、修改Makefile和脚本。

让make rootfs可以生成sd.img的内容。

4、make boot就可以了。

启动后，可以看到已经切换到SD卡的了。

```
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/mmcblk0             62.0M     11.7M     47.1M  20% /
/ # 
```

# 直接从SD卡的rootfs启动

initramfs其实可以没有的。

增加一个boot-sd的Makefile目标。

```
boot-sd:
	$(ROOT_DIR)/ifconfig_tap0.sh &
	qemu-system-arm -M vexpress-a9 -net nic,model=lan9118 -net tap \
	-smp 1 -kernel $(KERNEL_DIR)/arch/arm/boot/zImage  \
	-nographic  -initrd $(ROOT_DIR)/ramfs.gz -dtb $(KERNEL_DIR)/arch/arm/boot/dts/vexpress-v2p-ca9.dtb \
	-append "console=ttyAMA0 root=/dev/mmcblk0 rootfstype=ext2" -sd $(ROOT_DIR)/sd.img
```

现在把从SD卡的rootfs启动改为默认的，make boot的行为。

而之前的改为make boot-ramfs。



# 关闭initrd和initramfs的内核配置

我本来是想要看SD卡里的系统的挂载过程。

但是，加的打印一直看不到。

我就把内核配置里的initrd和initramfs都关闭。

这些对应的mount代码执行到了。

而且挂载的情况显示也不同了。现在是这样的。

```
/ # mount
/dev/root on / type ext2 (rw,relatime,errors=continue)
proc on /proc type proc (rw,relatime)
sysfs on /sys type sysfs (rw,relatime)
devpts on /dev/pts type devpts (rw,relatime,mode=600,ptmxmode=000)
/ # df -h
Filesystem                Size      Used Available Use% Mounted on
/dev/root                62.0M     11.7M     47.1M  20% /
/ # 
```

之前的/dev/root都是显示/dev/mmcblk0 。

