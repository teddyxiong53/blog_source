---
title: posix之标准头文件
date: 2022-12-07 15:48:19
tags:
	- posix

---

--

在toybox的toys.h里，有写着：

```
// General posix-2008 headers
```

然后下面include了一堆的头文件。

所以，posix 2008标准包含了哪些头文件？这个标准信息哪里可以查询到？

网上直接找总结的资料，不看原始文档了。

标准文档是在这里：

http://www.opengroup.org/austin/



# POSIX标准定义的必需的头文件 

（顺便配合musl库代码看这些头文件的内容）

```
aio.h
	异步io。核心结构体struct aiocb 
cpio.h
	cpio归档值。这个里面就20来个宏定义值。
dirent.h
	目录项。核心struct dirent，另外opendir等接口。
dlfcn.h
	动态库操作。dlopen等函数。
fcntl.h
	文件控制。就是各种flag宏定义。
fnmatch.h
	文件名匹配类型。就提供一个接口：int fnmatch(const char *, const char *, int);
glob.h
	路径名模式匹配与生成。
	提供一个glob函数。
grp.h
	用户组管理。
iconv.h
	代码集实用变换程序。iconv_open等函数。
langinfo.h
	语言相关的常量定义。
monetory.h
	货币数字相关。strfmon函数。
netdb.h
	网络数据库操作相关。struct addrinfo 
nl_types.h
	nl是什么的缩写？
	https://pubs.opengroup.org/onlinepubs/7908799/xsh/nl_types.h.html
	消息类型。具体用途不清楚。
poll.h
	poll的io多路复用。
pthread.h
	多线程。
pwd.h
	密码文件。
regex.h
	正则表达式。
sched.h
	调度。struct sched_param 
semaphore.h
	信号量。sem_post
strings.h
	这个提供的是bzero这些函数。跟C标准库的string.h不同。
tar.h
	tar相关的宏定义。
termios.h
	终端io。
unistd.h
	系统调用都在这里了。
wordexp.h
	word扩展。
arpa/inet.h
	internet相关的定义。ntohs这些函数就是在这里面。
net/if.h
	socket的本地接口。
netinet/in.h
	internet地址族。sockaddr_in
netinet/tcp.h
	tcp header等的定义。
sys/mman.h
	存储管理。mmap、shm_open。
sys/select.h
	select io多路复用。
sys/socket.h
	socket/accept等接口。
sys/stat.h
	stat、mkdir等函数。
sys/statvfs.h
	文件系统信息。
sys/times.h
	times函数。跟time不一样。
sys/types.h
	提供u_long这样的类型。一般不用。
sys/un.h
	unix socket。
sys/utsname.h
	系统名字。
sys/wait.h
	进程控制。
	
```

# C标准库头文件

这个不是posix的一部分。但是作为对比看看。

```
assert.h
	提供assert断言函数。
complex.h
	复数计算。
ctype.h
	isalpha等函数。
errno.h
	错误码。
fenv.h
	浮点环境。很少用。
float.h
	浮点常量。
	很少用。
inttypes.h
	提供了这样的宏：PRId64
	全是这种宏。
iso646.h
	没什么用。就是提供用and 来替代&&。
limits.h
	提供了一些_POSIX_TZNAME_MAX 这样的宏。
locale.h
	本地化。
math.h
	提供sine等函数。
setjmp.h
	被局部goto。
signal.h
	信号。
stdarg.h
	可边长参数，va_start这些。
stdbool.h
	就定义了这3个宏。
	#define true 1
    #define false 0
    #define bool _Bool
stddef.h
	标准定义。好像没有什么。
stdint.h
	提供了uint8_t这样的类型。常用。
stdio.h
	printf等函数。
stdlib.h
	malloc等函数。
string.h
	memcpy、strlen等函数。
tgmath.h
	通用类型数学宏。
	少用。
time.h
	常用。
wchar.h
	wchar_t类型。
wctype.h
	跟wchar.h作用类似。
```

# time.h和sys/time.h的区别

`time.h` 和 `sys/time.h` 是两个不同的头文件，它们提供了与时间和时间处理相关的不同功能。以下是它们的主要区别：

1. **`time.h`**：
   - `time.h` 是标准 C 库的一部分，提供了用于处理日期和时间的基本功能。
   - 它包含了常见的时间操作函数，如 `time`、`difftime`、`ctime`、`strftime` 等，以及与日历时间相关的类型和宏。
   - `time.h` 通常用于处理日期和时间的标准操作，例如获取当前时间、计算时间间隔、格式化时间字符串等。

2. **`sys/time.h`**：
   - `sys/time.h` 是一个与系统编程和底层系统调用相关的头文件，通常用于 UNIX-like 操作系统。
   - 它包含了一些与系统时间和系统调用相关的定义，如 `struct timeval`，`gettimeofday` 等。
   - `sys/time.h` 中的 `struct timeval` 结构通常用于测量时间间隔或执行一些需要高精度时间的系统调用。

总的来说，`time.h` 用于处理通用日期和时间操作，适用于应用程序级别的时间处理，而 `sys/time.h` 通常用于底层系统编程，与系统时间和高精度时间间隔测量相关的功能。在许多情况下，你可以使用 `time.h` 来满足一般的时间处理需求，而 `sys/time.h` 更适用于需要更底层的时间控制和精度的情况。需要注意的是，`sys/time.h` 头文件可能不在标准 C 库的一部分，因此在不同的操作系统上可能会有一些差异。



# 参考资料

1、POSIX.1各头文件简单说明

https://blog.csdn.net/mumoDM/article/details/81139411