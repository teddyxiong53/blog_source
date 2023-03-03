---
title: optee
date: 2023-03-03 16:43:25
tags:
	- secure

---



# 代码

获取代码

```
repo init -u https://github.com/OP-TEE/manifest.git -m default.xml --repo-url=git://codeaurora.org/tools/repo.git
```

![img](images/random_name/20170509193448025)

下载后的代码目录如图所示

该工程中各目录的作用介绍如下：

bios_qemu_tz_arm: 在qemu平台中运行tz arm的bios代码，启动最初阶段会被使用到，用来加载kernel, OP-TEE os image, rootfs并启动linux kernel和OP-TEE OS

build:这个工程的编译目录，里面包含了各种makefile文件和相关配置文件

busybox:busybox的源代码，用于制作rootfs的使用被使用到

gen_rootfs:存放制作rootfs时使用的相关脚本和配置文件

hello_work:一个示例代码，目录下包含了TA和CA部分的代码，在Linux shell端运行hello_world指令，就能调用CA接口，最终会穿到TEE中执行对应的TA部分的代码

linux:linux内核代码，在driver/tee目录下存放的是tee对应的驱动程序

optee_client:包含了CA程序调用的userspace层面的接口库的源代码。其中tee_supplicant目录中的代码会被编译成一个Binary，该binary主要的作用是，当调用CA接口，需要加载TA image时，TEE OS通过该binary从文件系统中来获取TA image，并传递給TEE OS，然后再讲TA image运行到TEE OS中。

optee_os:存放OP-TEE OS的源代码和相关文档

optee_test:opentee的测试程序xtest的源代码，主要用来测试TEE中提供的各种算法逻辑和提供的其他功能

out:编译完成之后输出目录（该目录编译完成之后才会生成）

qemu:qemu源代码

soc_term:在启动时与gnome-terminal命令一起启动终端,用于建立启动的两个terminal的端口监听，方便OP-TEE OS的log和linux kernel log分别输出到两个terminal中

toolchains:编译时需要使用的toolchain



# 参考资料

1、

https://blog.csdn.net/shuaifengyun/article/details/71499945

2、

这个作者的系列文章，非常专业。

https://blog.csdn.net/shuaifengyun/category_6909494.html

3、optee文档

https://optee.readthedocs.io/en/latest/