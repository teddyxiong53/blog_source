---
title: Linux内核之kprobe
date: 2018-03-26 15:17:30
tags:
	- Linux内核

---



# 定义

什么是kprobe？

kprobe是一个动态收集调试和性能信息的工具。

它由dprobe项目发展而来。是一种非破坏性的工具。

用户可它几乎可用跟踪任何函数、指令，以及一些异步事件（如timer）。

它工作的基本机制是：

用户指定一个探测点，并把一个用户定义的处理函数关联到这个探测点。当内核执行到这个探测点的时候，用户自定义的关联函数被调用。

所以这是一种往内核里加打印，而又不用担心把内核代码弄乱的好方法。



kprobe实现了3种探测点：

1、kprobes。内核任意位置。

2、jprobes。只能插入到一个内核函数的入口。

3、kretprobes（返回探测点）。在指定的函数返回值被执行。



kprobe需要CPU架构支持。不过目前大部分CPU都是支持的。



说了这么多，还是先看一个实例吧。

```
为了使能kprobe，用户必须在编译内核时设置CONFIG_KPROBES
如果用户希望动态加载和卸载使用kprobe的模块，还必须确保“Loadable module support” (CONFIG_MODULES)和“Module unloading” (CONFIG_MODULE_UNLOAD)设置为y。
如果用户还想使用kallsyms_lookup_name()来得到被探测函数的地址，也要确保CONFIG_KALLSYMS设置为y，当然设置CONFIG_KALLSYMS_ALL为y将更好。
```

内核里的samples下面的kprobes目录下有3个例子。

我们看kprobe_example.c。它实现的功能是探测_do_fork函数。

这个文件其实很简单，但是默认都没有加入arm的情况。我们改造为下面这样。

```
#include <linux/kernel.h>
#include <linux/module.h>
#include <linux/kprobes.h>


#define MAX_SYMBOL_LEN 64
static char symbol[MAX_SYMBOL_LEN] = "_do_fork";
module_param_string(symbol, symbol, sizeof(symbol), 0644);

static struct kprobe kp  ={
	.symbol_name =symbol,
};

static int handler_pre(struct kprobe *p, struct pt_regs *regs)
{
	printk("xhl -- func:%s, line:%d \n", __func__, __LINE__);
	return 0;
}

static void handler_post(struct kprobe *p, struct pt_regs *regs, unsigned long flags)
{
	printk("xhl -- func:%s, line:%d \n", __func__, __LINE__);
	return 0;
}

static int handler_fault(struct kprobe *p, struct pt_regs *regs, int trapnr)
{
	printk("xhl -- func:%s, line:%d \n", __func__, __LINE__);
	return 0;
}


static int kprobe_init(void)
{
	int ret;
	kp.pre_handler = handler_pre;
	kp.post_handler = handler_post;
	kp.fault_handler = handler_fault;
	ret = register_kprobe(&kp);
	if(ret < 0) {
		printk("register_kprobe failed\n");
		return -1;
	}
	printk("kprobe at %p \n", kp.addr);
	return 0;
}

static void kprobe_exit(void)
{
	unregister_kprobe(&kp);
	printk("kprobe at %p unregistered\n", kp.addr);
}

module_init(kprobe_init);
module_exit(kprobe_exit);

MODULE_LICENSE("GPL");
```

我这个就是在你调用fork的时候，会打印一下。



# 在debug中的实际用途

1、测量某个系统调用的执行时间。

```

```



# 参考资料

1、Linux下 kprobe工具的使用

https://blog.csdn.net/ysbj123/article/details/51125547

2、Linux内核调试技术——kprobe使用与实现

https://blog.csdn.net/luckyapple1028/article/details/52972315

3、Linux内核kprobe机制

https://blog.csdn.net/panfengyun12345/article/details/19480567

4、Linux内核调试技术——kprobe使用与实现

https://wenku.baidu.com/view/c3f746372bf90242a8956bec0975f46526d3a745.html

