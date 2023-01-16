---
title: Android使用termux
date: 2023-01-15 21:08:31
tags:
	- android

---



Termux的Wiki

官网中可以看到推荐的下载方式是Google Play 和F-Droid。Google Play在手机上安装太麻烦了，所以推荐F-Droid，虽然它比较慢…当然你可以离线下载Termux的apk文件，虽然这样没办法获取更新。安装果果橙比较简单，下载F-Droid，完成安装后搜索Termux，下载即可。



# 什么是termux

Termux 是运行在 Android 上的 terminal。不需要root，运行于内部存储（不在SD卡上）。


自带了一个包管理器，可以安装许多现代化的开发和系统维护工具。比如：

- neovim
- tmux
- zsh
- clang
- gcc
- weechat
- irssi



# 安装及配置

先安装apk。就谷歌搜索termux apk进行安装。

然后要配置清华的源。不然安装软件基本会失败。

```
termux-change-repo
```

然后是一个类似kernel的menuconfig的界面，选择Tsinghua的源即可。

然后id查看本机用户名。

```
id
```

我当前的uid是10426，用户名是u0_a426

然后修改密码：

```
passwd
```

这个时候提示缺少libcrypto。

```
pkg upgrade && pkg update
```

然后自动就可以了。

然后启动sshd

```
sshd
```

提示：

```
not hostkeys available
```

需要执行：

```
ssh-keygen -A
```

然后启动sshd就正常了。

然后需要允许termu访问内部存储。

```
termux-setup-storage
```

这个就跟普通app请求存储访问权限一样，会弹个窗口，允许就好了。

然后在电脑上访问即可：

```
ssh u0_a426@192.168.1.64 -p 8022
```

因为默认是用的8022端口，22端口需要root权限的。

# 安装需要的软件

首先是vim

```
pkg install vim
```



# 参考资料

1、

https://cloud.tencent.com/developer/article/1546845

2、

https://zhuanlan.zhihu.com/p/95865982

3、termux替换清华源

https://mirrors.tuna.tsinghua.edu.cn/help/termux/

4、Android终端termux玩机记录

https://juejin.cn/post/7157534195282083871

5、安卓开启ssh服务

https://blog.csdn.net/jxch____/article/details/109165515

6、

https://wiki.termux.com/wiki/Package_Management

7、Error(15) 解决 sshd: no hostkeys available -- exiting.

https://blog.csdn.net/qq_38225558/article/details/117793432