---
title: Linux之ld-linux.so分析
date: 2019-12-09 16:28:38
tags:
	 - Linux

---

1

ld-linux.so.2 是linux下的动态库加载器/链接器。

```
hlxiong@hlxiong-VirtualBox:~$ ldd /bin/cat
        linux-vdso.so.1 =>  (0x00007ffcc35e1000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007f8a94a19000)
        /lib64/ld-linux-x86-64.so.2 (0x00007f8a94de3000)
```

ld-linux.so这一行，没有=>符号。

ld-linux.so虽然看起来是一个so文件，但是可以独立运行。

它的功能是负责动态加载。

通过读取可执行文件的头部信息来确定哪些库文件是必须的，以及哪些需要加载。

加载完成后，它会修改执行文件里的相关的地址指针来跟加载的动态库完成动态链接。

这样程序就可以运行了。



参考资料

1、深入理解LINUX下动态库链接器/加载器ld-linux.so.2

https://www.cnblogs.com/tongongV/p/10744050.html