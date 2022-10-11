---
title: Linux之设备驱动模块自动加载
date: 2018-03-07 10:54:24
tags:
	- Linux

---



在树莓派上进行测试。

udev使用inotify机制来监测udev的规则文件是否发生变化。udev和驱动模块之间的uevent使用socket。

# 编写驱动文件

写一个demo_device.c和demo_driver.c。

demo_device.c内容：

```
#include <linux/module.h>  
#include <linux/types.h>  
#include <linux/fs.h>  
#include <linux/init.h>  
#include <linux/platform_device.h>  
#include <linux/device.h>  
#include <linux/io.h>  

static struct platform_device demo_device = {
    .name = "demo_device",
    .id = -1,
};

static  int __init demo_device_init(void)
{
    printk(KERN_INFO "demo device register \n");
    platform_device_register(&demo_device);
    return 0;
}

static void __exit demo_device_exit(void)
{
    printk(KERN_INFO "demo device unregister \n");
    platform_device_unregister(&demo_device);
    
}

module_init(demo_device_init);
module_exit(demo_device_exit);

MODULE_LICENSE("Dual BSD/GPL");
MODULE_AUTHOR("teddyxiong53 <1073167306@qq.com>");
MODULE_DESCRIPTION("demo device desc");


```

demo_driver.c

```
#include <linux/module.h>  
#include <linux/types.h>  
#include <linux/fs.h>  
#include <linux/init.h>  
#include <linux/platform_device.h>  
#include <linux/device.h>  
#include <linux/io.h>  
#include <linux/cdev.h>  
#include <linux/kmod.h>  
#include <linux/of_platform.h>  

static struct cdev demo_dev;
static dev_t ndev;
static struct class *demo_class;

static int demo_open(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "demo dev open \n");
    return 0;
}

static int demo_close(struct inode *inode, struct file *file)
{
    printk(KERN_INFO "demo dev close \n");
    return 0;
}

static ssize_t demo_read(struct file *file, char __user *buf, size_t len, loff_t *off)
{
    printk(KERN_INFO "demo dev read \n");
    return 0;
}


static struct file_operations demo_ops = {
    .owner = THIS_MODULE,
    .open = demo_open,
    .release = demo_close,
    .read = demo_read,
};


static int demo_driver_probe(struct platform_device *pdev)
{
    int ret;
    cdev_init(&demo_dev, &demo_ops);
    ret = alloc_chrdev_region(&ndev, 0, 1, "demo_dev");
    if(ret)
    {
        printk("alloc char dev error \n");
        return ret;
    }
    printk(KERN_INFO "demo_dev major:%d, minor:%d \n", MAJOR(ndev), MINOR(ndev));
    ret = cdev_add(&demo_dev, ndev, 1);
    device_create(demo_class, NULL, ndev, NULL, "demo_dev");
    return 0;
}

static int demo_driver_remove(struct platform_device *pdev)
{
    printk(KERN_INFO "demo driver remove \n");
    device_destroy(demo_class, ndev);
    cdev_del(&demo_dev);
    unregister_chrdev_region(ndev, 1);
    return 0;
} 


struct platform_driver demo_driver = {
    .driver = {
        .name = "demo_device",
        .owner = THIS_MODULE,
    },
    .probe = demo_driver_probe,
    .remove = demo_driver_remove,
    
};

static  int __init demo_driver_init(void)
{
    printk(KERN_INFO "demo driver register \n");
    demo_class = class_create(THIS_MODULE, "demo_dev");
    
    platform_driver_register(&demo_driver);
    return 0;
}

static void __exit demo_driver_exit(void)
{
    printk(KERN_INFO "demo driver unregister \n");
    class_destroy(demo_class);
    platform_driver_unregister(&demo_driver);
    
}

module_init(demo_driver_init);
module_exit(demo_driver_exit);

MODULE_LICENSE("Dual BSD/GPL");
MODULE_AUTHOR("teddyxiong53 <1073167306@qq.com>");
MODULE_DESCRIPTION("demo driver desc");

MODULE_ALIAS("platform:demo_device");

```



# 搭建树莓派上的驱动编译环境

1、在/home/pi目下，新建linux_src目录。把github上跟我当前树莓派同一个版本的源代码下载下来。

```
pi@raspberrypi:/lib/modules/4.4.33-v7+$ uname -r
4.4.33-v7+
```

2、解压，配置，编译。

```
1、zcat /proc/config.gz > ./.config
2、make ARCH=arm CROSS_COMPILE=arm-none-eabi- modules
```

树莓派编译特别慢。

3、编写Makefile。

```
KVERS := $(shell uname -r)
KERN_SRC_DIR = /home/pi/linux_src/linux-rpi-4.4.y
obj-m += demo_device.o demo_driver.o

all:
	make -C $(KERN_SRC_DIR) M=$(CURDIR) modules 
	
modules_install:
	make -C $(KERN_SRC_DIR) M=$(CURDIR) modules_install 
clean:
	make -C $(KERN_SRC_DIR) M=$(CURDIR) clean
```

4、编译安装。

指定安装路径。

```
make modules_install INSTALL_MOD_PATH=/home/pi/local_lib
```

安装module的时候，会自动调用depmod工具，更新/lib/modules/xxx/下的modules.alias、modules.alias.bin、modules.dep和modules.dep.bin文件。

```
pi@raspberrypi:~/local_lib/lib/modules/4.4.34-v7/extra$ tree
.
├── demo_device.ko
└── demo_driver.ko

0 directories, 2 files
```



5、运行测试。

```
modprobe demo_device
```

```
pi@raspberrypi:~/local_lib/lib/modules/4.4.34-v7/extra$ dmesg
[ 7732.015118] demo_device: no symbol version for module_layout
```

这个网上说是因为编译ko的内核代码跟当前系统内核的不是一个版本导致的。

查看正常的ko文件。

```
 modprobe --dump-modversions  /lib/modules/4.4.33-v7+/kernel/drivers/i2c/i2c-dev.ko | grep module_layout
0xf51a0302      module_layout
```

而我现在的ko文件。

```
pi@raspberrypi:~/local_lib/lib/modules/4.4.34-v7/extra$ modprobe --dump-modversions demo_device.ko 
```

没有任何输出。

我用apt-get来安装linux源代码头文件看看。

```
sudo apt-cache search linux-headers*
搜索到raspberrypi-kernel-headers 
sudo apt-get install raspberrypi-kernel-headers
```

现在把Makefile改一下，

```
KERN_SRC_DIR = /lib/modules/4.4.50-v7+/build
```

再编译。现在看看。

```
pi@raspberrypi:~/test/uevent$ modprobe --dump-modversions demo_device.ko
0xb344870e      module_layout
0x4faba9f8      platform_device_unregister
0x2e5810c6      __aeabi_unwind_cpp_pr1
0x3293da33      platform_device_register
0x27e1a049      printk
```

有版本信息了。但是版本信息跟其他的ko的还是不一样。

看dmesg信息：

```
disagrees about version of symbol module_layout
```

参考这篇文章：https://stackoverflow.com/questions/2720177/module-layout-version-incompatibility

强行把我的ko的版本号改了。

算了。不改了。



看dmesg信息。

可以看到demo_driver也会被自动加载了。设备和驱动匹配上了。



linux中存在一些特别的设备驱动，被编译进内核，在内核启动阶段就被加载。

但是它的驱动程序被编译为ko，在系统启动完成后，自动识别设备的类型并加载对应的设备驱动。



# 参考文章

1、http://blog.csdn.net/luckyapple1028/article/details/44261391

