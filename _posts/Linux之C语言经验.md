---
title: Linux之C语言经验
date: 2018-01-31 11:59:09
tags:
	- Linux
	- C语言

---



把一些以前不知道，但是有用的小技巧总结记录。

#atexit

注册main函数退出需要进行的操作。这个注册个数可以配置，可以很多的。

用法：

```
#include <stdlib.h>

static void my_atexit1(void)
{
	printf("my_ateixt1 handler \n");
}

static void my_atexit2(void)
{
	printf("my_ateixt2 handler \n");
}

int main(int argc, char **argv) 
{
	if((atexit(my_atexit1)) != 0) 
	{
		printf("register my_atexit1 failed \n");
	}
	if((atexit(my_atexit2)) != 0) 
	{
		printf("register my_atexit2 failed \n");
	}
	printf("main is done\n");
	return 0;
}
```

效果：

```
vm-alpine-0:~/work# ./a.out 
main is done
my_ateixt2 handler 
my_ateixt1 handler 
```

# 环境表

程序在运行的时候，会收到两张表。

一张参数表，就是在main函数的argv里。

一个就是环境表。用`extern char **environ;`来引用。

环境表的内容是键值对。

在以前老的UNIX系统里，main函数是3个参数，这样：

```
int main(int argc, char **argv, char **envp);
```

但是，ISO标准化的时候，main函数只有2个参数了。而且第三个参数确实没有必要通过参数传递进来。所以posix标准也把这个去掉了。

和环境表配套的是getenv和putenv这2个函数。另外还有一个setenv函数。

```
char *getenv(char *name);得到value
int putenv(char *item); item的形式是"aa=bb"这种样子。
int setenv(char *name, char *value, int rewrite) rewrite不是0，则会对同名的镜像覆盖。
```



当然你可以直接访问environ指针。不过直接操作数据，一向是不太妥当的，因为跳过了参数检查这一层。

内核并不管环境变量。

环境变量存放在进程空间的栈底上面（main函数的参数也放这里）。



# realloc使用场景

例如getcwd，这个函数里就用到了，这样就可以装下任意长度的路径名。



# 系统调用和库函数关系

系统调用一般是简单的实现单个功能。

库函数就是基于系统进行封装，把多个系统调用组合起来，让用户程序开发更加简单。

