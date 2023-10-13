---
title: Android之root原理
date: 2017-07-15 11:52:49
tags:

	- Android

	- root

---

--

Android的内核是Linux，获取Android的root权限和Linux下获取root权限是一回事。

在Linux下，你可以通过sudo来做。

而Android默认不提供su工具，而且它还要防止你获得root权限。

所以你要获得Android的root权限，

第一步就是把编译好的su程序文件拷贝到Android手机的/system/bin或者/system/xbin目录下。

把su文件放进去后，你就可以在adb shell下执行su了。

在Linux下，你执行su之后再输入密码就可以root了。

但是Android里的su和Linux的Android的su不一样，

Android里的su不是靠验证密码的，而是看你原来的权限是什么。

你可以从root用户切到其他，但是却不能从其他用户切到root。

也就是说，你得用root运行su才行。

我们先看一个Linux的文件的权限情况。

```
teddy@teddy-ubuntu:~$ ls -l /usr/bin/passwd 
-rwsr-xr-x 1 root root 49644  7月 21  2015 /usr/bin/passwd
```

注意前面的rws。

这个s表示任何一个用户执行该文件的时候都拥有文件所有者的权限，而这个文件的所有者是root。

所以，不管是谁来执行passwd程序，他都是以root身份在执行。

所以，现在的问题就清楚了，

你要把一个所有者是root的su程序拷贝到手机上，并且把权限标志设置为上面看到的值。

然后你就相当于把手机root了。用代码来表示这个过程就是：

```
cp /data/tmp/su /system/bin
chown root:root su
chmod 4775 /system/bin/su
```

但是，你执行这些代码都需要root权限，这就逻辑上形成闭环了，你必须有root权限才能执行，你必须执行后才有root权限。

那么如何打破这个闭环呢？

**一个办法就是找一个已经有root权限的进程来启动上面两行代码。**

但是具有root权限的进程都是出厂时就预装到手机上的，代码写死了，你没法控制它执行你的代码。

这时候，就需要找漏洞了。

例如破解Android2.3 root权限的zergRush漏洞就是利用一个拥有root权限的进程的堆栈溢出漏洞。

关于权限分配，Android建立了很多的内置用户，例如wifi、shell等。哪个用户可以做哪些操作，都被限制了。