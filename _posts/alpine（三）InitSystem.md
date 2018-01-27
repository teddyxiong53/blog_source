---
title: alpine（三）InitSystem
date: 2018-01-26 20:10:58
tags:
	- alpine
	- Linux

---



alpine使用OpenRC作为它的初始化系统。

# OpenRC

OpenRC是一个基于依赖的初始化系统。根提供了init的系统配合工作。一般是SysVinit。

busybox的一些命令还不能很好地跟OpenRC兼容 。

如果你把/bin/sh指向busybox，建议你禁用busybox的这些配置，以便更好地跟OpenRC配合使用。

```
1. CONFIG_START_STOP_DAEMON
start-stop-daemon这个applet跟OpenRC的不兼容。
2、CONFIG_MOUNT
3、CONFIG_SWAPONOFF
4、CONFIG_SETFONT
5、CONFIG_BB_SYSCTL
```

我们现在看看alpine的/bin目录下的命令都是指向了哪里。

基本上都是busybox的软链接。有4个不同的文件：

1、bbsuid。看网站上的描述信息，说这个可以被移除。依赖busybox。

2、kmod。lsmod和modinfo都指向了这个。

3、rc-status。

4、uniso。

bbsuid就对应一个bbsuid.c的文件。https://github.com/alpinelinux/aports/blob/master/main/busybox/bbsuid.c

```
#define BBSUID_PATH "/bin/bbsuid"

const static char * applets[] = {
	"/bin/mount",
	"/bin/umount",
	"/bin/su",
	"/usr/bin/crontab",
	"/usr/bin/passwd",
	"/usr/bin/traceroute",
	"/usr/bin/traceroute6",
	"/usr/bin/vlock",
	NULL
};
```

# rc-xxx命令

包括：

1、rc-update。格式：`rc-update add/del xxx runlevel`

2、rc-service。格式：`rc-service xxx start/stop/restart`。等价于`/etc/init.d/xxx start`

3、rc-status。



runlevel可以取的值有：

1、default。

2、hotplugged。

3、mannual。

我们一般用default就好了。

# 写init脚本

