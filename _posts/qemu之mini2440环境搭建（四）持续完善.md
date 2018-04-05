---
title: qemu之mini2440环境搭建（四）持续完善
date: 2018-04-05 20:26:20
tags:
	- qemu

---



# 加入usb相关支持

1、qemu启动里加入选项。usb.img，我是用dd生成的一个64M的文件，mkfs.ext2格式化一下。

```
-usb -usbdevice disk::./usb.img
```

2、编译内核的模块。默认的配置就是选配为module的。

我加了一个选项，来拷贝ko文件到nfs/ko目录下。

```
make kernel-modules
make module-copy 
```

3、重新做文件系统和nand.bin文件，启动。

4、手动加载模块。

```
insmod scsi_mod.ko
insmod sd_mod.ko 
insmod usb-storage.ko
```

5、现在用用mdev -s扫描一下，才能出现/dev/sda节点。

6、我可以用fdisk进行分区。格式化的时候，有不少的打印，但是还是格式化完成了。

```
/proc/bus # mkfs.ext2 /dev/sda1
Filesystem label=
OS type: Linux
Block size=1024 (log=0)
Fragment size=1024 (log=0)
16384 inodes, 65510 blocks
3275 blocks (5%) reserved for the super user
First data block=1
Maximum filesystem blocks=262144
8 block groups
8192 blocks per group, 8192 fragments per group
2048 inodes per group
Superblock backups stored on blocks:
        8193, 24577, 40961, 57345
usb 1-3: reset full-speed USB device number 2 using s3c2410-ohci
usb 1-3: reset full-speed USB device number 2 using s3c2410-ohci
usb 1-3: reset full-speed USB device number 2 using s3c2410-ohci
```

7、挂载。现在挂载不上去，总是提示

```
/proc/bus # mount -t ext2 /dev/sda1 /usb
mount: mounting /dev/sda1 on /usb failed: No such device
```

重启还是如此。我格式化为vfat的看看。

还是不行。

这个点默认不打开。增加一个boot-usb的选项。



