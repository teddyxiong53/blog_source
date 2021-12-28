---
title: Linux内核之PTR_ERR和ERR_PTR
date: 2021-12-20 13:30:11
tags:
	- Linux

---

--

内核空间最高地址0xffffffff,

那么最后一个page就是指的0xfffff000~0xffffffff(假设4k一个page).

这段地址是被保留的

linux的错误号，

例如最常见的几个 -EBUSY,-EINVAL,-ENODEV,-EPIPE,-EAGAIN,-ENOMEM 之类，

其值都位于这个空间。

其实未加负号之前的值（见下面），其实也位于一个内存的内存区域。

```
#define EPERM 1 /* Operation not permitted */
#define ENOENT 2 /* No such file or directory */
#define ESRCH 3 /* No such process */
#define EINTR 4 /* Interrupted system call */
```

任何一个指针,必然有三种情况,

一种是有效指针,

一种是NULL,空指针,

一种是错误指针,或者说无效指针.

**而所谓的错误指针就是指其已经到达了最后一个page.**

用IS_ERR()判断返回的指针是否有错,

如果指针并不是指向最后一个page,那么没有问题,申请成功了；

**如果指针指向了最后一个page,那么说明实际上这不是一个有效的指针,**

**这个指针里保存的实际上是一种错误代码。**

而通常很常用的方法就是先用IS_ERR()来判断是否是错误,

然后如果是,那么就调用PTR_ERR()来返回这个错误代码。

PTR_ERR()只是返回错误代码,

也就是提供一个信息给调用者,

**如果你只需要知道是否出错,而不在乎因为什么而出错,**

**那你当然不用调用PTR_ERR()了。**



参考资料

1、ERR_PTR()和PTR_ERR()

https://blog.csdn.net/adaptiver/article/details/40145313

