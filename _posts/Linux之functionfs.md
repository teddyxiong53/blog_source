---
title: Linux之functionfs
date: 2023-10-12 19:52:11
tags:
	- Linux

---

--

# 简介

FunctionFS（Function File System）是一个用于 Linux 内核的虚拟文件系统，

用于实现 USB 设备功能。

==FunctionFS 允许用户空间应用程序模拟 USB 设备功能，==

以便在 USB 主机和设备之间进行通信。





FunctionFS（Function Filesystem）是一个在Linux内核中引入的功能，

它允许用户空间程序通过文件系统接口与内核中运行的驱动程序进行通信。

FunctionFS允许开发者创建一个虚拟文件系统，通过文件和目录的方式向用户空间提供对设备的访问。

以下是FunctionFS的一些关键特性和用途：

1. **用户空间通信**：FunctionFS允许用户空间程序通过标准的文件系统接口（例如`read()`、`write()`等）与内核中运行的驱动程序进行通信。这使得用户空间程序能够以一种更加灵活和方便的方式与内核中的功能进行交互。

2. **设备模拟**：使用FunctionFS，开发者可以模拟一个设备，并通过文件和目录的方式向用户空间提供对该设备的访问。这使得开发者能够方便地测试和调试他们的设备驱动程序或应用程序，而无需实际的物理设备。

3. **USB设备功能**：==FunctionFS最常用于创建USB设备功能。==通过FunctionFS，开发者可以在Linux系统中实现各种USB设备功能，例如Mass Storage、MTP、Serial、以及Custom USB设备功能。

4. **嵌入式系统开发**：==FunctionFS在嵌入式系统开发中非常有用，因为它使得开发者能够方便地与内核中运行的驱动程序进行通信，而无需编写复杂的特定于硬件的驱动程序。==

总的来说，FunctionFS为Linux系统中的用户空间程序提供了一种简单而强大的方式来与内核中的驱动程序进行通信，特别适用于设备模拟和嵌入式系统开发。

# functionfs发展历史

FunctionFS的发展历史可以追溯到2008年，最初由Google工程师Greg KH提出并在Linux内核中实现。以下是FunctionFS的主要发展历程：

1. **2008年**：Greg KH最初提出FunctionFS的概念，并在Linux内核中进行了初步实现。他的目标是提供一种简单而灵活的方法，==使用户空间程序能够与内核中运行的驱动程序进行通信==，特别是在嵌入式系统和虚拟化环境中。

2. **2011年**：FunctionFS首次被合并到Linux内核主线中，作为Linux 3.1 版本的一部分。这一版本中的FunctionFS提供了基本的功能，包括文件和目录的创建、读写、以及设备模拟的支持。

3. **2012年**：随着FunctionFS的不断发展，一些新的功能和改进被陆续引入。例如，添加了对USB设备功能的更好支持，使得FunctionFS成为实现USB设备模拟的一种重要方式。

4. **2014年**：FunctionFS的发展进入了一个新的阶段，随着越来越多的开发者开始使用和贡献FunctionFS，社区中的讨论和改进也变得更加活跃。

5. **2018年**：随着嵌入式系统和物联网应用的增加，FunctionFS的重要性和影响进一步提升。它成为了许多嵌入式系统和物联网设备中实现USB设备功能的首选方式之一。

6. **2020年**：FunctionFS继续在Linux内核中得到改进和完善，以满足不断增长的需求和应用场景。社区中的开发者和用户持续致力于改进FunctionFS的性能、稳定性和功能。

总的来说，FunctionFS经过多年的发展和改进，已经成为了Linux内核中一个重要的功能，为开发者提供了一种方便、灵活和强大的方式来实现用户空间程序与内核中驱动程序之间的通信，并在嵌入式系统和物联网领域发挥着重要作用。

# functionfs的代码构成

FunctionFS的代码构成主要包括以下几个方面：

1. **内核代码**：
   - FunctionFS的核心功能是通过Linux内核中的代码实现的。这部分代码涵盖了FunctionFS的核心功能，包括文件系统接口的实现、设备模拟功能的支持、与USB子系统的集成等。
   - 内核中的FunctionFS代码通常位于`drivers/usb/gadget/function/`目录下，包括多个源文件和头文件，涵盖了FunctionFS的各个方面。

2. **用户空间工具**：
   - 为了方便开发者使用FunctionFS，通常会提供一些用户空间工具，用于创建FunctionFS的虚拟文件系统、加载驱动程序、配置设备模拟等。
   - 这些用户空间工具通常包括在Linux发行版的软件包中，例如`functionfs-utils`等。

3. **示例代码**：
   - 为了帮助开发者了解如何使用FunctionFS，通常会提供一些示例代码，展示如何创建一个简单的FunctionFS设备并与其进行通信。
   - 这些示例代码通常包括在Linux内核源码树中的`Documentation/usb/gadget_functionfs.txt`文件中，以及一些示例程序。

