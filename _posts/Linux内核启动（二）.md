---
title: Linux内核启动（二）
date: 2018-03-18 19:20:04
tags:
	 - Linux内核

---



启动的有些代码是通过把代码链接到固定的段，分段来执行的。

这些段的先后顺序是怎样的？

就是这样的：

```
static char *initcall_level_names[] __initdata = {
	"early",
	"core",
	"postcore",
	"arch",
	"subsys",
	"fs",
	"device",
	"late",
};
```

最先执行的是early这个段的。

在init.h里是这么定义的。

```
#define early_initcall(fn)		__define_initcall(fn, early)

#define pure_initcall(fn)		__define_initcall(fn, 0)

#define core_initcall(fn)		__define_initcall(fn, 1)
#define core_initcall_sync(fn)		__define_initcall(fn, 1s)
#define postcore_initcall(fn)		__define_initcall(fn, 2)
#define postcore_initcall_sync(fn)	__define_initcall(fn, 2s)
#define arch_initcall(fn)		__define_initcall(fn, 3)
#define arch_initcall_sync(fn)		__define_initcall(fn, 3s)
#define subsys_initcall(fn)		__define_initcall(fn, 4)
#define subsys_initcall_sync(fn)	__define_initcall(fn, 4s)
#define fs_initcall(fn)			__define_initcall(fn, 5)
#define fs_initcall_sync(fn)		__define_initcall(fn, 5s)
#define rootfs_initcall(fn)		__define_initcall(fn, rootfs)
#define device_initcall(fn)		__define_initcall(fn, 6)
#define device_initcall_sync(fn)	__define_initcall(fn, 6s)
#define late_initcall(fn)		__define_initcall(fn, 7)
#define late_initcall_sync(fn)		__define_initcall(fn, 7s)
```

early的，不多。都是内核基础设施。不关注。

虽然叫early，但是这一批的都是在相对靠后的位置调用的。

```
rest_init
	kernel_init
		kernel_init_freeable
			do_basic_setup（这个就快要到执行/init了）
				do_initcalls
					do_initcall_level
						for (fn = initcall_levels[level]; fn < initcall_levels[level+1]; fn++)
		                   do_one_initcall(*fn);
```

把这些函数名打印出来。

内核提供了一个initcall_debug的bootargs参数。但是我对qemu传递参数，总是不行。

我把内核的打印级别改到7 。

然后强行把do_one_initcall_debug里的printk改成KERN_ERR的。

这样就有打印出来了。内容还很多。

