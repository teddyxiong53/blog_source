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



# E表示什么

在 `udevadm info` 命令的输出中，前缀 **`E:`** 表示 **"Environment Variable"**（环境变量）。这些环境变量提供了与设备相关的属性信息，反映了系统如何识别和管理该设备。以下是一些常见的 **`E:`** 前缀的变量及其含义：

### 常见 `E:` 环境变量

1. **`E: DEVNAME`**：
   - 设备在 `/dev` 目录中的名称，比如 `/dev/sda1`。

2. **`E: DEVPATH`**：
   - 设备在系统中的路径，通常指向 `/sys` 文件系统中的位置。

3. **`E: DEVTYPE`**：
   - 设备类型，例如 `partition`、`disk`、`usb_device` 等。

4. **`E: ID_BUS`**：
   - 表示连接设备的总线类型，例如 `usb`、`pci` 等。

5. **`E: ID_VENDOR`** 和 **`E: ID_MODEL`**：
   - 设备制造商和型号信息。

6. **`E: ID_SERIAL`**：
   - 设备的序列号，用于唯一标识特定设备。

7. **`E: ID_FS_TYPE`**、**`E: ID_FS_UUID`**：
   - 文件系统类型和 UUID，提供关于设备内容的信息。

8. **`E: ID_PART_ENTRY_*`**：
   - 提供有关分区的信息，如分区类型、大小和偏移量等。

9. **`E: TAGS`**：
   - 与设备相关的标签，例如与 `systemd` 的集成信息。

# 如何使用这些环境变量来编写脚本？

使用 `udev` 环境变量编写脚本可以帮助您自动化设备管理、配置和监控。以下是一些常见的用法和示例，展示如何在脚本中利用这些环境变量。

### 示例场景

假设您想在 USB 音频设备连接时自动运行一个脚本来配置音频设置。

### 1. 创建 `udev` 规则

首先，您需要创建一个 `udev` 规则文件，例如 `/etc/udev/rules.d/99-usb-audio.rules`，内容如下：

```plaintext
ACTION=="add", SUBSYSTEM=="sound", ATTRS{idVendor}=="0951", ATTRS{idProduct}=="1643", RUN+="/usr/local/bin/setup-audio.sh"
```

这条规则会在符合条件的 USB 音频设备插入时运行 `setup-audio.sh` 脚本。

### 2. 编写脚本

接下来，编写 `/usr/local/bin/setup-audio.sh` 脚本，并确保它具有可执行权限：

```bash
#!/bin/bash

# 获取设备信息
DEVICE_NAME="$DEVNAME"
VENDOR_ID="$ID_VENDOR_ID"
MODEL_ID="$ID_MODEL_ID"
UUID="$ID_FS_UUID"

# 输出设备信息到日志
echo "Device connected: $DEVICE_NAME"
echo "Vendor ID: $VENDOR_ID"
echo "Model ID: $MODEL_ID"
echo "File system UUID: $UUID" >> /var/log/usb-audio.log

# 进行音频配置，例如调用 pulseaudio 的相关命令
# pulseaudio --load-module module-alsa-sink device="$DEVICE_NAME"

# 其他自定义操作
```

### 3. 设置脚本权限

确保脚本可执行：

```bash
sudo chmod +x /usr/local/bin/setup-audio.sh
```

### 4. 使用环境变量

在脚本中，您可以直接使用 `udev` 提供的环境变量。例如，上述脚本中使用了 `$DEVNAME`、`$ID_VENDOR_ID` 和 `$ID_MODEL_ID` 来获取设备名称和标识信息。

### 5. 测试

连接符合条件的 USB 音频设备，并检查 `/var/log/usb-audio.log` 文件，确认脚本是否按预期执行。

### 注意事项

- **权限**：确保脚本有足够的权限进行所需的操作，可能需要以 root 用户权限运行。
- **路径**：使用绝对路径来引用任何命令或文件，因为 `udev` 在不同的上下文中运行，可能没有用户的环境变量配置。
- **调试**：可以在脚本中添加调试信息，如输出到日志文件，帮助排查问题。

### 总结

