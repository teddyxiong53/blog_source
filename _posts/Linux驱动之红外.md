---
title: Linux驱动之红外
date: 2019-12-31 13:55:45
tags:
	- Linux

---

1



传输分成发送端(遥控器)，接收端(红外接收头)

发送端发出表示高低电平的不同的光, 接收端收到红外光后还原成对应的高低电平来表示二进制的0和1. 

常用的红外芯片有哪些？

HS0038

这个是红外接收器。

只有3个引脚。vcc、gnd、out。

out引脚输出什么信号呢？就是方波。需要做的就是把这个引脚上的方波自己写代码翻译出来。

发射时，产生38K的pwm载波。

先发射9ms的高电平，再是4.5ms的低电平，这个是表示开始信号。

然后是地址码，地址反码，操作码，操作反码。



与cpu的接口需要几根线？一根线就够了。

看看Linux内核里是怎样进行这个解码的操作的。



涉及的C文件有3个：

rc-main.c

gpio-rc-recv.c

rc-ir-raw.c



```
//申请gpio
gpio_request(pdata->gpio_nr, "gpio-ir-recv");
//设置为输入。
gpio_direction_input(pdata->gpio_nr);
//申请中断，上升沿和下降沿都会触发中断。
request_any_context_irq(gpio_to_irq(pdata->gpio_nr),
				gpio_ir_recv_irq,
			IRQF_TRIGGER_FALLING | IRQF_TRIGGER_RISING,
```

看中断处理函数：

```
gpio_ir_recv_irq
	1、拿到gpio_get_value
	2、如果是正常是低电平，则进行翻转。
	if (gpio_dev->active_low)
		gval = !gval;
	3.ir_raw_event_store_edge
		有一个内核线程和一个定时器来辅助处理。
		如果得到合适的键值了，就会产生input事件，应用层编程跟按键的类似。
```





参考资料

1、红外接收头在linux内核里的驱动

https://blog.csdn.net/jklinux/article/details/73498067

2、史上最全的红外资料 HS0038 PH302 免费下载

https://wenku.baidu.com/view/8f1cae1cc5da50e2524d7f48.html?sxts=1578017970594

3、HS0038（红外接收）

https://gaic.alicdn.com/aic/h5_daily/test/device/3.0.51/kumufp.html

4、46.Linux-分析rc红外遥控平台驱动框架,修改内核的NEC解码函数BUG(1)

https://www.cnblogs.com/lifexy/p/9783694.html