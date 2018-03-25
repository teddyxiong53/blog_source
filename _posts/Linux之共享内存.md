---
title: Linux之共享内存
date: 2018-03-25 21:18:33
tags:
	- Linux

---



对共享内存的操作就4个接口。

按照增删改查的模式来分：

增：shmget。相当于open一个文件的意思，返回一个id。相当于文件描述符。

删：shmdt。相当于close一个文件。

改：shmat。我open一个共享内存，我要用，怎么用？用id得到一个虚拟地址，然后用虚拟地址来操作。这个就是用来获取虚拟地址的。

查：shmctl。这个就可以进行各种控制操作。



有什么工具可以查看系统里共享内存的情况？

有。ipcs。这个名字是ipc show的意思，就是现实各种ipc的情况。

```
teddy@teddy-ubuntu:~/work/linux-rpi/linux-rpi-4.4.y$ ipcs -a

------ Message Queues --------
key        msqid      owner      perms      used-bytes   messages    

------ Shared Memory Segments --------
key        shmid      owner      perms      bytes      nattch     status      
0x00000000 131072     teddy      600        6660016    2          dest         
0x00000000 229378     teddy      600        262140     2          dest         
0x00000000 393219     teddy      600        92984      2          dest         

------ Semaphore Arrays --------
key        semid      owner      perms      nsems    
```

共享内存没有带同步机制，使用要小心一点。

