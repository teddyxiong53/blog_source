---
title: Linux驱动之led
date: 2018-03-01 15:22:43
tags:
	- Linux驱动

---



先看树莓派的情况。

```
pi@raspberrypi:/sys/class/leds/led0$ tree
.
├── brightness
├── device -> ../../../soc:leds
├── max_brightness
├── power
│   ├── autosuspend_delay_ms
│   ├── control
│   ├── runtime_active_time
│   ├── runtime_status
│   └── runtime_suspended_time
├── subsystem -> ../../../../../../class/leds
├── trigger
└── uevent

3 directories, 9 files
```

你可以`echo 0> brightness`来把led关闭。

led驱动倒还没有想象的简单。有多了很多的东西。

看drivers/led/leds-bcm6328.c。



关键在于led_classdev_register这个函数。

我还是回到s3c2440的看。

当前这种方式的驱动，没有/dev节点，用户编程要通过sysfs来做。



亮度值是这样的。在linux/leds.h里定义。

```
enum led_brightness {
	LED_OFF		= 0,
	LED_HALF	= 127,
	LED_FULL	= 255,
};
```



```
pi@raspberrypi:/sys/class/leds/led0$ cat trigger 
none kbd-scrollock kbd-numlock kbd-capslock kbd-kanalock kbd-shiftlock kbd-altgrlock kbd-ctrllock kbd-altlock kbd-shiftllock kbd-shiftrlock kbd-ctrlllock kbd-ctrlrlock [mmc0] mmc1 timer oneshot heartbeat backlight gpio cpu0 cpu1 cpu2 cpu3 default-on input rfkill0 rfkill1 
```

看这些会导致led发送变化的原因。

是如何注册进来的呢？

是靠led-triggers.c里的`led_trigger_register_simple`这个函数来注册的。

例如这样：

```
static int __init nand_base_init(void)
{
	led_trigger_register_simple("nand-disk", &nand_led_trigger);
	return 0;
}
```



