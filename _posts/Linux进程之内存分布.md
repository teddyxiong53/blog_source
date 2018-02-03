---
title: Linux进程之内存分布
date: 2018-02-03 12:08:31
tags:
	- Linux进程

---



很多书上多是以x86为例讲解linux进程的内存分布情况的，是从0x08048000这个位置开始的。具体分布情况也有经典图表来说明。

那么arm上的是什么情况？

我们可以自己写一个简单的程序来打印出各个部分的情况。

showmem.c

```
#include <sys/types.h>
#include <sys/shm.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE  0x100
#define MALLOC_SIZE  0x200
#define SHM_SIZE 0x1000
#define SHM_MODE (SHM_R| SHM_W)


int init_global_var = 1; //for data section
char array[ARRAY_SIZE];//for bss section

int main(void)
{
	int shmid;
	char *ptr;
	printf("The address of main function: %p \n", main);
	printf("The address of data section:%p \n", &init_global_var);
	printf("The address of bss section:%p \n", array);
	
	ptr = malloc(MALLOC_SIZE);
	if(!ptr)
	{
		printf("malloc failed \n");
		exit(-1);
	}
	printf("The address of heap: %p \n", ptr);
	
	shmid = shmget(IPC_PRIVATE, SHM_SIZE, SHM_MODE);
	if(shmid < 0)
	{
		printf("shmget failed \n");
		exit(-1);
	}
	char *shmptr = shmat(shmid, 0 , 0);
	if(!shmptr)
	{
		printf("shmat failed\n");
		exit(-1);
	}
	printf("The address of shm:%p \n", shmptr);
	if(shmctl(shmid, IPC_RMID, 0) < 0)
	{
		printf("shmctl IPC_RMID failed \n");
		exit(-1);
	}
	return 0;
	
}
```

在树莓派上的执行情况是这样的：

```
The address of main function: 0x10550 
The address of data section:0x20928 
The address of bss section:0x20930 
The address of heap: 0x12b4008 
The address of shm:0x76fb5000 
```

text段在0x10000这个位置附近。

data段在0x20000这个附近。

heap在0x1200000这个位置附近。

shm在0x7600 0000这个位置附近。

我们把这段代码在x86上运行一下看看。我是在32位的alpine系统上运行的。

```
The address of main function: 0x12def6c0 
The address of data section:0x12df1004 
The address of bss section:0x12df1040 
The address of heap: 0x4c9732b0 
The address of shm:0x4c8e7000 
```

上面的信息打印其实还不够细致。我们可以细化一下。

showmem2.c

```
#include <sys/types.h>
#include <sys/shm.h>
#include <stdio.h>
#include <stdlib.h>

#define ARRAY_SIZE  0x100
#define MALLOC_SIZE  0x200
#define SHM_SIZE 0x1000
#define SHM_MODE (SHM_R| SHM_W)

extern char _start, __data_start, __bss_start, etext, edata, end;
extern char **environ;

int init_global_var = 1; //for data section
char array[ARRAY_SIZE];//for bss section

int main(int argc, char **argv)
{
	int shmid;
	char *ptr;
	
	printf("mem map: \n");
	printf(".text:\t%p -> %p \n", &_start, &etext);
	printf(".data:\t%p -> %p \n", &__data_start, &edata);
	printf(".bss:\t%p -> %p \n", &__bss_start, &end);
	
	printf("stack:\t%p(local variable)\n", &shmid);
	printf("arg:\t%p \n",argv);
	printf("env: \t%p \n", environ);
	
	printf("The address of main function: %p \n", main);
	printf("The address of data section:%p \n", &init_global_var);
	printf("The address of bss section:%p \n", array);
	
	ptr = malloc(MALLOC_SIZE);
	if(!ptr)
	{
		printf("malloc failed \n");
		exit(-1);
	}
	printf("The address of heap: %p \n", ptr);
	
	shmid = shmget(IPC_PRIVATE, SHM_SIZE, SHM_MODE);
	if(shmid < 0)
	{
		printf("shmget failed \n");
		exit(-1);
	}
	char *shmptr = shmat(shmid, 0 , 0);
	if(!shmptr)
	{
		printf("shmat failed\n");
		exit(-1);
	}
	printf("The address of shm:%p \n", shmptr);
	if(shmctl(shmid, IPC_RMID, 0) < 0)
	{
		printf("shmctl IPC_RMID failed \n");
		exit(-1);
	}
	return 0;
	
}
```

树莓派上的打印输出：

```
pi@raspberrypi:~/work/test/mem$ ./a.out 
mem map: 
.text:  0x10478 -> 0x10810 
.data:  0x20aac -> 0x20ab8 
.bss:   0x20ab8 -> 0x20bc0 
stack:  0x7e86452c(local variable)
arg:    0x7e864694 
env:    0x7e86469c 
The address of main function: 0x105ac 
The address of data section:0x20ab4 
The address of bss section:0x20ac0 
The address of heap: 0x1b25008
```

上面的代码在alpine上编译不过。

