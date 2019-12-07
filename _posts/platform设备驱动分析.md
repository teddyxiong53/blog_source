---
title: platform设备驱动分析
date: 2016-11-04 22:30:44
tags:
	-linux驱动
---
1

看DM9000的驱动代码，会发现`platform_driver`这样一些概念，`platform_driver`具体怎么理解呢？它的设计初衷是什么呢？下面就进行分析。

对于I2C、SPI、USB设备而言，设备和驱动都挂接在对应的总线上，但是对于led、以太网这种不依附于总线的设备，设备和驱动如何进行关联呢？内核为此提供了虚拟的总线，platform。我们且称之为平台总线。
相应地，挂接在平台总线上的设备和驱动被称为平台设备`platform_device`和平台驱动`platform_driver`。

平台设备并不是与块设备、字符设备、网络设备并列的概念。

**平台设备的一致特点是：**

**可以通过CPU bus直接寻址。就是寄存器。**（不是必须的，例如我们自己写什么都不能做的demo用的platform设备）。

所以有platform_get_resource 这些函数。



可以说，paltform设备对Linux驱动工程师是非常重要的，因为我们编写的大多数设备驱动，都是为了驱动plaftom设备。



怎么在用户程序里操作平台设备呢？

例如led_s3c24xx.c里。led驱动，就是平台设备驱动。

没有看到read、write这些操作啊。



```
struct s3c24xx_gpio_led {
	struct led_classdev		 cdev;
	struct s3c24xx_led_platdata	*pdata;
};
```

从代码看，Linux对led也封装了一个框架。

就是struct led_classdev。

对应的头文件是：linux/leds.h

Documentation下面也有leds-class.txt文档。

看一下这个文档。

可以在/sys/class/leds目录下，看到三个子目录：

```
/sys/class/leds # ls  
blue   green  red     
```

进入到blue。

```
/sys/devices/platform/pwm_leds@0/leds/blue # ls           
brightness      device          power           trigger   
debug           max_brightness  subsystem       uevent    
```

直接：

```
echo "255" > brightness
```

灯就会变蓝。

rk_led_ctrl 是misc下面的一个设备。

```
/sys/devices/platform/pwm_leds@0/leds/blue # cat /proc/misc   
 58 memory_bandwidth                                          
 59 network_throughput                                        
 60 network_latency                                           
 61 cpu_dma_latency                                           
 62 vendor_storage                                            
  0 rk_led_ctrl                                               
183 hw_random                                                 
 63 rfkill                                                    
```

对应的代码：

```
./trigger/ledtrig-control-rk.c:665:     led_ctrl_miscdev.name = "rk_led_ctrl";
```

这个然后在leds-pwm.c里使用了。



led的你还是可以自己绕开led驱动框架自己来写的。

```
#include <linux/module.h>
#include <linux/kernel.h>
#include <linux/fs.h>
#include <linux/init.h>
#include <linux/device.h>
#include <linux/interrupt.h>
#include <linux/sched.h> 
#include <linux/irq.h>
#include <asm/uaccess.h>
 
#include <linux/platform_device.h>
#include <linux/io.h>
 
static int major;
 
static struct class *cls;
static struct device *dev;
 
static volatile unsigned long *gpio_con;
static volatile unsigned long *gpio_dat;
static int pin;
 
static int led_open(struct inode *inode, struct file *file){
 
	*gpio_con &= ~(0x03 << (pin*2));
	*gpio_con |=  (0x01 << (pin*2));
	return 0;
}
 
static ssize_t led_write(struct file *file, const char __user *buf,
	size_t count, loff_t *ppos){
 
	int val;
	copy_from_user(&val, buf, count);
 
	if(val == 1){
		
		*gpio_dat &= ~(1<<pin);
	}else{
	
		*gpio_dat &=  (1<<pin);
	}
 
	return 0;
}
 
static struct file_operations led_fops = {
 
	.owner = THIS_MODULE,
	.open  = led_open,
	.write = led_write,
};
 
static int led_probe(struct platform_device *pdev){
 
	struct resource *res;
	// 最后一个参数 0 表示第1个该类型的资源
	res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
	gpio_con = ioremap(res->start, res->end - res->start + 1);
	gpio_dat = gpio_con + 1;
 
	res = platform_get_resource(pdev, IORESOURCE_IRQ, 0);
	pin = res->start;
 
	printk("led_probe, found led\n");
 
	// 注册设备驱动 创建设备节点
	major = register_chrdev(0, "myled", &led_fops);
	// 创建类
	cls = class_create(THIS_MODULE, "myled");
	// 创建设备节点
	dev = device_create(cls, NULL, MKDEV(major, 0), NULL, "led");
 
	return 0;
}
 
static int led_remove(struct platform_device *pdev){
 
	printk("led_remove, remove led\n");	
	// 删除设备节点
	device_unregister(dev);
	// 销毁类
	class_destroy(cls);
	// 取消注册设备驱动
	unregister_chrdev(major, "myled");
	// 取消内存映射
	iounmap(gpio_con);
 
	return 0;
}
 
struct platform_driver led_drv = {
 
	.probe 	= led_probe,	//匹配到dev之后调用probe
	.remove = led_remove,
	.driver = {
		.name = "myled",
	},
};
 
static int led_drv_init(void){
 
	platform_driver_register(&led_drv);
	return 0;
}
 
static void led_drv_exit(void){
	
	platform_driver_unregister(&led_drv);
}
 
module_init(led_drv_init);
module_exit(led_drv_exit);
MODULE_LICENSE("GPL");
```



i2c-gpio

这个是用io引脚模拟i2c总线的驱动。

是一个典型的平台设备驱动。



参考资料

1、Linux Platform devices 平台设备驱动

https://www.cnblogs.com/alan666/p/8311851.html

2、Linux Platform devices 平台设备驱动

https://blog.csdn.net/lizuobin2/article/details/51607813

3、Linux led子系统

http://www.360doc.com/content/12/0312/20/6828497_193834197.shtml

4、

https://tinylab.org/lwn-448499/