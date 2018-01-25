---
title: rt-thread（四）menuconfig里的功能
date: 2018-01-24 14:06:40
tags:
	- rt-thread

---



现在3.0.2版本，跟我之前看到1.2.1的版本，增加了很多的东西。

menuconfig之后，会在bsp/xxx目录下生成一个.config文件，并且rtconfig.h文件也会同步更新。

我选择把mqtt打开。但是，发现没有作用。

看配置里，tftp、ping应该都是打开的，但是实际上也没有。到lwip-2.0.2目录下去看。发现Sconscript根本没有包含对应的代码。我自己加上下面的代码。

```
#teddyxiong53 add code below
ping_src = Glob("src/apps/ping/*.c") 
src += ping_src
mqtt_src = Glob("src/apps/mqtt/*.c") 
src += mqtt_src
tftp_src = Glob("src/apps/tftp/*.c") 
src += tftp_src
```

这样就可以编译进来了。测试可用。

把httpd的也加入进来。

1、把代码加入编译。

```
httpd_src = Glob("src/apps/httpd/*.c") 
src += httpd_src
path += [GetCurrentDir() + '/src/apps/httpd']
```

注意，这个目录下有头文件，所以path也要加上。

2、编译。会报错。

因为httpd目录下有c文件包含c文件的情况。我们把fsdata.c改成fsdata.c.dat。这样就不会被编译两次了。

3、在rt-thread留给我们的main函数里，加上httpd_init，启动后，配置好ip，可以在浏览器里访问了。

网页内容是lwip的介绍。

# online packages 

这部分看起来很强大，但是选中后，没有看到任何效果。网上查了下。

是需要借助一个叫env的工具。但是看文档描述，都是在windows下的。先下载下来包看看。

实际上，linux上是更加容易做的。

当你执行menuconfig之后，就已经在~/.env目录下放了东西了。

```
teddy@teddy-ubuntu:~/.env$ tree -L 1
.
├── env.sh
├── local_pkgs
├── packages
└── tools
```

我们现在要加入到环境变量：

```
alias hp='http_proxy=http://localhost:8123'
PATH=$PATH:~/.env/tools/scripts
```

```
. ~/.bashrc
```

然后就到bsp/qemu-vexpress-a9目录下，执行：

```
pkgs --update
```

这个命令会根据你的.config内容打开的内容，决定要把哪些包下载下来。就在当前目录下的packages目录下放着。

然后我们在make build一下，现在就可以在rt-thread上使用MicroPython了。

退出MicroPython的方法是Ctrl+D。