4. **文档和注释**：
   - 为了帮助开发者理解FunctionFS的设计和实现，通常会提供详细的文档和注释。这些文档包括在Linux内核源码树中的`Documentation/`目录下，以及源代码中的注释部分。

总的来说，FunctionFS的代码构成主要包括内核代码、用户空间工具、示例代码以及文档和注释。这些组成部分共同构成了FunctionFS的实现和使用框架，为开发者提供了一种方便、灵活和强大的方式来实现用户空间程序与内核中驱动程序之间的通信。

# functionfs使用举例

下面是一个简单的示例，展示了如何使用FunctionFS在Linux系统中模拟一个USB串口设备（USB CDC ACM）：

1. **准备工作**：
   - 确保你的Linux系统内核已经启用了FunctionFS，并且包含了USB设备功能模块（gadget）的支持。
   - 如果需要，安装FunctionFS相关的用户空间工具，例如`functionfs-utils`。

2. **创建FunctionFS设备**：
   - 首先，创建一个目录来作为FunctionFS的挂载点，例如`/mnt/functionfs`。
   - 使用`mount`命令将FunctionFS挂载到该目录，例如：
     ```
     sudo mount -t functionfs none /mnt/functionfs
     ```

3. **编写FunctionFS设备描述文件**：
   - 创建一个设备描述文件，该文件指定了FunctionFS设备的属性和功能。例如，可以创建一个名为`acm.usb`的文件，并写入以下内容：
     ```
     name = acm.usb
     functions = acm.usb
     ```

4. **编写ACM设备驱动程序**：
   - 创建一个简单的ACM设备驱动程序，该驱动程序将会在FunctionFS中运行。驱动程序通常需要实现`read()`和`write()`等文件系统接口，以模拟设备的行为。
   - 编译驱动程序并将其复制到FunctionFS的挂载点中。

5. **加载FunctionFS驱动程序**：
   - 在FunctionFS的挂载点中创建一个名为`configs/c.1`的目录，并将设备描述文件复制到该目录中。
   - 使用`mount`命令将FunctionFS驱动程序加载到USB gadget框架中，例如：
     ```
     sudo mount -t functionfs none /sys/kernel/config/usb_gadget/g1
     ```

6. **加载USB gadget驱动程序**：
   - 加载USB gadget驱动程序，例如`g_cdc`（CDC ACM功能）。
   - 在`/sys/kernel/config/usb_gadget/g1`目录下创建相应的配置文件，并加载USB gadget驱动程序。

7. **连接设备**：
   
   - 现在，你的Linux系统应该已经模拟了一个USB串口设备。将该设备连接到另一台计算机，然后在另一台计算机上使用串口终端工具（如`minicom`或`screen`）连接到该串口，即可进行数据通信。

这只是一个简单的示例，演示了如何使用FunctionFS在Linux系统中模拟一个USB串口设备。实际应用中，你可以根据需要定制FunctionFS设备和驱动程序，以实现更复杂的功能和应用场景。

# functionfs和configfs是什么关系

FunctionFS（Function Filesystem）和ConfigFS（Configuration Filesystem）都是Linux内核中的虚拟文件系统，但它们的功能和用途略有不同。

1. **FunctionFS**：
   - FunctionFS是一种虚拟文件系统，用于向用户空间程序提供对内核中运行的功能的访问。它通常用于创建模拟设备，使得用户空间程序能够与内核中的驱动程序进行通信。
   - 主要用途是创建USB设备模拟功能，例如模拟USB串口设备、USB存储设备等。通过FunctionFS，开发者可以在Linux系统中方便地模拟各种USB设备，而无需实际的物理设备。
   - FunctionFS的配置和管理通常通过ConfigFS完成。

2. **ConfigFS**：
   - ConfigFS是一种虚拟文件系统，用于在运行时配置内核中的功能和子系统。它提供了一种机制，允许用户空间程序动态地创建、配置和管理内核中的对象，例如USB gadget、USB配置、USB接口等。
   - 主要用途是在内核运行时动态配置和管理各种内核对象和功能，例如USB gadget功能、USB配置、USB接口等。ConfigFS的一个常见用途是配置USB gadget功能，包括创建USB设备、添加USB接口、配置USB描述符等。
   - FunctionFS通常用于创建模拟设备，并通过ConfigFS进行配置和管理。

因此，FunctionFS和ConfigFS之间存在着密切的关联。

==FunctionFS用于创建模拟设备，==

==而ConfigFS则用于配置和管理这些模拟设备的属性和行为。==

两者结合使用，使得开发者能够在Linux系统中方便地创建和配置各种虚拟设备，并与用户空间程序进行通信。