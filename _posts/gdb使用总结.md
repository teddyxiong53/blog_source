---
title: gdb使用总结
date: 2017-05-04 20:31:22
tags:
	- gdb

---



# 图形化界面

gdb可以打开图像界面的，这样调试的时候，就直观多了。

快捷键是Ctrl +X +A。在gdb界面进入退出都是这个。

这样就可以跟visual studio那样看到单步的效果了。



# 实时显示数组内容

我的数组名字是a，长度是5 。

```
display *a@5
```

效果是这样：

```
(gdb) n
1: *a@5 = {1, 2, 4, 3, 1}
1: *a@5 = {1, 2, 4, 3, 1}
```

要取消，就输入：

```
undisplay 1 #1是一个序号，上面有的。
```

如果只看一次，就用p替代display就好了。

# 优化问题

1、打印变量内容，提示`optimized out`。

我是在调试linux内核的时候碰到这个问题的。

```
ifdef CONFIG_PROFILE_ALL_BRANCHES
KBUILD_CFLAGS	+= -O2 $(call cc-disable-warning,maybe-uninitialized,)
else
KBUILD_CFLAGS   += -O2 //这个O2改成O0
endif
```

O0的编译不过。我加上一个函数，还是有一堆找不到，改成O1的编译可以。

```
void __bad_cmpxchg(volatile void *ptr, int size)
{
	printk("cmpxchg: bad data size: pc 0x%p, ptr 0x%p, size %d\n",
		__builtin_return_address(0), ptr, size);
	BUG();
}
EXPORT_SYMBOL(__bad_cmpxchg);
```

# 调试带参数的程序

```
set args xxx
show args
```

# 清除断点

delete 断点编号。



#十六进制打印