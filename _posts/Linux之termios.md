---
title: Linux之termios
date: 2018-09-19 22:31:31
tags:
	- Linux

---



之前一直没有关注过termios的，现在看telnet源代码。里面很多用到termios的东西。

所以现在学习一下。



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