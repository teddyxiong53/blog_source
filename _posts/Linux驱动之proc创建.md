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



# seq分析

我现在以miscdevice的misc.c文件为入口，来分析seq的相关情况。

对应的文件是fs/seq_file.c和linux/seq_file.h。

主要结构体有：

```
struct seq_file。buf和size。
struct seq_operations：4个函数指针，start/stop/next/show。
```

对外提供的接口主要就是seq_open/release/read/write这4个接口。

在misc.c里。

```
static int misc_seq_open(struct inode *inode, struct file *file)
{
	return seq_open(file, &misc_seq_ops);
}
```

其他的地方，也基本是这么用的，就是在自己的file_operations里的open函数里，调用seq_open，传递自己的xx_seq_ops进去。

xx_seq_ops就是struct seq_operations的。里面start/stop/next/show 4个函数的实现。

我们看看seq_open里具体做了什么。

```
参数：
	1、struct file *file
	2、struct seq_operations *ops
处理：
	1、分配一个struct seq_file *p的指针结构体内存。
	2、file->private_data = p;
		p->op = ops;
		就这些了。
```

看看seq_read。

```
参数：
	跟普通文件的read参数一样。
处理：
	1、通过file->private_data取到seq_file指针。就是在open的时候，赋值过来的。
	2、分配内存。buf和size。是用kmalloc的。如果分配不成功，而且size大于page，就用vmalloc。
		还是那句话，轻易不要用vmalloc。
	3、这里面就是会调用到seq_operations的show函数了。
```

