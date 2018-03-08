---
title: Linux之内核中的同步机制辨析
date: 2018-03-08 17:04:13
tags:
	- Linux

---



##mutex

mutex相当于一个厕所坑位，只能一个人上。后面要用的人得排队等前面的一个人出来才行。

## semaphore

这个是一个教室，可以容纳多人，还有座位就能进去。

## 二值semaphore和mutex区别

1、有的系统是没有区别的。

2、有的系统有区别。mutex谁拿着谁释放。而semaphore可以由其他人释放。

mutex用来保护，semaphore用来同步。分工明确。

## spinlock和semaphore区别

1、spinlock是一直占用CPU的等。

2、semaphore会sleep让出CPU。

3、只有多CPU的内核态非进程空间，才会用到spinlock。

结论：spinlock很少用。

