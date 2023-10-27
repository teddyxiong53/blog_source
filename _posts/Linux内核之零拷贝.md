---
title: Linux内核之零拷贝
date: 2019-12-03 09:28:32
tags:
	- Linux

---

--

# mmap

用mmap替代read函数，可以把os拷贝数据的次数减少一半。

当要传输的数据量很大的时候，这样做可以明显提高效率。

但是mmap存在潜在的问题。

```
1、mmap了一个文件后，执行write。
2、但是这个时候，另外一个进程截断了这个文件。
3、这时候的write会触发SIGBUS，这个信号会导致当前进程被杀死。
```

解决这个问题，有两种方法：

```
1、自己处理SIGBUS信号。这种可能会掩盖真实的错误。
2、使用文件锁来处理。
```

mmap是posix兼容的。

但是使用mmap不一定能够获得理想的数据传输性能。

数据传输过程中，仍然需要一次cpu拷贝操作。

而且mmap也是一个开销很大的虚拟内存操作。

这种操作需要通过更改页表和flush TLB来维持存储的一致性。

只有在数据量很大的时候，mmap才有优势。

# sendfile

为了简化用户接口，同时还要继续保留mmap和write的优点：减少cpu拷贝的次数。

Linux在2.1版本引入了一个新的系统调用：sendfile。

sendfile不仅减少了数据拷贝操作，也减少了上下文切换。

sendfile的数据，没有进入到用户空间，直接从文件系统跑到socket的缓冲区。

所以sendfile的局限性就很明显：

1、只适用于app不需要修改数据的情况。这个主要是web服务器，发送文件。

​	据说最初Linux引入sendfile这个syscall，就是因为apache服务器有这个需求。

2、sendfile仍然有一次从文件到socket缓冲区的cpu拷贝操作，这就导致page cache有可能被传输的数据污染。



上面的sendfile，还是有一次拷贝行为，距离我们的目标零拷贝还差一步。

这个需要硬件上进行支持。

网卡支持DMA scatter gather，就可以不需要这一次拷贝。



# splice

这个词的含义是粘接。

splice可以理解成一种管道。

函数原型：

```
ssize_t splice(int fd_in, loff_t *off_in, int fd_out,
                      loff_t *off_out, size_t len, unsigned int flags);
```

需要2个fd，一个输出，一个输出。

在Linux2.6.23中，sendfile的原始实现已经没有了。接口还保留着，但是其实是封装了splice的新的实现。



零拷贝的分类：

```
1、直接io。
	app直接访问硬件。
2、数据传输不经过user space。
	mmap、sendfile、splice都是这种。
3、copy-on-write。
	
```

tee函数原型：

```
ssize_t tee(int fd_in, int fd_out, size_t len, unsigned int flags);
```

splice和tee的使用示例：

```
#define _GNU_SOURCE //必须定义这个宏，不然编译会提示有些宏找不到。
/*splice()和tee()实现将文件"./1.txt"同时拷贝到文件"./2.txt"和"./3.txt"中*/
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

int main(){
    int fd1 = open("./1.txt", O_RDONLY);
    int fd2 = open("./2.txt", O_RDWR| O_CREAT | O_TRUNC, 0666);
    int fd3 = open("./3.txt", O_RDWR| O_CREAT | O_TRUNC, 0666);

    /*用于向"./2.txt"输入数据*/
    int pipefd2[2];
    /*用于向"./3.txt"输入数据*/
    int pipefd3[2];
    pipe(pipefd2);
    pipe(pipefd3);

    /*将fd1文件的内容输入管道pipefd2中*/
    splice(fd1, NULL, pipefd2[1], NULL, 10086, SPLICE_F_MORE);
    /*将管道pipefd2的内容复制到管道pipefd3中，不消耗管道pipefd2上的数据，管道pipefd2上的数据可以用于后续操作*/
    tee(pipefd2[0], pipefd3[1], 10086, SPLICE_F_NONBLOCK);
    /*将管道pipefd2的内容写入fd2文件中*/
    splice(pipefd2[0], NULL, fd2, NULL, 10086, SPLICE_F_MORE);
    /*将管道pipefd3的内容写入fd3文件中*/
    splice(pipefd3[0], NULL, fd3, NULL, 10086, SPLICE_F_MORE);

    close(fd1);
    close(fd2);
    close(fd3);
    close(pipefd2[0]);
    close(pipefd2[1]);
    close(pipefd3[0]);
    close(pipefd3[1]);
    return 0;
}
```



# 参考资料

1、Linux的零拷贝技术(zero-copy)

https://blog.csdn.net/zuijinhaoma8/article/details/47858223/

2、剖析linux下的零拷贝技术（zero-copy）

https://blog.csdn.net/z_ryan/article/details/79604192

