---
title: linux进程间通信
date: 2017-01-13 19:19:48
tags:
	- linux
	- ipc
---
最简单的进程间通信就是通过文件（可以是普通文件，也可以是设备文件）来做，一个进程写文件，另外一个进程读文件，就实现了2个进程之间的通信了。但是这样并不是最合适的方法。linux另外有提供进程间通信的机制。
这些机制有好几种，为了便于记忆，我们可以归纳点线面的。
点：信号量。
线：管道、fifo、消息队列。
面：共享内存。
一般说管道就是pipe，叫做无名管道。fifo是有名管道。
常用的就是上面罗列的这5种。现在我们按点线面的顺序一一分析。
# 1. 信号量
信号量的本质是一个计数器，用来对各个进程共享的数据进行保护。其类似作用的还有记录锁和互斥量。
相关的API有3个：semget、semctl、semop。
一般的操作步骤是下面的4步：
1. 用semget创建一个信号量。
2. 用semctl的`SETVAL`操作来初始化信号量，一般把初始值设置为1。
3. 进行信号量的PV操作。是用semop函数。
4. 如果不需要信号量了。用semctl的`IPC_RMID`来删掉。

下面给一个简单的示例。看看最基本的使用。
```
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/sem.h>

int main()
{
	int semid;
	semid = semget(1234, 1, IPC_CREAT|0666);
	printf("semid:%d \n", semid);
	return 0;
}
```
运行效果如下：
```
teddy@teddy-ubuntu:~/test/tmp$ ./a.out 
semid:0 
teddy@teddy-ubuntu:~/test/tmp$ ipcs -s

--------- 信号量数组 -----------
键        semid      拥有者  权限     nsems     
0x000004d2 0          teddy      666        1         

```
如果要删掉这个信号量，则用命令`ipcrm -s 0`（0是上面看到的semid）来删掉。
完整的示例后续再补充。

# 2. 管道
管道有比较大的局限性。它只能在有共同祖先的2个进程直接使用，一个读，一个写。
一般是在父进程和子进程之间通信用的。
pipe函数，它的作用是得到2个fd，fd[0]是读的，fd[1]是用来写的。
一个简单示例程序如下：
```
#include <unistd.h>
#include <stdlib.h>
#include <stdio.h>

int main()
{
	int fd[2];
	int ret = -1;
	ret = pipe(fd);
	if(ret < 0)
	{
		printf("pipe failed \n");
		exit(1);
	}
	int pid;
	pid = fork();
	if(pid < 0)
	{
		printf("fork failed \n");
		exit(1);
	}
	else if(pid == 0)
	{
		close(fd[1]);//child read
		char line[100];
		memset(line, 0, 100);
		int n = read(fd[0], line, 100-1);
		write(STDOUT_FILENO, line, n);
	}
	else 
	{
		//parent write
		close(fd[0]);
		write(fd[1], "hello pipe\n", 12);
	}
	return 0;
}
```
运行效果如下：
```
teddy@teddy-ubuntu:~/test/tmp$ ./a.out 
hello pipe
```
另外还有2个API，是popen和pclose。可以用来替代system函数。

# 3. FIFO

FIFO是有名管道，可以在2个不相关的进程间进行通信，这个是比无名管道好的地方。
FIFO是一种文件类型。
在看用c语言操作fifo之前，我们先看看在shell下fifo的表现，这样就有直观的认识。
```
teddy@teddy-ubuntu:~/test/tmp$ mkfifo myfifo
teddy@teddy-ubuntu:~/test/tmp$ ls -l
总用量 12
-rwxrwxr-x 1 teddy teddy 7640  1月 13 20:13 a.out
prw-rw-r-- 1 teddy teddy    0  1月 13 20:26 myfifo
-rwxrw-r-- 1 teddy teddy  516  1月 13 20:13 test.c
```
可以看到fifo是一种特殊的文件。
执行`echo xx > myfifo `，可以看到当前的shell会卡住，另外启动一个shell窗口，执行`cat myfifo`。可以看到"xx"打印出来，卡住shell也继续执行了。

不过我们产生fifo文件一般都是放在tmp目录下，放在内存文件系统里。
因为fifo是文件，所以出来产生文件要用mkfifo来做之外，其余的操作与文件操作相同。

# 4. 消息队列
消息队列的工作过程和FIFO类似，api的风格则跟信号量的类型。
api有：msgget创建、msgsend、msgrcv、msgctl。
示例后续补充。

# 5. 共享内存
共享内存是最快的ipc方式。
api风格还是system v的那个xxxget这些风格的。




