---
title: Linux之进程相关各种id
date: 2018-01-31 13:41:22
tags:
	- Linux

---



先从pid说起，pid是讨论的开端。

# pid

pid，进程id，在系统中有唯一性。

但是，pid是可以被回收利用的。当一个进程结束就，它的pid就空出来了。但是这个pid不会马上就分给新的进程。会冷却一下。叫做延迟复用算法。

这个可以避免被其他进程把新进程误认为是老的进程。

pid为0的，叫做调度进程。是主要负责内存换页的。是内核的一部分。

pid为1的，就是大名鼎鼎的init进程。所有用户进程的祖先。init进程一定不会终止。init进程是root权限的。init会收养所有的孤儿进程。



# uid和gid

uid，用户id。

gid，组id。

还配套了有效用户id（euid），有效组id（egid）。

一般情况下，

euid == uid

egid == gid。



```
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>

int main(void)
{
    printf(" UID\t= %d\n", getuid());
    printf(" EUID\t= %d\n", geteuid());
    printf(" GID\t= %d\n", getgid());
    printf(" EGID\t= %d\n", getegid());

    return EXIT_SUCCESS;
}
```

运行情况：

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ./a.out 
 UID    = 1000
 EUID   = 1000
 GID    = 1000
 EGID   = 1000
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ sudo ./a.out 
 UID    = 0
 EUID   = 0
 GID    = 0
 EGID   = 0
```

用sudo运行的时候，都变成root对应的了。

下面演示一下uid和euid不同的情况。

先修改一下a.out的属性。

```
chmod u+s ./a.out
```

然后用sudo来执行这个程序。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ sudo ./a.out 
 UID    = 0
 EUID   = 1000
 GID    = 0
 EGID   = 0
```

现在uid和euid就不同了。



我们看看这个特性的应用。

查看/etc/passwd文件，可以看到只有root用户对这个文件有修改权限。

```
hlxiong@hlxiong-VirtualBox:~/work/test/c-test$ ls /etc/passwd -lh
-rw-r--r-- 1 root root 3.1K 11月 21 14:54 /etc/passwd
```



但是，实际上，用户修改自己的密码是不需要sudo的。

那么是怎么做到的呢？

就是借助setuid来解决这个问题的。



参考资料

1、Linux进程的uid和euid

https://www.cnblogs.com/itech/archive/2012/04/01/2429081.html