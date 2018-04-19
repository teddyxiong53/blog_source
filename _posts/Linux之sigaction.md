---
title: Linux之sigaction
date: 2018-04-18 23:05:28
tags:
	- Linux

---



一直是用signal函数来注册信号处理函数。看到现在有一个struct sigaction，看看怎么用。

既然是推出的新的接口，肯定是有signal做不到的功能。



我通过阅读musl代码，发现signal就是sigaction封装出来的简单接口。



#signal的缺点

1、signal设置的函数，只能生效一次。响应一次后，就被恢复成默认的处理了。如果要保持，就需要在signal处理函数里再次设置，这样无疑是比较麻烦的。

2、就算我们在signal处理函数里再次设置，这里有时间窗口，可能漏掉了一个信号，而默认的信号处理可能是杀掉程序，这样就无法达到我们预期的效果。

3、signal不能用了关闭信号。



# sigaction的改进

1、信号处理函数被调用的时候，系统会屏蔽一个新的本类型的信号的产生，保证当前处理完成。

2、一次设置，后面不需要再重新设置。



# 使用原则

1、一次性的，就用signal好了。

2、多次的，用sigaction。



# 接口分析

1、结构体sigaction定义在signal.h里。

```
struct sigaction {
  union {
    void (*sa_handler)(int);
    void (*sa_sigaction)(int, siginfo_t *, void *);
  } __sa_handler;
  sigset_t sa_mask;
  int sa_flags;
  void (*sa_restore)(void);
};
#define sa_handler __sa_handler.sa_handler //这2个辅助宏。
#define sa_sigaction __sa_handler.sa_sigaction
```

2、注册函数sigaction。

```
int sigaction(int sig, const struct sigaction *act, struct sigaction *oact);
```

3个参数，第一个是信号的编号。

act如果 不是NULL，就要修改动作。

oact如果不是NULL，系统通过oact指针返回该信号的是一个动作。



# 简单例子

```
#include <stdio.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>

static void int_handler(int sig)
{
    printf("catch a signal int\n");
}

int main()
{
    struct sigaction act, oact;
    act.sa_handler = int_handler;
    sigemptyset(&act.sa_mask);

    act.sa_flags = 0;
    sigaction(SIGINT, &act, &oact);
    int i;
    while(1) {
        for(i=0; i<5; i++) {
            write(1, ".", 1);
            sleep(1);
        }
    }
}
```

测试：

```
teddy@teddy-ubuntu:~/work/test/c-test$ ./a.out 
...^Ccatch a signal int
.....^Ccatch a signal int
...^Z
[1]+  Stopped  
```



# 参考资料

1、为什么使用sigaction而非signal

https://blog.csdn.net/suifengpiao_2011/article/details/51837822

2、百度百科

https://baike.baidu.com/item/sigaction/4515754?fr=aladdin