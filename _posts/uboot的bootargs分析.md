---
title: uboot的bootargs分析
date: 2016-12-14 20:33:28
tags:
	- uboot
	- bootargs
---


经常使用的几种组合：
1). 假设文件系统是ramdisk，且直接就在内存中，bootargs的设置应该如下：

```
setenv bootargs ‘initrd=0x32000000,0xa00000 root=/dev/ram0 console=ttySAC0 mem=64M init=/linuxrc’
```
2). 假设文件系统是ramdisk，且在flash中，bootargs的设置应该如下：

```
setenv bootargs ‘mem=32M console=ttyS0,115200 root=/dev/ram rw init=/linuxrc’
```
注意这种情况下你应该要在bootm命令中指定ramdisk在flash中的地址，如bootm kernel_addr ramdisk_addr (fdt_addr)

3). 假设文件系统是jffs2类型的，且在flash中，bootargs的设置应该如下
```
setenv bootargs ‘mem=32M console=ttyS0,115200 noinitrd root=/dev/mtdblock2 rw rootfstype=jffs2 init=/linuxrc’
```
4). 假设文件系统是基于nfs的，bootargs的设置应该如下
```
setenv bootargs ‘noinitrd mem=64M console=ttySAC0 root=/dev/nfs nfsroot=192.168.0.3:/nfs ip=192.168.0.5:192.168.0.3:192.168.0.3:255.255.255.0::eth0:off’
```
或者
```
setenv bootargs ‘noinitrd mem=64M console=ttySAC0 root=/dev/nfs nfsroot=192.168.0.3:/nfs ip=192.168.0.5’
```



Initrd 和noinitrd 之间的区别和用途

当你没有使用ramdisk启动系统的时候，

你需要使用noinitrd 这个参数，

但是如果你使用了的话，

就需要制动initrd=r_addr,size,

r_addr表示initrd在内存中的的位置，size表示initrd的大小，

（从上面的几种情况也可以看出来。使用ramdisk启动并且直接在内存中的时候，就必须使用initrd。）







# 参考资料

1、

https://blog.csdn.net/yusiguyuan/article/details/9471779