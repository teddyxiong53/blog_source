---
title: Linux内核之debugfs使用
date: 2019-12-16 11:06:25
tags:
	- Linux内核

---

--

# debugfs出现的背景

通常情况下，最常用的内核调试手段是printk。

但printk并不是所有情况都好用，比如打印的数据可能过多，

我们真正关心的数据在大量的输出里不是那么一目了然；

或者我们在调试时可能需要修改某些内核变量，这种情况下printk就无能为力，

而如果为了修改某个值重新编译内核或者驱动又过于低效，

**此时就需要一个临时的文件系统可以把我们需要关心的数据映射到用户空间。**

在过去，procfs可以实现这个目的，到了2.6时代，新引入的sysfs也同样可以实现，

**但不论是procfs或是sysfs，用它们来实现某些debug的需求，似乎偏离了它们创建的本意。**

比如procfs，其目的是反映进程的状态信息；

而sysfs主要用于Linux设备模型。

不论是procfs或是sysfs的接口应该保持相对稳定，

因为用户态程序很可能会依赖它们。

当然，如果我们只是临时借用procfs或者sysfs来作debug之用，在代码发布之前将相关调试代码删除也无不可。

但如果相关的调试借口要在相当长的一段时间内存在于内核之中，

就不太适合放在procfs和sysfs里了。

故此，debugfs应运而生。





在调试Linux驱动的时候，可以用debugfs来调试。

**debugfs类似字符设备驱动。**

但是更加简单。

只需要实现一个file_operations，然后通过debugfs_create_file，就可以在debugfs里建立一个文件节点。

然后就可以对这个文件节点进行open/read/write/ioctl/close这些操作。

打开是CONFIG_DEBUG_FS。在kernel Hacking目录下。

以gpio的为例。

debugfs的节点都放在/sys/kernel/debug目录下。

```
/sys/kernel/debug # ls gpio -lh                             
-r--r--r--    1 root     root           0 Jan  1 08:00 gpio 
```

目前我的板子上看到的是只读的。

如果真的是处于调试目前，都是设置为可写的。

gpio文件内容：

```
/sys/kernel/debug # cat gpio                                        
GPIOs 0-31, platform/pinctrl, gpio0:                                
 gpio-2   (                    |reset               ) out hi        
 gpio-5   (                    |spk-ctl             ) out lo        
 gpio-6   (                    |media key           ) in  hi        
 gpio-7   (                    |volume down         ) in  hi        
 gpio-8   (                    |volume up           ) in  hi        
 gpio-10  (                    |micmute             ) in  hi        
 gpio-12  (                    |micbias1_ext        ) out hi        
 gpio-21  (                    |vbus_host           ) out lo        
                                                                    
GPIOs 32-63, platform/pinctrl, gpio1:                               
                                                                    
GPIOs 64-95, platform/pinctrl, gpio2:                               
                                                                    
GPIOs 96-127, platform/pinctrl, gpio3:                              
                                                                    
GPIOs 128-159, platform/pinctrl, gpio4:                             
 gpio-135 (                    |bt_default_rts      ) out lo        
 gpio-139 (                    |bt_default_poweron  ) out hi        
 gpio-140 (                    |bt_default_wake_host) in  hi        
 gpio-158 (                    |vcc_sd              ) out hi        
```

代码里是这样：

在gpiolib.c里。

```
static int __init gpiolib_debugfs_init(void)
{
	/* /sys/kernel/debug/gpio */
	(void) debugfs_create_file("gpio", S_IFREG | S_IRUGO,
				NULL, NULL, &gpiolib_operations);
	return 0;
}
subsys_initcall(gpiolib_debugfs_init);
```

内核启动后会把debugfs文件系统挂载到/sys/kernel/debug目录下，我们的gpio文件结点就在这里。

如果没有找到，那么可以手动挂载mount-t debugfs none /mnt，这样就挂载到/mnt目录下了。

更为强大的调试选项：

CONFIG_GPIO_SYSFS   定义此宏后 会在/sys/class/gpio/下面导出gpio的设备文件 可以通过此设备文件对gpio进行控制与读取   



# 手动挂载debugfs

```
mount -t debugfs none /sys/kernel/debug
```

# 用途

`debugfs`是Linux内核中一个非常有用的文件系统，专门用于调试和性能分析。它允许开发人员将调试信息和性能统计数据以文件和目录的形式暴露给用户空间。以下是一些`debugfs`的妙用：

