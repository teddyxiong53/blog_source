---
title: Linux之应用死机问题调试方法
date: 2018-08-13 11:11:40
tags:
	- Linux

---

--

1、如果复现时间较短，而且现象确定的，直接在板端运行gdb无疑是最简单直接的。

2、现在复现时间长，而且usb的adb不稳定。不能挂着adb跑。

板端的空间也不是很多。这样应该如何进行调试呢？

# segment fault的死机

现在可以看到死机的堆栈信息。

```
#include<stdio.h>  
#include<string.h>  
#include<stdlib.h>  
#include <signal.h>  
  
static void WidebrightSegvHandler(int signum)  
{  
    void *array[10];  
    size_t size;  
    char **strings;  
    size_t i, j;  
  
    signal(signum, SIG_DFL); /* 还原默认的信号处理handler */  
  
    size = backtrace (array, 10);  
    strings = (char **)backtrace_symbols (array, size);  
  
    fprintf(stderr, "widebright received SIGSEGV! Stack trace:\n");  
    for (i = 0; i < size; i++) {  
        fprintf(stderr, "%d %s \n",i,strings[i]);  
    }  
      
    free (strings);  
    exit(1);  
}  
  
int invalide_pointer_error(char * p)  
{  
    *p = 'd'; //让这里出现一个访问非法指针的错误  
    return 0;  
}  
  
void error_2(char * p)  
{  
    invalide_pointer_error(p);  
}  
  
void error_1(char * p)  
{  
     error_2(p);  
}  
  
void error_0(char * p)  
{  
     error_1(p);  
}  
  
int main()   
{  
    //设置 信好的处理函数  
    signal(SIGSEGV, WidebrightSegvHandler); // SIGSEGV    11       Core Invalid memory reference  
    signal(SIGABRT, WidebrightSegvHandler); // SIGABRT     6       Core Abort signal from  
      
    char *a = NULL;  
    error_0(a);  
    exit(0);  
}  
```



编译时，gcc加上-g和-rdynamic参数。

运行输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
widebright received SIGSEGV! Stack trace:
0 ./a.out() [0x40076e] 
1 /lib/x86_64-linux-gnu/libc.so.6(+0x354b0) [0x7f9d159374b0] 
2 ./a.out() [0x40081e] 
3 ./a.out() [0x400840] 
4 ./a.out() [0x40085b] 
5 ./a.out() [0x400876] 
6 ./a.out() [0x4008b3] 
7 /lib/x86_64-linux-gnu/libc.so.6(__libc_start_main+0xf0) [0x7f9d15922830] 
8 ./a.out() [0x400659] 
```

用addr2line工具来看位置。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ addr2line -e ./a.out 0x40076e
/home/hlxiong/work/test/c-test/test.c:15
```



arm上，不行。

是要加上这3个选项：

```
 arm-linux-gnueabihf-gcc -g -rdynamic test.c -rdynamic -funwind-tables -ffunction-sections 
```

# 非segment fault的死机

这种要算偏移量，然后addr2line来看。

```
虚拟地址出错的位置是5263e3，对应的开始地址是00517000，那么对应的offset地址就是5263e3 - 00517000 = f3e3，这样就可以拿这个偏移地址在代码环境里面使用.debug路径下面的bin来定位了。
```

```
addr2line -e xx offset
```

这个-e是表示后面的跟的是exe文件。

如果是so文件呢？

这样可以来定位：

```
arm-linux-gnueabihf-objdump -x --disassemble -l ./hardware/aml-4.9/npu/nanoq/nnsdk/lib/lib32/libnnsdk.so

```

## level 3 translation fault in



参考资料

1、

https://blog.csdn.net/zhenglie110/article/details/89372378



## 参考资料

1、

https://blog.csdn.net/xlnaan/article/details/121429894

2、

https://stackoverflow.com/questions/7556045/how-to-map-function-address-to-function-in-so-files

3、so 动态库崩溃问题定位（addr2line与objdump）

https://blog.csdn.net/afei__/article/details/81181827

# SegmentFault处理流程



参考资料

https://www.jianshu.com/p/6573801b6213

# 参考资料



https://blog.csdn.net/u012256258/article/details/54983326





https://blog.csdn.net/twtydgo/article/details/51578395

linux backtrace()详细使用说明，分析Segmentation fault

http://velep.com/archives/1032.html

Stacktrace arm-linux-gcc

https://stackoverflow.com/questions/10864882/stacktrace-arm-linux-gcc



https://stackoverflow.com/questions/77005/how-to-automatically-generate-a-stacktrace-when-my-gcc-c-program-crashes

ARM Linux BackTrace

https://blog.csdn.net/geniuszm2/article/details/52016102

Linux 段错误详解

https://tinylab.org/explore-linux-segmentation-fault/



