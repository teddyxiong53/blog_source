---
title: Linux内核之devtmpfs
date: 2020-06-22 11:28:49
tags:
	- Linux

---



devtmpfs是什么？

是一个内核启动早期用到的一个临时的用来挂载/dev的文件系统。

这样就可以不用依赖udev。

```
/sys/devices/system # df -T
Filesystem           Type       1K-blocks      Used Available Use% Mounted on
/dev/root            squashfs       41856     41856         0 100% /
devtmpfs             devtmpfs      123444         0    123444   0% /dev
```

devtmpfs是一个设备文件系统，它将其所有文件保存在虚拟内存中。

devtmpfs中的所有内容都是临时的，

因为不会在您的硬盘驱动器上创建任何文件。

**如果卸载devtmpfs实例，其中存储的所有内容都将丢失。**

devtmpfs的根路径在/dev，它通过文件系统上下文创建mount(挂载)对象，使得用户层可以访问。

devtmpfs通过devtmpfsd线程函数，

分配新的命名空间代理(nsproxy)对象，并分配、关联多类命名空间，

如mnt、uts、ipc、pid、cgroup、net、time等，

紧接着mount(挂载)文件系统，

初始工作完成后，进入while循环函数(设备处理函数)。

**届时，devtmpfs进入工作状态，设备可以正常注册或移除。**



设备通过device_add、device_del等相关的函数

以设备节点形式(经过devtmpfs_submit_req函数)注册到requests对象，

它属于req结构，

通过handle函数删除或增加这个设备到(或删除)req的某一级next节点，

期间会再次唤醒devtmpfsd线程函数，为设备节点近一步分配资源。



devtmpfs挂载属于初始化过程中的重要部分，

通过fc_mount函数为文件系统上下文创建mount对象，

分配mount结构对象并指定一个未使用的ID，

设置mount设备名称，

每cpu区域分配mount_pcp结构对象，初始化各种链接对象、关联init用户命名空间等等，关联根目录的用户命名空间，检查是否初始映射，返回vfsmount对象(用于快速访问超级块)等等。

init_mount函数还做了如下操作，

解析名称(是否已经挂载)，挂载路径过程包括安全块检查，使用超级用户权限，注册为内核模块，设置模块释放回调函数free_modprobe_argv，设置用户模式助手，初始化工作列表，队列执行函数call_usermodehelper_exec_work，启动一个用户模式的应用程序call_usermodehelper_exec_work，唤醒kmod_wq工作队列等等。

**devtmpfs与设备模型的关联性不大，**

**但它作为设备节点的挂载区间，还是把它列入设备模型系列比较合适一些**。



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

# 简介

`devtmpfs` 是 Linux 内核中的一个虚拟文件系统，用于管理和提供 `/dev` 目录下的设备节点。`/dev` 目录包含了表示硬件设备的特殊文件，例如磁盘分区、串口端口、输入设备等等。`devtmpfs` 是 Linux 内核中的一个机制，用于自动创建和管理这些设备节点，从而简化了设备管理和设备文件的创建过程。

以下是关于 `devtmpfs` 的一些重要信息：

1. **自动设备节点创建**：`devtmpfs` 负责在 `/dev` 目录中自动创建设备节点。这些设备节点是在内核初始化和设备探测过程中动态创建的，而不需要手动创建或配置。这减轻了系统管理员的工作，因为他们不必手动管理 `/dev` 目录下的设备节点。

2. **冷插拔设备支持**：`devtmpfs` 也支持冷插拔设备，这些设备在运行时可以动态添加或移除。当新设备插入到系统时，`devtmpfs` 会自动为该设备创建相应的设备节点，并在设备被移除时删除相应的节点。

3. **文件系统类型**：`devtmpfs` 是一个特殊的文件系统，与传统的文件系统（如 ext4、XFS 等）不同，它没有一个实际的磁盘存储，而是存在于内存中。它主要用于设备节点的管理，不存储文件数据。

4. **设备访问权限**：`devtmpfs` 会根据设备节点的属性为其设置适当的权限。这通常遵循设备的默认权限和系统规则。

5. **udev 和 mdev**：==在一些 Linux 发行版中，用户空间工具如 `udev` 和 `mdev` 与 `devtmpfs` 一起使用，以管理设备节点并执行更高级的设备管理任务。==

总之，`devtmpfs` 是 Linux 内核的一部分，它为设备节点的创建和管理提供了自动化的机制，简化了设备管理的任务。这对于支持冷插拔设备和简化设备节点的维护非常有用，特别是在嵌入式和嵌入式 Linux 系统中。

# 参考资料

1、

http://blog.chinaunix.net/uid-27717694-id-3574368.html

2、

https://blog.csdn.net/longwang155069/article/details/52757592

3、

https://blog.csdn.net/lickylin/article/details/101922106

4、

https://blog.csdn.net/a29562268/article/details/127719243