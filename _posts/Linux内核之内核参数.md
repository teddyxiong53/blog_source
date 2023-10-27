---
title: Linux内核之内核参数
date: 2020-10-27 09:57:30
tags:
	- Linux
---

--

Linux内核参数是在Linux内核中由宏__setup定义的一系列参数。

内核参数包括**启动参数和内核模块参数**，完整的内核参数列表可以参见Documents/kernel-parameters.txt。

以lpj为例子。分析一下。

```
static int __init lpj_setup(char *str)
{
	preset_lpj = simple_strtoul(str,NULL,0);
	return 1;
}

__setup("lpj=", lpj_setup);
```

__setup 展开的效果

```
static const char __setup_str_lpj_setup[] __initconst	__aligned(1) = "lpj="; 
static struct obs_kernel_param __setup_lpj_setup	__used __section(.init.setup)	__attribute__((aligned((sizeof(long))))) = { __setup_str_lpj_setup, lpj_setup, 0 }
```

简化一下：

```
static const char __setup_str_lpj_setup[] = "lpj="; 
static struct obs_kernel_param __setup_lpj_setup = { __setup_str_lpj_setup, lpj_setup, 0 }
```

就是定义了2个变量。一个字符串。一个结构体。

结构体的定义是：

```
struct obs_kernel_param {
	const char *str;
	int (*setup_func)(char *);
	int early;
};
```

该结构体在链接后存在于.init.setup段。其实该段也就是所有内核参数所在的处。该段的起始地址是`__setup_start`，结束地址为`__setup_end`。



参考资料

1、kernel/Documentation/kernel-parameters.txt

2、Kernel Parameters

https://blog.csdn.net/liushuimpc/article/details/44201223