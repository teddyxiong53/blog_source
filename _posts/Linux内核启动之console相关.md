---
title: Linux内核启动之console相关
date: 2019-12-11 14:18:38
tags:
	- Linux

---

1

在start_kernel里，有调用一个console_init。

在drivers/char/tty_io.c里。

tty

tty是teletypes的意思。它是最早出现的一种终端设备。

类似于电传打字机。由teletype公司生产。

最初tty是指连接到unix系统上的物理或者虚拟终端。

终端是一种字符设备。

随着时间的推移，当可以通过串口建立起终端连接后，tty也被用来指任何的串口设备。



终端和控制台，都是出现的大型机上的概念，大型机会多人共用。



个人电脑只有控制台，没有终端。



Linux是按照posix标准，把个人计算机当成小型机来用的。

在控制台上，通过getty程序虚拟了6个字符哑终端。tty1到tty6 。和一个图形终端。



系统控制台/dev/console



当前控制台/dev/tty



虚拟控制台 /dev/ttyn



看一下busybox里的getty做了些什么。



getty就是弹出一个名字让你输入用户，然后用拿到的名字去执行login。

login的时候，会执行登陆脚本，设置一下环境变量。

```
/dev # cat /proc/devices 
Character devices:       
  1 mem                  
  4 ttyS                 
  5 /dev/tty             
  5 /dev/console         
  5 /dev/ptmx            
```

tty和console是什么关系？

```
/dev # ls console tty -lh                                        
crw-------    1 root     root        5,   1 Jan  1  1970 console 
crw-rw-rw-    1 root     tty         5,   0 Jan  1  1970 tty     
```

主设备号都是5，次设备号不同。



```
/dev # echo "123" > /dev/tty       
123                                
/dev # echo "123" > /dev/console   
/dev #                             
```



串口终端ttyS0

如果你`echo "123" > /dev/ttyS0`，通过ttyS0连接到系统的用户，就会收到这个123 。

控制终端tty

如果当前进程有控制终端的话，可以用ps -ax 查看进程与哪个终端连接的。

输入tty命令，可以看你当前的登陆tty是哪个。

```
hlxiong@hlxiong-VirtualBox:~/work2$ tty
/dev/pts/0
```

控制台终端 ttyn、console。

在Linux系统里，显示器被称为控制台终端。

```
/proc/tty # cat drivers                                           
/dev/tty             /dev/tty        5       0 system:/dev/tty    
/dev/console         /dev/console    5       1 system:console     
/dev/ptmx            /dev/ptmx       5       2 system             
rfcomm               /dev/rfcomm   216 0-255 serial               
serial               /dev/ttyS       4 64-68 serial               
pty_slave            /dev/pts      136 0-1048575 pty:slave        
pty_master           /dev/ptm      128 0-1048575 pty:master       
fiq-debugger         /dev/ttyFIQ   254       0 serial             
```



参考资料

1、对于Linux内核tty设备的一点理解

https://www.cnblogs.com/listenerln/p/6780570.html

2、LINUX下的tty，console与串口分析

https://www.cnblogs.com/lidabo/p/5390918.html