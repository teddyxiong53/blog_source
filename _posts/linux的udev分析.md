---
title: linux的udev分析
date: 2016-12-10 21:58:22
tags:
	- linux驱动
	- udev
---
--

# 简介

好的，这里是关于udev的简介：

## udev 简介

**udev** 是 Linux 系统中用于管理设备节点的设备管理器。它动态创建和删除 `/dev` 目录下的设备节点，并能够根据设备的属性自动执行用户定义的任务。

### 主要功能

1. **设备节点管理**：自动创建和删除 `/dev` 目录中的设备文件。
2. **事件处理**：当设备插入或拔出时，udev 会触发相应的事件，并执行预定义的规则。
3. **属性匹配**：通过设备属性（如设备类型、厂商、型号等）来匹配规则。
4. **持久命名**：为设备提供一致的名称，即使设备的物理连接发生变化。

### udev 工作原理

1. **内核事件**：当设备连接或断开时，内核会产生 `udev` 事件。
2. **udev 事件处理**：`udev` 监听这些事件，并根据配置规则进行处理。
3. **规则匹配**：`udev` 通过 `/etc/udev/rules.d` 和 `/lib/udev/rules.d` 下的规则文件匹配设备属性，决定如何处理该设备。
4. **设备节点创建**：`udev` 创建或删除相应的设备节点，并执行相关操作（如设置权限、创建符号链接等）。

### 常用命令

| 命令              | 功能                               |
| ----------------- | ---------------------------------- |
| `udevadm info`    | 显示设备的信息                     |
| `udevadm control` | 控制 udev daemon，例如重载规则文件 |
| `udevadm monitor` | 监视内核和 udev 事件               |
| `udevadm trigger` | 手动触发 udev 事件，重新应用规则   |

### 示例规则

```plaintext
# /etc/udev/rules.d/99-usb.rules

# 为特定的 USB 设备创建符号链接
SUBSYSTEM=="usb", ATTR{idVendor}=="1234", ATTR{idProduct}=="5678", SYMLINK+="my_usb_device"
```

### 配置文件位置

| 目录                  | 描述                   |
| --------------------- | ---------------------- |
| `/etc/udev/udev.conf` | udev 主配置文件        |
| `/etc/udev/rules.d/`  | 用户自定义规则文件目录 |
| `/lib/udev/rules.d/`  | 系统默认规则文件目录   |

### 小结

udev 是一个强大的工具，可以根据设备的属性自动执行各种操作，从而简化设备管理和提高系统的灵活性。如果你有更多关于 udev 的具体问题或需要深入了解某个功能，请告诉我！

# 发展历史

以下是udev的发展历史：

| 时间   | 事件                                                         |
| ------ | ------------------------------------------------------------ |
| 2003年 | udev 由 Greg Kroah-Hartman 创建，并首次引入到 Linux 内核中。 |
| 2004年 | udev 成为 Linux 内核的一部分，并取代了之前的设备管理工具 devfs。 |
| 2005年 | udev 开始在 Linux 发行版中得到广泛采用，取代了 devfs，成为 Linux 系统中设备管理的主要解决方案。 |
| 2008年 | udev 开始支持基于 sysfs 和内核事件的设备管理模型，大大简化了设备节点的管理和维护。 |
| 2012年 | systemd 项目开始整合 udev，并将其作为 systemd 的一部分进行维护。 |
| 2015年 | udev 项目整合到 systemd 中，成为 systemd 的一个组件，这导致一些争议，因为一些人认为将设备管理和系统初始化工具整合在一起不合适。 |
| 至今   | udev 仍然是 Linux 系统中最常用的设备管理器之一，虽然它已经成为 systemd 的一部分，但它仍然保持着独立的发展和维护。 |

udev 的发展历程展示了它作为 Linux 系统中设备管理的关键组件的重要性，并且随着时间的推移，它不断地融入了更多的功能和改进，以满足日益增长的系统需求。

# 基本信息

linux下的设备文件处理这一块，在多年的发展过程中，经历了几次策略的改变。

在早期，设备文件仅仅是一些带有适当属性集的普通文件，它由mknod命令创建，文件存放在/dev目录下。

