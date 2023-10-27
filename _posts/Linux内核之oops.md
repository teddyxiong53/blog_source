---
title: Linux内核之oops
date: 2018-04-04 10:18:12
tags:
	- Linux内核

---

--

# 简介

Linux中的"Oops"（Out of Print Service）是一种内核错误，

通常是由于内核遇到了无法继续执行的致命错误而引发的。

Oops通常是由于内核代码中的一个错误或异常情况引起的，

它表示内核无法继续正常工作，因此通常会导致系统崩溃。

Oops通常在以下情况下发生：

1. **内核代码错误**：Oops通常由内核代码中的一个错误，如空指针解引用、内存越界、调用堆栈溢出等引起。这些错误可能是由于编程错误、驱动程序问题或硬件故障引起的。

2. **硬件问题**：Oops也可能由硬件问题引起，例如内存错误或其他硬件故障。硬件问题可能导致内核在执行期间遇到异常情况。

3. **模块问题**：内核模块的加载和卸载可能会引发Oops。如果模块的依赖关系或版本不匹配，可能导致内核发生问题。

4. **不一致性状态**：在多处理器系统中，不一致的状态可能导致Oops。这可能是由于竞争条件或同步问题引起的。

当Oops发生时，内核通常会生成一条错误消息，其中包含关于发生Oops的信息，

如堆栈跟踪、寄存器状态和错误原因。

这些信息对于诊断问题和解决内核错误非常有用。

通常，Oops消息会被记录在系统日志中（如`/var/log/messages`或`/var/log/syslog`），

以便管理员或开发人员可以查看它们以进行故障排除。

开发人员通常会使用Oops消息中提供的信息来定位并修复内核问题。

这可能涉及到分析内核堆栈跟踪、检查相关代码和数据结构，以确定问题的根本原因。

需要注意的是，Oops通常是Linux内核的一种保护机制，用于避免出现更严重的问题，例如系统崩溃或数据损坏。

一旦Oops发生，内核会尝试终止当前进程，并在可能的情况下尝试继续运行其他进程，以保持系统的稳定性。因此，当出现Oops时，通常需要及时进行故障排除，以避免进一步的问题。



# oops在哪里？

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