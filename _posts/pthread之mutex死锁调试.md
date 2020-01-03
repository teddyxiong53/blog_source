---
title: pthread之mutex死锁调试
date: 2019-12-30 10:14:08
tags:
	- 多线程

---

1

把下面的内容，保存成deadlock_gdb_debug.txt文件。

```
set pagination off
set logging file gdb.log
set logging overwrite
set logging on

start
set $lock_addr=pthread_mutex_lock
set $unlock_addr=pthread_mutex_unlock
break *$lock_addr
break *$unlock_addr

while 1
	continue
	if $pc != $lock_addr && $pc != $unlock_addr
		quit
	end
	bt
end

#不出现Type<Enter>to continue的提示消息
#设置日志文件gdb.log
#写日志模式为覆盖写
#开启日志功能

#在main函数第一句设置断点并开始执行程序
#记录lock和unlock的系统函数地址并给他们设置断点
#调试对象程序执行后若出现死锁，立刻结束程序(quit，等效用户Ctrl-C)
#bt就是每次有锁操作时就打印堆栈到log
```

然后用gdb启动程序，带上参数：

```
gdb ./xx -x ./deadlock_gdb_debug.txt
```





参考资料

1、用gdb脚本解决死锁的调试方法(由pthread_mutex_lock引起的死锁)

https://blog.csdn.net/u012421852/article/details/51793698