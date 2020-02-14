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



红外编码格式有两种：

1、pwm。脉冲宽度调制。典型是NEC。

2、ppm。脉冲位置调制。典型是Philips的RC-5/6/7系列。



# NEC红外编码

这个是最主流的编码方式。

```
1、载波频率是38KHz。
2、逻辑1是，HLLL。逻辑0是HL。
	H是高电平。L是低电平。
	逻辑1是4个单位时间，逻辑0是2个单位时间。
	一个单位时间是560us。
	根据这个来进行解码的。
	
```

协议格式：

```
|9ms高电平|  5ms低电平 | 地址（8bit） |地址反码  | 命令（8bit）| 命令反码|
```

有个特殊情况，就是一直按住一个键的时候。会简化数据。

# 学习模式

对于电视，音箱，一般使用专门的遥控芯片，而不是通用的单片机。

专用的遥控芯片的特点是：编码格式固定，一个键只有一个编码 ，学习比较容易。

而空调是各自用单片机来做的。

而且空调的状态多，必须一次发送完毕。所以编码很长，并且同一个按键，在不同状态下的编码不一样，造成学习上的困难。



学习型遥控常用的载波频率为38kHz,这是由发射端编码芯片所使用的455kHz晶振来决定的。

现在基本上采用一体化接收头做为信号的接收，把解调出来的信号送入单片机进行学习（记录各个高低电平的时间长度），然后存入EEPROM内，学习完成后再将EEPROM的高低电平的时间数据读取并与38kHz载波进行调制，然后红外发光管发送出去。

这里使用具有I2C总线接口的E2PROM芯片AT24C32作为存储器，其容量为4KB,用来保存识别出来的遥控信号的高电平与低电平宽度数据。



学习分为两类：

1、固定码格式学习。需要收集不同类型的遥控器信号，然后进行识别比较，最后再记录。

​	优点是对硬件要求不高，存储空间要求也小。

​	缺点是对未知编码的遥控器无效。

2、波形拷贝方式。这个是对信号的时间信息进行存储。这个就任何遥控器都可以学习。



在进行学习的是，遥控举例接收器的距离要在2到6cm。



这里有个智能遥控，

https://item.taobao.com/item.htm?id=558396096340



参考资料：

https://wenku.baidu.com/view/0a17f5e8172ded630b1cb6d1.html

学习型红外遥控器要点

这篇论文不错。

https://wenku.baidu.com/view/a0a2bd2826284b73f242336c1eb91a37f11132b0.html?from=search

学习型红外使用指南

https://wenku.baidu.com/view/53c61f2153ea551810a6f524ccbff121dc36c559.html?from=search

常用万能学习型红外遥控器设计资料

https://wenku.baidu.com/view/5060592ce2bd960590c67788.html?sxts=1578385256890

# lirc

lirc是一个开源项目，用来解码和发送红外信号。

现在的Linux内核已经把红外纳入到常规的input device里了。这就让lirc显得有点多余。

但是lirc还是提供了更大的灵活性。

官网在这里：

http://lirc.org/

lirc最重要的就是lircd这个daemon程序。它可以解码driver收到的红外信号。然后把这个信号提供到一个socket上。也可以在socket进行红外发送。



# 红外的价值

当前这么多无线技术群雄逐鹿的情况下，红外它存在的价值是什么？

性价比高，实现简单，抗电磁干扰，适用于数据量很小，实时性要求不高，例如家电设备的遥控。

https://blog.csdn.net/qq_15904867/article/details/84503090

红外的功耗非常低。在不按键的时候，几乎不耗电。



## irda

irda是InfraRed Data Association，红外数据标准协会。

例如，支持irda接口的相机，可以通过irda无线地向笔记本或者打印件传输照片。

这个是基本是可以淘汰的技术了。太慢，而且要求对准。



生活中的红外光非常多。我们需要让自己的红外信号区别与这些噪声信号。

所以我们对信号进行调制。把我们要发送的信息调制到38KHz的载波上。

在接收器看来，发送信号就是一个红灯在不停地进行闪烁。

红外因为是不怎么精确的东西，所以对晶振要求没有那么高。

石英晶振比较脆弱。陶瓷晶振精度没有那么高，但是皮实，所以用陶瓷晶振。



<https://blog.bschwind.com/2016/05/29/sending-infrared-commands-from-a-raspberry-pi-without-lirc/>

<http://wiki.t-firefly.com/en/Firefly-RK3399/driver_ir.html>



关于红外的发送，代码在drivers/input/remotectl下面的rockchip_pwm_remotectl.c里。这个目录下，只有rockchip的代码。

在设备树里，是配置pwm。

```
compatible = "rockchip,remotectl-pwm"
```

但是读代码，没有看出是发送的。

这个还是输入的。

那么可能就是要打补丁才能行了。



参考资料

1、红外接收头在linux内核里的驱动

这个代码和简单易懂。

https://blog.csdn.net/jklinux/article/details/73498067

2、史上最全的红外资料 HS0038 PH302 免费下载

https://wenku.baidu.com/view/8f1cae1cc5da50e2524d7f48.html?sxts=1578017970594

3、HS0038（红外接收）

https://gaic.alicdn.com/aic/h5_daily/test/device/3.0.51/kumufp.html

4、46.Linux-分析rc红外遥控平台驱动框架,修改内核的NEC解码函数BUG(1)

https://www.cnblogs.com/lifexy/p/9783694.html

5、

https://blog.csdn.net/a651588/article/details/44041005

6、Android 上面实现红外解析(NEC编码)

https://blog.csdn.net/hhnimei/article/details/86593428

7、linux下添加IR驱动后的event事件处理

https://blog.csdn.net/djman007/article/details/53084001

8、[RK3399] IR(红外线)移植步骤

这篇很有参考意义。

http://www.voidcn.com/article/p-msxhaepj-oo.html

9、全面了解红外遥控(中文版)

这个非常好。很全面系统。

https://wenku.baidu.com/view/417f0fc34028915f804dc242.html?sxts=1578383389629