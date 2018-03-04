---
title: 树莓派之DIY扩展板
date: 2018-03-03 09:53:00
tags:
	- 树莓派

---



本文是对这篇文章的学习总结。

http://shumeipai.nxez.com/2015/09/12/diy-a-standard-raspberry-pi-hat.html?variant=zh-cn



这块DIY的扩展板就命名为ICA HAT。支持：

1、5个用户按键。上下左右、确定。

2、4个led。

3、1个蜂鸣器。

4、2个红外发射器，1个红外接收器。

5、2个七段数码管。通过spi接口的max7219芯片驱动。

6、io和电源扩展排针若干。



先用排线把树莓派上的40个gpio都引到扩展板上。

其实这个扩展板的，可以用面包板来搭建出来。



我们看一下led的测试代码，Python写的。

```
import wiringpi2 as wpi
import time

# Pin definition of LED
LED_PIN = [2, 4, 3, 5]

# Init GPIO to wiringPi pin mode
io = wpi.GPIO(wpi.GPIO.WPI_MODE_PINS)

# Init LED pins
for i in range(0, 4):
    io.pinMode(LED_PIN[i], io.OUTPUT)
    io.digitalWrite(LED_PIN[i], io.HIGH)

# LED Flasher
while True:
    for ledPinOn in range(0, 4):
        for i in range(0, 4):
            io.digitalWrite(LED_PIN[i], io.HIGH)
        io.digitalWrite(LED_PIN[ledPinOn], io.LOW)
        time.sleep(0.3)

```