后来，从内核2.3.46版本开始，采用了devfs，一个基于内核的动态设备文件系统。

但是devfs有比较严重的限制，于是，从内核2.6.13版本起，devfs又被移除了。替换为现在要说的udev。

devfs的缺点有很多，主要有这些：

* 不确定的设备映射。你的设备名字跟你插入的顺序有关。
* 主设备号和从设备号不够用，它们的数值都是最大为255 。
* 内核内存使用，devfs会消耗大量的内核内存。
相比于前辈们，udev很好地解决了设备的热拔插问题，还有解决了devfs的设备号短缺的问题，这一点对于有上千个硬盘的系统非常关键。

udev的配置文件是`/etc/udev/udev.conf`。
在树莓派上，该文件的内容如下所示，是空的。

```
# see udev(7) for details
#
# udevd is started in the initramfs, so when this file is modified the
# initramfs should be rebuilt.

#udev_log="info"
                                                                         
```
我的当前的树莓派插着一个U盘，被格式化为2个分区。查看一下sda1的信息。
```
pi@raspberrypi:/sys/block/sda/sda1 $ udevadm info /sys/block/sda/sda1 
P: /block/sda/sda1
N: sda1
S: disk/by-id/usb-Kingston_DataTraveler_G3_001CC07CEB39FBB1C91A24D0-0:0-part1
S: disk/by-label/BOOT
S: disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1
S: disk/by-uuid/47CE-67C0
E: DEVLINKS=/dev/disk/by-id/usb-Kingston_DataTraveler_G3_001CC07CEB39FBB1C91A24D0-0:0-part1 /dev/disk/by-label/BOOT /dev/disk/by-path/platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0-part1 /dev/disk/by-uuid/47CE-67C0
E: DEVNAME=/dev/sda1
E: DEVPATH=/block/sda/sda1
E: DEVTYPE=partition
E: ID_BUS=usb
E: ID_FS_LABEL=BOOT
E: ID_FS_LABEL_ENC=BOOT
E: ID_FS_TYPE=vfat
E: ID_FS_USAGE=filesystem
E: ID_FS_UUID=47CE-67C0
E: ID_FS_UUID_ENC=47CE-67C0
E: ID_FS_VERSION=FAT32
E: ID_INSTANCE=0:0
E: ID_MODEL=DataTraveler_G3
E: ID_MODEL_ENC=DataTraveler\x20G3\x20
E: ID_MODEL_ID=1643
E: ID_PART_ENTRY_DISK=8:0
E: ID_PART_ENTRY_NUMBER=1
E: ID_PART_ENTRY_OFFSET=2048
E: ID_PART_ENTRY_SCHEME=dos
E: ID_PART_ENTRY_SIZE=192512
E: ID_PART_ENTRY_TYPE=0xc
E: ID_PART_ENTRY_UUID=885f1eb8-01
E: ID_PART_TABLE_TYPE=dos
E: ID_PART_TABLE_UUID=885f1eb8
E: ID_PATH=platform-3f980000.usb-usb-0:1.5:1.0-scsi-0:0:0:0
E: ID_PATH_TAG=platform-3f980000_usb-usb-0_1_5_1_0-scsi-0_0_0_0
E: ID_REVISION=1.00
E: ID_SERIAL=Kingston_DataTraveler_G3_001CC07CEB39FBB1C91A24D0-0:0
E: ID_SERIAL_SHORT=001CC07CEB39FBB1C91A24D0
E: ID_TYPE=disk
E: ID_USB_DRIVER=usb-storage
E: ID_USB_INTERFACES=:080650:
E: ID_USB_INTERFACE_NUM=00
E: ID_VENDOR=Kingston
E: ID_VENDOR_ENC=Kingston
E: ID_VENDOR_ID=0951
E: MAJOR=8
E: MINOR=1
E: SUBSYSTEM=block
E: TAGS=:systemd:
E: USEC_INITIALIZED=76296
```

##  udevadm info 输出信息解读

`udevadm info` 命令用于显示设备的详细信息，包括设备的属性、子系统、设备节点等。以下是 `udevadm info` 输出信息的解读：

