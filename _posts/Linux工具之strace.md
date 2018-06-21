---
title: Linux工具之strace
date: 2018-03-17 22:44:10
tags:
	- Linux工具

---



strace是用来跟踪系统调用和系统的一个工具。

先看一个简单的例子。一条条看输出内容。加上注释。

```
pi@raspberrypi:~$ strace cat /dev/null
execve("/bin/cat", ["cat", "/dev/null"], [/* 15 vars */]) = 0 //用execve来产生新的进程。
brk(0)                                  = 0x1e04000
uname({sys="Linux", node="raspberrypi", ...}) = 0 //调用uname
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)//找不到这个文件，没有关系的。
mmap2(NULL, 8192, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f47000
access("/etc/ld.so.preload", R_OK)      = 0//这个文件找到了。我们看看这个文件的内容。里面就是一句话
//写着/usr/lib/arm-linux-gnueabihf/libarmmem.so
open("/etc/ld.so.preload", O_RDONLY|O_CLOEXEC) = 3//打开这个文件，fd就是3 。
fstat64(3, {st_mode=S_IFREG|0644, st_size=42, ...}) = 0//统计文件
mmap2(NULL, 42, PROT_READ|PROT_WRITE, MAP_PRIVATE, 3, 0) = 0x76f46000//mmap一下，提高访问速度。
close(3)                                = 0 //mmap后，就可以关闭了。可以继续对文件进行写入的。
open("/usr/lib/arm-linux-gnueabihf/libarmmem.so", O_RDONLY|O_CLOEXEC) = 3
read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0(\0\1\0\0\0h\5\0\0004\0\0\0"..., 512) = 512
lseek(3, 17960, SEEK_SET)               = 17960
read(3, "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"..., 960) = 960
lseek(3, 17696, SEEK_SET)               = 17696
read(3, "A.\0\0\0aeabi\0\1$\0\0\0\0056\0\6\6\10\1\t\1\n\3\f\1\22\4\24"..., 47) = 47
fstat64(3, {st_mode=S_IFREG|0644, st_size=18920, ...}) = 0
mmap2(NULL, 83236, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76f05000
mprotect(0x76f0a000, 61440, PROT_NONE)  = 0
mmap2(0x76f19000, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x4000) = 0x76f19000
mprotect(0x7eb19000, 4096, PROT_READ|PROT_WRITE|PROT_EXEC|PROT_GROWSDOWN) = 0
close(3)                                = 0
munmap(0x76f46000, 42)                  = 0
open("/etc/ld.so.cache", O_RDONLY|O_CLOEXEC) = 3 //这个里面是缓存的一些so的名字。
fstat64(3, {st_mode=S_IFREG|0644, st_size=62197, ...}) = 0
mmap2(NULL, 62197, PROT_READ, MAP_PRIVATE, 3, 0) = 0x76ef5000
close(3)                                = 0
access("/etc/ld.so.nohwcap", F_OK)      = -1 ENOENT (No such file or directory)
open("/lib/arm-linux-gnueabihf/libc.so.6", O_RDONLY|O_CLOEXEC) = 3 //打开libc了。
read(3, "\177ELF\1\1\1\0\0\0\0\0\0\0\0\0\3\0(\0\1\0\0\0L\204\1\0004\0\0\0"..., 512) = 512
lseek(3, 1239936, SEEK_SET)             = 1239936
read(3, "\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0"..., 2840) = 2840
lseek(3, 1236500, SEEK_SET)             = 1236500
read(3, "A.\0\0\0aeabi\0\1$\0\0\0\0056\0\6\6\10\1\t\1\n\2\22\4\23\1\24"..., 47) = 47
fstat64(3, {st_mode=S_IFREG|0755, st_size=1242776, ...}) = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f46000
mmap2(NULL, 1312152, PROT_READ|PROT_EXEC, MAP_PRIVATE|MAP_DENYWRITE, 3, 0) = 0x76db4000
mprotect(0x76edf000, 65536, PROT_NONE)  = 0
mmap2(0x76eef000, 12288, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_DENYWRITE, 3, 0x12b000) = 0x76eef000
mmap2(0x76ef2000, 9624, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_FIXED|MAP_ANONYMOUS, -1, 0) = 0x76ef2000
close(3)                                = 0
mmap2(NULL, 4096, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76f45000
set_tls(0x76f454c0, 0x76f45ba8, 0x76f4a050, 0x76f454c0, 0x76f4a050) = 0
mprotect(0x76eef000, 8192, PROT_READ)   = 0
mprotect(0x76f05000, 20480, PROT_READ|PROT_WRITE) = 0
mprotect(0x76f05000, 20480, PROT_READ|PROT_EXEC) = 0
cacheflush(0x76f05000, 0x76f0a000, 0, 0x15, 0x7eb198d0) = 0
mprotect(0x28000, 4096, PROT_READ)      = 0
mprotect(0x76f49000, 4096, PROT_READ)   = 0
munmap(0x76ef5000, 62197)               = 0
brk(0)                                  = 0x1e04000
brk(0x1e25000)                          = 0x1e25000
open("/usr/lib/locale/locale-archive", O_RDONLY|O_LARGEFILE|O_CLOEXEC) = 3
fstat64(3, {st_mode=S_IFREG|0644, st_size=1607760, ...}) = 0
mmap2(NULL, 1607760, PROT_READ, MAP_PRIVATE, 3, 0) = 0x76c2b000
close(3)                                = 0
fstat64(1, {st_mode=S_IFCHR|0620, st_rdev=makedev(136, 0), ...}) = 0
open("/dev/null", O_RDONLY|O_LARGEFILE) = 3  //打开null设备。
fstat64(3, {st_mode=S_IFCHR|0666, st_rdev=makedev(1, 3), ...}) = 0
fadvise64_64(3, 0, 0, POSIX_FADV_SEQUENTIAL) = 0
mmap2(NULL, 139264, PROT_READ|PROT_WRITE, MAP_PRIVATE|MAP_ANONYMOUS, -1, 0) = 0x76c09000
read(3, "", 131072)                     = 0
munmap(0x76c09000, 139264)              = 0
close(3)                                = 0
close(1)                                = 0
close(2)                                = 0
exit_group(0)                           = ?
+++ exited with 0 +++
```



strace有很多参数，加上参数，让输出结果更加符合我们的需求。

```
pi@raspberrypi:~$ strace -Tr cat /dev/null
     0.000000 execve("/bin/cat", ["cat", "/dev/null"], [/* 16 vars */]) = 0 <0.000977>
     0.001537 brk(0)                    = 0x92b000 <0.000171>
     0.000414 uname({sys="Linux", node="raspberrypi", ...}) = 0 <0.000167>
```

这样就可以看到执行的时间了。

如果要跟踪一个正在运行的程序，该怎么做？

用-p参数就好了。

```
pi@raspberrypi:~$ sleep 50&
[1] 26587
pi@raspberrypi:~$ strace -p 26587
Process 26587 attached
nanosleep({50, 0}, 

^CProcess 26587 detached
 <detached ...>
pi@raspberrypi:~$ 
```



交叉编译

```
./configure --host=aarch64-linux-gnu CC=aarch64-linux-gnu-gcc LD=aarch64-linux-gnu-ld --prefix=/home/hlxiong/tools/install/strace
```

```
strace -p `pidof doss_speaker` -e signal -e trace=process -e trace=signal -t -o /tmp/doss_speaker &
```

