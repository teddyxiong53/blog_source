---
title: chroot的用途
date: 2016-12-01 21:24:13
tags:
	- linux
---
chroot的本质是把某个程序的根目录指定到某个特定路径。而这么做的目的，主要是为了安全。一般是把web server这样的程序chroot到指定路径，这样即使web server被黑客攻破，黑客也只能在这个假的根目录下打转，无法直接对服务器的整个环境带来危害。
chroot还有一个用途就在linux系统下安装另外一个linux系统。

chroot的格式
```
chroot 选项  路径名 命令
```
例如`chroot /home/teddy/test_chroot /bin/bash` 。
但是你当前执行这条语句会失败，提示没有/bin/bash。所以现在做的是，先退出来，输入exit就可以了。
把/bin/bash软件及依赖的动态库拷贝到`/home/teddy/test_chroot`先。
1. 先把目录建好。
```
export J=/home/teddy/test_root
mkdir -p $J/{bin,lib64,lib}
cd $J
```
2. 把bash和ls拷贝到我们新建的bin目录。
```
cp /bin/{bash,ls} $J/bin
```
3. 查看bash和ls依赖的库文件，并拷贝到新建的lib目录。
```
list="$(ldd /bin/bash | egrep -o '/lib.*\.[0-9]')"
for i in $list;do cp -v "$i" "${J}${i}";done

list="$(ldd /bin/ls | egrep -o '/lib.*\.[0-9]')"
for i in $list;do cp -v "$i" "${J}${i}";done
```
得到的目录结构如下：
```
teddy@teddy-ubuntu:~/test_root$ tree
.
├── bin
│   ├── bash
│   └── ls
├── lib
│   ├── i386-linux-gnu
│   │   ├── libacl.so.1
│   │   ├── libattr.so.1
│   │   ├── libc.so.6
│   │   ├── libdl.so.2
│   │   ├── libpcre.so.3
│   │   ├── libpthread.so.0
│   │   ├── libselinux.so.1
│   │   └── libtinfo.so.5
│   └── ld-linux.so.2
└── lib64
```
4. 可以执行chroot了。
```
teddy@teddy-ubuntu:~/test_root$ sudo chroot ./ /bin/bash
[sudo] teddy 的密码： 
bash-4.3# ls
bin  lib  lib64
bash-4.3# pwd
/
bash-4.3# 
bash-4.3# exit
exit
teddy@teddy-ubuntu:~/test_root$ 
```
