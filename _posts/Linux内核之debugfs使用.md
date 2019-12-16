---
title: Linux内核之debugfs使用
date: 2019-12-16 11:06:25
tags:
	- Linux内核

---

1

# debugfs出现的背景

通常情况下，最常用的内核调试手段是printk。但printk并不是所有情况都好用，比如打印的数据可能过多，我们真正关心的数据在大量的输出里不是那么一目了然；或者我们在调试时可能需要修改某些内核变量，这种情况下printk就无能为力，而如果为了修改某个值重新编译内核或者驱动又过于低效，此时就需要一个临时的文件系统可以把我们需要关心的数据映射到用户空间。在过去，procfs可以实现这个目的，到了2.6时代，新引入的sysfs也同样可以实现，**但不论是procfs或是sysfs，用它们来实现某些debug的需求，似乎偏离了它们创建的本意。**比如procfs，其目的是反映进程的状态信息；而sysfs主要用于Linux设备模型。不论是procfs或是sysfs的接口应该保持相对稳定，因为用户态程序很可能会依赖它们。当然，如果我们只是临时借用procfs或者sysfs来作debug之用，在代码发布之前将相关调试代码删除也无不可。但如果相关的调试借口要在相当长的一段时间内存在于内核之中，就不太适合放在procfs和sysfs里了。故此，debugfs应运而生。





在调试Linux驱动的时候，可以用debugfs来调试。

debugfs类似字符设备驱动。

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

CONFIG_GPIO_SYSFS   定义此宏后 会在/sys/class/gpio/下面到处gpio的设备文件 可以通过此设备文件对gpio进行控制与读取   



参考资料

1、Linux驱动调试中的Debugfs的使用简介

https://blog.csdn.net/wealoong/article/details/7992071