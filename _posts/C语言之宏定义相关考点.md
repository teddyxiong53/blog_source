---
title: C语言之宏定义相关考点
date: 2019-12-16 12:16:22
tags:
	- C语言

---

1

# #号在宏定义里的使用

平时这个用得少。但是做题目经常碰到，总是记得不太清楚。

所以现在梳理一下。

都是写在宏参数的前面。

一个#号

```
表示字符串化。stringfy。
举例：
#include <stdio.h>
#define myprint(x) printf(#x"=%d", x)

int main()
{
    int a = 1;
    int b = 2;
    myprint(a+b);//输入是：a+b=3
}
```

2个# 号

```
这个叫做片段连接符。
它的作用是先分隔，然后进行强制连接。

#include"stdio.h"
#define Add(n,value)\
{\
	num##n+=value;\
 }
int main()
{
	int num1=1;
	int num2=10;
	Add(2,10); //等价于num2+=10; 这里把num和2连接成了num2
	printf(" num1=%d\n num2=%d",num1,num2);
	return 0;
}
```



参考资料

1、

https://blog.csdn.net/qq_41865229/article/details/86746707