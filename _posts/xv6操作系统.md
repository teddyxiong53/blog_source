---
title: xv6操作系统
date: 2024-08-29 11:28:11
tags:
	- os

---

--

xv6是一个简单的教学用途操作系统内核。

代码简单容易理解掌握。

# 资源收集

这个是中文文档

https://github.com/ranxian/xv6-chinese

直接进目录看md文档就可以了。

https://github.com/ranxian/xv6-chinese/blob/master/content/chapter1.md

https://dihe-pku.github.io/files/xv6_5_vm.pdf

http://staff.ustc.edu.cn/~chizhang/OS/Labs/MIT-XV6-%D6%D0%CE%C4%B7%AD%D2%EB%B0%E6.pdf

# xv6 riscv版本环境搭建

代码在这里：

https://github.com/mit-pdos/xv6-riscv

需要依赖`*# riscv64-unknown-elf- or riscv64-linux-gnu-*`的工具链。

工具链在这里：

https://github.com/riscv-collab/riscv-gnu-toolchain

没有必要自己编译工具链了。

这里有定期release的编译好的工具链。

https://github.com/riscv-collab/riscv-gnu-toolchain/releases/tag/2024.08.28

我下载这个版本。

[riscv64-elf-ubuntu-20.04-gcc-nightly-2024.08.28-nightly.tar.gz](https://github.com/riscv-collab/riscv-gnu-toolchain/releases/download/2024.08.28/riscv64-elf-ubuntu-20.04-gcc-nightly-2024.08.28-nightly.tar.gz)

解压放好，把bin目录加入到PATH里。



需要这个qemu：qemu-system-riscv64

```
sudo apt install qemu-system-misc
```

但是不行。

我直接用qemu的源代码编译安装得了。

```
./configure --target-list=riscv64-softmmu
```



```
Dependency glib-2.0 found: NO found 2.56.4 but need: '>=2.66.0'
```

我改meson.build的版本要求。

但是后面编译还是报错。



# rust版本的xv6

https://github.com/Ko-oK-OS/xv6-rust