---
title: Linux之cloud-lab（四）uboot
date: 2018-03-04 11:45:51
tags:
	- Linux

---



执行`make boot V=1`，看到打印如下：

```
sudo qemu-system-arm -M vexpress-a9 -m 128M -net nic,model=lan91118 -net tap -smp 1 -kernel /labs/linux-lab/prebuilt/uboot/arm/vexpress-a9/v2015.07/u-boot -no-reboot -pflash tftpboot/pflash.img -nographic
```

pflash.img里就是把uImage和rootfs.img都放在里面的。



当前的环境变量如下：

```
baudrate=38400
bootcmd=env import 0x43f00000 1024; run bootcmdx
bootdelay=2
bootflash=run flashargs; cp ${ramdisk_addr} ${ramdisk_addr_r} ${maxramdisk}; bootm ${kernel_addr} ${ramdisk_addr_t}
dram=1024M
ethact=smc911x-0
ethaddr=...
flashargs=setenv bootargs root=${root} console=${console} mem=${dram} mtdparts=${mtd} mmci.fmax=190000 devtmpfs.mount=0 vmalloc=256M
kernel_addr=0x44100000
kernel_addr_r=0x80008000
loadaddr=0x80008000
maxramdisk=0x1800000
mtd=armflash:1M@800000(uboot),7M@0x1000000(kernel);24M@0x2000000(initrd)
pxefile_addr_r=0x88000000
ramdisk_addr=0x44800000
ramdisk_addr_r=0x61000000
root=/dev/sda1 rw
stderr=serial
stdout=serial
stdin=serial
```



重点看看bootcmd的。

```
env import 0x43f00000 1024
```

这个是从0x43f0 0000这个nor flash地址上引入环境变量。放的就是一个bootcmdx命令。

```
bootcmdx=set bootargs 'route=172.17.0.3 root=/dev/ram0 console=ttyAMA0'; cp 0x40000000 0x60003000 0x500000 ; cp 0x40500000 0x60900000 0x400000; cp 0x40900000 0x60500000 0x100000; bootm 0x60003000 0x60900000 0x60500000
```

现在就是需要找到这个芯片手册，以及这个板子的硬件框图。

主板Express uATX是Versatile Express系列的第一款可用主板。它嵌入在uATX尺寸的塑料壳子里。盖子是活动的，方便打开来接线。

有个背板，露出了需要外接的接口。就像一台小的台式机。

https://item.taobao.com/item.htm?spm=a230r.1.14.17.afd846c2p4qOu7&id=39150655346&ns=1&abbucket=8#detail

这里有这个板子卖。好贵的。

https://www.youtube.com/watch?v=cysJky0GvRQ

这里有介绍。

由一块uATX的motherboard和一块CoreTile的A9x4的daughterboard构成。

支持：flash、SD卡、兼容flash、网络这几种boot方式。

```
qemu-system-arm -M vexpress-a9 -m 512M -dtb ./arch/arm/boot/dts/vexpress-v2p-ca9.dtb -kernel ./arch/arm/boot/zImage -append “console=ttyAMA0” -serial stdio
```

（qemu要加入dtb就-dtb ./XXX.dtb就可以了。）

好难找到详细资料。我找一下cortex-a9的资料看看。

也没有找到有用。

我就自己做一下推断。

ddr：128MB。在0x6000 0000这个位置。

nor flash：128MB。在0x4000 0000这个位置。

镜像都放在nor flash里。



现在我们再来分析bootcmdx的内容：

```
bootcmdx=set bootargs 'route=172.17.0.3 root=/dev/ram0 console=ttyAMA0'; cp 0x40000000 0x60003000 0x500000 ; cp 0x40500000 0x60900000 0x400000; cp 0x40900000 0x60500000 0x100000; bootm 0x60003000 0x60900000 0x60500000
```

得到这些结论：

```
1、根文件系统是一个initrd。
2、flash里的排列是：
|   uImage    |      initrd    |    dtb   |
|   5M        |      4M        |    1M    |
3、在ddr里的布局，文件系统放在偏移9M的位置。dtb放在偏移5M的位置。
4、bootm把3个地址都带进去了。
5、其他的环境变量基本都没用。
```



# 编译uboot

1、make  uboot，会碰到一些编译错误，根据提示解决就好了。

2、如果编译成功，make boot就会使用你编译的uboot来启动了。

3、运行看看。提示for、do、done这些命令找不到。

而且地址也不对。不知道这些地址命令从哪里配置进来的。