通过结合 `udev` 规则和脚本，您可以自动化设备管理任务，利用环境变量获取设备相关信息并执行相应操作。这种方式在系统管理和设备配置中非常有用。如果您有更多问题或需要进一步帮助，请告诉我！

# buildroot里udev

在/etc/init.d/S10udev里进行的。往proc/sys/kernel/hotplug   写入了0，是说明不支持热插拔吗？

向 `/proc/sys/kernel/hotplug` 文件写入四个 null 字节的目的通常是清空该文件中的内容。在某些情况下，系统可能会期望该文件为空，因此通过写入 null 字节来实现清空操作是一种常见的做法。

```
 printf "Populating %s using udev: " "${udev_root:-/dev}"      
 printf '\000\000\000\000' > /proc/sys/kernel/hotplug          
 $UDEV_BIN -d || { echo "FAIL"; exit 1; }                      
 udevadm trigger --type=subsystems --action=add                
 udevadm trigger --type=devices --action=add                   
 udevadm settle --timeout=30 || echo "udevadm settle failed"   
 echo "done"                                                   
```

 udevadm settle --timeout=30 这个是等待前面的操作完成，最多等30s。过期不候。

对应的配置文件是在/etc/udev目录下。

```
/etc/udev # ls                   
hwdb.d     这个下面有很多文件。
rules.d   空的
udev.conf  这个是空的
```

buildroot的udev是一个virtual-package，实际的实现是eudev。

```
EUDEV_PROVIDES = udev
```

我找个板子udev打开看看。



```
BR2_PACKAGE_EUDEV=y
BR2_PACKAGE_PROVIDES_UDEV="eudev"
# BR2_PACKAGE_EUDEV_RULES_GEN is not set
BR2_PACKAGE_EUDEV_ENABLE_HWDB=y
BR2_PACKAGE_HAS_UDEV=y
BR2_PACKAGE_KMOD=y
BR2_PACKAGE_HOST_EUDEV=y
```

需要修改cpio/init，里面不要用mdev的。



# eudev和udev关系

eudev 是一个udev的分支项目，它最初是由 Gentoo Linux 社区发起的。

==它的目标是提供一个独立于 systemd 的udev实现，使得udev能够在非 systemd 系统中使用。==

它们之间的关系可以总结如下：

1. **共同点**：
   - 两者都是 Linux 系统中用于设备管理的重要组件，负责管理设备的插拔、命名、权限等方面。
   - 两者都提供类似的功能，包括设备的自动识别、创建符号链接、设置设备权限等。

2. **区别**：
   - **依赖关系**：udev是 systemd 的一部分，因此它的设计和发展与systemd密切相关。而eudev是独立于 systemd 的udev实现，可以在非 systemd 系统中使用。
   - **社区支持**：udev由 systemd 社区维护和开发，而eudev则主要由 Gentoo 社区维护和开发。
   - **发行版本**：udev通常作为systemd的一部分发布，而eudev则独立发布，可以在各种Linux发行版中使用。

3. **选用建议**：
   - 如果你的系统基于 systemd，通常建议使用系统默认的udev实现。
   - 如果你的系统不依赖于 systemd，或者你想在非 systemd 环境中使用udev，那么可以考虑使用eudev。

总的来说，eudev和udev在功能上非常相似，但由于其不同的依赖和维护者，适用于不同的使用场景。

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

使用 `udev` 实现 USB 和 SD 卡设备的重命名、自动挂载和自动卸载，可以通过创建相应的 `udev` 规则和脚本来完成。以下是一个完整的步骤指南。

### 步骤 1: 创建 `udev` 规则

首先，您需要创建 `udev` 规则文件，以便在设备插入时触发相应的操作。创建文件 `/etc/udev/rules.d/99-usb-sd.rules`。

```bash
sudo nano /etc/udev/rules.d/99-usb-sd.rules
```

在文件中添加以下规则：

