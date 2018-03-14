---
title: Linux内核之启动时挂载文件系统过程
date: 2018-03-14 21:17:14
tags:
	- Linux内核

---



讨论问题，需要先尽量辨明概念。

vfs。这个没有疑问，就是一套规范，linux里所有的支持的文件系统都要符合这个规范。

rootfs。在内核里是一种文件系统类型，跟ext4这些是一个层次的东西。跟我们用busybox做出来了的那套目录内容不是一个概念的东西。虽然那个我们也习惯叫做rootfs。

```
static struct file_system_type rootfs_fs_type = {
	.name		= "rootfs",
	.mount		= rootfs_mount,
	.kill_sb	= kill_litter_super,
};
```

```
static struct file_system_type ext4_fs_type = {
	.owner		= THIS_MODULE,
	.name		= "ext4",
	.mount		= ext4_mount,
	.kill_sb	= kill_block_super,
	.fs_flags	= FS_REQUIRES_DEV,
};
```

为什么需要rootfs这个东西的存在？

是为了在vfs机制下，给系统提供最原始的挂载点。

这个rootfs是在内存里的。



mount实际上就是新建了一个vfsmount结构体。



释放Initramfs到rootfs；如果Initramfs中有init，这种情况比较特殊、rootfs就是最后系统使用的根文件系统。

而且此时，不需要在单独烧录根文件系统的img；此时，根文件系统就是内核uImage的一部分。当然，缺陷就是该文件系统运行时的介质是ramdisk即内存盘、它不再与磁盘对应；因此，此时修改根目录下的文件将不被得到保存。它的内核配置项为：CONFIG_INITRAMFS_SOURCE。实际项目中会经常碰到。



```
if (!ramdisk_execute_command)  ramdisk_execute_command = "/init";  
  if (sys_access((const char __user *) ramdisk_execute_command, 0) != 0) {  
    ramdisk_execute_command = NULL;  
    //如果此时rootfs中没有init，则加载initfd、nfs或磁盘文件系统  
    //也即磁盘的文件系统挂载至rootfs的/root目录，并设置系统current对应的根目录项为磁盘根目录项、系统current根文件系统为磁盘文件系统  
    //至此，rootfs对于以后所有进程而言、已被隐藏。  
    prepare_namespace();   
  }  
  init_post(); //启动init进程 
```



挂载实际文件系统至rootfs，并调用set_fs_root设置为系统current的根文件系统





# 参考文章

1、

http://blog.csdn.net/tankai19880619/article/details/12093239

