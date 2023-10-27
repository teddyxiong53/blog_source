---
title: Linux的模块分析
date: 2017-04-15 00:11:59
tags:
	- Linux
---
--

Linux的module的ko文件，跟普通的目标文件一样，都是可重定位的文件。

而普通目标文件，是不能直接执行的，

它需要经过链接器的地址空间分配、符号解析和菜的味道 过程，转化为可执行文件才能执行。



内核在加载一个ko文件的时候，经历了怎样的一个过程呢？

现在就分析一下。

我先看Linux源代码里的module对应的数据结构的定义。

在`include/linux/module.h`里。

成员较多，我们现在关注的是其中init和exit这2个函数指针。

这2个指针就是我们写驱动文件里的init和exit函数注册到这里。

当我们在执行`insmod test.ko`的时候，内核通过系统调用`init_module`来完成。
如下：

```
SYSCALL_DEFINE3(init_module, void __user *, umod,
		unsigned long, len, const char __user *, uargs)
{

	//...
	err = copy_module_from_user(umod, len, &info);
	//...
	return load_module(&info, uargs, 0);
}
```


