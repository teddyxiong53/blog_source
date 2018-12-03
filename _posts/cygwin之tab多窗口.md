---
title: cygwin之tab多窗口
date: 2018-12-03 14:45:13
tags:
	- cygwin

---

```
git clone https://github.com/juho-p/fatty.git 
cd fatty 
make 
cp src/fatty.exe /bin
```

我的编译会出现错误：

```
child.h:4:25: fatal error: sys/termios.h: No such file or directory
 #include <sys/termios.h>
                         ^
compilation terminated.
'res.o' -> 'build/res.o'
'res.d' -> 'build/res.d'
make[1]: *** [Makefile:46：build/winxx.o] 错误 1
make[1]: 离开目录“/home/Administrator/tools/fatty/src”
make: *** [Makefile:2：exe] 错误 2
```

其实是有这个文件的。

知道了，gcc是没有问题的，是g++有问题。

我强行加上-I/usr/include目录也不行。

```
g++ -DTARGET=i686-pc-cygwin -D_GNU_SOURCE -DNDEBUG -Wall -Wextra -std=gnu++11 -I/usr/include -Os -c childxx.cc -o build/childxx.o -MMD -MT build/childxx.o
In file included from win.hh:15:0,
                 from childxx.cc:1:
child.h:4:25: fatal error: sys/termios.h: No such file or directory
 #include <sys/termios.h>
```

网上找了一下，发现问题的症结所在了。

因为我的g++执行了mingw里的了。

```
Administrator@doss ~/work/test
$ which g++
/cygdrive/c/MinGW/bin/g++
```

根本原因还是我的cygwin没有安装g++。

可以这样来安装。

```
./setup-x86.exe -q -P wget -P gcc-g++ -P make -P diffutils -P libmpfr-devel -P libgmp-devel -P libmpc-devel 
```

过程如下：

```
D:\tools\cygwin_install
λ  ./setup-x86.exe -q -P wget -P gcc-g++ -P make -P diffutils -P libmpfr-devel -P libgmp-devel -P libmpc-devel
D:\tools\cygwin_install
λ  Starting cygwin install, version 2.893
User has backup/restore rights
Current Directory: d:\cygwin_down_32
Could not open service McShield for query, start and stop. McAfee may not be installed, or we don't have access.
root: d:\cygwin system
Selected local directory: d:\cygwin_down_32
net: Proxy
site: http://cygwin.mirror.constant.com/
solving: 4 tasks, update: no, use test packages: no
Augmented Transaction List:
   0 install                                         gcc-g++             7.3.0-3
   1 install                                            mpfr          4.0.1-4p11
   2 install                                      pkg-config            0.29.1-1
   3 install                                       libgmpxx4             6.1.2-1
   4 install                                    libmpc-devel             1.1.0-1
   5 install                                             gmp             6.1.2-1
   6 install                                    libgmp-devel             6.1.2-1
   7 install                                   libmpfr-devel          4.0.1-4p11
Augmented Transaction List:
   0 install                                         gcc-g++             7.3.0-3
   1 install                                            mpfr          4.0.1-4p11
   2 install                                      pkg-config            0.29.1-1
   3 install                                       libgmpxx4             6.1.2-1
   4 install                                    libmpc-devel             1.1.0-1
   5 install                                             gmp             6.1.2-1
   6 install                                    libgmp-devel             6.1.2-1
   7 install                                   libmpfr-devel          4.0.1-4p11
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gcc/gcc-g++/gcc-g++-7.3.0-3.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/mpfr/mpfr-4.0.1-4p11.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/pkg-config/pkg-config-0.29.1-1.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gmp/libgmpxx4/libgmpxx4-6.1.2-1.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/mpclib/libmpc-devel/libmpc-devel-1.1.0-1.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gmp/gmp-6.1.2-1.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gmp/libgmp-devel/libgmp-devel-6.1.2-1.tar.xz
Downloaded d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/mpfr/libmpfr-devel/libmpfr-devel-4.0.1-4p11.tar.xz
Extracting from file://d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gcc/gcc-g++/gcc-g++-7.3.0-3.tar.xz
Extracting from file://d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/pkg-config/pkg-config-0.29.1-1.tar.xz
Extracting from file://d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gmp/libgmpxx4/libgmpxx4-6.1.2-1.tar.xz
Extracting from file://d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/mpclib/libmpc-devel/libmpc-devel-1.1.0-1.tar.xz
Extracting from file://d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/gmp/libgmp-devel/libgmp-devel-6.1.2-1.tar.xz
Extracting from file://d:\cygwin_down_32/http%3a%2f%2fcygwin.mirror.constant.com%2f/x86/release/mpfr/libmpfr-devel/libmpfr-devel-4.0.1-4p11.tar.xz
Changing gid back to original
running: d:\cygwin\bin\dash.exe "/etc/postinstall/0p_000_autorebase.dash"
running: d:\cygwin\bin\dash.exe "/etc/postinstall/0p_update-info-dir.dash"
Changing gid to Administrators
Ending cygwin install

D:\tools\cygwin_install
```



然后是设置fatty.exe。

```
# vi ~/.bashrc
# Some shortcuts for different directory listings
alias ls='ls -hF --color=tty'                 # classify files in colour
alias dir='ls --color=auto --format=vertical'
alias vdir='ls --color=auto --format=long'
alias ll='ls -l'                              # long list
alias la='ls -A'                              # all but . and ..
alias l='ls -CF'                              #
```

但是有个问题，就是中文会乱码。



参考资料

1、cygwin 多 tab 窗口页面

https://blog.csdn.net/ubuntu64fan/article/details/80520699