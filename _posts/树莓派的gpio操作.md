---
title: 树莓派的gpio操作
date: 2017-04-17 21:17:10
tags:
	- 树莓派
---
树莓派和普通电脑的不同在于，它带了17个可编程的gpio。但是gpio的编号方法有些混乱。
不同的库对gpio的端口编号不一样，本文就是要对此进行梳理。
我们只用RPi.GPIO（Python编程）wiringPi（C编程）这两种库。

对于RPi.GPIO库来说，树莓派上的gpio可以有两种编号方式：board方式和博通GPIO方式。board方式就是安装板子上1到40号引脚这个编号来算。博通gpio方式从上面图中可以查到。


![](/images/rpi_gpio_number.jpg)

安装wiringPi：`sudo apt-get install wiringPi`。
上面的引脚图，可以用`gpio readall`来得到。



用RPi.GPIO来操作，可以这样操作：
```
# python #进入Python环境
> import RPi.GPIO as gpio
> gpio.RPI_INFO
{'P1_REVISION': 3, 'RAM': '1024M', 'REVISION': 'a22082', 'TYPE': 'Pi 3 Model B', 'PROCESSOR': 'BCM2837', 'MANUFACTURER': 'Embest'}

```


