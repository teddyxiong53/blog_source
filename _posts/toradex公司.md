---
title: toradex公司
date: 2023-04-18 19:00:31
tags:
	- 行业

---

--

toradex，中文名韬睿。

Toradex 是嵌入式硬件和软件设计的专家。 我们的产品线，包括基于Arm架构的产品，都是由我们在瑞士的工程师团队设计和开发的。

成立于2003年，员工150人左右。

一些该公司的产品和服务：

Torizon 在线服务

简化 Linux IoT 设备的开发和操作

TORIZONCORE

易于使用的工业 Linux 软件平台

感觉这个公司的文档写得很不错。可以作为学习的对象。

https://developer.toradex.com/software/toradex-embedded-software/toradex-embedded-linux-support-strategy/#Introduction



截止到我的知识截止日期（2021年），Toradex 是一家总部位于瑞士的嵌入式计算模块制造商。

该公司专注于提供高性能、低功耗的计算模块和开发板，

用于嵌入式系统、物联网（IoT）和嵌入式计算应用。

以下是一些关于 Toradex 公司的主要信息：

1. **产品范围**：Toradex 生产多种类型的计算模块，包括采用不同处理器架构的 ARM 和 x86 架构的模块。这些模块通常采用标准尺寸和接口，可轻松嵌入到自定义硬件设计中。它们通常包括处理器、内存、存储和连接性选项。此外，Toradex 还提供了相应的开发板和支持软件，以帮助开发人员快速启动嵌入式项目。

2. **支持的处理器架构**：Toradex 的计算模块支持多种处理器架构，包括 ARM Cortex-A 系列、ARM Cortex-M 系列和 x86 架构。这使得开发人员可以选择适合其特定应用需求的模块。

3. **操作系统支持**：Toradex 提供支持多种操作系统的计算模块，包括 Linux、Windows Embedded、FreeRTOS 等。这为开发人员提供了灵活性，可以选择适合其应用程序的操作系统。

4. **应用领域**：Toradex 的计算模块广泛用于各种嵌入式计算应用，包括医疗设备、工业自动化、物联网设备、嵌入式视觉系统、自动控制系统等。它们的高性能和低功耗特性使其适用于许多领域。

5. **支持和社区**：Toradex 提供了广泛的技术支持，包括开发工具、文档、示例代码和在线社区。他们的开发板通常与标准开发环境集成，以加速开发流程。

6. **总部和全球存在**：Toradex 的总部位于瑞士，但他们在全球范围内设有办事处和分销商。这使得他们的产品和服务能够覆盖全球市场。



# yocto测试

下载代码：

```
$ repo init -u git://git.toradex.com/toradex-manifest.git -b kirkstone-6.x.y -m tdxref/default.xml
$ repo sync
```

设置环境变量

```
source export
```

根据需要修改build/conf/local.conf文件。

编译

```
You can now run 'bitbake <target>'

Common targets are:
    core-image-minimal
    core-image-full-cmdline
    core-image-sato
    core-image-weston
    meta-toolchain
    meta-ide-support

You can also run generated qemu images with a command like 'runqemu qemux86-64'.

Other commonly useful commands are:
 - 'devtool' and 'recipetool' handle common recipe tasks
 - 'bitbake-layers' handles common layer tasks
 - 'oe-pkgdata-util' handles common target package tasks

Toradex targets are:
    tdx-reference-minimal-image
    tdx-reference-multimedia-image
    other (unsupported) targets may be found in
    meta-toradex-demos/recipes-images/images/
```

可以选择：

```
bitbake tdx-reference-minimal-image
```



# 参考资料

1、维基百科

https://zh.wikipedia.org/zh-cn/%E9%9F%AC%E7%9D%BF

2、官网

https://www.toradex.com/zh-cn