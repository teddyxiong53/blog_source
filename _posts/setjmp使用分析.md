---
title: setjmp使用分析
date: 2016-12-20 21:05:23
tags:
	- setjmp
	- c语言
---


# 为什么会有setjmp的存在？

C语言的前辈是汇编，在汇编里，程序员是想怎么跳转就怎么跳转。但是到了C语言里，goto只能在函数内部打转。如果我就是想从一个函数跳到另外一个函数，怎么办？setjmp就是干这个的。





setjmp是C语言里处理exception的标准方案。
C语言里的运行控制模型，是一个基于栈结构的指令执行序列，是一个call/return的过程。
而setjmp/longjmp是另外一种形式的call/return。
return是以C语言关键字的方式提供，setmp和longjmp是以库的方式提供，它们提供了2套平行的运行流控制方式。
setjmp可以用来模拟coroutine。但是不是很好用。
C++里的异常处理就是通过封装了setjmp和longjmp来实现的。
一个简单的演示程序如下。

```
#include <stdio.h>
#include <setjmp.h>

jmp_buf buf;

void test()
{
	printf("begin test function \n");
	longjmp(buf, 1);
	printf("end test function \n");
}
int main()
{
	if(setjmp(buf))
	{
		printf("main setjmp return by longjump \n");
	}
	else
	{
		printf("main setjmp ok \n");
		test();
	}
	return 0;
}
```
运行的结果如下：
```
teddy@teddy-ubuntu:~/test/c-test$ ./a.out    
main setjmp ok 
begin test function 
main setjmp return by longjump 
```

下面再用一个小程序来演示异常处理的方式。

```
#include <stdio.h>
#include <setjmp.h>
#include <stdlib.h>


jmp_buf buf;

void f1()
{
	printf("begin f1 \n");
	if(0) //
	{
		//normal
	}
	else //error
	{
		longjmp(buf, 1);
	}
	printf("end f1 \n");
}

void f2()
{
	printf("begin f2 \n");
	if(1) //
	{
		//normal
	}
	else //error
	{
		longjmp(buf, 2);
	}
	printf("end f2 \n");
}



int main()
{
	int r = setjmp(buf);
	if(r == 0)
	{
		f1();
		f2();
	}
	else if(r == 1)
	{
		printf("f1 error proc \n");
		exit(1);
	}
	else if(r == 2)
	{
		printf("f2 error proc \n");
		exit(2);
	}
	return 0;
}
```
运行结果如下：
```

teddy@teddy-ubuntu:~/test/c-test$ ./a.out 
begin f1 
f1 error proc 
```


