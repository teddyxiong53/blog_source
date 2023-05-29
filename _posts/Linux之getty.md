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

我们不执行这个，就不会要求验证用户了。



# agetty和getty什么区别

`agetty` 和 `getty` 都是终端登录程序，用于在 Linux 系统上管理终端设备的登录。它们在功能上非常相似，但存在一些细微的区别。

1. 来源：`agetty` 和 `getty` 来自不同的软件包。`agetty` 包含在 `util-linux` 软件包中，而 `getty` 包含在 `sysvinit` 软件包中。

2. 特性：`agetty` 提供了比 `getty` 更多的功能和选项。例如，`agetty` 支持多种终端类型和参数，能够处理多个终端设备并行登录，并提供更灵活的配置选项。

3. 兼容性：`agetty` 是更现代化的终端登录程序，与较新的 Linux 发行版和系统配置更兼容。而 `getty` 是更传统的终端登录程序，通常与 SysV 初始化系统一起使用。

**在现代的 Linux 系统中，通常会使用 `agetty` 替代 `getty`**，因为它提供更多的功能和更好的兼容性。但在某些特定的系统或特殊需求下，仍然可以使用 `getty`。

需要注意的是，`agetty` 和 `getty` 都是终端登录程序的实现，其核心功能是提供终端设备的登录服务，并不涉及图形界面或其他高级特性。



# 参考资料

1、

