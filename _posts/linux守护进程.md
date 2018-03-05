---
title: linux守护进程
date: 2016-12-04 22:56:15
tags:
	- linux
---
守护进程是在系统后台运行的程序，其生存周期一般是从系统开机到关机。守护进程运行时没有控制终端可以进行交互。
要写出一个守护进程程序，需要按照下面的基本规则来写。规则如下：
```
#include <syslog.h>
#include <fcntl.h>
#include <sys/resource.h>

void daemonize(const char *cmd)
{
	int i, fd0,fd1,fd2;
	pid_t pid;
	struct sigaction sa;
	struct rlimit rl;
	//步骤1.把创建文件的mask值清零
	umask(0);
	if(getrlimit(RLIMIT_NOFILE, &rl) <0)
	{
		printf("get file limit failed \n");
		exit(1);
	}
	//步骤2.调用fork，然后让父进程退出。这样做是因为：
	//1）如果这个程序是在命令行调用的，这样可以告诉shell，我已经运行完了，退出了。
	//2）用fork得到的子进程得到的父进程的进程组ID，但是进程ID是新的。
	if((pid = fork()) < 0)
	{
		//创建进程失败
		printf("fork failed \n");
		exit(1);
	}
	else if(pid != 0)
	{
		exit(0);//父进程退出
	}
	//下面代码就是子进程代码了。
	//步骤3.调用setsid来创建一个新的会话。
	setsid();
	sa.sa_handler = SIG_IGN;
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = 0;
	if(sigaction(SIGHUP, &sa, NULL) <0)
	{
		printf("can't ignore SIGHUP \n");
		exit(1);
	}
	//再次调用fork
	if((pid = fork()) <0 )
	{
		printf("fork failed \n");
		exit(1);
	}
	else if(pid != 0)
	{
		exit(0);
	}
	//步骤4. 把当前工作目录切换到根目录。这样最保险
	if(chdir("/") < 0)
	{
		printf("chdir to / failed \n");
		exit(1);
	}
	//步骤5.关闭所有不再需要的文件描述符。
	if(rl.rlim_max == RLIM_INFINITY)
	{
		rl.rlim_max = 1024;
	}
	for(i=0; i<rl.rlim_max; i++)
	{
		close(i);
	}
	//步骤6.把0、1、2都指向null设备，这样调用的库函数即使有打印也没有效果的。
	fd0 = open("/dev/null", O_RDWR);
	fd1 = dup(0);
	fd2 = dup(0);
	
	//步骤7.初始化log文件
	openlog(cmd, LOG_CONS, LOG_DAEMON);
	
	
}
```



其实，linux已经提供了这样一个现成的函数。daemon。

```
#include <unistd.h>
int daemon(int nochdir, int noclose);
```

默认2个参数都给0，表示：工作目录设置为根目录。输入输出重定向到/dev/null。



守护进程没有终端，那么怎么来调试呢？怎么记录出错信息呢？在一个系统里，运行着很多的守护进程，所以必须有os来提供一个机制，集中处理不同守护进程的出错信息。
这个机制就是syslog。
