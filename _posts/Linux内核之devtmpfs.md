---
title: Linux内核之devtmpfs
date: 2020-06-22 11:28:49
tags:
	- Linux

---

1

devtmpfs是什么？

是一个内核启动早期用到的一个临时的用来挂载/dev的文件系统。

这样就可以不用依赖udev。

```
/sys/devices/system # df -T
Filesystem           Type       1K-blocks      Used Available Use% Mounted on
/dev/root            squashfs       41856     41856         0 100% /
devtmpfs             devtmpfs      123444         0    123444   0% /dev
```



```
int __init devtmpfs_init(void)
{
    int err = register_filesystem(&dev_fs_type);//注册dev_fs_type文件系统，即将dev_fs_type添加到内核全局总链表中file_systems
    if (err) {
        printk(KERN_ERR "devtmpfs: unable to register devtmpfs ""type %i\n", err);
        return err;
    }
    
    thread = kthread_run(devtmpfsd, &err, "kdevtmpfs");//创建并启动一个内核线程devtmpfsd
    if (!IS_ERR(thread)) {
        wait_for_completion(&setup_done);//进行一个不可打断的等待,允许一个线程告诉另一个线程工作已经完成
    } else {
        err = PTR_ERR(thread);
        thread = NULL;
    }
```

对于devtmpfs，会挂载两次，

```
第一次，挂载到/
在devtmpfs模块初始化时，在其处理线程中，通过调用sys_mount将其挂载至"/"目录下，其代码如下：
*err = sys_mount("devtmpfs", "/", "devtmpfs", MS_SILENT, options);

第二次，挂载到/dev
而在prepare_namespace接口中，通过调用devtmpfs_mount接口，将其挂载至/dev目录下，其代码如下：

/*

挂载devtmpfs_mount函数。

该接口主要调用sys_mount接口实现sys_mount接口的挂载。

目前该接口被prepare_namespace接口调用，进行devtmpfs接口的二次挂载操作，且挂载点为/dev目录。

*/
```



# 参考资料

1、

http://blog.chinaunix.net/uid-27717694-id-3574368.html

2、

https://blog.csdn.net/longwang155069/article/details/52757592

3、

https://blog.csdn.net/lickylin/article/details/101922106