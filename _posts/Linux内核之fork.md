---
title: Linux内核之fork
date: 2018-03-30 20:55:08
tags:
	- Linux内核

---



在arch/arm/kernel目录下面，有个sys_arm.c文件。

这个文件里实现了几个系统调用：

```
sys_fork
sys_vfork
sys_clone
sys_execve
```

我们先看看sys_fork和sys_vfork的区别 ：

```
asmlinkage int sys_fork(struct pt_regs *regs)
{
	return do_fork(SIGCHLD, regs->ARM_sp, regs, 0, NULL, NULL);
}
```

```
asmlinkage int sys_vfork(struct pt_regs *regs)
{
	return do_fork(CLONE_VFORK | CLONE_VM | SIGCHLD, regs->ARM_sp, regs, 0, NULL, NULL);
}
```

就是do_fork的参数不一样，sys_vfork多了CLONE_VFORK和CLONE_VM这2个flag。

regs也不一样。

vfork得到的是轻量级进程，也就是线程。



# 参考资料

1、

https://blog.csdn.net/gatieme/article/details/51417488