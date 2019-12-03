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

#调整分区大小

现在编译后，kernel超过5M了。导致mini2440-lab的nand.bin里的布局覆盖到后面了。
我现在最稳妥的做法，就是把kernel的分区加大。
需要做的事情有：
1、改uboot代码。

```
unsigned int dynpart_size[] = {
    CFG_UBOOT_SIZE, 0x20000, 0x500000, 0xffffffff, 0 };
char *dynpart_names[] = {
    "u-boot", "u-boot_env", "kernel", "rootfs", NULL };
```

虽然有这个代码，但是没有看到哪里使用了。

有，是在nand里使用的。

不过是属于一个命令里的，那就是可用不用的。

结论：uboot里不用改。

2、改kernel代码。

这里我之前就注意到，我改bootargs，分区信息并不能生效。

在arch/arm/mach-s3c24xx/mach-mini2440.c里。

```
把kernel的改成8M。rootfs的往后推。
```

3、改bootcmd。

```
nand read 0x31000000 0x60000 0x800000;
set bootargs noinitrd root=/dev/mtdblock3   rootfstype=jffs2  console=ttySAC0,115200  ;
bootm 0x31000000 
```

测试一下，发现还是不行。难道是uboot也要改？

我改了试一下。

我把uboot的改了。再看。

```
MINI2440 # mtdparts

device nand0 <mini2440-nand>, # parts = 4
 #: name                        size            offset          mask_flags
 0: u-boot              0x00040000      0x00000000      0
 1: env                 0x00020000      0x00040000      0
 2: kernel              0x00500000      0x00060000      0
 3: root                0x03aa0000      0x00560000      0
```

怎么是没有改的效果呢？

这个分区信息怎么读取出来的呢？我觉得需要改的地方都改了啊。

在uboot里打开jffs2的调试。

```
---mtdparts_init---
last_ids  : 
env_ids   : <NULL>
last_parts: 
env_parts : mtdparts=mini2440-nand:256k@0(u-boot),128k(env),5m(kernel),-(root)
```

我看mini2440.h里，有环境变量的宏，我也都改成8M的。

还是有问题。

```
VFS: Cannot open root device "mtdblock3" or unknown-block(31,3): error -5
Please append a correct "root=" boot option; here are the available partitions:
```

```
1f00            2048 mtdblock0  (driver?)
1f01             256 mtdblock1  (driver?)
1f02             128 mtdblock2  (driver?)
1f03            8192 mtdblock3  (driver?)
1f04           56960 mtdblock4  (driver?)
```

怎么有5个分区啊。

我发现问题越来越奇怪了。

uImage都不到3M的。

我现在把改成8M的改动都回退。

把之前打开nor flash的相关内容都关闭。

现在回退到之前正常的状态了。



