---
title: qemu之跟host共享文件的方法
date: 2021-06-10 16:57:11
tags:
	- qemu

---

--

The documentation suggests to expose a Samba server running somewhere in the network, or use the `-net user,smb=/path/to/folder` to start a samba server.



For vexpress-a9, the only available kind of disk is an emulated SD card. You can set one up with "-drive if=sd,cache=writeback,file=yoursd.img". Note that emulated SD is not very fast. Also you'll need to make sure your guest kernel has the SD controller and SD card support compiled in and that your initrd will mount and pivot to it.

For a QEMU VM with more flexible options (support for more RAM, better performing disk and networking, etc) you should look at the 'virt' board instead. 'vexpress-a9' is only really recommended if you specifically have an image you want to run on an emulation of that devboard.



对于vexpress的板子，唯一可行的方式是用模拟的SD卡。

增加一个：

```
-drive if=sd,cache=writeback,file=mysd.img
```

用默认的那个rootfs.ext的，在make后会丢失。

好像不行。





对于仿真运行，更加推荐virt的板子。



```
  qemu_riscv32_virt_defconfig         - Build for qemu_riscv32_virt
  qemu_riscv64_virt_defconfig         - Build for qemu_riscv64_virt
qemu_aarch64_virt_defconfig         - Build for qemu_aarch64_virt
    
```



参考资料

1、Shared folder between QEMU Windows guest and Linux host

https://unix.stackexchange.com/questions/165554/shared-folder-between-qemu-windows-guest-and-linux-host

2、

https://stackoverflow.com/questions/51105603/how-to-use-persistent-storage-on-a-qemu-machine

3、

https://blog.csdn.net/goodwillyang/article/details/46910465