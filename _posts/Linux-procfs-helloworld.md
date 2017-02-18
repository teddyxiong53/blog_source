---
title: Linux procfs helloworld
date: 2017-02-18 21:35:07
tags:
---
总的来说，procfs有点过时了，现在sysfs在取代它。但是procfs比sysfs简单易用，所以也还有存在的价值。
testproc.c
```
#include <linux/module.h>
#include <linux/init.h>

#include <linux/kernel.h>
#include <linux/proc_fs.h>

int read_proc(char *page, char **start, off_t offset, int count, int *eof, void *data)
{
	int len = sprintf(page, "%s\n", "hello world");
	return len;
}

static int __init test_proc_init(void)
{
	create_proc_read_entry("read_proc",0,NULL, read_proc, NULL);
	return 0;
}

static void __exit test_proc_exit(void)
{
	remove_proc_entry("read_proc", NULL);
}

module_init(test_proc_init);
module_exit(test_proc_exit);
```
Makefile就用简单的通用的编译驱动的Makefile就行了。

测试：
`cat /proc/test_proc`，得到hello world的打印。


