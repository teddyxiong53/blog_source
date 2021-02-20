---
title: Linux之cdev和device关系
date: 2017-08-05 22:27:51
tags:
	- Linux

---

--

看Linux里struct cdev的定义，按照我的理解，cdev应该是一种特别的device，按道理应该包含一个device的成员变量才对，但是实际上并不是。这个改怎么理解？

cdev和device是如何关联起来的？

可以采用共同拥有的Kobjcet这个成员作为纽带。





cdev和device的联系纽带是dev_t的设备号。还有共有的kobject。



**cdev更适合理解为一种接口，而不是一种设备。**

**cdev只是对kobject进行一次封装，属于比较底层的东西。**



cdev的主要作用在于提供file_operations结构体和设备号。

leds-gpio.c代码里，为什么没有cdev相关代码？

ledtrig-control-rk.c 这个里面有，

作为一个misc设备。

```
ret = misc_register(&led_ctrl_miscdev);
```

是被leds-pwm.c里调用的。

是靠/dev/rk_led_ctrl这个名字来打开操作的。

也可以通过sysfs来操作。



如果只是普通的cdev，这样的驱动加载后，不会在/sys目录下生成节点的。如果要生成的话。

要调用：

```
class_create
device_create
```



struct file和struct inode关系？



struct file是内核里的一个数据结构，和C库里的FILE是不一样的。file这个结构体不会出现在应用程序里。

file结构体表示一个打开的文件。



inode表示一个文件。和file的不同在于，可以用多个file结构体李艾表示同一个文件的多个文件描述符。而所有的file都指向同一个inode结构体。也就是说，file和inode是多对一的关系。



编写驱动的步骤：

1、看原理图和数据手册，了解设备的操作方法。

2、在内核里找到相近的驱动程序 ，基于它来改，如果没有类似的，就自己写。

3、实现初始化函数。

4、实现open、close、read、write等函数。

5、实现中断函数。

6、编译加载。

7、测试驱动。



led、按键、蜂鸣器pwm这一类gpio的，都是用ioremap来操作寄存器就好。



ioremap和mmap的区别：

1、mmap需要先打开一个文件得到fd，然后把对文件的操作转成对一个指针的操作。在用户程序里用。





我看三星的rtc-s3c.c文件，里面没有明确提到cdev相关的函数，但是有rtc device。那么cdev和rtc device又是什么关系？

是rtc_device_register里调用了rtc_dev_prepare。这个函数里调用了`cdev_init(&rtc->char_dev, &rtc_dev_fops);`。

然后在drivers/char/目录下有个rtc.c文件。