1. **设备路径 (`P: /devices/...`)**：显示设备在系统中的路径，可以用来定位设备在设备树中的位置。

2. **设备节点 (`N: /dev/...`)**：显示设备在 `/dev` 目录下的节点名称，通过这个节点可以访问设备。

3. **设备名称 (`E: NAME="..."`)**：显示设备的名称，通常是设备的物理地址或者设备类型。

4. **设备子系统 (`S: ...`)**：显示设备所属的子系统，例如 `usb`、`pci` 等。

5. **设备属性 (`E: ...`)**：显示设备的属性信息，包括设备的厂商、型号、序列号等。

6. **驱动程序 (`E: DRIVER="..."`)**：显示设备正在使用的驱动程序名称。

7. **设备连接 (`E: DEVNAME="..."`)**：显示设备的连接信息，通常是设备节点的路径。

8. **设备识别号 (`E: ID_...`)**：显示设备的识别号，通常根据设备的属性生成。

9. **其他信息**：还可以显示其他一些设备的信息，例如设备的协议、类别、设备类型等。

通过分析 `udevadm info` 的输出信息，可以了解设备的详细属性和特征，从而编写相应的udev规则来管理设备。



udev的命名规则保存在`/etc/udev/rules.d`目录下。

目录下的脚本名字是用数字来编号。

从数字小的开始执行，**一旦发现匹配的规则，则停止执行返回。**

树莓派的Raspbian系统的该目录下，就一个`99-com.rules`文件。内容如下：

```
SUBSYSTEM=="input", GROUP="input", MODE="0660"
SUBSYSTEM=="i2c-dev", GROUP="i2c", MODE="0660"
SUBSYSTEM=="spidev", GROUP="spi", MODE="0660"
SUBSYSTEM=="bcm2835-gpiomem", GROUP="gpio", MODE="0660"

SUBSYSTEM=="gpio*", PROGRAM="/bin/sh -c '\
    chown -R root:gpio /sys/class/gpio && chmod -R 770 /sys/class/gpio;\
    chown -R root:gpio /sys/devices/virtual/gpio && chmod -R 770 /sys/devices/virtual/gpio;\
    chown -R root:gpio /sys$devpath && chmod -R 770 /sys$devpath\
'"

KERNEL=="ttyAMA[01]", PROGRAM="/bin/sh -c '\
    ALIASES=/proc/device-tree/aliases; \
    if cmp -s $ALIASES/uart0 $ALIASES/serial0; then \
        echo 0;\
    elif cmp -s $ALIASES/uart0 $ALIASES/serial1; then \
        echo 1; \
    else \
        exit 1; \
    fi\
'", SYMLINK+="serial%c"

KERNEL=="ttyS0", PROGRAM="/bin/sh -c '\
    ALIASES=/proc/device-tree/aliases; \
    if cmp -s $ALIASES/uart1 $ALIASES/serial0; then \
        echo 0; \
    elif cmp -s $ALIASES/uart1 $ALIASES/serial1; then \
        echo 1; \
    else \
        exit 1; \
    fi \
'", SYMLINK+="serial%c"
```





# buildroot里udev

在/etc/init.d/S10udev里进行的。往proc/sys/kernel/hotplug   写入了0，是说明不支持热插拔吗？

```
 printf "Populating %s using udev: " "${udev_root:-/dev}"      
 printf '\000\000\000\000' > /proc/sys/kernel/hotplug          
 $UDEV_BIN -d || { echo "FAIL"; exit 1; }                      
 udevadm trigger --type=subsystems --action=add                
 udevadm trigger --type=devices --action=add                   
 udevadm settle --timeout=30 || echo "udevadm settle failed"   
 echo "done"                                                   
```

对应的配置文件是在/etc/udev目录下。

```
/etc/udev # ls                   
hwdb.d     这个下面有很多文件。
rules.d   空的
udev.conf  这个是空的
```



udev是一个通用的内核设备管理器。它以守护进程的方式运行于Linux系统，并监听在新设备初始化或设备从系统中移除时，内核（通过netlink socket）所发出的uevent。