```plaintext
# 规则以 USB 设备为例，您可以根据需要更改 idVendor 和 idProduct
ACTION=="add", SUBSYSTEM=="block", ENV{ID_BUS}=="usb", RUN+="/usr/local/bin/mount-usb.sh %k"
ACTION=="remove", SUBSYSTEM=="block", ENV{ID_BUS}=="usb", RUN+="/usr/local/bin/unmount-usb.sh %k"

# 规则以 SD 卡为例
ACTION=="add", SUBSYSTEM=="block", ENV{ID_BUS}=="mmc", RUN+="/usr/local/bin/mount-sd.sh %k"
ACTION=="remove", SUBSYSTEM=="block", ENV{ID_BUS}=="mmc", RUN+="/usr/local/bin/unmount-sd.sh %k"
```

### 步骤 2: 编写挂载和卸载脚本

接下来，您需要创建挂载和卸载脚本。以下是示例脚本。

#### 2.1 创建挂载脚本

创建挂载脚本 `/usr/local/bin/mount-usb.sh`：

```bash
sudo nano /usr/local/bin/mount-usb.sh
```

添加以下内容：

```bash
#!/bin/bash

DEVICE=$1
MOUNT_POINT="/media/usb/$DEVICE"

# 创建挂载点
mkdir -p "$MOUNT_POINT"

# 挂载设备
mount "/dev/$DEVICE" "$MOUNT_POINT"

# 输出信息
echo "Mounted $DEVICE at $MOUNT_POINT"
```

#### 2.2 创建卸载脚本

创建卸载脚本 `/usr/local/bin/unmount-usb.sh`：

```bash
sudo nano /usr/local/bin/unmount-usb.sh
```

添加以下内容：

```bash
#!/bin/bash

DEVICE=$1
MOUNT_POINT="/media/usb/$DEVICE"

# 卸载设备
umount "$MOUNT_POINT"

# 删除挂载点
rmdir "$MOUNT_POINT"

# 输出信息
echo "Unmounted $DEVICE from $MOUNT_POINT"
```

#### 2.3 创建 SD 卡 脚本

您可以为 SD 卡创建类似的挂载和卸载脚本 `/usr/local/bin/mount-sd.sh` 和 `/usr/local/bin/unmount-sd.sh`，逻辑类似。

### 步骤 3: 设置脚本权限

确保所有脚本可执行：

```bash
sudo chmod +x /usr/local/bin/mount-usb.sh
sudo chmod +x /usr/local/bin/unmount-usb.sh
sudo chmod +x /usr/local/bin/mount-sd.sh
sudo chmod +x /usr/local/bin/unmount-sd.sh
```

### 步骤 4: 测试

1. 插入 USB 或 SD 卡设备。
2. 检查 `/media/usb/` 目录，确认设备是否已自动挂载。
3. 卸载设备后，检查挂载点是否已被删除。

### 注意事项

- **挂载点**：确保挂载点目录存在并具有适当的权限。
- **文件系统类型**：根据需要，您可以在挂载时指定文件系统类型，例如 `mount -t vfat`。
- **日志记录**：可以在脚本中添加日志记录，以便于故障排除。
- **环境变量**：`udev` 规则中的 `%k` 将被替换为设备名称，例如 `sda1`。





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

# udev.conf

`udev.conf` 是 udev 的配置文件，用于定义 udev 守护进程的全局配置选项。下面是一个典型的 `udev.conf` 文件的说明及其示例配置：

### `udev.conf` 文件的主要选项

1. **`udev_log`**：设置日志级别。常见的值包括 `err`（错误）、`info`（信息）、`debug`（调试）。
2. **`udev_rules`**：设置 udev 规则文件的目录路径。
3. **`udev_log`**：设置 udev 守护进程的日志级别。
4. **`udev_event_timeout`**：设置 udev 事件的超时时间，以秒为单位。
5. **`udev_children_max`**：设置 udev 同时处理的最大事件数。
6. **`udev_timeout`**：设置 udev 事件处理的超时时间（秒）。

### 示例 `udev.conf` 文件

以下是一个示例的 `udev.conf` 文件内容：

```ini
# udev.conf
#
# See udev(7) for details.

# udevd is started in the following default log priority. Valid values are:
# err, info, debug
udev_log="info"

# path to udev rules
udev_rules="/etc/udev/rules.d"

# path to udev log
udev_log="/var/log/udev.log"

# maximum number of events udevd can handle at the same time
udev_children_max=8

# udev event processing timeout in seconds
udev_timeout=180
```

