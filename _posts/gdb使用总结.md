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

# 自动执行一些命令

主要是用来设置默认的参数。

在~/.gdbinit里加上：

```
set args -i input.wav output.aac -y
```



# 清除断点

delete 断点编号。



# 十六进制打印

p/x var 这样就可以了。

还可以这样：

```
x/100 buf
```

表示打印100字节。



# gdb乱序问题

用-g -O0来编译，就可以保证顺序了。



# 去掉watch

watch的作用，还导致了设置了断点。

```
watch xx这样就可以监视变量xx的变化。
```

```
info watchpoints 
	这个查看所有的监视点。
```

watch point是一种特殊的断点。

所以清除也是用delete breakpoints来进行清除。



# 跳出循环

有时候进入到一个循环了，发现这个循环次太多了。想要跳出来。

```
until xx
```

xx表示行号。



# 实时attach到已经运行的进程上

```
gdb attach `pidof xxx`
```

查看所有线程的栈：

```
thread apply all bt full 
```



# tui界面乱了怎么解决

使用cgdb。

安装：

```
sudo apt-get install cgdb
```

```
cgdb ./a.out
```

界面会带颜色。直接用就好了。跟gdb没有什么区别。

至少SecureCRT不再跟我乱闪了，而且显示界面和独特的vi风格交互感也算是加分项了，唯一遗憾的是中文字符没法正常显示，但总体还是比较推荐的。cgdb通过Trivial GDB(libtgdb)的库和后端gdb通信，通过这个库做到前端和后端分离的效果。

# 嵌入式使用

https://blog.csdn.net/Bgm_Nilbb/article/details/124853547

# gdb stub

看arduino有个gdb stub的包。

libraries\GDBStub\examples\gdbstub_example\gdbstub_example.ino

看看这个的原理是什么。



# 参考资料

https://blog.taozj.org/201703/cgdb-cheatsheet.html