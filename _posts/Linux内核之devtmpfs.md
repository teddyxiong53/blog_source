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



参考资料

1、

http://blog.chinaunix.net/uid-27717694-id-3574368.html