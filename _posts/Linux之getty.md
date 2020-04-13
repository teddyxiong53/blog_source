---
title: Linux之getty
date: 2020-04-11 11:51:51
tags:
	- Linux

---

1

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



参考资料

1、

