---
title: Linux内核之select实现原理
date: 2018-03-26 13:22:33
tags:
	- Linux内核

---



代码调用流程是这样：

```
SYSCALL_DEFINE5(select //在fs/select.c里。
	core_sys_select
		get_fd_set(n, inp, fds.in)) //这里面就是一个copy_from_user。所以说select效率低。
		do_select
			poll_initwait
			
```

