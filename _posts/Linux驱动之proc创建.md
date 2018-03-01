---
title: Linux驱动之proc创建
date: 2018-03-01 11:51:13
tags:
	- Linux驱动

---



大多数/proc目录下的文件都是只读的，如果提供写方法也没问题。

创建proc文件的方法有3种：

1、用create_proc_entry函数，简单，但是写操作有缓冲区溢出的危险。

2、用proc_create和seq_file来创建proc文件。比方法3简洁。

3、使用proc_create_data和seq_file来创建proc文件。复杂点，但是完整。



seq流函数的使用保证了数据能顺序输出，这也就是/proc只读文件中使用它的最大原因吧。