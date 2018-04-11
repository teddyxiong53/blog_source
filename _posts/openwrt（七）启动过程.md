---
title: openwrt（七）启动过程
date: 2018-04-11 20:49:18
tags:
	- openwrt

---



任何系统的启动都是开发人员首先需要关注的问题。因为只有了解了系统的启动流程，才能真正掌握一个系统。

内核补丁，openwrt因为有自己一些特殊的修改，所以用的内核不是标准内核，需要给内核打一些补丁。

补丁文件放在openwrt/target/linux/generic目录下。

我们先看看针对启动流程的补丁。

```
teddy@teddy-ubuntu:~/work/openwrt/openwrt-master/target/linux/generic/pending-4.4$ vi ./921-use_preinit_as_init.patch
  1 --- a/init/main.c                                                                                                                                                      
  2 +++ b/init/main.c
  3 @@ -966,7 +966,8 @@ static int __ref kernel_init(void *unuse
  4         panic("Requested init %s failed (error %d).",
  5         ┊   ┊ execute_command, ret);
  6     }
  7 -   if (!try_to_run_init_process("/sbin/init") ||
  8 +   if (!try_to_run_init_process("/etc/preinit") ||
  9 +       !try_to_run_init_process("/sbin/init") ||
 10     ┊   !try_to_run_init_process("/etc/init") ||
 11     ┊   !try_to_run_init_process("/bin/init") ||
 12     ┊   !try_to_run_init_process("/bin/sh"))
```

我们可以看到，把默认的init进程改成了/etc/preinit了。

这个是一个脚本文件，我们到openwrt里去看看。

内容就这么多。

```
[ -z "$PREINIT" ] && exec /sbin/init

export PATH="/usr/sbin:/usr/bin:/sbin:/bin"

. /lib/functions.sh
. /lib/functions/preinit.sh
. /lib/functions/system.sh

boot_hook_init preinit_essential
boot_hook_init preinit_main
boot_hook_init failsafe
boot_hook_init initramfs
boot_hook_init preinit_mount_root

for pi_source_file in /lib/preinit/*; do
	. $pi_source_file
done

boot_run_hook preinit_essential

pi_mount_skip_next=false
pi_jffs2_mount_success=false
pi_failsafe_net_message=false

boot_run_hook preinit_main
```

注意这里面的2个函数：boot_hook_init和boot_run_hook。

定义在/lib/functions/preinit.sh里。

boot_hook_init：初始化一个函数队列。

boot_run_hook：运行一个函数队列。



在/init/preinit目录下有一堆的脚本。

```
root@LEDE:/lib/preinit# tree
.
├── 00_preinit.conf
├── 02_default_set_state
├── 03_preinit_do_brcm2708.sh
├── 05_set_preinit_iface_brcm2708
├── 10_indicate_failsafe
├── 10_indicate_preinit
├── 10_sysinfo
├── 30_failsafe_wait
├── 40_run_failsafe_hook
├── 50_indicate_regular_preinit
├── 70_initramfs_test
├── 79_move_config
├── 80_mount_root
├── 81_urandom_seed
├── 99_10_failsafe_login
└── 99_10_run_init
```

preinit脚本还是有调用busybox的标准init。



# 参考资料

1、openwrt启动流程

https://blog.csdn.net/maclinuxye/article/details/52958717