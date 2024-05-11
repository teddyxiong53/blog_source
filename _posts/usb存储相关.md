---
title: usb存储相关
date: 2024-05-10 16:14:11
tags:
	- usb
---

--

# usb存储相关主题

与USB存储相关的主题涉及了各种技术、标准和应用，以下是一些常见的主题：

1. **USB Mass Storage（USB大容量存储）**：
   - USB Mass Storage是一种常见的USB设备模式，允许计算机直接访问连接设备上的存储器，例如U盘、移动硬盘等。这种模式使得用户可以像访问本地磁盘一样管理设备上的文件。

2. **USB OTG（USB On-The-Go）**：
   - USB On-The-Go是一种USB标准，允许两个USB设备直接连接，而无需通过计算机作为中间设备。这种标准常用于移动设备，例如智能手机和平板电脑，可以通过USB OTG功能连接U盘、键盘、鼠标等外部设备。

3. **USB Mass Storage Class（USB大容量存储类）**：
   - USB Mass Storage Class是一种USB协议规范，定义了USB设备作为大容量存储设备时应遵循的通信协议和数据格式。通过USB Mass Storage Class，设备可以实现与操作系统的兼容性，从而实现即插即用的功能。

4. **USB存储安全**：
   - USB存储设备常常涉及到数据安全和隐私保护的问题。例如，USB加密盘可以通过硬件或软件加密来保护存储在设备上的数据，防止未经授权的访问。

5. **USB存储虚拟化**：
   - USB存储虚拟化是一种技术，允许多个虚拟机或容器共享主机上的USB存储设备。这种技术常用于虚拟化环境和云计算平台中，提高资源利用率和灵活性。

6. **USB存储应用**：
   - USB存储设备在各种应用场景中得到广泛应用，包括数据备份、文件传输、媒体播放、固件更新等。例如，U盘、移动硬盘常用于数据备份和文件传输，而USB存储设备也常被用于嵌入式系统中的固件更新和数据存储。

这些主题涵盖了USB存储领域的各种技术、标准和应用，是USB技术中的一个重要部分。

# MTP

https://wiki.archlinux.org/title/Media_Transfer_Protocol



https://blog.csdn.net/wangyongh/article/details/128292258

这篇文章提到了一些调试经验，但是已经比较老了。

https://www.trivialfeat.com/home/2016/11/17/media-transfer-protocol-in-a-usb-composite-gadget



https://bbs.elecfans.com/jishu_2274311_1_1.html



https://github.com/YuzukiHD/Buildroot-YuzukiSBC

这里找到release的固件。

https://github.com/YuzukiHD/Buildroot-YuzukiSBC/releases/tag/YuzukiCK1N.0.0.1

下载，解压，是一个全志的img文件。

找一下解包工具。

https://github.com/osnetni/tab744/blob/master/imgrepacker

这个工具不能用。

我直接把https://github.com/YuzukiHD/Buildroot-YuzukiSBC这个代码下载下来编译看看。

顺便了解一下全志的sdk的情况。

这个是适用于*F1C100s*芯片的sdk。

看.config里这个也是使能的。

BR2_PACKAGE_UMTPRD=y

先编译完成后，看看相关的配置项再说。

正常编译完了。

看buildroot\output\target\etc\umtprd\umtprd.conf的内容：