### 详细说明

- **`udev_log="info"`**：设置日志级别为 `info`。可以改为 `err` 或 `debug`，具体取决于需要的日志详细程度。
- **`udev_rules="/etc/udev/rules.d"`**：指定 udev 规则文件所在的目录。默认路径通常是 `/etc/udev/rules.d`。
- **`udev_log="/var/log/udev.log"`**：指定 udev 守护进程的日志文件路径。如果需要查看 udev 日志，可以检查这个文件。
- **`udev_children_max=8`**：设置 udev 可以同时处理的最大事件数。可以根据系统性能和需求调整这个值。
- **`udev_timeout=180`**：设置 udev 事件处理的超时时间，单位为秒。可以根据具体需求调整这个值。

### 修改 `udev.conf`

要修改 `udev.conf` 文件，按照以下步骤进行：

1. 打开 `udev.conf` 文件：

   ```bash
   sudo nano /etc/udev/udev.conf
   ```

2. 根据需要编辑配置选项，例如修改日志级别：

   ```ini
   udev_log="debug"
   ```

3. 保存文件并退出编辑器（在 nano 中按 `Ctrl+X`，然后按 `Y` 确认保存）。

4. 重启 `udevd` 守护进程以使配置生效：

   ```bash
   sudo systemctl restart udev
   ```

或者在一些系统中，使用以下命令：

   ```bash
   sudo service udev restart
   ```

通过以上步骤，您可以配置和调整 udev 的全局行为，以适应系统的具体需求。

# udev默认的规则文件

```
# cd /lib/udev/rules.d/
# ls
50-udev-default.rules             60-sensor.rules
60-block.rules                    60-serial.rules
60-cdrom_id.rules                 64-btrfs.rules
60-drm.rules                      70-joystick.rules
60-evdev.rules                    70-mouse.rules
60-input-id.rules                 70-touchpad.rules
60-persistent-alsa.rules          75-net-description.rules
60-persistent-input.rules         75-probe_mtd.rules
60-persistent-storage-tape.rules  78-sound-card.rules
60-persistent-storage.rules       80-drivers.rules
60-persistent-v4l.rules           80-net-name-slot.rules
# 
```



| 文件名                             | 说明                                               |
| ---------------------------------- | -------------------------------------------------- |
| `50-udev-default.rules`            | 默认的 udev 规则，处理基本的设备管理。             |
| `60-sensor.rules`                  | 针对传感器设备的规则，管理传感器相关设备。         |
| `60-block.rules`                   | 处理块设备（如硬盘、USB存储设备）的规则。          |
| `60-serial.rules`                  | 管理串口设备的规则。                               |
| `60-cdrom_id.rules`                | 处理光盘驱动器的 ID 规则。                         |
| `64-btrfs.rules`                   | 针对 Btrfs 文件系统设备的规则。                    |
| `60-drm.rules`                     | 处理 DRM (Direct Rendering Manager) 设备的规则。   |
| `70-joystick.rules`                | 管理游戏手柄设备的规则。                           |
| `60-evdev.rules`                   | 处理 evdev 设备（输入设备）的规则。                |
| `70-mouse.rules`                   | 管理鼠标设备的规则。                               |
| `60-input-id.rules`                | 识别输入设备的规则，提供设备 ID 信息。             |
| `70-touchpad.rules`                | 针对触摸板设备的规则。                             |
| `60-persistent-alsa.rules`         | 管理 ALSA 音频设备的持久规则。                     |
| `75-net-description.rules`         | 为网络设备生成描述信息的规则。                     |
| `60-persistent-input.rules`        | 处理持久化输入设备的规则。                         |
| `75-probe_mtd.rules`               | 管理 MTD (Memory Technology Device) 的规则。       |
| `60-persistent-storage-tape.rules` | 针对磁带存储设备的持久规则。                       |
| `78-sound-card.rules`              | 管理声卡设备的规则。                               |
| `60-persistent-storage.rules`      | 针对持久化存储设备的规则。                         |
| `80-drivers.rules`                 | 管理驱动程序的规则，处理设备与驱动的关联。         |
| `60-persistent-v4l.rules`          | 针对视频设备（Video4Linux）的持久规则。            |
| `80-net-name-slot.rules`           | 管理网络接口名称的规则，确保网络设备的名称一致性。 |



