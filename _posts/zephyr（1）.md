---
title: zephyr（1）
date: 2023-08-24 16:38:33
tags:
	- rtos

---

--

之前没有太留意这个系统。但是现在已经比较成气候了。

给人的感觉就是非常接近Linux kernel的代码风格。

写得还是很严谨的。

相关配置工具都写得很全面，值得学习研究一下。

# 快评

1. Zephyr的内核模式是宏内核，不是微内核；设备驱动都被集成在内核中；内核编译采用Kconfig脚本配置，资源配置也通过它在编译时指定
2. Zephyr支持的平台：arm、x86、RISC-v、ARC、NIOS 2、POSIX等
3. ARM平台支持不完全：只支持arm 32系列的m/r平台，a平台不支持；同时，也不支持arm64
4. Zephyr支持100多种嵌入式开发平台，嵌入式友好；内核size可以小至8kB
5. Zephyr只有[mpu](https://en.wikipedia.org/wiki/Memory_protection_unit)（内存保护单元）的支持，任务之间的内存是相互隔离的，但不支持虚拟内存；多个用户应用同时运行有一定的困难，目前仅支持单应用的形式



**Zephyr采用的是标准的宏内核的架构**，这对于它面向MCU进行开发是有利的。如果采用微内核的话，需要有稳健的IPC机制，不仅执行效率上有所降低，并且需要更多的代码量。

当前的Zephyr代码结构和Linux十分相似。它有一个架构无关的通用的内核逻辑部分（Kernel目录），架构相关的实现被分离到不同的目录中去了（arch目录），基础的总线和外设的驱动也独立实现（driver目录），并在编译的时候集成在内核中。此外，一些重要的基础能力包括文件系统的支持、网络连接的支持，也是要在编译的时候和内核集成在一起的（ext目录）。



除了有较多的平台支持外，**Zephyr更大的能力体现在驱动栈的成熟**。它对于嵌入式常用的总线如I2C、I2S、GPIO、CAN甚至x86平台上的PCI等全都支持，支持fat32、nffs这两个轻量文件系统，有完整的USB驱动栈，完整的网络驱动栈，对包括WIFI、Zigbee、蓝牙等在内的无线连接也全部支持，它对于audio和显示也有一定的支持。这使得嵌入式系统可以通过它进行快速的开发。



先看三个Zephyr的系统特性：

1. Zephyr有内存保护，但不支持虚拟内存，亦即只做到MPU的支持，没有做到MMU的支持；
2. 支持多线程，不同的线程可以使用独有的内存区域；
3. 用户程序的入口地址是全局唯一的main函数。

从上述这3个基本事实出发，同时结合它的众多的sample示例，我们知道Zephyr是一个单应用的操作系统。全局唯一的main函数是用户应用的入口地址，这从设计上就不允许两个独立应用同时存在。但这个应用内部可以创建多个线程。

应用通过ymal文件进行配置，通过它来指定应用的描述信息，配置依赖信息。如果要支持多应用，可以通过一些简单的改造来快速实现。主要的思路是：

1. 通过一个通用的init任务对用户空间进行初始化，内核完成初始任务后，将执行权交给init；
2. 实现一种用户交互的方式，比如串口方式的terminal shell，以支持用户操作；
3. 或者不实现2，而通过静态的用户配置文件，由init进程启动指定的用户进程。

# linux下编译运行

需要这些依赖：

```
sudo apt-get install --no-install-recommends git cmake ninja-build gperf \
  ccache dfu-util device-tree-compiler wget \
  python3-dev python3-pip python3-setuptools python3-tk python3-wheel xz-utils file libpython3.8-dev \
  make gcc gcc-multilib g++-multilib libsdl2-dev libmagic1
```



从这个地址来下载：

https://github.com/zephyrproject-rtos/sdk-ng/releases/tag/v0.16.1

先看看这些东西的分类逻辑是什么。

```
wget https://github.com/zephyrproject-rtos/sdk-ng/releases/download/v0.16.1/zephyr-sdk-0.16.1_linux-x86_64.tar.xz
```

这个压缩包有1G大。
解压后，执行里面的setup.sh脚本即可。

安装时的打印：

```
Zephyr SDK 0.16.1 Setup

** NOTE **
You only need to run this script once after extracting the Zephyr SDK
distribution bundle archive.

Install host tools [y/n]? y
Register Zephyr SDK CMake package [y/n]? y

Installing host tools ...

Registering Zephyr SDK CMake package ...
Zephyr-sdk (/home/amlogic/work/zephyr-sdk-0.16.1/cmake)
has been added to the user package registry in:
~/.cmake/packages/Zephyr-sdk
```

这个解压后，就是一堆各种工具链。

然后参考这里来进行编译测试：

https://zephyr-doc.readthedocs.io/zh_CN/latest/getting_started/getting_started.html#id4

```
export ZEPHYR_GCC_VARIANT=zephyr
export ZEPHYR_SDK_INSTALL_DIR=~/work/zephyr-sdk-0.16.1
```

从这里下载代码：

https://github.com/zephyrproject-rtos/zephyr

这个代码提交也已经不小了。

```
pip3 install --user -U west
```

是用west这个工具来实现代码下载和包管理。

https://blog.csdn.net/wanyisq/article/details/119850694

```
echo 'export PATH=~/.local/bin:"$PATH"' >> ~/.bash_profile
source ~/.bash_profile
```

下面这个地址用gitee的，所以速度还很快的。

```
west init ./zephyr-prj  -m https://gitee.com/zephyr-rots/zephyr --mr v3.0.0
```



```
west build -b native_sim samples/hello_world
```



```
west build -b arduino_due samples/hello_world
```

还是构造不成功。

因为需要安装这些依赖：

```
pip3 install --user -r ./scripts/requirements.txt
```

安装失败，但是报错是elftools没有。那我单独安装：

```
 pip3 install pyelftools -U
```

现在编译x86的：

```
 west build -p auto -b qemu_x86 samples/hello_world
```

可以编译通过：

```
 west build -p auto -b qemu_x86 samples/hello_world
[111/125] Linking C executable zephyr/zephyr_pre0.elf

[115/125] Linking C executable zephyr/zephyr_pre1.elf

[125/125] Linking C executable zephyr/zephyr.elf
Memory region         Used Size  Region Size  %age Used
             RAM:       53280 B         3 MB      1.69%
        IDT_LIST:          0 GB         2 KB      0.00%
```

运行：

```
west build -t run
```

运行结果：

```
west build -t run
-- west build: running target run
[0/1] To exit from QEMU enter: 'CTRL+a, x'[QEMU] CPU: qemu32,+nx,+pae
SeaBIOS (version zephyr-v1.0.0-0-g31d4e0e-dirty-20200714_234759-fv-az50-zephyr)
Booting from ROM..*** Booting Zephyr OS build zephyr-v3.0.0  ***
Hello World! qemu_x86
```

https://blog.csdn.net/u013463707/article/details/121682590

# west构造工具

可以理解为aosp的repo工具类似的东西。

`west` 是一个用于管理Zephyr项目和构建的命令行工具，它提供了一种方便的方式来配置、构建和管理Zephyr嵌入式应用程序。以下是一些关于`west`构造工具的重要信息：

1. **安装 West**：您可以通过pip（Python包管理器）来安装`west`。在终端中运行以下命令以安装`west`：

   ```bash
   pip install west
   ```

2. **West初始化**：要开始使用`west`，您需要在您的Zephyr项目根目录中运行以下命令来初始化`west`：

   ```bash
   west init -l <url_to_zephyr_repository>
   ```

   `<url_to_zephyr_repository>` 是指向Zephyr代码仓库的URL，通常是Zephyr的GitHub仓库地址。

3. **West更新**：运行以下命令可以更新`west`工具以获取最新版本：

   ```bash
   west update
   ```

4. **构建Zephyr应用程序**：使用`west`构建Zephyr应用程序非常简单。在项目根目录中，运行以下命令：

   ```bash
   west build -b <board_name> <app_directory>
   ```

   - `<board_name>` 是您要构建的目标开发板的名称。
   - `<app_directory>` 是您的应用程序代码的目录路径。

   例如，要构建一个名为`my_app`的应用程序，可以运行：

   ```bash
   west build -b my_board my_app
   ```

5. **其他`west`命令**：`west`提供了其他一些有用的命令，例如创建新的Zephyr应用程序、列出可用的开发板、配置应用程序选项、进行调试等。您可以运行以下命令来获取有关`west`命令的帮助：

   ```bash
   west -h
   ```

6. **配置文件**：`west`使用一个名为`west.yml`的配置文件来管理项目和依赖关系。该文件通常位于项目根目录下。

7. **多仓库支持**：`west`支持管理多个仓库，这对于构建和开发依赖于多个Zephyr模块的复杂项目非常有用。

8. **自动下载依赖项**：`west`会自动下载和管理Zephyr的依赖项，包括Zephyr内核和模块。这使得构建过程更加简单和可维护。

`west`工具使Zephyr开发更加方便，特别是对于需要管理多个依赖项和模块的项目。您可以根据项目需求使用不同的`west`命令来配置和构建Zephyr应用程序。要了解更多关于`west`工具的详细信息和使用方法，请查阅Zephyr官方文档中的相关部分。

官方文档：

https://docs.zephyrproject.org/latest/develop/west/index.html

代码在这里：

https://github.com/zephyrproject-rtos/west



West 的内置命令提供了一个多存储库管理系统，其功能受到 Google 的 Repo 工具和 Git 子模块的启发。 West 也是“可插入的”：您可以编写自己的 west 扩展命令，为 west 添加附加功能。 Zephyr 使用它来为构建应用程序、刷新和调试应用程序等提供便利。

##  west list

列出当前的仓库的版本信息。

```
 west list
manifest     zephyr                       HEAD                                     N/A
canopennode  modules/lib/canopennode      1052dae561497bef901f931ef75e117c9224aecd https://github.com/zephyrproject-rtos/canopennode
civetweb     modules/lib/civetweb         094aeb41bb93e9199d24d665ee43e9e05d6d7b1c https://github.com/zephyrproject-rtos/civetweb
cmsis        modules/hal/cmsis            b0612c97c1401feeb4160add6462c3627fe90fc7 https://github.com/zephyrproject-rtos/cmsis
```



# west.yml文件分析



# BabbleSim

https://babblesim.github.io/

这个是一个用于网络开发的网络模拟器。

# 代码层次分析

## include

这个下面大概有1100个头文件。

170多个目录。

只看最上层的zephyr目录下，是这些目录和文件。

```
├── acpi
├── app_memory
├── arch
├── audio
├── bluetooth
├── cache.h
├── canbus
├── console
├── crypto
├── data
├── debug
├── device.h
├── devicetree
├── devicetree.h
├── dfu
├── display
├── drivers
├── dsp
├── dt-bindings
├── exc_handle.h
├── fatal.h
├── fatal_types.h
├── fs
├── init.h
├── input
├── ipc
├── irq.h
├── irq_nextlevel.h
├── irq_offload.h
├── kernel
├── kernel.h
├── kernel_includes.h
├── kernel_structs.h
├── kernel_version.h
├── linker
├── logging
├── lorawan
├── math
├── mgmt
├── modbus
├── multi_heap
├── net
├── pm
├── portability
├── posix
├── random
├── retention
├── rtio
├── sd
├── sensing
├── settings
├── shared_irq.h
├── shell
├── sip_svc
├── smf.h
├── spinlock.h
├── stats
├── storage
├── sw_isr_table.h
├── sys
├── syscall.h
├── syscall_handler.h
├── sys_clock.h
├── task_wdt
├── timeout_q.h
├── timing
├── toolchain
├── toolchain.h
├── tracing
├── types.h
├── usb
├── usb_c
├── wait_q.h
├── xen
├── zbus
└── zephyr.h
```

acpi

```
结构体：
struct acpi_dev
函数：
acpi_legacy_irq_get
acpi_current_resource_get
acpi_possible_resource_get
acpi_current_resource_free
acpi_get_irq_routing_table
acpi_resource_parse
acpi_device_get
acpi_device_by_index_get
acpi_device_type_get
acpi_table_get

```



# 参考资料

1、Zephyr系统快评

http://yiiyee.cn/blog/2019/10/17/zephyr/

2、教程

https://tidyjiang8.gitbooks.io/zephyr-inside/content/get_started/introduce.html