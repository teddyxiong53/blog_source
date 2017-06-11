---
title: 区分Linux的串口登陆和telnet登陆
date: 2017-06-07 22:00:41
tags:

	- Linux

	- shell

---

要让一个程序在/etc/profile里启动，但是不想telnet连接时再次执行。所以需要区分串口本地登录和telnet登录。解决方法是这样的。

先在串口终端里输入set，查看环境变量的情况。再在telnet的终端里输入set查看环境变量。把两者的结果对比一下，可以发现PPID是不一样的，而且串口终端里的PPID是1，这样就可以唯一标识出串口登陆了。

在/etc/profile里加上下面的语句即可：

```
if [ $PPID == 1 ]; then
	echo "login from ttyAMA0"
	# add your code here
fi
```

