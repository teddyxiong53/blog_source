---
title: Linux内核之调试
date: 2018-03-26 16:07:35
tags:
	- Linux内核

---



相比于用户程序开发，内核调试的难度要艰苦得多。更加可怕的是，内核问题带来的风险更高，内核的一个问题，就会让系统崩溃。

驾驭内核调试的能力，很大程度上取决于经验和对整个系统的把握。

解决问题，首先需要找到问题的重现方法。如果找不到重现方法，就只能慢慢啃代码了。

# 用printk来打印

printk除了使用简单外，还有这些特点：

1、健壮。任何时候都可以使用。而且很健壮，这是这种方法受到极大欢迎的重要原因。

2、提供日志等级控制。

3、记录缓冲区。内核消息都保存在一个LOG_BUF_LEN长度的环形队列里。

```
为什么使用环形队列？
1、同步很容易做。
2、在中断上下文里也可以使用printk。
3、不会导致溢出问题。
有的问题：
1、消息被覆盖。导致消息丢失。
```

4、syslogd和klogd。



printk使用时需要注意的：

1、printk的实现非常低效。不要加太多。

2、内核在切换模式的时候，不保存处理器的浮点状态，因此printk并不支持浮点数计算。

# 动态打印

## Dynamic Debug

如果/proc/dynamic_debug/control这个文件节点存在，说明打开了dynamic debug。

否则没有打开。

我当前的代码：

```
# CONFIG_DYNAMIC_DEBUG is not set
# CONFIG_DYNAMIC_DEBUG_CORE is not set
```



注意这个功能需要内核开启 CONFIG_DEBUG_FS，然后再开启 CONFIG_DYNAMIC_DEBUG 这两个选项。

请参考以下文档：

https://www.kernel.org/doc/html/latest/admin-guide/dynamic-debug-howto.html

https://lwn.net/Articles/434833/

在内核的代码中，有类似以下代码的形式：

```
dev_dbg(&client->dev, ``"probing for EDT FT5x06 I2C\n"``);
```

这种，还有

- pr_debug()
- dev_dbg() 

都可以动态使能，可以选择性的使能以下情况：

- 源文件名
- 函数名
- 行号
- 模块名称
- 打印语句的字符串

这些信息可以通过一个文件来查询（如果dynamic_debug这个文件夹不存在，则需要使能 CONFIG_DYNAMIC_DEBUG），不需要都去查源代码，如：



通过bootloader传递给kernel的启动参数来动态打开调试。

```
setenv mmcargs setenv 'bootargs console=${console},${baudrate} root=${mmcroot} dyndbg="\\"file mxsfb_sii902x.c +p"\\"'
```

dyndbg这个参数。

也可以在kernel shell来修改。

```
echo "func omap_i2c_xfer_msg +p" > /sys/kernel/debug/dynamic_debug/control
```

这里比较推荐前两种方法，在启用后，可以通过下面的指令来查询：

```
cat /sys/kernel/debug/dynamic_debug/control | grep keyword
before:
drivers/i2c/busses/i2c-imx.c:896 [i2c_imx]i2c_imx_xfer =_ "<%s>\012"
after:
drivers/i2c/busses/i2c-imx.c:896 [i2c_imx]i2c_imx_xfer =p "<%s>\012"
```

注意其中 “=_” 变为 "=p"，说明改打印信息已开启。



参考资料

1、

https://wiki.phytec.com/pages/viewpage.action?pageId=132776352

# oops

oops是内核通知用户有错误发生的最常用的方式。

因为内核是整个系统的管理者，所以它不能像用户程序出错那样简单处理，它很难自我修复，它也不能把自己杀死。

发布oops的过程，包括向终端输出信息，输出寄存器里的值，输出调用栈。

发布oops之后，内核处于一种不稳定的状态。

oops产生的原因有很多，例如内存访问越界、非法指令等。

内核2.5版本开始引入了kallsyms特性。



# 内核调试配置选项

这些选项都在kernel Hacking里面。

一些很有用的选项是：

1、slab layer debugging

2、high-memory debugging

3、io mapping debugging

4、spinlock debugging

从2.5版本开始，为了检查各类由原子操作引起的问题，内核提供了很好的工具。

托内核抢占的福，内核提供了一个原子操作计数器，它可以配置为一旦在原子操作过程中进程进入睡眠，就打印警告信息，并提供追踪线索。

这种方式捕捉到了很多的bug，受到内核开发者的一致欢迎。

怎样打开这个功能呢？

```
1、CONFIG_PREEMPT=y
2、CONFIG_DEBUG_KERNEL=y
3、CONFIG_KALLSYMS=y
4、CONFIG_DEBUG_SPINLOCK_SLEEP=y
```

# 触发错误并打印信息

其实就是一种断言机制。

最常用的就是BUG()和BUG_ON()。

用法是这样的：

```
if(no_ok) {
  BUG();
}
或者
BUG_ON(no_ok)
```

可以用panic来触发更加严重的错误。调用panic不但会打印错误信息，而且还会挂起整个系统。

```
if(not_ok) {
  panic("something not ok:%ld\n", not_ok);
}
```