# udev系统架构：

udev系统可以分为三个部分：

- libudev函数库，可以用来获取设备的信息。
- udevd守护进程，处于用户空间，用于管理虚拟/dev
- 管理命令udevadm，用来诊断出错情况。



# udevadm命令



```
/etc # udevadm info --query=all --name=rk_led_ctrl       
P: /devices/platform/pwm_leds@0/misc/rk_led_ctrl         
N: rk_led_ctrl                                           
E: DEVNAME=/dev/rk_led_ctrl                              
E: DEVPATH=/devices/platform/pwm_leds@0/misc/rk_led_ctrl 
E: MAJOR=10                                              
E: MINOR=0                                               
E: SUBSYSTEM=misc                                        
```

## 常用命令

以下是一些常用的udev命令：

1. `udevadm trigger`: 强制触发udev事件处理，用于重新扫描设备或处理设备更改事件。

2. `udevadm settle`: 等待udev事件处理完成，确保设备的创建和配置已经完成。

3. `udevadm monitor`: 监视udev事件流，实时显示设备的插拔和状态变化。

4. `udevadm info`: 显示设备的详细信息，包括设备属性、驱动程序、路径等。

5. `udevadm control`: 控制udev的运行行为，如重载规则、重新加载配置文件等。

6. `udevadm test`: 测试udev规则文件的匹配和执行结果，用于调试和验证规则。

7. `udevadm settle --timeout=<seconds>`: 设置udev事件处理的超时时间，超过指定时间后终止等待。

这些命令可以在终端中直接运行，需要使用root权限或者使用sudo命令来执行。更详细的命令用法和参数选项可以通过`man udevadm`来查看相关的手册页。





# 使用udev实现USB，SD卡设备的重命名、自动挂载、自动卸载。



自动创建设备节点，靠class机制就可以做到了。

