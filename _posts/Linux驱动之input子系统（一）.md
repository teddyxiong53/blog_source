---
title: Linux驱动之input子系统（一）
date: 2018-03-28 11:25:14
tags:
	- Linux驱动

---



用mx2的按键为入口，研究一下Linux的input子系统。

先还是从按键的开始看。内核里关于按键的主要文件是：

头文件：

1、include/linux/gpio_keys.h

c文件：

1、drivers/input/keyboard/gpio_keys.c

en

gpio_keys.h主要内容：

```
定义2个结构体：
struct gpio_keys_button {
  uint code;//就是以KEY_开头的那些值，定义在
  int gpio;
  int active_low;
  char *desc;
  uint type;//EV_KEY
  int wakeup;//是否是唤醒源。
  int debounce_interval;
  bool can_disable;
  int value;//坐标值，当前不管。
};
//这个结构体就是要在bsp文件里进行定义的了。然后注册进来。gpio_keys.c模块初始化的时候，获取到。
struct gpio_keys_platform_data {
  struct gpio_keys_button *buttons;
  int nbuttons;
  //...其他的不管先。
};
```

然后看gpio_keys.c文件。

是平台设备，probe函数：

```
1、用input_allocate_device得到一个input设备。
2、然后根据情况对input进行设置。
	例如，如果支持rep（就是按住键不放连续输入的意思），__set_bit(EV_REP, input->evbit)

```

bsp文件里的按键是这样的：

type都是EV_KEY的。

```
static struct gpio_keys_button m040_gpio_keys_tables[] = {
	{
		.code			= KEY_POWER,
		.gpio			= M040_POWER_KEY,
		.desc			= "gpio-keys: KEY_POWER",
		.type			= EV_KEY,
		.active_low		= 1,
		.wakeup			= 1,
		.debounce_interval	= 1,
	}, {
		.code			= KEY_HOME,
		.gpio			= M040_HOME_KEY,
		.desc			= "gpio-keys: KEY_HOME",
		.type			= EV_KEY,
		.active_low		= 1,
		.wakeup			= 1,
		.debounce_interval	= 1,
	}, 
```

应用层怎样读取input子系统的东西呢？

```
/proc/bus/input # cat devices 
I: Bus=0019 Vendor=0001 Product=0001 Version=0100
N: Name="gpio-keys"
P: Phys=gpio-keys/input0
S: Sysfs=/devices/platform/gpio-keys/input/input0
U: Uniq=
H: Handlers=kbd event0 
B: PROP=0
B: EV=3
B: KEY=100000 0 b8000000 0
```



看我的虚拟机里的Ubuntu是这样：

```
teddy@teddy-ubuntu:/dev/input$ ls
by-id  by-path  event0  event1  event2  event3  event4  mice  mouse0  mouse1  mouse2
```

```
teddy@teddy-ubuntu:/dev/input$ cat /proc/bus/input/devices 
I: Bus=0019 Vendor=0000 Product=0001 Version=0000
N: Name="Power Button"
P: Phys=LNXPWRBN/button/input0
S: Sysfs=/devices/LNXSYSTM:00/LNXPWRBN:00/input/input0
U: Uniq=
H: Handlers=kbd event0 //event0是对应按键的。
B: PROP=0
B: EV=3
B: KEY=10000000000000 0

I: Bus=0011 Vendor=0001 Product=0001 Version=ab41
N: Name="AT Translated Set 2 keyboard"
P: Phys=isa0060/serio0/input0
S: Sysfs=/devices/platform/i8042/serio0/input/input1
U: Uniq=
H: Handlers=sysrq kbd event1 leds //event1对应按键
B: PROP=0
B: EV=120013
B: KEY=402000000 3803078f800d001 feffffdfffefffff fffffffffffffffe
B: MSC=10
B: LED=7

I: Bus=0011 Vendor=0002 Product=0013 Version=0006
N: Name="VirtualPS/2 VMware VMMouse"
P: Phys=isa0060/serio1/input1
S: Sysfs=/devices/platform/i8042/serio1/input/input4
U: Uniq=
H: Handlers=mouse0 event2 //event2对应鼠标。
B: PROP=0
B: EV=b
B: KEY=70000 0 0 0 0
B: ABS=3

I: Bus=0011 Vendor=0002 Product=0013 Version=0006
N: Name="VirtualPS/2 VMware VMMouse"
P: Phys=isa0060/serio1/input0
S: Sysfs=/devices/platform/i8042/serio1/input/input3
U: Uniq=
H: Handlers=mouse1 event3 //event3也是对应鼠标。
B: PROP=1
B: EV=7
B: KEY=30000 0 0 0 0
B: REL=103

I: Bus=0003 Vendor=0e0f Product=0003 Version=0110
N: Name="VMware VMware Virtual USB Mouse"
P: Phys=usb-0000:02:00.0-1/input0
S: Sysfs=/devices/pci0000:00/0000:00:11.0/0000:02:00.0/usb2/2-1/2-1:1.0/0003:0E0F:0003.0001/input/input5
U: Uniq=
H: Handlers=mouse2 event4 //还是对应鼠标，是鼠标的左中右分别对应吗？
B: PROP=0
B: EV=17
B: KEY=ff0000 0 0 0 0
B: REL=103
B: MSC=10
```



一个应用程序这样写：

```
#include <stdio.h>    
#include <stdlib.h>    
#include <linux/input.h>    
#include <fcntl.h>    
#include <sys/time.h>    
#include <sys/types.h>    
#include <sys/stat.h>    
#include <unistd.h>    
    
    
int main(int argc,char **argv)    
{    
    int fd, retval;    
    char buf[6];    
    fd_set readfds;    
    struct timeval tv;    
    // 打开鼠标设备    
    fd = open( "/dev/input/mice", O_RDONLY );    
    // 判断是否打开成功    
    if(fd<0) {    
        printf("Failed to open \"/dev/input/mice\".\n");    
        exit(1);    
    } else {    
        printf("open \"/dev/input/mice\" successfuly.\n");    
    }    
    
    while(1) {    
        // 设置最长等待时间    
        tv.tv_sec = 5;    
        tv.tv_usec = 0;    
    
        FD_ZERO( &readfds );    
        FD_SET( fd, &readfds );    
    
        retval = select( fd+1, &readfds, NULL, NULL, &tv );    
        if(retval==0) {    
            printf( "Time out!\n" );    
        }    
        if(FD_ISSET(fd,&readfds)) {    
            // 读取鼠标设备中的数据    
            if(read(fd, buf, 6) <= 0) {    
                continue;    
            }    
            // 打印出从鼠标设备中读取到的数据    
            printf("Button type = %d, X = %d, Y = %d, Z = %d\n", (buf[0] & 0x07), buf[1], buf[2],   buf[3]);    
        }    
    }    
    close(fd);    
    return 0;    
}    
```

在Ubuntu图形界面下运行。鼠标移动，点击都有打印出来。

```
Button type = 0, X = 7, Y = -3, Z = 34
Button type = 0, X = 3, Y = 0, Z = 34
Button type = 0, X = 1, Y = -1, Z = 34
Button type = 1, X = 0, Y = 0, Z = 34
Button type = 0, X = 0, Y = 0, Z = 34
```

