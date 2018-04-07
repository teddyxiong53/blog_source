---
title: lcd与CPU的接口
date: 2018-04-07 21:04:15
tags:
	- lcd
---



彩色lcd与CPU的连接方式有这些：

1、mcu模式。

2、rgb模式。

3、spi模式。

4、vsync模式。

5、mddi模式。

# mcu模式

目前最常用的模式。一般是用80并口。数据位一般有8位、9位、16位和18位这4种。

优点：

1、控制简单，不需要时钟和同步信号。

缺点：

1、比较耗费gram。（Graphic RAM）。所以做大屏比较难。

这个的模式是因为经常在单片机上使用而得名的。



# rgb模式

大屏经常采用这种模式。数据位宽度也有6位、16位、18位。

它的优缺点和mcu模式正好相反。

跟mcu模式的区别：

数据直接写入到屏幕上。而mcu模式是先写入到gram上。

所以比mcu模式的要快。一般用来显示视频和动画。

而mcu的一般用来显示静态图片。



# spi模式

就是数据全部用spi来传输。比较慢。

# vsync模式

在mcu模式下，增加了一根vsync信号线。用于运动画面更新。

# mddi模式

高通在2004年提出。





# 参考资料

1、LCD的CPU接口和RGB接口

https://blog.csdn.net/sunnytina/article/details/7261356

2、gram

https://baike.baidu.com/item/GRAM/19660526#viewPageContent

3、MCU模式和RGB模式，区别究竟在哪？

http://m.elecfans.com/article/607905.html