我们在刚开始写[Linux](http://lib.csdn.net/base/linux)设备驱动程序的时候，很多时候都是利用mknod命令手动创建设备节点，实际上Linux内核为我们提供了一组函数，可以用来在模块加载的时候自动在/dev目录下创建相应设备节点，并在卸载模块时删除该节点，当然前提条件是用户空间移植了udev。



内核中定义了struct class结构体，顾名思义，一个struct class结构体类型变量对应一个类，内核同时提供了class_create(…)函数，可以用它来创建一个类，这个类存放于sysfs下面，一旦创建好了这个类，再调用device_create(…)函数来在/dev目录下创建相应的设备节点。**这样，加载模块的时候，用户空间中的udev会自动响应device_create(…)函数，去/sysfs下寻找对应的类从而创建设备节点。**



# buildroot里的udevd

是在eudev目录下，而不是udevd目录下。

# udev和mdev比较

udev和mdev是用于设备管理的工具，它们在不同的Linux发行版中使用。下面是它们的比较：

udev：
- udev是Linux系统中最常用的设备管理工具，**它由systemd项目提供和维护。**
- udev负责设备的动态管理和事件处理，它基于内核的设备事件通知机制（sysfs和netlink）来监视设备的插拔和状态变化。
- udev通过规则文件（udev rules）来识别和配置设备，可以根据设备属性、路径、类型等信息进行匹配和操作。
- udev支持灵活的规则配置和自定义脚本，可以实现自动加载驱动程序、创建设备节点、设置设备属性等操作。
- udev具有丰富的功能和广泛的应用，可以管理各种类型的设备，包括硬盘、网络接口、USB设备、输入设备等。

mdev：
- mdev是BusyBox工具集中的一个小型设备管理工具，适用于嵌入式系统和轻量级发行版。
- mdev的设计目标是提供一个简单而轻量级的设备管理解决方案，适用于资源受限的环境。
- **mdev不依赖于sysfs和netlink等内核事件通知机制，而是通过轮询设备目录来检测设备的插拔和状态变化。**
- mdev的配置是通过设备目录下的特定文件（如/dev/mdev.conf）进行，用户可以定义规则和脚本来处理设备事件。
- mdev支持的功能相对有限，主要包括设备节点的创建、权限设置和执行用户定义的脚本。

总体而言，udev是一个功能强大且广泛使用的设备管理工具，适用于各种Linux发行版和使用场景。mdev则更适合嵌入式系统和资源受限的环境，提供了一个简单轻量级的设备管理解决方案。选择使用哪个工具取决于系统的需求和特定的应用场景。

# udev代码分析

udev的代码是在systemd目录下的。

./systemd/systemd-stable-244.3/src/udev

udev是Linux系统中的设备管理器，负责管理设备的插拔、设备节点的创建、设备属性的配置等任务。udev的源代码主要由C语言编写，并且分为多个模块和文件，下面是udev代码的基本结构和组成部分的简要说明：

1. `udev`目录：udev的源代码存放在`udev`目录中，包括核心功能和模块化组件。

2. `udev.h`：包含udev的主要头文件，定义了常量、数据结构和函数声明等。

3. `udevadm`：udev命令行工具的源代码，提供了与udev交互的功能，如事件触发、设备信息查询等。

4. `rules`目录：存放udev规则文件的目录，包含设备匹配规则和对应的动作处理。

5. `src`目录：存放udev核心功能模块的源代码，包括设备事件处理、设备节点管理、属性配置等。

6. `libudev`：udev库的源代码，提供了对外的API接口，用于应用程序与udev进行交互。

7. `udevadm.c`：udev命令行工具的主要源文件，包含了命令行参数解析和对应的操作处理逻辑。

8. `udev_monitor.c`：实现了udev事件监视功能的源文件，负责监听和处理设备事件。

9. `udev_device.c`：实现了设备节点管理的源文件，负责设备节点的创建、删除和属性设置等操作。

10. `udev_rules.c`：解析和处理udev规则文件的源文件，负责匹配设备和执行对应的规则动作。

以上是udev源代码的一些主要部分和模块，udev的代码较为复杂，涉及到设备管理的多个方面，包括设备事件处理、规则匹配、设备节点管理等。如果需要更详细的代码分析，建议参考udev的源代码和相关文档，以深入了解其内部实现和具体细节。

# udev规则文件编写方法

编写udev规则文件是配置Linux系统中设备管理的重要方式。以下是编写udev规则文件的基本方法：

1. **选择规则文件的存放位置：**规则文件通常存放在 `/etc/udev/rules.d/` 目录中。你可以在这个目录下创建一个新的规则文件，或者修改现有的文件。

2. **确定规则匹配条件：**在规则文件中，你需要确定哪些条件会触发规则的执行。这些条件通常包括设备的子系统、属性、内核名称等。你可以使用 `udevadm info` 命令来查看设备的属性信息，从而确定匹配条件。

3. **编写规则：**根据确定的匹配条件，编写规则来定义udev应该如何处理特定类型的设备。规则的语法遵循基于键值对的格式。

4. **重载规则：**在修改了规则文件之后，需要重新加载udev规则，以使更改生效。可以使用 `udevadm control --reload-rules` 命令来实现。

5. **测试规则：**修改或创建规则文件后，最好测试规则是否按预期工作。可以通过插入或拔出相应的设备，然后查看系统行为来测试规则是否生效。

下面是一个简单的示例，展示了如何编写一个udev规则文件来为特定的USB设备创建符号链接：

```plaintext
# /etc/udev/rules.d/99-usb.rules

# 当 USB 设备的子系统为 usb 且 idVendor 属性为 1234，idProduct 属性为 5678 时，创建名为 my_usb_device 的符号链接
SUBSYSTEM=="usb", ATTR{idVendor}=="1234", ATTR{idProduct}=="5678", SYMLINK+="my_usb_device"
```

这个规则会在系统中创建一个名为 `my_usb_device` 的符号链接，指向匹配的USB设备。

编写udev规则需要一定的经验和理解，但一旦掌握了基本的语法和原理，就可以轻松地管理系统中的设备。

# 参考资料

1、udev udevadm介绍及linux设备重命名和自动挂载应用实例分析

https://blog.csdn.net/li_wen01/article/details/89435306

2、linux下自动创建设备文件节点---class

https://www.cnblogs.com/Ph-one/p/6720087.html