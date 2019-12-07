---
title: Linux内核之early param分析
date: 2019-12-07 15:03:43
tags:
	- Linux
---

1

先搜索一下内核里用到的early_param有哪些。

```
bootmem_debug
	打开bootmem的调试。
debug_objects
no_debug_objects
kgdbcon
nokgdbroundup
kgdbwait
earlyprintk
initrd
kmemleak
nosmp
nr_cpus
maxcpus
debug
quiet
loglevel
memblock
cachepolicy
nocache
nowb
ecc
vmalloc
mminit_loglevel
numa_zonelist_order
kernelcore
movablecore
percpu_alloc
ignore_loglevel
sched_debug
mem
```



early_param和setup都是对同一个宏的展开。

```
#define __setup(str, fn)					\
	__setup_param(str, fn, fn, 0)

/* NOTE: fn is as per module_param, not __setup!  Emits warning if fn
 * returns non-zero. */
#define early_param(str, fn)					\
	__setup_param(str, fn, fn, 1)
```

early_param和setup没有大的区别，就是一个优先级的区别。

都是uboot传递过来的cmdline里设置。early_param定义的，会被先执行。

执行完early_param的，才解析setup的。

如果early被设置为1,则执行对应的setup_func，而对于early没有设置为1的obs_kernel_param数组成员，则留到后面去执行。



setup的项有：

```
lpj=
no_file_caps
有很多，不一一列举了。
```



参考资料

1、

https://blog.csdn.net/rikeyone/article/details/79979887