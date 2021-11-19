---
title: Linux之通过sysfs操作gpio
date: 2021-11-16 14:36:43
tags:
	- Linux

---

--

在amlogic芯片上。

```
#define gpio_base 411
#define gpioz_2 (gpio_base + 2) // gpioz_2 --> 1640 data_pin
#define gpioz_3 (gpio_base + 3) // gpioz_3 --> 1640 clk_pin
```

这个gpio_base值是怎么确定的？

这样来导出gpio到sysfs，然后进行操作。

```
/*
  echo 501 > /sys/class/gpio/export
  echo out > /sys/class/gpio/gpio501/direction
  echo 1 > /sys/class/gpio/gpio501/value
  */
```

amlogic的gpio寄存器有哪几个bank？



```
/sys/kernel/debug/pinctrl/pinctrl@ff634480 # cat gpio-ranges 
GPIO ranges handled:
0: periphs-banks GPIOS [411 - 496] PINS [0 - 85]
```

```
/sys/kernel/debug/pinctrl/pinctrl@ff634480 # cat pinconf-pins 
# 这个的就是0到85的。
# 可以跟上面的进行偏移对应。
pin 0 (GPIOZ_0): input bias pull down, input enabled
pin 1 (GPIOZ_1): input bias pull up, input enabled
pin 2 (GPIOZ_2): input bias pull down, pin output (0 level)
pin 3 (GPIOZ_3): input bias pull up, pin output (0 level)
pin 4 (GPIOZ_4): input bias pull up, input enabled
pin 5 (GPIOZ_5): input bias pull up, pin output (0 level)
pin 6 (GPIOZ_6): input bias pull up, pin output (1 level)
```



参考资料

1、

