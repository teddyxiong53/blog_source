---
title: alpine（五）编译分析
date: 2018-01-26 21:42:33
tags:	
	- alpine	
	- Linux

---



我其实一直很好奇的是musl这个c库。现在看看编译的情况。

# 安装

```
apk add gcc
```

然后写一个hello.c，编译。出错。找不到stdio.h。

其实要这样：

```
apk add build-base
```

```
vm-alpine-0:/usr/lib/gcc/i586-alpine-linux-musl/6.4.0# apk add build-base
(1/6) Installing musl-dev (1.1.18-r2)
(2/6) Installing libc-dev (0.7.1-r0)
(3/6) Installing g++ (6.4.0-r5)
(4/6) Installing make (4.2.1-r0)
(5/6) Installing fortify-headers (0.9-r0)
(6/6) Installing build-base (0.5-r0)
Executing busybox-1.27.2-r7.trigger
```

查看文件：

```
vm-alpine-0:~/work# file a.out 
a.out: ELF 32-bit LSB shared object, Intel 80386, version 1 (SYSV), dynamically linked, interpreter /lib/ld-musl-i386.so.1, with debug_info, not stripped
vm-alpine-0:~/work# 
```

可以看到链接的是musl的库。

这样看也可以：

```
vm-alpine-0:~/work# lddtree a.out 
a.out => ./a.out (interpreter => /lib/ld-musl-i386.so.1)
    libc.musl-x86.so.1 => /lib/libc.musl-x86.so.1
```

