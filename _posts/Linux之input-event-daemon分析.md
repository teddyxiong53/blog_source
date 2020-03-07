---
title: Linux之input-event-daemon分析
date: 2020-03-06 09:57:28
tags:
	- Linux

---

1

input-event-daemon，是Linux下的按键监听daemon进程。

通过/etc/input-event-daemon.conf里来进行配置。

buildroot里需要选配上input-event-daemon。

```
#                                          
# /etc/input-event-daemon.conf             
#                                          
                                           
[Global]                                   
listen = /dev/input/event0                 
listen = /dev/input/event1                 
listen = /dev/input/event2                 
#listen = /dev/input/event3                
                                           
[Keys]                                     
#POWER        = echo mem > /sys/power/state
MICMUTE         = amixer -q set Master mute
MEDIA   = echo MEDIA                       
VOLUMEUP  = volumeup                       
VOLUMEDOWN  = volumedown                   
#CTRL+ALT+ESC = beep                       
#FN = softapServer Rockchip-Echo-123 &     
                                           
[Switches]                                 
RADIO:0 = ifconfig wlan0 down              
                                           
[Idle]                                     
1h 30m = vbetool dpms off                  
reset  = vbetool dpms on                   
```

这个配置文件需要调整。

目前gpio-keys对应的是event1 。

但是配置的这些按键名字，如何跟物理按键对应上呢？MICMUTE这些名字，就是Linux下面按键的标准名。

在设备树里，配置了按键的类型：

```
micmute-key {
			gpios = <&gpio0 RK_PB2 GPIO_ACTIVE_LOW>;
			linux,code = <KEY_MICMUTE>;//这个就跟conf文件里的MICMUTE对应上了。
			label = "micmute";
			debounce-interval = <50>;
		};
```

运行需要注意的就是，

```
Idle这个标签下面的vbetool，工具没有，所以那两行都注释掉。
event2没有，event0不关注，
所以只留下event1的。
```

运行后，按键操作，用`amixer sget Master`查看音量，可以看到操作有效果。

volumeup和volumedown是系统里的命令。





代码在这里：

https://github.com/gandro/input-event-daemon



参考资料

1、

