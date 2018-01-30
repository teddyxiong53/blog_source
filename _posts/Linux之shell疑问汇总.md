---
title: Linux之shell疑问汇总
date: 2018-01-20 10:28:47
tags:
	- Linux
	- shell

---



这篇文章主要把自己在阅读shell脚本中碰到的疑问记录下来，以备查阅。

# `2>&1`是什么意思

在有些脚本里，会有`which docker > /dev/null 2>&1`这种用法。代表的具体内涵是什么呢？

0/1/2分别代表了stdin、stdout、stderr。这个是知道的。

我们先看看一条命令在命令行上执行时的输出情况。

以普通用户执行：find /etc -name passwd

这条命令会有正确输出和错误信息的。

如下：

```
teddy@teddy-ubuntu:~/work/test$ find /etc -name passwd
find: ‘/etc/polkit-1/localauthority’: Permission denied
find: ‘/etc/vmware-tools/GuestProxyData/trusted’: Permission denied
/etc/passwd
find: ‘/etc/docker’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
find: ‘/etc/ssl/private’: Permission denied
/etc/pam.d/passwd
/etc/cron.daily/passwd
```

可以看到，默认stdout和stderr都是输出到屏幕上的。我们现在就把stdout和stderr分开看看。

```
find /etc -name passwd > find.out 2>find.err
```

我们看find.out有什么内容：

```
teddy@teddy-ubuntu:~/work/test$ cat find.out
/etc/passwd
/etc/pam.d/passwd
/etc/cron.daily/passwd

```

find.err内容：

```
teddy@teddy-ubuntu:~/work/test$ cat find.err
find: ‘/etc/polkit-1/localauthority’: Permission denied
find: ‘/etc/vmware-tools/GuestProxyData/trusted’: Permission denied
find: ‘/etc/docker’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
find: ‘/etc/ssl/private’: Permission denied

```

可以用一个`&`来表示1和2。

例如：

```
teddy@teddy-ubuntu:~/work/test$ find /etc/ -name passwd &>find.all
teddy@teddy-ubuntu:~/work/test$ cat find.all
find: ‘/etc/polkit-1/localauthority’: Permission denied
find: ‘/etc/vmware-tools/GuestProxyData/trusted’: Permission denied
/etc/passwd
find: ‘/etc/docker’: Permission denied
find: ‘/etc/cups/ssl’: Permission denied
find: ‘/etc/ssl/private’: Permission denied
/etc/pam.d/passwd
/etc/cron.daily/passwd
teddy@teddy-ubuntu:~/work/test$ 
```

有时候是希望把stderr重定向到跟stdout一样的地方。按照自然的写法是2>1，但是这个实际上会是重定向到一个名字叫`1`的文件里去了。所以需要加一个`&`来表示。就是`2>&1`了。

`which docker > /dev/null 2>&1`这句的完整含义，就是stdout不输出，stderr也不输出。

# `[`的知识

`[`的作用相当于test命令。

有个选项，-a表示与的关系。例如`[ "$xxx=a" -a "$yyy=b" ]`。表示这2个条件同时为真。

```
teddy@teddy-ubuntu:~$ [ "$xxx" = "a" ]
teddy@teddy-ubuntu:~$ echo $?
1
teddy@teddy-ubuntu:~$ xxx=a
teddy@teddy-ubuntu:~$ [ "$xxx" = "a" ]
teddy@teddy-ubuntu:~$ echo $?
0
teddy@teddy-ubuntu:~$ 
```

# 用`.`执行和直接执行脚本的区别

用点来执行是使得脚本内容在当前shell里执行，而不是另外开一个shell来执行。

这个带来的一个好处就是环境变量都可以访问到。

一个典型用途，就是让脚本直接可以进行包含。

新建一个inc.sh和一个test.sh。

inc.sh：

```
#!/bin/sh 

xxx=a
echo "abc"

```

test.sh：

```
#!/bin/sh
. ./inc.sh
echo $xxx

```

在test.sh里可以访问到inc.sh里定义的变量。这就是最大的好处。

用`.`执行时的参数情况和直接执行的也不同。

test.sh内容：

```
#!/bin/sh
echo "0:$0" 
echo "1:$1"
```

直接执行：

```
teddy@teddy-ubuntu:~/work/test/shell$ ./test.sh aa
0:./test.sh
1:aa
```

用`.`执行：

```
teddy@teddy-ubuntu:~/work/test/shell$ . ./test.sh aa
0:-bash
1:aa
```

感觉用点执行的效果就像是把脚本内容一条条扒出来在命令行上敲是一样的效果。



# su和su -的区别

su -会把环境变量也带过去。相当于以root用户登录一样。



# printf和echo区别

1、printf的用法跟c语言中的很类似，可以格式化打印。

2、printf打印后，不会自动换行的。

