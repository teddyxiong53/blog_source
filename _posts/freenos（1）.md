---
title: freenos（1）
date: 2019-04-15 14:10:28
tags:
	 - cpp
---



在找c++学习代码时，看到了freenos这个项目。

这个是c++写的一个小的os内核。

可以在qemu下运行。

基于scons进行编译的。

下载代码：

```
git clone https://github.com/Neirth/FreeNOS
```

编译：

```
scons
```

不知道改怎么运行，看文档。

说是：

```
scons qemu
```

我目前运行报错。

```
scons: Building targets ...
  ISO  build/intel/pc/boot.iso
grub-mkrescue: warning: Your xorriso doesn't support `--grub2-boot-info'. Some features are disabled. Please use xorriso 1.2.9 or later..
grub-mkrescue: warning: Your xorriso doesn't support `--grub2-boot-info'. Your core image is too big. Boot as disk is disabled. Please use xorriso 1.2.9 or later..
scons: done building targets.
```

看这意思是我的xorriso版本太低了。

我看了一下，我的系统没有安装xorrios这个软件。用apt-get安装就好了。

运行，登陆名用root。没有密码。

其实用户名是可以随意写的。



这个项目的代码特点就是没有使用stl，是纯基本c++写的。

感觉写起来还是很像C的风格。



参考资料

1、FreeNOS Documentation

http://www.freenos.org/doxygen/

2、

https://centos.org/forums/viewtopic.php?t=62572