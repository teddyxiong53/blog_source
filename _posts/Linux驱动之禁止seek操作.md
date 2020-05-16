---
title: Linux驱动之禁止seek操作
date: 2020-05-16 15:47:43
tags:
	- Linux
---

1

需要2个步骤：

1、在驱动的fops的open函数里，调用：

```
nonseekable_open(inode,filp);
```

2、把fops的llseek赋值为no_llseek。



对于串口这些流操作，是不允许seek的。



参考资料

1、不允许lseek文件 | nonseekable_open()

https://blog.csdn.net/gongmin856/article/details/8273545