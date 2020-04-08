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

def_trigger这个属性值得注意。



# rk3308的led

以rk3308的为例。

led对应的设备名字是：rk_led_ctrl。

## 内核里的代码

kernel的配置里，有这2个宏。

CONFIG_LEDS_TRIGGER_MULTI_CTRL=y
CONFIG_LEDS_TRIGGER_CONTROL_RK=y

rk_led_ctrl是一个misc设备。

名字写在ledtrig-control-rk.c文件里。

初始化函数被leds-pwm.c调用。

```
./leds-pwm.c:219:       rk_led_control_init(&pdev->dev,count);
```

当前是配置了3颗led。红绿蓝三种颜色。

在设备树里配置的。



支持的操作

```
#define RK_ECHO_GET_LED_NUM				_IOWR('I', 101, int)
#define RK_ECHO_SET_LED_EFFECT			_IOWR('I', 102, int)
```

定义了灯效数据结构。

```
struct led_effect_data {
	int leds_type;
    int force_bright[LED_NUM_MAX];
    int back_bright[LED_NUM_MAX];
    int bright[LED_NUM_MAX];
	int step_bright[LED_NUM_MAX];
    char data_valid;
    int steps_time;
	struct delayed_work timer_work;
};
```

这个可以实现的灯效还是比较全的。

灯效分类有：

```
2：呼吸灯
3：渐弱。
4：闪烁。
5：exchange
6：marquee
7：light add
8：scroll one。

那些没有翻译的，是因为不知道具体指什么。
0:关闭灯效, 1：常亮 2:呼吸灯效,  3:淡进淡出 4:闪烁灯效 5:互换 6:跑马灯效  7:走马灯效 8：一个灯单色循环
这个是从led_effect.json这个应用层的配置文件里找出来的。

可以看到，驱动里没有处理类型为0和1的灯效。这个估计在应用层就拦截了。
这2个处理倒也简单，直接操作sys下的文件就可以达到目的。
但是其实可以加到驱动里的。

```

重点看看rk_led_ctrl_ioctl这个。

```
ioctl就支持2个命令。
1：获取led数目。
2：设置灯效。
```

简单写一个测试程序。先获取一下led数目看看是否可以生效。

```
#include <stdio.h>
#include <asm-generic/ioctl.h>
#include <fcntl.h>

#define RK_ECHO_GET_LED_NUM				_IOWR('I', 101, int)
#define RK_ECHO_SET_LED_EFFECT			_IOWR('I', 102, int)


int main()
{
	int fd = open("/dev/rk_led_ctrl", O_RDWR);
	if(fd < 0) {
		printf("open rk_led_ctrl fail\n");
		return -1;
	}
	int num = 0;
	int ret = ioctl(fd, RK_ECHO_GET_LED_NUM, &num);
	if(ret < 0) {
		printf("ioctl fail\n");
		return -1;
	}
	printf("get led num:%d\n", num);
	return 0;
}
```

可以正确获取到led数目为3 。

现在看看控制灯效。

```
这需要传递下来的是一个结构体指针：
struct led_effect {
    int period;
    int back_color;
    int fore_color;
    int start;//从哪个等开始。
    int num;//总共点亮几个灯。
    int scroll_num;//跑马灯个数，只对跑马灯灯效有用。其他不填。
    int actions_per_period;//每个周期进行多少次动作。呼吸灯填
    int led_effect_type;
};
```

一个呼吸灯效果的是这样：

```
"led_effect_type": 2,
"back_color": "000000",
"fore_color": "0000FF",
"period": 1000,
"start": 0,
"num": 1,
"actions_per_period": 4
```

```
#include <stdio.h>
#include <asm-generic/ioctl.h>
#include <fcntl.h>
#include <unistd.h>

#define RK_ECHO_GET_LED_NUM				_IOWR('I', 101, int)
#define RK_ECHO_SET_LED_EFFECT			_IOWR('I', 102, int)
struct led_effect {
    int period;
    int back_color;
    int fore_color;
    int start;
    int num;
    int scroll_num;
    int actions_per_period;
    int led_effect_type;
};

int main()
{
	int fd = open("/dev/rk_led_ctrl", O_RDWR);
	if(fd < 0) {
		printf("open rk_led_ctrl fail\n");
		return -1;
	}
	int num = 0;
	int ret = ioctl(fd, RK_ECHO_GET_LED_NUM, &num);
	if(ret < 0) {
		printf("ioctl fail\n");
		return -1;
	}
	printf("get led num:%d\n", num);
	//控制灯效。
	struct led_effect effect = {
		.period = 1000,
		.back_color = 0,
		.fore_color = 0xff,
		.start = 0,
		.num = 1,
		.actions_per_period = 4,
		.led_effect_type =2
	};
	ret = ioctl(fd, RK_ECHO_SET_LED_EFFECT, &effect);
	if(ret < 0) {
		printf("set led effect fail\n");
		return -1;
	}
	return 0;
}
```

上面的代码是实现了蓝牙的呼吸灯效果。



发现一个问题，直接设置颜色，无法结束当前的呼吸灯效果。导致设置常亮时，颜色并不能得到预期的效果。

实际上，驱动里是有处理常亮和灭灯操作的。所以没有必要自己另外去操作sys目录下的文件。而且操作sys文件也没法得到预期效果。

```
switch(leffect->led_effect_type)
        {
            case 0: led_effect_close(leffect);
                break;
            case 1: led_effect_open(leffect);
                break;
            default:break;
        }
```





参考资料

1、Linux led子系统

http://www.360doc.com/content/12/0312/20/6828497_193834197.shtml