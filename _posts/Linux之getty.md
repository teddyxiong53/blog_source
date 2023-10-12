---
title: Linux之getty
date: 2020-04-11 11:51:51
tags:
	- Linux

---

--

getty是loginutils里的一个。

从busybox的loginutils目录下，可以看到这些：

```
addgroup
adduser
chpasswd
cryptpwd
deluser
getty
login
passwd
su
sulogin
vlock
```

先看getty。

基本格式：

```
[OPTIONS] BAUD_RATE[,BAUD_RATE]... TTY [TERMTYPE]
```



getty的一般参数是这样：

```
/sbin/getty -L  ttyFIQ0 0 vt100
```

_L 表示设置CLOCAL。这样就会忽略回车的检测？

作用就是提示用户要输入用户名和密码。

**我们不执行这个，就不会要求验证用户了。**



# agetty和getty什么区别

`agetty` 和 `getty` 都是终端登录程序，用于在 Linux 系统上管理终端设备的登录。它们在功能上非常相似，但存在一些细微的区别。

1. 来源：`agetty` 和 `getty` 来自不同的软件包。`agetty` 包含在 `util-linux` 软件包中，而 `getty` 包含在 `sysvinit` 软件包中。

2. 特性：`agetty` 提供了比 `getty` 更多的功能和选项。例如，`agetty` 支持多种终端类型和参数，能够处理多个终端设备并行登录，并提供更灵活的配置选项。

3. 兼容性：`agetty` 是更现代化的终端登录程序，与较新的 Linux 发行版和系统配置更兼容。而 `getty` 是更传统的终端登录程序，通常与 SysV 初始化系统一起使用。

**在现代的 Linux 系统中，通常会使用 `agetty` 替代 `getty`**，因为它提供更多的功能和更好的兼容性。但在某些特定的系统或特殊需求下，仍然可以使用 `getty`。

需要注意的是，`agetty` 和 `getty` 都是终端登录程序的实现，其核心功能是提供终端设备的登录服务，并不涉及图形界面或其他高级特性。

# agetty登陆逻辑

agetty 是一个用于终端登录的程序，它在 Linux 系统中提供了终端的登录功能。下面是 agetty 登录的基本逻辑：

1. agetty 监听特定的终端设备：agetty 会通过指定的参数或配置文件指定要监听的终端设备，如串口设备（如 `/dev/ttyS0`）或虚拟控制台设备（如 `/dev/tty1`）。

2. 等待用户登录：一旦 agetty 监听到指定的终端设备上有输入活动，它会开始等待用户登录。agetty 会显示一个登录提示符，并等待用户输入用户名。

3. 验证用户身份：一旦用户输入了用户名，agetty 会验证用户身份。它通常会与系统的用户数据库（如 /etc/passwd、/etc/shadow）进行比对，以验证用户名和密码的正确性。某些配置下也可能不验证密码，比如无密码登录或自动登录。

4. 启动登录会话：如果用户的身份验证成功，agetty 会启动一个登录会话。它会执行一系列操作，包括设置环境变量、切换用户身份、启动 shell 程序等。通常，会启动用户默认的登录 shell（如 Bash、Zsh）。

5. 提供终端登录界面：一旦登录会话启动，agetty 将终端设备连接到登录会话的输入输出。用户可以在终端上执行命令、查看输出等，就像在一个交互式终端中一样。

6. 监听终端断开：agetty 会继续监听终端设备上的输入活动。如果检测到用户退出或终端断开的事件，它将关闭登录会话，并终止该终端的使用。

agetty 通过这种逻辑实现了终端登录功能，允许用户通过终端设备与系统进行交互。它是 Linux 系统中提供登录服务的关键组件之一，负责验证用户身份并提供登录会话。



## getty的等价逻辑

从busybox的getty的usage注释里可以看到：

```
//config:	this script approximates getty:
//config:
//config:	exec </dev/$1 >/dev/$1 2>&1 || exit 1
//config:	reset
//config:	stty sane; stty ispeed 38400; stty ospeed 38400
//config:	printf "%s login: " "`hostname`"
//config:	read -r login
//config:	exec /bin/login "$login"
```



# 参考资料

1、

