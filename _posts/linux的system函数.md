---
title: linux的system函数
date: 2016-12-10 20:00:52
tags:
	- linux
---

system函数一般用来在C代码里调用系统的命令。例如system("ls")就跟在shell里输入ls是一样的效果。
这个函数使用起来是很方便，但是如果用得不好，容易出现严重问题。现在总结一下。
system函数的流程是这样：先fork，再exec，再waitpid。
调用fork产生子进程会将当前进程的数据段内容拷贝一份，这个过程可能会失败，失败的原因可能有2个：

* 系统的进程数达到规定的上限值了。errno被设置为EAGIN。EAGAIN错误码的字面含义是请稍后重试。
* 分配内存失败。errno被设置为ENOMEM。分配失败，这个可以通过`/proc/sys/vm/overcommit_memory`来设置策略。这个文件的值可以是0/1/2。0表示检查能否分配，分配不了就返回失败。1表示不限制，如果分配真正物理内存时出问题，会导致应用被系统OOM杀掉。2表示限制所有进程的虚拟地址空间的总和，比0更容易导致分配内存失败。

system函数的返回值：
* -1：fork函数失败了，就返回-1。
* 127：如果exec函数执行失败了，返回127 。
* 1：如果传递给system的参数是NULL，一般返回1 。
* 0：在exec执行命令成功后返回0。

一般父进程在产生子进程之后，可能有2种情况：一是父进程继续做别的事情，二是父进程什么都不做，一直等子进程退出。
如果是第一种情况，父进程需要注册对信号SIGCHLD的处理。可以注册为忽略。

system函数使用起来容易出错，返回值也多。返回值容易跟传递进去的command的返回值混淆。所以一般推荐用popen函数来替代。



popen的用法



参考资料

1、ENV33-C. Do not call system()

https://wiki.sei.cmu.edu/confluence/pages/viewpage.action?pageId=87152177