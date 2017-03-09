---
title: Linux的sbrk分析
date: 2017-03-02 22:20:17
tags:
	- linux
---
Linux中每个用户进程可以访问的虚拟内存空间为3G，但是一般写程序用不了这么多，所以系统默认只给程序分配了并不大的数据段空间，如果空间不够时，malloc函数内部会调用sbrk函数，再把数据段的边界移动，sbrk函数再内核的管理下，将虚拟地址空间映射到内存。
sbrk并不是系统调用，而是一个C库函数。
我们可以用sbrk(0)来查询当前程序用到的内存是多少。示例如下：
```

int main()
{
	int start ,end;
	start = sbrk(0);
	malloc(0x1);
	end = sbrk(0);
	printf("used memory:0x%x \n", end - start);
}

```
