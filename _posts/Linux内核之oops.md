---
title: Linux内核之oops
date: 2018-04-04 10:18:12
tags:
	- Linux内核

---



#oops在哪里？

通常，oops的内容是由klogd从ringbuffer里读取，并且传递给syslogd。

由syslogd写入到syslog文件。一般这个文件是/var/log/messages。

有时候，klogd也崩溃了。

如果机器崩溃到你不能输入命令或者磁盘无法写入的话，你还有这三种选择：

1、手抄屏幕文本。你也可以拍照。

2、用串口终端启动。

3、使用kdump。



# 受污染的内核

例如下面这段崩溃，是我主动调用panic产生的。

```
Tainted: G
```

Tainted后面跟的内容，可以有：

1、G。说明所有模块都是GPL协议的。P则说明是私有模块。

2、F。有通过insmod -f装载的模块。

3、S。oops发生在smp硬件上。只会发生在集中速龙的处理器上。

4、R。如果模块通过insmod -f加载。

5、M 。机器检查异常。

6、B。如果page释放函数发现了一个错误的页引用。

7、U。如果用户特别请求设置污染标志。

8、D。如果内核刚刚死掉。

下面一行行分析这个oops信息。

```
/mnt/mod # insmod hello.ko
hello module init
# xxx是我主动加的打印。
Kernel panic - not syncing: xxxxxxxxxxxxx
# 在CPU2上，pid是800，命令是insmod。
CPU: 2 PID: 800 Comm: insmod Tainted: G           O    4.14.0 #57
# 硬件名字。这个应该是为了方便给内核开发人员去看的。
Hardware name: ARM-Versatile Express
# 调用栈。
[<8010fcdc>] (unwind_backtrace) from [<8010bfa4>] (show_stack+0x10/0x14)
[<8010bfa4>] (show_stack) from [<8066e608>] (dump_stack+0x8c/0xa8)
[<8066e608>] (dump_stack) from [<8011ef50>] (panic+0xf4/0x298)
[<8011ef50>] (panic) from [<7f00701c>] (cleanup_module+0x0/0xfe4 [hello])
[<7f00701c>] (cleanup_module [hello]) from [<80101be4>] (do_one_initcall+0xb0/0x168)
[<80101be4>] (do_one_initcall) from [<801932ec>] (do_init_module+0x64/0x1dc)
[<801932ec>] (do_init_module) from [<801950e4>] (load_module+0x1c10/0x219c)
[<801950e4>] (load_module) from [<8019577c>] (SyS_init_module+0x10c/0x13c)
[<8019577c>] (SyS_init_module) from [<80107600>] (ret_fast_syscall+0x0/0x48)
# CPU3的状态。
CPU3: stopping
CPU: 3 PID: 0 Comm: swapper/3 Tainted: G           O    4.14.0 #57
Hardware name: ARM-Versatile Express
[<8010fcdc>] (unwind_backtrace) from [<8010bfa4>] (show_stack+0x10/0x14)
[<8010bfa4>] (show_stack) from [<8066e608>] (dump_stack+0x8c/0xa8)
[<8066e608>] (dump_stack) from [<8010e87c>] (handle_IPI+0x1a4/0x388)
[<8010e87c>] (handle_IPI) from [<801014b8>] (gic_handle_irq+0x8c/0x90)
[<801014b8>] (gic_handle_irq) from [<8010cacc>] (__irq_svc+0x6c/0x90)
Exception stack(0xbf0c7f70 to 0xbf0c7fb8)
7f60:                                     00000001 00000000 3ee7b000 801184c0
7f80: bf0c6000 809688c8 bf0c7fd0 00000000 00000000 410fc090 00000000 00000000
7fa0: 00000000 bf0c7fc0 80108114 80108118 600d0013 ffffffff
[<8010cacc>] (__irq_svc) from [<80108118>] (arch_cpu_idle+0x34/0x38)
[<80108118>] (arch_cpu_idle) from [<80688014>] (default_idle_call+0x28/0x2c)
[<80688014>] (default_idle_call) from [<801571c4>] (do_idle+0xd8/0x1d4)
[<801571c4>] (do_idle) from [<8015754c>] (cpu_startup_entry+0x18/0x1c)
[<8015754c>] (cpu_startup_entry) from [<8010e508>] (secondary_start_kernel+0x130/0x138)
[<8010e508>] (secondary_start_kernel) from [<6010188c>] (0x6010188c)
CPU0: stopping
CPU: 0 PID: 0 Comm: swapper/0 Tainted: G           O    4.14.0 #57
Hardware name: ARM-Versatile Express
[<8010fcdc>] (unwind_backtrace) from [<8010bfa4>] (show_stack+0x10/0x14)
[<8010bfa4>] (show_stack) from [<8066e608>] (dump_stack+0x8c/0xa8)
[<8066e608>] (dump_stack) from [<8010e87c>] (handle_IPI+0x1a4/0x388)
[<8010e87c>] (handle_IPI) from [<801014b8>] (gic_handle_irq+0x8c/0x90)
[<801014b8>] (gic_handle_irq) from [<8010cacc>] (__irq_svc+0x6c/0x90)
Exception stack(0x80a01f38 to 0x80a01f80)
1f20:                                                       00000001 00000000
1f40: 3ee4b000 801184c0 80a00000 809688c8 80a01f98 00000000 00000000 809528c0
1f60: 00000000 00000000 00000000 80a01f88 80108114 80108118 60000013 ffffffff
[<8010cacc>] (__irq_svc) from [<80108118>] (arch_cpu_idle+0x34/0x38)
[<80108118>] (arch_cpu_idle) from [<80688014>] (default_idle_call+0x28/0x2c)
[<80688014>] (default_idle_call) from [<801571c4>] (do_idle+0xd8/0x1d4)
[<801571c4>] (do_idle) from [<8015754c>] (cpu_startup_entry+0x18/0x1c)
[<8015754c>] (cpu_startup_entry) from [<80682254>] (rest_init+0xac/0xb0)
[<80682254>] (rest_init) from [<80900cb8>] (start_kernel+0x360/0x36c)
CPU1: stopping
CPU: 1 PID: 0 Comm: swapper/1 Tainted: G           O    4.14.0 #57
Hardware name: ARM-Versatile Express
[<8010fcdc>] (unwind_backtrace) from [<8010bfa4>] (show_stack+0x10/0x14)
[<8010bfa4>] (show_stack) from [<8066e608>] (dump_stack+0x8c/0xa8)
[<8066e608>] (dump_stack) from [<8010e87c>] (handle_IPI+0x1a4/0x388)
[<8010e87c>] (handle_IPI) from [<801014b8>] (gic_handle_irq+0x8c/0x90)
[<801014b8>] (gic_handle_irq) from [<8010cacc>] (__irq_svc+0x6c/0x90)
Exception stack(0xbf0c3f70 to 0xbf0c3fb8)
3f60:                                     00000001 00000000 3ee5b000 801184c0
3f80: bf0c2000 809688c8 bf0c3fd0 00000000 00000000 410fc090 00000000 00000000
3fa0: 00000000 bf0c3fc0 80108114 80108118 600f0013 ffffffff
[<8010cacc>] (__irq_svc) from [<80108118>] (arch_cpu_idle+0x34/0x38)
[<80108118>] (arch_cpu_idle) from [<80688014>] (default_idle_call+0x28/0x2c)
[<80688014>] (default_idle_call) from [<801571c4>] (do_idle+0xd8/0x1d4)
[<801571c4>] (do_idle) from [<8015754c>] (cpu_startup_entry+0x18/0x1c)
[<8015754c>] (cpu_startup_entry) from [<8010e508>] (secondary_start_kernel+0x130/0x138)
[<8010e508>] (secondary_start_kernel) from [<6010188c>] (0x6010188c)
---[ end Kernel panic - not syncing: xxxxxxxxxxxxx

```



# 参考资料

1、内核文档oops-tracing.txt