有时候，你只是想要打印一些栈上的回溯信息。

```
if(debug) {
  dump_stack();//这个函数就可以打印栈信息。这个是在linux/printk.h里。
}
```

我在我的mylinuxlab里实验，

````
int hello_init(void)
{
    printk("hello module init\n");
	dump_stack();
    return 0;
}
````

insmod时，打印如下。

```
/mnt/mod # insmod hello.ko
hello: loading out-of-tree module taints kernel.
hello module init
CPU: 1 PID: 795 Comm: insmod Tainted: G           O    4.14.0 #57
Hardware name: ARM-Versatile Express
[<8010fcdc>] (unwind_backtrace) from [<8010bfa4>] (show_stack+0x10/0x14)
[<8010bfa4>] (show_stack) from [<8066e608>] (dump_stack+0x8c/0xa8)
[<8066e608>] (dump_stack) from [<7f000014>] (init_module+0x14/0x1c [hello])
[<7f000014>] (init_module [hello]) from [<80101be4>] (do_one_initcall+0xb0/0x168)
[<80101be4>] (do_one_initcall) from [<801932ec>] (do_init_module+0x64/0x1dc)
[<801932ec>] (do_init_module) from [<801950e4>] (load_module+0x1c10/0x219c)
[<801950e4>] (load_module) from [<8019577c>] (SyS_init_module+0x10c/0x13c)
[<8019577c>] (SyS_init_module) from [<80107600>] (ret_fast_syscall+0x0/0x48)
```

再实验一下panic的。

```
int hello_init(void)
{
    printk("hello module init\n");
	//dump_stack();
	panic("xxxxxxxxxxxxx");
    return 0;
}
```

打印如下：

```
/mnt/mod # insmod hello.ko
hello module init
# 这一行的xxx是我打印的。
Kernel panic - not syncing: xxxxxxxxxxxxx
CPU: 2 PID: 800 Comm: insmod Tainted: G           O    4.14.0 #57
Hardware name: ARM-Versatile Express
[<8010fcdc>] (unwind_backtrace) from [<8010bfa4>] (show_stack+0x10/0x14)
[<8010bfa4>] (show_stack) from [<8066e608>] (dump_stack+0x8c/0xa8)
[<8066e608>] (dump_stack) from [<8011ef50>] (panic+0xf4/0x298)
[<8011ef50>] (panic) from [<7f00701c>] (cleanup_module+0x0/0xfe4 [hello])
[<7f00701c>] (cleanup_module [hello]) from [<80101be4>] (do_one_initcall+0xb0/0x168)
[<80101be4>] (do_one_initcall) from [<801932ec>] (do_init_module+0x64/0x1dc)
[<801932ec>] (do_init_module) from [<801950e4>] (load_module+0x1c10/0x219c)
[<801950e4>] (load_module) from [<8019577c>] (SyS_init_module+0x10c/0x13c)
[<8019577c>] (SyS_init_module) from [<80107600>] (ret_fast_syscall+0x0/0x48)
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

关于oops的详细说明，在内核文档里的oops-tracing.txt里。这个内容较多，我专门写一篇文章来总结。



# 神奇的系统请求键

英文是Magic SysRq Key。

SysRq键在大多数的键盘上，都是标准键。

内核里通过配置CONFIG_MAGIC_SYSRQ来打开这个功能。

这样，无论内核在什么情况下，你都可以通过键盘上的SysRq键跟其他按键组合，来给内核发送消息。

下面是一些常用的按键组合：

1、SysRq + s。将脏缓冲区跟硬盘交换分区同步。

2、SysRq + u。卸载所有的文件系统。

3、SysRq + b。重启设备。

这样比你直接重启会安全一点。

内核里的sysrq.txt有详细说明。



# 内核调试器

很多的内核开发者一直都希望有一个用于内核的调试器，但是，Linus本人是很反对的在内核源代码里加入一个调试器，他认为会误导开发者，从而导致引入不良的修正。

所以很多开发者就曲线救国，做了一些非官方的补丁，虽然官方不认可，但是确实功能完善而且强大。

kgdb就是一个补丁。

它让我们可以在另外一台电脑上，通过串口，利用gdb的所有功能对内核进行调试。

这个补丁在内核文档下面有很多的说明。

# 探测系统

你可以有一些小窍门来进行调试。

1、利用uid。

在内核里，这样加入新的东西，避免整个系统直接崩溃。

```
if(current->uid != 7777) {
  //老算法
} else {
  //新算法。
}
```

这样就可以利用7777这个特殊的用户来进行调试了。



# 用二分法找出出错的版本

知道bug是哪个版本开始引入的，这一点对于定位问题非常重要。

git对于这种情况有专门的命令进行支持。



内核开发比用户空间开发更难的一个因素就是内核调试艰难。内核错误往往会导致系统宕机，很难保留出错时的现场。调试内核的关键在于你的对内核的深刻理解。 

# 参考资料

1、《Linux内核设计与实现》

2、使用printk的注意点

https://blog.csdn.net/u010987837/article/details/52595744

3、Linux内核调试方法总结

https://www.cnblogs.com/alantu2018/p/8997149.html