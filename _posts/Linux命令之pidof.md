---
title: Linux命令之pidof
date: 2017-08-11 23:41:02
tags:

	- Linux命令

---

pidof是一个简单的命令，用来获取进程的pid。但是还是有几点值得注意的地方。

# 1. 如何获取一个脚本的pid？

加-x选项就可以了。

# 2. 多个值怎么看？

```
teddy@teddy-ubuntu:~$ pidof sshd
3273 3212 3056 3018 1250
```

如上。为什么会有这么多值呢？怎么理解？说明了有5个进程是由sshd来启动的。

依次找出来如下：

```
teddy@teddy-ubuntu:~$ ps aux | grep 3273
teddy     3273  0.0  0.1  13780  3936 ?        S    23:21   0:00 sshd: teddy@pts/27  
teddy     3494  0.0  0.0   5980  2032 pts/27   S+   23:44   0:00 grep --color=auto 3273
teddy@teddy-ubuntu:~$ ps aux | grep 3212
root      3212  0.0  0.1  13640  6460 ?        Ss   23:21   0:00 sshd: teddy [priv]  
teddy     3496  0.0  0.0   5980  1960 pts/27   S+   23:44   0:00 grep --color=auto 3212
teddy@teddy-ubuntu:~$ ps aux | grep 3056
teddy     3056  0.0  0.0  13640  3756 ?        S    22:28   0:00 sshd: teddy@pts/2   
teddy     3498  0.0  0.0   5980  2012 pts/27   S+   23:44   0:00 grep --color=auto 3056
teddy@teddy-ubuntu:~$ ps aux | grep 3018
root      3018  0.0  0.1  13640  6348 ?        Ss   22:28   0:00 sshd: teddy [priv]  
teddy@teddy-ubuntu:~$ ps aux | grep 1250
root      1250  0.0  0.1  10420  5528 ?        Ss   22:14   0:00 /usr/sbin/sshd -D
teddy     1937  0.0  0.8 125020 33976 ?        Ssl  22:15   0:00 /usr/lib/i386-linux-gnu/hud/hud-service
teddy     3505  0.0  0.0   5984  1988 pts/27   S+   23:45   0:00 grep --color=auto 1250
teddy@teddy-ubuntu:~$ 
```

加上-s选项，表示single的意思，这样就只会返回一个pid。

