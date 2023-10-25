---
title: Linux内核之early param分析
date: 2019-12-07 15:03:43
tags:
	- Linux
---

--

# 基本情况

先搜索一下内核里用到的early_param有哪些。

```
bootmem_debug
	打开bootmem的调试。
debug_objects
no_debug_objects
kgdbcon
nokgdbroundup
kgdbwait
earlyprintk
initrd
kmemleak
nosmp
nr_cpus
maxcpus
debug
quiet
loglevel
memblock
cachepolicy
nocache
nowb
ecc
vmalloc
mminit_loglevel
numa_zonelist_order
kernelcore
movablecore
percpu_alloc
ignore_loglevel
sched_debug
mem
```



early_param和setup都是对同一个宏的展开。

```
#define __setup(str, fn)					\
	__setup_param(str, fn, fn, 0)

/* NOTE: fn is as per module_param, not __setup!  Emits warning if fn
 * returns non-zero. */
#define early_param(str, fn)					\
	__setup_param(str, fn, fn, 1)
```

early_param和setup没有大的区别，就是一个优先级的区别。

都是uboot传递过来的cmdline里设置。early_param定义的，会被先执行。

执行完early_param的，才解析setup的。

如果early被设置为1,则执行对应的setup_func，而对于early没有设置为1的obs_kernel_param数组成员，则留到后面去执行。



setup的项有：

```
lpj=
no_file_caps
有很多，不一一列举了。
```

# 简介

`early_param` 是 Linux 内核中的一个机制，

用于在内核启动早期（early boot）阶段传递和处理命令行参数。

这是一种使内核能够在启动时接收和处理参数的机制，而在内核完全初始化之前。

以下是有关 `early_param` 的一些关键信息：

1. **早期启动阶段**：`early_param` 主要用于内核的早期启动阶段，这是内核初始化的早期阶段，==在这个阶段，内核可能尚未完全初始化，但需要获取一些启动参数。==

2. **命令行参数**：通过 `early_param` 机制，内核可以处理命令行参数，这些参数通常在引导加载程序（如 GRUB）中传递给内核。这些参数可以用于配置内核参数、启用或禁用特性，或传递其他启动选项。

3. **`early_param` 结构**：`early_param` 参数通常以 `early_param` 结构的形式存在，其中包含了参数的名称、处理函数以及帮助文本等信息。这些结构在内核源代码中定义和注册，以便内核能够识别和处理这些参数。

4. **参数处理函数**：`early_param` 参数的处理函数是用户定义的函数，用于解析和处理特定参数。这些函数在早期启动阶段调用，以根据参数的值执行相应的操作。处理函数通常负责检查参数的有效性，设置内核选项或执行必要的操作。

5. **注册参数**：`early_param` 参数需要在内核源代码中注册，以便内核在启动时能够识别和处理这些参数。注册通常在内核的启动代码中进行。

6. **示例用途**：`early_param` 参数可以用于许多用途，例如设置内核的命令行参数、指定根文件系统、启用调试选项等。这些参数使系统管理员和开发人员能够动态配置内核的行为，而不需要修改内核源代码。

`early_param` 是内核启动和初始化的一个重要部分，它允许内核在早期阶段接收和处理命令行参数，从而增加了内核的灵活性和可配置性。这对于系统调试、性能优化和适应不同环境的要求非常有用。

# 代码举例

以下是一个示例，演示如何在 Linux 内核中使用 `early_param` 注册和处理一个自定义的早期命令行参数。

```c
#include <linux/module.h>
#include <linux/init.h>
#include <linux/kernel.h>
#include <linux/moduleparam.h>

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");

// 自定义参数的默认值
static int my_param = 0;

// 声明并注册早期参数
static int __init my_param_setup(char *str)
{
    return kstrtoint(str, 10, &my_param);
}
early_param("my_param", my_param_setup);

static int my_init(void) {
    printk(KERN_INFO "Module with early_param: my_param = %d\n", my_param);
    return 0;
}

static void my_exit(void) {
    printk(KERN_INFO "Module with early_param exiting\n");
}

module_init(my_init);
module_exit(my_exit);
```

在此示例中，我们执行以下操作：

1. 定义了一个名为 `my_param` 的自定义参数，它的默认值为 0。

2. 编写了一个 `my_param_setup` 函数，用于解析 `my_param` 参数的值。这个函数将命令行参数的字符串值转换为整数，并将其存储在 `my_param` 变量中。

3. 使用 `early_param` 宏注册了 `my_param` 参数。这会告诉内核在早期引导过程中寻找并处理名为 "my_param" 的命令行参数。当内核在启动时检测到 "my_param" 参数时，它将调用 `my_param_setup` 函数来解析参数的值，并将其存储在 `my_param` 中。

4. 在 `my_init` 函数中，我们打印出 `my_param` 参数的值。

此示例允许您在内核启动时传递命令行参数 "my_param"，并将该参数的值存储在 `my_param` 变量中。您可以在模块加载时通过 `insmod` 命令传递该参数，例如：

```shell
insmod my_module.ko my_param=42
```

这将设置 `my_param` 的值为 42。通过 `early_param` 机制，您可以为内核模块提供灵活的配置选项，而无需修改内核源代码。

# 参考资料

1、

https://blog.csdn.net/rikeyone/article/details/79979887