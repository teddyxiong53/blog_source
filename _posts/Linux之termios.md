---
title: Linux之termios
date: 2018-09-19 22:31:31
tags:
	- Linux

---



之前一直没有关注过termios的，现在看telnet源代码。里面很多用到termios的东西。

所以现在学习一下。



tty设备的名字是从过去的电传打字机缩写而来。

最初指的是连接到unix系统上的物理或者虚拟终端。

随着时间的推移，当通过串口可以建立终端连接后，tty这个名字也用来指任何的串口设备。

物理tty设备的例子有：串口、usb到串口转化器。

tty虚拟设备支持虚拟console。

它能通过键盘、网络等登陆到Linux系统。



Linux系统里有三种类型的tty驱动程序：控制台、串口、tty。

控制台和pty驱动程序是不需要我们去改的。



为了确定目前load到系统里的是什么类型的tty驱动程序，以及确定当前使用的是哪种tty设备。

可以查看/proc/tty/drivers。

```
# cat /proc/tty/drivers
/dev/tty             /dev/tty        5       0 system:/dev/tty
/dev/console         /dev/console    5       1 system:console
/dev/ptmx            /dev/ptmx       5       2 system
rfcomm               /dev/rfcomm   216 0-255 serial
serial               /dev/ttyS       4 64-68 serial
pty_slave            /dev/pts      136 0-1048575 pty:slave
pty_master           /dev/ptm      128 0-1048575 pty:master
fiq-debugger         /dev/ttyFIQ   254       0 serial
```

另外sys目录下也可以查看。

```
# cd /sys/class/tty/
# ls
console  tty      ttyS0    ttyS2    ttyS4
ptmx     ttyFIQ0  ttyS1    ttyS3
```



#什么是termios

termios是在posix里定义的标准接口。类似system V里的termio接口。

用来对终端进行控制的。

一个最小的termios结构的典型定义如下：

```
struct termios {
	tcflag_t c_iflag,//输入模式。
		c_oflag,//输出模式
		c_cflag,//控制模式
		c_lflag;//本地模式。
	cc_t c_cc[NCCS];
};
```

对应头文件是termios.h。

获取属性

```
int tcgetattr(int fd, struct termios *termios_p);
```

设置属性：

```
int tcsetattr(int fd, int actions, struct termios *termios_h);
```

actions的取值有：

1、TCSANOW：立刻进行修改。

2、TCSADRAIN。等当前的输出完成在对值进行修改。

3、TCSAFLUSH。



# 输入模式



# 参考资料

1、终端I/O termios属性设置 tcsetattr设置

https://www.cnblogs.com/dartagnan/archive/2013/04/25/3042417.html

2、Linux ~ termios 串口编程

https://www.cnblogs.com/einstein-2014731/p/6922977.html

3、Linux 串口编程 一些背景

这个系列文章不错。

https://blog.csdn.net/jazzsoldier/article/details/72457580