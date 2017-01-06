---
title: busybox的globals结构体分析
date: 2016-12-23 19:30:38
tags:
	- busybox
---
在busybox的很多的命令对应的c文件里，都有定义一个struct globals，这个是起什么作用呢？本文就分析一下。
我们就先看看代码。
在arp.c里：
```
struct globals {
	const struct aftype *ap; /* current address family */
	const struct hwtype *hw; /* current hardware type */
	const char *device;      /* current device */
	smallint hw_set;         /* flag if hw-type was set (-H) */
} FIX_ALIASING;
#define G (*(struct globals*)bb_common_bufsiz1)
```
在ls.c里：
```
struct globals {
#if ENABLE_FEATURE_LS_COLOR
	smallint show_color;
# define G_show_color (G.show_color)
#else
# define G_show_color 0
#endif
	smallint exit_code;
	unsigned all_fmt;
#if ENABLE_FEATURE_AUTOWIDTH
	unsigned terminal_width;
# define G_terminal_width (G.terminal_width)
#else
# define G_terminal_width TERMINAL_WIDTH
#endif
#if ENABLE_FEATURE_LS_TIMESTAMPS
	/* Do time() just once. Saves one syscall per file for "ls -l" */
	time_t current_time_t;
#endif
} FIX_ALIASING;
#define G (*(struct globals*)bb_common_bufsiz1)
```
可以看到在不同的c文件里都定义了一个同名的结构体类型globals。然后都定义了一个宏G，来指向`bb_common_bufsiz1`这个全局变量。这个变量在libbb/common_bufsiz.c里定义。长度是1024字节。
```
char bb_common_bufsiz1[COMMON_BUFSIZE] ALIGNED(sizeof(long long));
```
关于这个点的分析，在`busybox/docs/keep_data_small.txt`里说明。是一种减小busybox空间占用的手段。
总的来说，就是把各个applet的全局变量所占用的空间提取成公共的，这样就可以节省大量的bss段内存。
根据busybox官方给出的统计数据，用ulibc编译的静态的busybox，每个applet需要的内存在x86上，需要26K内存。在x64上，需要55K内存。




