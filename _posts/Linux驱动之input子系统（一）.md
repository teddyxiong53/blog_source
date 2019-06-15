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

看看input子系统核心所涉及的c文件。

```
linux-stable/drivers/input$ ls *.c -l
 apm-power.c
 evbug.c
 evdev.c：重要。
 ff-core.c
 ff-memless.c
 input.c：重要。
 input-compat.c
 input-leds.c
 input-mt.c
 input-polldev.c
 joydev.c
 matrix-keymap.c
 mousedev.c
 sparse-keymap.c
```

头文件有input.h。input/mt.h（mt表示multitouch多点触控）。

有2个input.h，一个是在uapi目录下。



input子系统的major是13 。最多可以有1024个minor。

看input_register_device函数。

```
1、每个input设备都一定支持EV_SYN和SYN_REPORT。
__set_bit(EV_SYN, dev->evbit);

```



input子系统的整体流程是怎样的？

用cat /proc/bus/input/devices查看是event几

我们可以`cat /dev/input/event1`。

然后按键，就可以看到打印出来了。

这个是读取板子的按键值的。

```
#include <stdio.h>
#include <stdlib.h>
#include <linux/input.h>
#include <fcntl.h>
#include <sys/time.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <linux/input.h>

int main(int argc, char **argv)
{
    int fd, retval;
    char buf[1024] = {0};
    fd_set readfds;
    struct timeval tv;
    // 打开鼠标设备
    fd = open("/dev/input/event1", O_RDONLY);
    // 判断是否打开成功
    if (fd < 0)
    {
        printf("Failed to open \"/dev/input/event1\".\n");
        exit(1);
    }
    else
    {
        printf("open \"/dev/input/event1\" successfuly.\n");
    }
    int flags = fcntl(fd, F_GETFL, 0);
    flags |= O_NONBLOCK;

    fcntl(fd, F_SETFL, flags);

    printf("fd:%d\n", fd);
    struct input_event key;
    while (1)
    {
        // 设置最长等待时间
        tv.tv_sec = 5;
        tv.tv_usec = 0;

        FD_ZERO(&readfds);
        FD_SET(fd, &readfds);

        retval = select(fd + 1, &readfds, NULL, NULL, &tv);
        if (retval == 0)
        {
            printf("Time out!\n");
        }
        if (FD_ISSET(fd, &readfds))
        {
            // 读取鼠标设备中的数据
            if (read(fd, &key, sizeof(struct input_event)) <= 0)
            {
                continue;
            }
            printf("\r\ntype:%d, code:%d, value:%d\r\n",  key.type, key.code, key.value);
            // 打印出从鼠标设备中读取到的数据
            //printf("Button type = %d, X = %d, Y = %d, Z = %d\n", (buf[0] & 0x07), buf[1], buf[2], buf[3]);
        }
    }
    close(fd);
    return 0;
}
```

运行：

```
/oem # ./a.out
open "/dev/input/event1" successfuly.
fd:3

type:1, code:114, value:1

type:0, code:0, value:0

type:1, code:114, value:0

type:0, code:0, value:0

type:1, code:248, value:1

type:0, code:0, value:0

type:1, code:248, value:0

type:0, code:0, value:0
```

这些type、code、value，分别代表了什么意思？

```
struct input_event {

struct timeval time; //按键时间

__u16 type; //类型，在下面有定义

__u16 code; //要模拟成什么按键

__s32 value;//是按下还是释放

};
```



type是这样：

```
#define EV_SYN 0x00

#define EV_KEY 0x01 //按键

#define EV_REL 0x02 //相对坐标(轨迹球)

#define EV_ABS 0x03 //绝对坐标

#define EV_MSC 0x04 //其他
```

我关注EV_KEY就好了。

所以我就看type为1的就行。



我在笔记本上测试，按住a键不放。

```

type:4, code:4, value:30

type:1, code:30, value:1

type:0, code:0, value:0

type:4, code:4, value:30

type:1, code:30, value:2 //这里value为什么是2？

type:0, code:0, value:0

type:4, code:4, value:30

type:1, code:30, value:2

type:0, code:0, value:0

type:4, code:4, value:30

type:1, code:30, value:2

type:0, code:0, value:0

type:4, code:4, value:30

type:1, code:30, value:2

```

难道是1按下，2长按，0是松开？

```
value:根据Type的不同而含义不同。
例如：
Type为EV_KEY时，value: 0表示按键抬起。1表示按键按下。（4表示持续按下等？）。
Type为EV_REL时，value:　表明移动的值和方向（正负值）。
```

我当前就管value为1的。

```
code:根据Type的不同而含义不同。
例如：
Type为EV_KEY时，code表示键盘code或者鼠标Button值。
```



# 参考资料

1、

https://blog.csdn.net/ielife/article/details/7814108

2、

https://blog.csdn.net/morixinguan/article/details/70040127

3、struct input_event详解

https://blog.csdn.net/bingqingsuimeng/article/details/8178122

4、input_event结构体详解

https://blog.csdn.net/liwei405499/article/details/42025123