---
title: unix signal program
date: 2016-11-01 21:10:58
tags:
	- signal
---
1

信号是软件中断。

各种类unix系统的信号的个数不同，信号的名字都是SIG这3个字母开头，都是正整数的宏，定义在`<signal.h>`文件里。

可以用`kill -l`来查看系统支持的信号有哪些。

```
teddy@teddy-ubuntu:~/work/test/apue/signal$ kill -l
 1) SIGHUP       2) SIGINT       3) SIGQUIT      4) SIGILL       5) SIGTRAP
 6) SIGABRT      7) SIGBUS       8) SIGFPE       9) SIGKILL     10) SIGUSR1
11) SIGSEGV     12) SIGUSR2     13) SIGPIPE     14) SIGALRM     15) SIGTERM
16) SIGSTKFLT   17) SIGCHLD     18) SIGCONT     19) SIGSTOP     20) SIGTSTP
21) SIGTTIN     22) SIGTTOU     23) SIGURG      24) SIGXCPU     25) SIGXFSZ
26) SIGVTALRM   27) SIGPROF     28) SIGWINCH    29) SIGIO       30) SIGPWR
31) SIGSYS      34) SIGRTMIN    35) SIGRTMIN+1  36) SIGRTMIN+2  37) SIGRTMIN+3
38) SIGRTMIN+4  39) SIGRTMIN+5  40) SIGRTMIN+6  41) SIGRTMIN+7  42) SIGRTMIN+8
43) SIGRTMIN+9  44) SIGRTMIN+10 45) SIGRTMIN+11 46) SIGRTMIN+12 47) SIGRTMIN+13
48) SIGRTMIN+14 49) SIGRTMIN+15 50) SIGRTMAX-14 51) SIGRTMAX-13 52) SIGRTMAX-12
53) SIGRTMAX-11 54) SIGRTMAX-10 55) SIGRTMAX-9  56) SIGRTMAX-8  57) SIGRTMAX-7
58) SIGRTMAX-6  59) SIGRTMAX-5  60) SIGRTMAX-4  61) SIGRTMAX-3  62) SIGRTMAX-2
63) SIGRTMAX-1  64) SIGRTMAX
```
0到31号为不可靠信号。
后面的为可靠信号。



为什么叫不可靠信号？

Linux的信号机制基本上是从unix系统里继承过来的。

早起unix系统中的信号机制比较简单和原始。

后面在实践中发现一些问题。

因此把这些基于早期机制建立的信号，叫做不可靠信号。

不可靠信号的问题具体是什么？

进程每次处理信号后，将会自动把信号的处理函数设置为默认的。

如果你不希望这样的效果，那你就得自己在信号处理函数里自己手动再设置一次signal处理函数。

这个期间，信号可能会丢失。

早期的unix的不可靠信号，主要是指进程可能对信号做出错误响应，以及信号可能丢失。

Linux里的不可靠信号，不会自动把处理函数改成默认的，但是可能会丢失的问题还是存在。

既然信号是不可靠的，那么就要改进，做出一套可靠的信号出来。

但是之前的那些不可靠信号使用已经很广泛了，只能在之前的基础上扩展，而不能直接替换。

可靠信号支持排队，不会丢失。

配合可靠信号的出现，也提供了新的函数：

发送函数：sigqueue。

信号安装函数：sigaction。

信号是否可靠，只跟signal的号码有关系，跟它用什么函数进行安装和发送无关。

即使你使用sigaction来安装SIGINT，SIGINT仍然是不可靠的。



信号的发送函数有：

```
kill()、raise()、sigqueue()、alarm()、setitimer()以及abort()。
```




### 1. 哪些条件可以产生信号？
* 用户按下某些终端按键时，例如按Ctrl+C来强制停止当前程序时，就是产生了SIGINT信号。
* 硬件异常。典型的除数为0、无效的内存引用。这些错误由硬件检测到，然后通知给内核。无效内存引用是产生SIGSEGV信号。
* **程序调用kill函数可以把任意信号发射给另一个进程。**
* 用户用kill命令来杀掉一个进程时。
* 某些软件条件发生时。**典型的如网络通信上的带外数据就会产生信号（SIGURG）。**另外定时器超时产生的SIGALM。
### 2. 信号产生后，怎么处理？
有3种方法：
1. 忽略。SIGKILL和SIGSTOP这2个信号不能忽略，这是杀死一个进程的最后手段了。所以不能忽略。忽略信号的方法，把这样注册一下：`signal(SIG_USR1, SIG_IGN);`。
2. 自己处理。这样注册：`signal(SIG_USR1, my_signal_proc);`
3. 给系统默认处理。这样注册：`signal(SIG_USR1, SIG_DFL);`
### 3. 一个信号简单示例
先来一个简单程序，对信号来点直观的认识。
signal函数是用来注册信号的处理函数的。
新建一个signal.c的文件。内容如下：

```
 #include 
 #include 
 
 static void sig_usr(int signo)
 {
     if(signo == SIGUSR1)
     {
         printf("receive SIGUSR1 \n");
     }
     else if (signo == SIGUSR2)
     {
         printf("receive SIGUSR2 \n");
     }
     else
     {
         printf("receive sig:%d \n", signo);
         exit(1);
     }  
 }
 
 
 int main()
 {
     if(signal(SIGUSR1, sig_usr) == SIG_ERR)
     {
         printf("cannot catch SIGUSR1 \n");
         exit(1);
     }
     if (signal(SIGUSR2, sig_usr) == SIG_ERR)
     {
         printf("cannot catch SIGUSR2 \n");
         exit(1);
     }
     while(1)
     {
         pause();
     }
 }
```
编译并运行。
```
teddy@teddy-ubuntu:~/work/test/apue/signal$ gcc signal.c 
teddy@teddy-ubuntu:~/work/test/apue/signal$ ls
a.out  signal.c
teddy@teddy-ubuntu:~/work/test/apue/signal$ ./a.out &
[1] 15199
teddy@teddy-ubuntu:~/work/test/apue/signal$ kill -USR1 15199
teddy@teddy-ubuntu:~/work/test/apue/signal$ receive SIGUSR1 

teddy@teddy-ubuntu:~/work/test/apue/signal$ kill -USR2 15199
teddy@teddy-ubuntu:~/work/test/apue/signal$ receive SIGUSR2 

teddy@teddy-ubuntu:~/work/test/apue/signal$ kill  15199     
teddy@teddy-ubuntu:~/work/test/apue/signal$ ps
  PID TTY          TIME CMD
15115 pts/20   00:00:00 bash
15201 pts/20   00:00:00 ps
[1]+  已终止               ./a.out
teddy@teddy-ubuntu:~/work/test/apue/signal$ 
```



内核里对信号是怎样进行实现的？

内 核给一个进程发送软中断信号的方法，是在进程所在的**进程表项的信号域设置对应于该信号的位**。

这里要补充的是，如果信号发送给一个正在睡眠的进程，那么要看 该进程进入睡眠的优先级，如果进程睡眠在可被中断的优先级上，则唤醒进程；否则仅设置进程表中信号域相应的位，而不唤醒进程。

这一点比较重要，因为进程检 查是否收到信号的时机是：一个进程在即将从内核态返回到用户态时；或者，在一个进程要进入或离开一个适当的低调度优先级睡眠状态时。 



参考资料

1、linux内核剖析（九）进程间通信之-信号signal

https://www.cnblogs.com/alantu2018/p/8991365.html

2、Linux 信号/软中断signal处理机制

https://blog.csdn.net/g1036583997/article/details/44935515