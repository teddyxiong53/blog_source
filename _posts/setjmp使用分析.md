---
title: setjmp使用分析
date: 2016-12-20 21:05:23
tags:
	- setjmp
	- c语言
---

--

# 最简单的理解

setjmp+longjmp = 函数间的goto。

jmp_buf里存放的cpu的运行信息。

# 说明

`setjmp` 和 `longjmp` 是C语言中提供的两个函数，用于实现非局部跳转。

它们通常被用来处理异常、错误处理或者实现类似于 `try-catch` 语句的功能。

`setjmp` 函数的作用是将当前的程序状态保存起来，

包括程序计数器、堆栈指针等信息，并返回0。

这个保存的状态被保存在一个 `jmp_buf` 结构体中，它是一个数组类型，可以将其传递给 `longjmp` 函数。

`longjmp` 函数则是将程序状态恢复到之前通过 `setjmp` 保存的状态，

然后返回到 `setjmp` 调用处，

但是 `longjmp` ==会使程序执行跳转而不是通过正常的函数调用返回。==

通常情况下，==`longjmp` 的第二个参数是一个非零值，用于指示跳转原因。==

这种非局部跳转的机制通常被用来处理异常情况，

比如在函数嵌套调用中出现错误时，

可以通过 `longjmp` 跳转到事先设定好的错误处理代码处，==从而避免多层函数逐层返回。==

在没有 `setjmp` 和 `longjmp` 的情况下，这种错误处理可能会导致函数调用链的多次返回操作，非常复杂且易出错。

需要注意的是，`setjmp` 和 `longjmp` 并==不是线程安全的，==

而且它们的使用会使程序的控制流变得混乱，

因此在实际开发中，应该谨慎使用，最好使用更为安全和可读性更高的错误处理机制，如 `errno`、`try-catch` 等。

# 为什么会有setjmp的存在？

C语言的前辈是汇编，在汇编里，程序员是想怎么跳转就怎么跳转。

但是到了C语言里，goto只能在函数内部打转。

如果我就是想从一个函数跳到另外一个函数，怎么办？setjmp就是干这个的。



**setjmp是C语言里处理exception的标准方案。**

C语言里的运行控制模型，是一个基于栈结构的指令执行序列，是一个call/return的过程。

**而setjmp/longjmp是另外一种形式的call/return。**

**return是以C语言关键字的方式提供，setmp和longjmp是以库的方式提供，**它们提供了2套平行的运行流控制方式。

setjmp可以用来模拟coroutine。但是不是很好用。

setjmp和longjmp是互补的两个函数。

在信号处理机制里，进程在收到信号时，会从原来的系统调用直接返回，而不是等到该调用结束。

**这种进程突然改变上下文的情况，就是使用setjmp和longjmp**



C语言没有C++或Java的异常机制，但可以通过setjmp/longjmp实现类似的效果：

- 使用setjmp保存`当前执行环境`到jmp_buf，**然后默认返回0。**
- 程序继续执行，到某个地方**调用longjmp，传入上面保存的jmp_buf，以及另一个值。**
- 此时执行点又回到调用setjmp的返回处，**且返回值变成longjmp设置的值**。



C++里的异常处理就是通过封装了setjmp和longjmp来实现的。

一个简单的演示程序如下。

```
#include <stdio.h>
#include <setjmp.h>

jmp_buf buf;

void test()
{
	printf("begin test function \n");
	longjmp(buf, 1);//这样会让setjmp返回1，所以有进到main里面的if分支了。
	printf("end test function \n");//这里不会执行到。
}
int main()
{
	if(setjmp(buf))//默认返回0，所以走到else分支了
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



# setjmp.h头文件

这个头文件里定义3个东西：

1、setjmp

2、longjmp

3、jmp_buf类型。这个会绕过正常的调用返回规则。

setjmp这种机制，为C语言里任意进行跳转留下了活动空间。

看看musl里的定义是怎样的，针对arm平台的。

```
typedef unsigned long long __jmp_buf[32];//放32个寄存器。
typedef struct __jmp_buf_tag {
	__jmp_buf __jb;
	unsigned long __fl;
	unsigned long __ss[128/sizeof(long)];
} jmp_buf[1];
```



```
#include <setjmp.h>
#include <stdio.h>

int main()
{
	jmp_buf env;
	int i;
	i = setjmp(env);
	printf("i=%d\n", i);
	if(i!=0) {
		return 0;
	}
	longjmp(env, 10);
	printf("xxxx\n");
}
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
i=0
i=10
```

# jmp_buf

`jmp_buf` 是一个C语言中的特殊类型，通常用于保存程序执行状态的信息，以便后续通过 `longjmp` 来实现非局部跳转。

它实际上是一个数组类型，用来存储程序状态的信息。在许多系统中，`jmp_buf` 被定义为==长度足够存储所有寄存器和其他必要信息的数组==。它的实现通常是平台相关的，但是在几乎所有的系统中，`jmp_buf` 的大小都是固定的。

您可以将 `jmp_buf` 用作局部变量，以保存当前的执行状态。然后，当您调用 `setjmp` 函数时，它将会保存当前执行状态到 `jmp_buf` 中，并返回一个标记值（通常是0），以便在后续需要时作为跳转点。而 `longjmp` 函数可以根据之前保存的状态，将程序的执行跳转到 `setjmp` 处，实现非局部跳转。

需要注意的是，`jmp_buf` 是一个非常底层的特性，它的使用应该非常小心，因为滥用它可能导致程序的控制流非常难以理解和维护。通常情况下，它被用来实现一些特殊的控制流机制，比如错误处理或者实现协程。

# 参考资料

1、C 标准库 - < setjmp.h >

http://wiki.jikexueyuan.com/project/c/c-standard-library-setjmp-h.html

2、C 语言中 setjmp 和 longjmp

http://www.cnblogs.com/hazir/p/c_setjmp_longjmp.html

3、setjmp.h

https://zh.wikipedia.org/wiki/Setjmp.h