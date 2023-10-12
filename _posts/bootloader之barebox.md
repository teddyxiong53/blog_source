---
title: bootloader之barebox
date: 2023-10-12 14:31:31
tags:
	- bootloader

---

--

看到这里有提到使用barebox这个bootloader，之前没有用过。了解一下。

https://wiki.phytec.com/pages/viewpage.action?pageId=69501808#barebox%E4%BD%BF%E7%94%A8%E6%95%99%E7%A8%8B/Introducingbarebox-%E5%86%85%E6%A0%B8%E5%90%AF%E5%8A%A8%E5%8F%82%E6%95%B0%E4%BF%AE%E6%94%B9

# barebox和uboot比较

Barebox 和 U-Boot（Universal Boot Loader）都是用于嵌入式系统的引导加载程序，用于引导嵌入式设备的操作系统。它们有一些相似之处，但也有一些重要的区别。以下是 Barebox 和 U-Boot 的比较：

**1. 开源性：**
   - Barebox：Barebox 是一个开源项目，其源代码在 GPLv2 许可下发布。
   - U-Boot：U-Boot 也是一个开源项目，其源代码在 GPLv2 许可下发布。

**2. 软件架构：**
   - Barebox：Barebox 的软件架构相对较轻，注重最小化，专注于引导和初始化系统。
   - U-Boot：U-Boot 拥有更多功能，包括网络启动、USB 支持、多文件系统支持等。它通常更大、更强大。

**3. 定制性：**
   - Barebox：Barebox 通常更容易适应各种嵌入式平台，因为它专注于最小化和裁剪。
   - U-Boot：U-Boot 提供了更多配置选项和功能，可以更灵活地适应不同的硬件平台和需求。

**4. 启动速度：**
   - Barebox：Barebox 通常启动速度较快，因为它专注于最小化和快速启动。
   - U-Boot：U-Boot 启动时间可能较长，因为它加载了更多功能和驱动。

**5. 文件系统支持：**
   - Barebox：Barebox 支持少量的文件系统，通常较小。
   - U-Boot：U-Boot 支持更多文件系统，包括 FAT、ext2/3/4 等。

**6. 硬件支持：**
   - Barebox：Barebox 可能需要更多的硬件特定驱动程序来支持不同的平台。
   - U-Boot：U-Boot 通常拥有更广泛的硬件支持，包括各种处理器架构和嵌入式板。

**7. 社区和生态系统：**
   - Barebox：Barebox 的社区相对较小，相应的生态系统也较小。
   - U-Boot：U-Boot 有一个庞大的社区和广泛的生态系统，因此有更多的资源和支持可用。

**8. 使用场景：**
   - Barebox：Barebox 适用于对启动时间要求较高、希望最小化引导加载程序的应用，例如嵌入式控制器或某些嵌入式设备。
   - U-Boot：U-Boot 适用于需要更多功能和灵活性的应用，如嵌入式计算机、网络设备、嵌入式 Linux 设备等。

总之，Barebox 和 U-Boot 都是重要的嵌入式引导加载程序，选择哪一个取决于特定的硬件、性能和功能需求。 Barebox 适用于对启动速度和最小化要求较高的场景，而 U-Boot 适用于需要更多功能和硬件支持的应用。

# 资料

barebox命令参考文档：http://www.barebox.org/doc/latest/commands.html

barebox用户手册：http://www.barebox.org/doc/latest/user/user-manual.html

Barebox源代码：https://git.phytec.de/barebox/

barebox 设置从网络启动参考文档：[开发板从网络启动 / boot board from network](https://wiki.phytec.com/pages/viewpage.action?pageId=66489092)

