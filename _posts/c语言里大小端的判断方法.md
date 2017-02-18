---
title: c语言里大小端的判断方法
date: 2017-02-18 11:23:04
tags:
	- 大小端
---
先说一下记忆的方法。网络上传输是大端的。符合人的习惯认知的也是大端。总之，你觉得那个顺眼，那个就是大端的。
下面是两种常用的判断大小端的方法。
```
#include <stdio.h>

void judgeEndian1()
{
	unsigned short x = 0x1234;
	char c = *(char *)&x;
	if(c == 0x12)
	{
		printf("your machine is big endian \n");
	}
	else 
	{
		printf("your machine is little endian \n");
	}
}

void judgeEndian2()
{
	union xy_u
	{
		short x;
		char y;
	} xy;
	memset(&xy, 0, sizeof(xy));
	xy.x = 0x1234;
	if(xy.y == 0x34)
	{
		printf("little endian \n");
	}
	else
	{
		printf("big endian \n");
	}
}
int main()
{
	judgeEndian1();
	judgeEndian2();
}

```
