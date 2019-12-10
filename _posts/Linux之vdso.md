---
title: Linux之vdso
date: 2019-09-10 14:33:48
tags:
	- Linux

---

1

在看vma相关的文章的时候，看到vdso这个东西。了解一下。

vdso是Virtual Dynamic Shared Object的意思。出现的背景是避免内核和libc之间大量的版本兼容问题。

是内核提供的虚拟的so。这个so是在内核里的。

例如syscall这个函数，就是在linux-vdso.so.1里面。

```
hlxiong@hlxiong-VirtualBox:~$ ldd /bin/bash
        linux-vdso.so.1 =>  (0x00007ffdf9bf8000)
        libtinfo.so.5 => /lib/x86_64-linux-gnu/libtinfo.so.5 (0x00007fbf5a1eb000)
        libdl.so.2 => /lib/x86_64-linux-gnu/libdl.so.2 (0x00007fbf59fe7000)
        libc.so.6 => /lib/x86_64-linux-gnu/libc.so.6 (0x00007fbf59c1d000)
        /lib64/ld-linux-x86-64.so.2 (0x00007fbf5a414000)
```

通过这种方式，随内核发行的libc就唯一地和一个特定版本的内核绑定到一起了。

注意，vdso只是随内核发行，没有在内核空间里。

不会导致内核膨胀。

这样内核和libc都不需要为兼容多个不同的版本的对方而写太多的代码。



可以把vdso看成一个so（其实不存在对应的文件）。内核固定把它映射在某个地址空间上，所有的进程共享了这个vdso。



参考资料

1、Linux内核特性之VDSO

https://blog.csdn.net/juana1/article/details/6904932