1. **调试信息输出**：`debugfs`可用于向用户空间提供内核模块或驱动程序的调试信息。您可以在`debugfs`中创建文件，其中包含有关内核状态、变量值和其他调试信息的内容。这对于排除问题和了解内核运行时状态非常有帮助。

2. **性能分析和监控**：您可以使用`debugfs`来公开性能统计数据，如内存使用、CPU利用率、I/O操作等。这些统计数据可以帮助开发人员优化内核模块、驱动程序或整个系统的性能。

3. **动态配置**：`debugfs`还可以用于动态配置内核参数。您可以创建文件，允许用户空间应用程序更改内核参数，以适应不同的需求。这种动态配置对于调试和性能优化非常有用。

4. **追踪内核事件**：通过`debugfs`，您可以启用和配置内核事件追踪（Kernel Tracepoints），以监视内核的各个方面。这对于识别性能问题和调试内核问题非常重要。

5. **定制化监控**：开发人员可以根据自己的需求创建自定义的`debugfs`目录和文件，以公开与其特定应用程序或驱动程序相关的信息。这使得监控和调试非常灵活。

6. **调试嵌入式系统**：对于嵌入式系统开发，`debugfs`也非常有用。它可以帮助开发人员了解系统的内部状态，特别是在没有标准输出或图形界面的情况下。

请注意，`debugfs`仅在内核配置中启用后才可用。您可以在内核配置中启用它，然后在内核模块或驱动程序中使用相关的API来创建和管理`debugfs`文件和目录。具体的使用方法会根据您的需求和内核版本有所不同，因此请查看相关的内核文档和示例代码以获取更多信息。

## debufs动态配置举例

`debugfs`的动态配置通常用于在运行时更改内核参数，以适应不同的需求。

下面是一个简单的示例，

演示如何使用`debugfs`创建一个文件来**允许用户空间应用程序动态更改内核参数。**

假设我们有一个名为`my_module`的内核模块，它具有一个参数`my_param`，我们想要在运行时允许用户空间应用程序更改这个参数。

首先，在内核模块中，我们需要创建`debugfs`文件并提供相应的读取和写入操作。

```c
#include <linux/module.h>
#include <linux/debugfs.h>

static struct dentry *my_dir;
static struct dentry *my_param_file;

static int my_param = 0;

static int my_param_show(struct seq_file *m, void *v) {
    seq_printf(m, "my_param = %d\n", my_param);
    return 0;
}

static ssize_t my_param_write(struct file *file, const char __user *user_buf,
        size_t count, loff_t *ppos) {
    int val;

    if (kstrtoint_from_user(user_buf, count, 0, &val))
        return -EINVAL;

    my_param = val;
    return count;
}

static const struct file_operations my_param_fops = {
    .owner = THIS_MODULE,
    .write = my_param_write,
};

static int __init my_module_init(void) {
    my_dir = debugfs_create_dir("my_module", NULL);
    if (!my_dir) {
        pr_err("Failed to create debugfs directory.\n");
        return -ENOMEM;
    }

    my_param_file = debugfs_create_file("my_param", 0644, my_dir, NULL, &my_param_fops);
    if (!my_param_file) {
        pr_err("Failed to create debugfs file.\n");
        return -ENOMEM;
    }

    return 0;
}

static void __exit my_module_exit(void) {
    debugfs_remove_recursive(my_dir);
}

module_init(my_module_init);
module_exit(my_module_exit);

MODULE_LICENSE("GPL");
MODULE_AUTHOR("Your Name");
```

上述代码创建了一个名为`my_param`的`debugfs`文件，用户空间应用程序可以通过写入该文件来更改`my_param`的值。读取该文件会显示当前的`my_param`值。

在这个示例中，`kstrtoint_from_user()`函数用于将用户提供的值转换为整数，并检查是否成功。`my_param_show`函数用于显示`my_param`的值。`my_param_write`函数用于在用户空间写入新值以更改`my_param`。

要使用这个功能，您可以在用户空间应用程序中打开`/sys/kernel/debug/my_module/my_param`文件，然后将新的值写入该文件来更改内核参数。这种方法可以用于动态配置内核模块的参数。

# 参考资料

1、Linux驱动调试中的Debugfs的使用简介

https://blog.csdn.net/wealoong/article/details/7992071