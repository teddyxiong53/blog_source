---
title: Linux之各种trace工具
date: 2018-03-26 16:55:36
tags:
	- Linux

---



Linux下有各种trace工具，现在统一梳理一下。

我们在Ubuntu下输入ftrace，可以炸出一堆的类似命令来。

```
teddy@teddy-ubuntu:~/work/linux-rpi/linux-rpi-4.4.y$ ftrace
No command 'ftrace' found, did you mean:
 Command 'itrace' from package 'irpas' (multiverse)
 Command 'rtrace' from package 'radiance' (universe)
 Command 'fstrace' from package 'openafs-client' (universe)
 Command 'dtrace' from package 'systemtap-sdt-dev' (universe)
 Command 'btrace' from package 'blktrace' (universe)
 Command 'ltrace' from package 'ltrace' (main)
 Command 'mftrace' from package 'mftrace' (universe)
 Command 'fatrace' from package 'fatrace' (universe)
 Command 'xtrace' from package 'xtrace' (universe)
 Command 'mtrace' from package 'libc-dev-bin' (main)
 Command 'strace' from package 'strace' (main)
ftrace: command not found
```

我们一个个看看。



itrace

1、安装

```
sudo apt install irpas
```

2、查看man信息。

```
itrace - similar to traceroute, yet uses ICMP echo
```

3、用法。

```
teddy@teddy-ubuntu:~/work/linux-rpi/linux-rpi-4.4.y$ sudo itrace -i eth0 -d www.baidu.com
 1(1)   [192.168.190.2]
 2(all) Timeout
 3(all) Timeout
```

是查看路由信息的。

对我来说，不重要。

rtrace

这个安装包很大。就不管了。不重要。



我感觉大部分都是没用的。

重要的是下面这几个。

1、ftrace。

2、strace。

3、ltrace。

使用的层次关系是这样。

```
  App
  |
  |  <--------ltrace
  |
libc ld  < -------strace
  |
  |     <----------systemtap
 kernel  <---------ftrace
```



我们先看ltrace的效果。这个是对应用程序起作用的。

对于一个helloworld程序，是这样。

```
teddy@teddy-ubuntu:~/work/test/c-test$ ltrace ./a.out 
__libc_start_main(0x400526, 1, 0x7ffeb9af76e8, 0x400540 <unfinished ...>
puts("hello world"hello world
)                                                                                      = 12
+++ exited (status 12) +++
```



strace也是对应用程序其作用。

```
teddy@teddy-ubuntu:~/work/test/c-test$ strace ./a.out 
execve("./a.out", ["./a.out"], [/* 32 vars */]) = 0
brk(NULL)                               = 0x1f0d000
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
access("/etc/ld.so.preload", R_OK)      = -1 ENOENT (No such file or directory)
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3
fstat(3, {st_mode=S_IFREG|0644, st_size=135792, ...}) = 0
mmap(NULL, 135792, PROT_READ, MAP_PRIVATE, 3, 0) = 0x7fc5d3030000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/x86_64-linux-gnu/libc.so.6", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\2\1\1\3\0\0\0\0\0\0\0\0\3\0>\0\1\0\0\0P\t\2\0\0\0\0\0"..., 832) = 832
fstat(3, {st_mode=S_IFREG|0755, st_size=1868984, ...}) = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fc5d302f000
mmap(NULL, 3971488, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x7fc5d2a63000
mprotect(0x7fc5d2c23000, 2097152, PROT_NONE) = 0
mmap(0x7fc5d2e23000, 24576, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x1c0000) = 0x7fc5d2e23000
mmap(0x7fc5d2e29000, 14752, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x7fc5d2e29000
close(3)                                = 0
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fc5d302e000
mmap(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x7fc5d302d000
arch_prctl(ARCH_SET_FS, 0x7fc5d302e700) = 0
mprotect(0x7fc5d2e23000, 16384, PROT_READ) = 0
mprotect(0x600000, 4096, PROT_READ)     = 0
mprotect(0x7fc5d3052000, 4096, PROT_READ) = 0
munmap(0x7fc5d3030000, 135792)          = 0
fstat(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 3), ...}) = 0
brk(NULL)                               = 0x1f0d000
brk(0x1f2e000)                          = 0x1f2e000
write(1, "hello world\n", 12hello world
)           = 12
exit_group(12)                          = ?
+++ exited with 12 +++
```

 ftrace不同于其他的调试工具，他需要debugfs的辅助。debugfs是一种特殊的文件系统，本身无法进行编辑，任何写入信息都要靠echo载入。另外由于是kernel debug，所以需要最高的root权限。 我们要先挂载这个文件系统到特殊的文件目录。这个/mnt/与/sys/kernel/debug/tracing是等同的。



# 参考资料

1、调试工具ltrace strace ftrace的使用

http://lzz5235.github.io/2013/11/22/ltrace-strace-ftrace.html

