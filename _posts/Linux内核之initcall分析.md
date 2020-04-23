---
title: Linux内核之initcall分析
date: 2017-08-27 21:30:13
tags:
	- kernel
---



在看某个板子的适配文件中，有init_machine这样一个函数指针。

找到是在arch/arm/kernel/setup.c里：

```
static void (*init_machine)(void) __initdata;

static int __init customize_machine(void)
{
	/* customizes platform devices, or adds new ones */
	if (init_machine)
		init_machine();
	return 0;
}
arch_initcall(customize_machine);
```

那么arch_initcall有是什么呢？会导致函数如何被调用呢？

这个宏会被分为两种情况，我们现在只看被编译到内核里的情况。

```
#define arch_initcall(fn)		__define_initcall("3",fn,3)
```

`__define_initcall`这个就是定义了一个函数指针变量了，指定到某个section里，那么还是没有看到在哪里调用。

接下来就要用到链接的知识了。

在arch/arm/kernel/vmlinux.lds.S里。

```
	.init : {			/* Init code and data		*/
		_stext = .;
		_sinittext = .;
			HEAD_TEXT
			INIT_TEXT
		_einittext = .;
		__proc_info_begin = .;
			*(.proc.info.init)
		__proc_info_end = .;
		__arch_info_begin = .;
			*(.arch.info.init)
		__arch_info_end = .;
		__tagtable_begin = .;
			*(.taglist.init)
		__tagtable_end = .;

		INIT_SETUP(16) 

		INIT_CALLS 《--这里。
		CON_INITCALL
```

而在include/asm-generic/vmlinux.lds.S文件里：

```
#define INITCALLS							\
	*(.initcallearly.init)						\
	VMLINUX_SYMBOL(__early_initcall_end) = .;			\
  	*(.initcall0.init)						\
  	*(.initcall0s.init)						\
  	*(.initcall1.init)						\
  	*(.initcall1s.init)						\
  	*(.initcall2.init)						\
  	*(.initcall2s.init)						\
  	*(.initcall3.init)						\
  	*(.initcall3s.init)						\
  	*(.initcall4.init)						\
  	*(.initcall4s.init)						\
  	*(.initcall5.init)						\
  	*(.initcall5s.init)						\
	*(.initcallrootfs.init)						\
  	*(.initcall6.init)						\
  	*(.initcall6s.init)						\
  	*(.initcall7.init)						\
  	*(.initcall7s.init)

#define INIT_CALLS							\
		VMLINUX_SYMBOL(__initcall_start) = .;			\
		INITCALLS						\
		VMLINUX_SYMBOL(__initcall_end) = .;
```



然后接下来的调用顺序是：

kernel_init

​	do_basic_setup

​		do_initcalls：这个就是遍历这个初始化指针区域，一个个依次调用。

