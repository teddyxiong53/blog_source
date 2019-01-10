---
title: Linux之fcntl相关操作
date: 2019-01-10 14:32:51
tags:
	- Linux
---



fcntl、flock、lockf

这3个函数都是给文件加锁，那他们之间有什么区别呢？

fcntl和flock是系统调用。

lockf是库函数。lockf是对fcntl的封装。

所以我们重点是看fcntl和flock的区别。



flock函数原型：

```
int flock(int fd, int operation);
```

operation的值：

1、LOCK_SH。共享锁。

2、LOCK_EX。排它锁。或者叫独占锁。

3、LOCK_UN。解锁。

4、LOCK_NB。非阻塞。

flock只能对整个文件上锁，而不能对文件的一部分上锁。

而fcntl可以对文件的局部上锁。

flock只能进行劝告锁（advisory lock），不能进行强制锁（mandatory lock）。

flock和fcntl的区别主要在fork和dup。



flock是跟struct file关联的，而不是fd。

这意味着，在fork或者dup复制fd后，你通过新的fd和老的fd，都可以操作这把锁。

你可以用老的fd加锁，用新的fd解锁。

你在加锁后，关闭掉其中一个fd，锁不会释放。

只有所有的fd都关闭后，锁才会释放。

flock自己单独一个头文件的。sys/file.h。

#看dup的例子

```
#include <stdio.h>
#include <unistd.h>
#include <sys/file.h>
#include <fcntl.h>

int main(int argc, char const *argv[])
{
    int fd1 = open("1.txt", O_RDWR|O_CREAT);
    int fd2 = dup(fd1);
    printf("fd1:%d, fd2:%d\n", fd1, fd2);
    int ret;
    ret = flock(fd1, LOCK_EX);
    printf("get lock1, ret:%d\n", ret);
    ret = flock(fd2, LOCK_EX);
    printf("get lock2 , ret:%d\n", ret);
    return 0;
}
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
fd1:3, fd2:4
get lock1, ret:0
get lock2 , ret:0
```

可以看到，同一个文件的多个fd，上锁不受影响。

#看看fork的情况

```
#include <stdio.h>
#include <unistd.h>
#include <sys/file.h>
#include <fcntl.h>

int main(int argc, char const *argv[])
{
    int fd = open("1.txt", O_RDWR);
    int pid;
    int ret;
    if((pid = fork())==0) {
        ret = flock(fd, LOCK_EX);
        printf("child get lock, fd:%d, ret:%d\n", fd, ret);
        sleep(5);
        printf("child exit\n");
        exit(0);

    }
    ret = flock(fd, LOCK_EX);
    printf("parent get lock, fd:%d, ret:%d\n", fd, ret);
    printf("parent exit\n");
}
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
parent get lock, fd:3, ret:0
parent exit
child get lock, fd:3, ret:0
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ child exit
```

# 对一个文件open 两次

open两次，本质上是在内核了产生了2个struct file结构体。

```
#include <stdio.h>
#include <unistd.h>
#include <sys/file.h>
#include <fcntl.h>

int main(int argc, char const *argv[])
{
    int fd1 = open("1.txt", O_RDWR);
    int fd2 = open("1.txt", O_RDWR);
    printf("fd1:%d, fd2:%d\n",fd1,fd2);
    int ret = flock(fd1, LOCK_EX);
    printf("fd1 lock, ret:%d\n", ret);
    ret = flock(fd2, LOCK_EX);
    printf("fd2 lock, ret:%d\n", ret);

}
```

运行：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
fd1:3, fd2:4
fd1 lock, ret:0

^C
```



# lockf

函数的原型是：

```
int lockf(int fd, int op, off_t size);
```

cmd的取值：unistd.h里定义。

```
#define F_ULOCK 0
#define F_LOCK  1
#define F_TLOCK 2
#define F_TEST  3
```

lockf只支持独占锁，不支持共享锁。



flock和fcntl/lockf的锁之间有什么关系？没有关系，两种锁之间没有影响。





参考资料

1、linux中fcntl()、lockf、flock的区别

http://blog.chinaunix.net/uid-28541347-id-5678998.html