```
#
# uMTP Responder config file
# Must be copied to /etc/umtprd/umtprd.conf
#

# Loop / daemon mode
# Set to 1 to don't shutdown uMTPrd when the link is disconnected.

loop_on_disconnect 1

#storage command : Create add a storage entry point. Up to 16 entry points supported
#Syntax : storage "PATH" "NAME"

storage "/" "rootfs" "rw"

# Set the USB manufacturer string

manufacturer "yuzukihd"

# Set the USB Product string

product "yuzukiruler"

# Set the USB Serial number string

serial "01234567"

# Set the USB interface string. Should be always "MTP"

interface "MTP"

# Set the USB Vendor ID, Product ID and class

usb_vendor_id  0x1D6B # Linux Foundation
usb_product_id 0x0100 # PTP Gadget
usb_class 0x6         # Image
usb_subclass 0x1      # Still Imaging device
usb_protocol 0x1      #

# Device version

usb_dev_version 0x3008

# inotify support
# If you want disable the events support (beta), uncomment the following line :

# no_inotify 0x1

#
# Internal buffers size
#

# Internal default usb_max_rd_buffer_size and usb_max_wr_buffer_size value set to 0x10000.
# Internal default read_buffer_cache_size value set to 0x100000.
# Uncomment the following lines to reduce the buffers sizes to fix USB issues on iMX6 based systems.

# usb_max_rd_buffer_size 0x200      # MAX usb read size. Must be a multiple of 512 and be less than read_buffer_cache_size
# usb_max_wr_buffer_size 0x200      # MAX usb write size. Must be a multiple of 512.
# read_buffer_cache_size 0x4000     # Read file cache buffer. Must be a 2^x value.

#
# USB gadget device driver path
#

########################################################################
#
# -- Generic FunctionFS Mode --
#
########################################################################

usb_functionfs_mode 0x1

usb_dev_path   "/dev/ffs-mtp/ep0"
usb_epin_path  "/dev/ffs-mtp/ep1"
usb_epout_path "/dev/ffs-mtp/ep2"
usb_epint_path "/dev/ffs-mtp/ep3"

usb_max_packet_size 0x200

```

但是没有看到开机启动脚本有打开umtprd。

搜索当前的kernel的 .config里，是打开了这2个mass_storage 的配置的：

```
CONFIG_USB_F_MASS_STORAGE=y
CONFIG_USB_CONFIGFS_MASS_STORAGE=y
```

我的配置也是打开了的。

我觉得我当前的问题，应该就是那个conf文件没有放进去。



## umtprd分析

任何带有USB设备端口的主板都应该兼容。

唯一的要求是在Linux内核中启用

USB function fs（CONFIG _ USB _ function fs）

或gadget fs（CONFIG _ USB _ gadget fs）支持。

您还需要启用特定于主板的USB设备端口驱动程序（如RaspberryPi Zero的dwc2）。

一旦在umtprd.conf中配置了正确的设置，

您就可以使用umtprd_ffs.sh或umtprd_gfs.sh在FunctionFS/GadgetFS模式下启动它，

或者在连接usb设备端口时使用udev启动守护程序。

这里有个尝试把荔枝派使用mtp的问题解决。

https://whycan.com/t_8585.html

这里也有说明。

https://forums.ubports.com/topic/4189/mtp-on-mainline-devices-with-umtp-responder

就是在放入umtprd.conf文件后，手动执行下面的这些。

挂载 uMTPr 期望的 gadgetfs：

```bash
modprobe gadgetfs
mkdir /dev/gadget
mount -t gadgetfs gadgetfs /dev/gadget/
```



Plug your PinePhone in with USB and start uMTPr:
用 USB 插入 PinePhone 并启动 uMTPr：

```sql
sudo start umtpr
```



# usb mass storage

# usb msc 和mtp的区别？

msc是拥有对文件系统的绝对控制权的，这意味着，当通过msc协议控制了设备之后，直到释放之前其他人都不能访问。

而mtp协议建立在msc之上的一个逻辑层，可以在持有设备msc控制权的同时，通过mtp让其他对象也有访问设备上文件的能力。当然是有限的能力，不如msc权限大。

Android自从4.0之后很多设备都用了内置存储，内置存储不是FAT文件系统，而是其他的，比如Nexus设备上通常为了方便的多用户管理使用了虚拟的文件系统（/sdcard的内容实际在/data/里面）。

大容量存储模式是直接把存储器卸载连接在电脑上，

大多数电脑不支持新的Android使用的文件系统。

所以只能用MTP了……有的依然使用FAT的设备还是支持大容量存储的。

# avr单片机实现msc存储

https://www.microchip.com/content/dam/mchp/documents/OTH/ApplicationNotes/ApplicationNotes/doc7631.pdf



https://wiki.phytec.com/pages/viewpage.action?pageId=175113924