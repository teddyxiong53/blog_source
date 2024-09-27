---
title: python ctypes使用
date: 2016-10-31 20:02:57
tags:
	- python
---
# 基本介绍
ctypes是python的一个外部库，提供和C语言兼容的数据类型。从python2.3开始引入。
使用ctypes模块，能够在python代码中创建创建和使用C语言的数据类型，而且是可以跨平台使用的。
ctypes的类型命名是把C应用的类型前面加上c\_前缀，指针类型的都加上\_p的后缀，所以记忆起来也比较方便。类型如下：

```
ctypes类型             C语言类型 
c_char                 char    
c_wchar                wchar_t
c_byte                 char
c_ubyte                unsigned char
c_short                short
...
int/long/long long/float/double都类似
c_char_p               char *
c_wchar_p              wchar_t *
c_void_p               void *
```
# 调用dll库里面的函数
ctypes的一个主要用途是用来调用c语言的动态库文件。

python有一个绰号叫“胶水语言”，就在于它可以比较好地黏合其他语言的库来完成功能。

我们先产生一个dll动态库文件。

简单起见，不用visual studio来做了。

一般安装git的windows客户端的时候，会安装一个mingw。

我一般会另外在windows上安装gcc编译器。

然后gcc和mingw配合，在git bash里就可以用linux的方式来进行基本的编译了。

这样比较简单快捷。

现在我们用gcc编译生成一个dll文件，顺便测试一下是否可用。方法如下：

```
1、新建一个dlltest.c文件。
#include <stdio.h>
void dllprint()
{
	printf("c print dll \n");
}

2、编译生成dll文件。
gcc dlltest.c -shared -o dlltest.dll -Wl,--out-implib,dlltest.lib

3、新建一个main.c文件。测试dll文件的可用性。
#include <stdio.h>
void dllprint();
void main()
{
	dllprint();
	return ;
}

4、编译main.c并链接动态库。这个dlltest.lib可以改成dlltest.dll。
gcc main.c dlltest.lib -o main.exe
这样就可以了。
```
然后写一个test.py文件，内容如下：
```
from ctypes import *
testdll = windll.LoadLibrary(r'D:\work\test\dll-test\dlltest.dll')
testdll.dllprint()
```
运行这个test.py文件，就可以看到效果了。



