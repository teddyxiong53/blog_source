---
title: Linux命令之lsof
date: 2017-08-11 23:49:52
tags:

	- Linux命令

---

lsof表示list open files。列出打开的文件。在一个pc系统上输入这个命令，输出的内容是居多的，难以阅读。不过在嵌入式系统上，一般输出不多。可以用来定位一些格式化SD卡失败，删除文件失败等问题。



# 1. 找到某个进程打开的文件

可以先找到pid，然后用pid来查看。

```
teddy@teddy-ubuntu:~$ ps -aux | grep sshd
root      1250  0.0  0.1  10420  5528 ?        Ss   22:14   0:00 /usr/sbin/sshd -D
root      3018  0.0  0.1  13640  6348 ?        Ss   22:28   0:00 sshd: teddy [priv]  
teddy     3056  0.0  0.0  13640  3756 ?        S    22:28   0:00 sshd: teddy@pts/2   
root      3212  0.0  0.1  13640  6460 ?        Ss   23:21   0:00 sshd: teddy [priv]  
teddy     3273  0.0  0.1  13780  3936 ?        S    23:21   0:00 sshd: teddy@pts/27  
teddy     4450  0.0  0.0   5984  1932 pts/27   S+   23:52   0:00 grep --color=auto sshd
teddy@teddy-ubuntu:~$ lsof -p 1250
COMMAND  PID USER   FD      TYPE DEVICE SIZE/OFF NODE NAME
sshd    1250 root  cwd   unknown                      /proc/1250/cwd (readlink: Permission denied)
sshd    1250 root  rtd   unknown                      /proc/1250/root (readlink: Permission denied)
sshd    1250 root  txt   unknown                      /proc/1250/exe (readlink: Permission denied)
sshd    1250 root NOFD                                /proc/1250/fd (opendir: Permission denied)
```



# 2. 关于lsof的缺点和替代品

lsof不是posix标准中规定的命令。可移植性不太好。