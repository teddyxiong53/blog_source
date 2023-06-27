---
title: Linux内核音频之dummy_codec作用
date: 2021-10-28 11:27:25
tags:
	- Linux内核

---

--

dummy_codec作用是什么？

虚拟声卡的注册主要应用于**硬解码芯片**的使用，

硬件设计上主控I2S直接接到该类芯片，

硬解码芯片能够将数字信号直接转换成模拟信号输出。

同时，**这类芯片需要主控提供mclk、bclk，**

那么就需要注册个虚拟声卡来控制I2S的输出，才能保证正常工作。

对应的驱动代码

./soc/codecs/amlogic/dummy_codec.c

代码就170行左右，很多函数都是直接返回0的实现。



**但是有些场合，我们是不需要一个“真实”的codec做处理的，**

例如蓝牙通话，这时候只要一个虚拟声卡即可。

这里提供一个虚拟声卡的驱动：



这个虚拟到声卡驱动是通用的，就一个虚拟codec，里面啥都没做，就规定了一些参数：

最大两通道，采样率在8k~48k，支持16、20、24、32bit位宽。

既然codec是通用的，那么machine是否也有通用的例子的？

还真有！！！就是simple card framework



# amlogic

什么时候可以用dummy_codec？

The CODEC that doesn't need i2c / spi / other bus controllers, can be configured as

dummy_codec

==就是不需要i2c、spi这种控制接口的codec，就是dummy_codec。==



# 参考资料

1、虚拟Codec设计思路

https://blog.csdn.net/qq_30295609/article/details/106767735

2、RK系列SDK -- dummy codec虚拟声卡注册

https://blog.csdn.net/hb9312z/article/details/103315401

3、

https://www.codenong.com/cs110820640/