# hwdb文件说明

`hwdb`（Hardware Database）是 Linux 系统中 `udev` 使用的一种硬件数据库，用于存储和查询硬件设备的特性和属性信息。它帮助系统识别硬件并为其应用适当的配置或规则。

### `hwdb` 的主要功能

1. **设备识别**：
   - `hwdb` 存储设备的各种属性，如制造商、产品 ID、序列号、类型等，允许系统根据这些信息进行识别和分类。

2. **动态配置**：
   - 系统可以根据硬件特性动态生成 `udev` 规则，自动识别和配置设备。

3. **信息查询**：
   - 通过 `hwdb`，用户和系统管理员可以查询硬件设备的详细信息，方便进行故障排除和设备管理。

### 文件位置

`hwdb` 数据库通常位于 `/lib/udev/hwdb.bin`，并且可以通过 `/etc/udev/hwdb.d/` 目录中的配置文件进行扩展和覆盖。用户可以在 `/etc/udev/hwdb.d/` 中创建自定义的 `hwdb` 条目。

### `hwdb` 文件格式

`hwdb` 文件使用简单的文本格式，每行包含一个或多个键值对。以下是常见的格式示例：

```plaintext
# 注释行以 # 开头
idVendor=1234
idProduct=5678
NAME="My USB Device"
```

### 关键字段

- **`idVendor`**：设备制造商的 ID。
- **`idProduct`**：设备的产品 ID。
- **`NAME`**：设备的可读名称。
- **其他属性**：可以包含其他特定于设备的信息，如类型、版本等。

### 使用示例

1. **查询 `hwdb` 信息**：
   通过 `udevadm` 命令查询某个设备的信息，可以使用以下命令：

   ```bash
   udevadm info --query=all --name=/dev/sda1
   ```

   然后结合 `hwdb` 数据库的信息。

2. **更新 `hwdb`**：
   在修改或添加 `hwdb` 文件后，需要运行以下命令来更新数据库：

   ```bash
   sudo udevadm hwdb --update
   ```

### 总结

`hwdb` 是一个重要的工具，用于增强 `udev` 的能力，通过提供详细的硬件信息来支持设备识别和动态配置。通过适当的配置，用户可以改进设备管理和系统性能。如果您有更多问题或需要进一步的说明，请告诉我！

# mdev没有hwdb机制，为什么也可以工作？

`mdev` 没有 `hwdb` 机制，但仍然可以正常工作，主要原因如下：

1. **简单设备管理**：`mdev` 是一个轻量级的设备管理器，设计上用于嵌入式系统或资源受限的环境。它通过简单的规则和脚本来处理设备的添加、移除和配置，而不依赖于复杂的数据库。

2. **基于规则的配置**：`mdev` 使用配置文件（如 `/etc/mdev.conf`）来定义设备的处理规则。这些规则可以基于设备的属性（如设备类型、ID 等）来执行相应的操作，例如加载驱动程序、设置权限或执行初始化脚本。

3. **内核事件监听**：`mdev` 通过监听内核发出的设备事件（如 `udev`），能够实时响应设备的添加和移除。这种机制使得它能够动态管理设备，即使没有 `hwdb` 数据库。

4. **轻量级实现**：由于 `mdev` 的设计目标是简化和减小系统开销，因此它省略了一些复杂的功能（如 `hwdb`），而选择通过直接的规则和脚本来处理设备。

### 总结
尽管 `mdev` 没有 `hwdb` 机制，但它通过简单的规则和内核事件管理设备，依然能够有效地进行设备管理。这种设计使得 `mdev` 特别适合于嵌入式和轻量级的系统环境。

# 参考资料

1、udev udevadm介绍及linux设备重命名和自动挂载应用实例分析

https://blog.csdn.net/li_wen01/article/details/89435306

2、linux下自动创建设备文件节点---class

https://www.cnblogs.com/Ph-one/p/6720087.html