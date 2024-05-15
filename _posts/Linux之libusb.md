---
title: Linux之libusb
date: 2018-12-12 12:00:35
tags:
	- Linux

---

--

看btstack的源代码，我看的port版本是libusb版本的，最后是调用到libusb的函数进行的数据收发。

那么最后libusb里干了些什么呢？

源代码在这里：https://github.com/libusb/libusb

这里面有些简单的example可以看看。

lsusb这个命令就是基于libusb来做的。

Ubuntu下安装：

```
sudo apt-get install libusb-1.0-0-dev
```

链接的时候，加上-lusb-1.0就好。

需要包含的头文件是：

```
#include <libusb-1.0/libusb.h>
```

官网：https://libusb.info/

libusb是一个跨平台的用户态的库，用来访问usb设备。

当前版本是1.0。之前的版本0.1 ，这个版本已经过时了。

需要Linux支持usbfs。

代码在这里：

Https://github.com/libusb/libusb



这种新的协议的问题一般是采用后者来实现，

因为内核主线是不会采纳不通用的驱动代码的。

所以为了不一直为所有的版本内核都添加自己的驱动，可以在用户空间直接USB通信。

这才是大家都好的结局。

 这个时候大家猛然发现已经在内核中实现的基于printer协议的打印驱动程序也可以采用这个方法直接在用户空间USB通信实现，

这样就可以完全和系统无关了，内核只要有usb通信协议就好了。

上半场已经捋顺了，下面说说下半场。

方向明确了，如何实现，这时候大家发现了libusb，

libusb可以实现用户空间直接和usb设备直接通信。

这样大家都采用了基于libusb的免驱模式，如实说就是免掉内核中的驱动模式。



Linux 平台上的usb驱动开发，主要有内核驱动的开发和基于libusb的无驱设计。

*libusb是基于用户空间的usb库。

*libusb* 设计了一系列的外部*API* 为应用程序所调用，

通过这些*API*应用程序可以操作硬件，

从*libusb*的源代码可以看出，

这些*API* 调用了内核的底层接口，

和*kernel driver*中所用到的函数所实现的功能差不多，

**只是*libusb*更加接近*USB* 规范。使得*libusb*的使用也比开发内核驱动相对容易的多。**





usb驱动分为通过usbfs操作设备的用户空间驱动，内核空间的内核驱动。

两者不能同时进行，否则容易引发对共享资源访问的问题，死锁！使用了内核驱动，就不能在usbfs里驱动该设备。

libusb中须要先detach内核驱动后，才能claim interface，否则claim会返回的vice busy的错误。

如果你不dettach，也不claim interface，也能使用libusb对设备进行访问，但是，容易导致内核usbfs瘫痪，这是不允许的。



# 简介

| 名称     | libusb                                                   |
| -------- | -------------------------------------------------------- |
| 类型     | 库                                                       |
| 概述     | libusb是一个用于在用户空间操作USB设备的开源库。          |
| 特点     | 跨平台，支持Linux、macOS、Windows等操作系统。            |
|          | 提供简单易用的API，方便开发人员对USB设备进行控制和通信。 |
|          | 不需要特权权限或者特殊的驱动程序即可使用。               |
| 主要功能 | 1. 发现和枚举USB设备。                                   |
|          | 2. 打开和关闭USB设备。                                   |
|          | 3. 控制USB设备的端点进行数据的读写。                     |
|          | 4. 提供异步I/O接口。                                     |
|          | 5. 支持控制传输、批量传输和中断传输等数据传输类型。      |
|          | 6. 支持USB设备描述符的解析。                             |
| 使用案例 | 1. USB设备调试和测试。                                   |
|          | 2. USB设备驱动程序的开发。                               |
|          | 3. USB设备固件的升级。                                   |
|          | 4. USB设备与计算机之间的数据通信。                       |
|          | 5. USB设备的监控和控制。                                 |



libusb 是一个 C 库，提供对 USB 设备的通用访问。它旨在供开发人员用来促进与 USB 硬件通信的应用程序的生成。

它是可移植的：使用单个跨平台 API，它可以访问 Linux、macOS、Windows 等上的 USB 设备。

==它是用户模式：应用程序与设备通信不需要特殊权限或提升。==

它与版本无关：支持所有版本的 USB 协议，从 1.0 到 3.1（最新）。



如果您使用的是 Linux，那么您的发行版很可能已经包含 libusb，因此您可能只需要在源代码中引用 libusb 标头即可。

对于其他平台，或者如果您想使用最新版本，我们鼓励您从源代码重新编译。请检查下载菜单。

如果您愿意，也可以直接从 github 访问源代码。

一旦您确保了对库及其标头的访问，请检查 libusb API 或 libusb 示例。

## 库的特点

- 支持所有传输类型（控制/批量/中断/等时）
- 2个传输接口：
  - 同步（简单）
  - 异步（更复杂，但更强大）
- 线程安全（尽管异步接口意味着您通常不需要线程）
- 轻量级的精益 API
- 通过 libusb-compat-0.1 翻译层与 libusb-0.1 兼容
- 热插拔支持（在某些平台上）。请参阅设备热插拔事件通知。



# api文档

## debug

libusb 使用 stderr 进行所有日志记录。

默认情况下，日志记录设置为 NONE，这意味着不会生成任何输出。

但是，除非在禁用日志记录的情况下编译库，否则任何对 libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, level) 的应用程序调用或应用程序外部环境变量 LIBUSB_DEBUG 的设置都可能导致生成日志记录。

因此，您的应用程序不应关闭 stderr，而应将其定向到空设备（如果其输出不合需要）。

libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, level) 函数可用于启用某些消息的日志记录。

==在标准配置下，libusb 并不真正记录太多信息，因此建议您使用此功能来启用所有错误/警告/信息消息。==

它将有助于调试软件的问题。

记录的消息是非结构化的。

记录的消息与 libusb 函数的成功或失败返回代码之间没有一一对应的关系。

==消息没有格式，因此您不应尝试捕获或解析它们。==

它们没有也不会被本地化。

这些消息无意传递给您的应用程序用户；

相反，您应该解释从 libusb 函数返回的错误代码并向用户提供适当的通知。

这些消息只是为了帮助您作为一名程序员，如果您因为从 libusb 函数中收到奇怪的错误代码而感到困惑，那么启用消息记录可能会给您一个合适的解释。

LIBUSB_DEBUG 环境变量可用于在运行时启用消息日志记录。

该环境变量应设置为日志级别号，其解释与 libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, level) 参数相同。

设置此环境变量后，消息记录详细级别将被固定，并且 libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, level) 实际上不执行任何操作。

libusb 可以在没有任何日志记录功能的情况下进行编译，这对于嵌入式系统很有用。

在这种情况下，libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, level) 和 LIBUSB_DEBUG 环境变量不起作用。

libusb 也可以始终使用详细的调试消息进行编译。

当以这种方式编译库时，所有详细程度的所有消息都会被记录。 libusb_set_option(ctx, LIBUSB_OPTION_LOG_LEVEL, level) 和 LIBUSB_DEBUG 环境变量没有影响。

## 模块

| 模块             | 函数/结构体                                                  | 说明                                                         |
| ---------------- | ------------------------------------------------------------ | ------------------------------------------------------------ |
| 初始化和去初始化 | libusb_init                                                  |                                                              |
|                  | libusb_exit                                                  |                                                              |
|                  | libusb_set_log_cb                                            |                                                              |
|                  | libusb_set_debug                                             |                                                              |
|                  | libusb_set_option                                            |                                                              |
|                  | libusb_context                                               | 结构体。<br />表示 libusb 会话的结构。可以同时开多个会话。会话由 libusb_init() 创建并通过 libusb_exit() 销毁。 |
| 设备处理和枚举   | libusb_device                                                | 结构体。<br />表示系统上检测到的 USB 设备的结构。<br />这是一种不透明类型，您只能获得一个指针，通常源自 libusb_get_device_list() 或 libusb_hotplug_register_callback()。<br />某些操作可以在设备上执行，但为了执行任何 I/O，您必须首先使用 libusb_open() 获取设备句柄。<br />设备使用 libusb_ref_device() 和 libusb_unref_device() 进行引用计数，并在引用计数达到 0 时释放。 libusb_get_device_list() 提供的新设备的引用计数为 1，并且 libusb_free_device_list() 可以选择减少所有设备上的引用计数在列表中。 libusb_open() 添加了另一个引用，该引用随后被 libusb_close() 销毁。 |
|                  | libusb_device_handle                                         | 结构体。<br />表示 USB 设备上的句柄的结构。这是一种不透明类型，您只能获得一个指针，通常源自 libusb_open()。设备句柄用于执行 I/O 和其他操作。完成设备句柄后，您应该调用 libusb_close()。 |
|                  | libusb_get_device_list<br />libusb_free_device_list          |                                                              |
|                  | libusb_get_bus_number                                        |                                                              |
|                  | libusb_get_port_number                                       |                                                              |
|                  | libusb_get_port_numbers                                      |                                                              |
|                  | libusb_get_port_path                                         |                                                              |
|                  | libusb_get_parent                                            |                                                              |
|                  | libusb_get_device_address                                    |                                                              |
|                  | libusb_get_device_speed                                      |                                                              |
|                  | libusb_get_max_packet_size                                   |                                                              |
|                  | libusb_get_max_iso_packet_size                               |                                                              |
|                  | libusb_ref_device<br />libusb_unref_device                   |                                                              |
|                  | libusb_wrap_sys_device                                       |                                                              |
|                  | libusb_open<br />libusb_open_device_with_vid_pid             |                                                              |
|                  | libusb_close                                                 |                                                              |
|                  | libusb_get_device                                            |                                                              |
|                  | libusb_get_configuration<br />libusb_set_configuration       |                                                              |
|                  | libusb_claim_interface                                       |                                                              |
|                  | libusb_release_interface                                     |                                                              |
|                  | libusb_set_interface_alt_setting                             |                                                              |
|                  | libusb_clear_halt                                            |                                                              |
|                  | libusb_reset_device                                          |                                                              |
|                  | libusb_kernel_driver_active                                  |                                                              |
|                  | libusb_detach_kernel_driver                                  |                                                              |
|                  | libusb_attach_kernel_driver                                  |                                                              |
|                  | libusb_set_auto_detach_kernel_driver                         |                                                              |
| misc             | libusb_has_capbility                                         |                                                              |
|                  | libusb_error_name                                            |                                                              |
|                  | libusb_get_version                                           |                                                              |
|                  | libusb_cpu_to_le16                                           |                                                              |
|                  | libusb_setlocale                                             |                                                              |
|                  | libusb_strerror                                              |                                                              |
| usb描述符        |                                                              | 有10来个descriptor的结构体定义。<br />以及配套的函数。就不一一列举了。 |
| 热插拔通知       | 枚举                                                         | libusb_hotplug_event<br />libusb_hotplug_flag                |
|                  | 函数                                                         |                                                              |
|                  | libusb_hotplug_register_callback                             |                                                              |
|                  | libusb_hotplug_deregister_callback                           |                                                              |
|                  | libusb_hotplug_get_user_data                                 |                                                              |
| 异步设备io       | 结构体                                                       |                                                              |
|                  | libusb_control_setup                                         |                                                              |
|                  | libusb_iso_packet_descriptor                                 |                                                              |
|                  | libusb_transfer                                              |                                                              |
|                  | 枚举                                                         |                                                              |
|                  | libusb_transfer_type                                         |                                                              |
|                  | libusb_transfer_status                                       |                                                              |
|                  | libusb_transfer_flags                                        |                                                              |
|                  | 函数                                                         |                                                              |
|                  | libusb_alloc_streams<br />libusb_free_streams                |                                                              |
|                  | libusb_dev_mem_alloc<br />libusb_dev_mem_free                |                                                              |
|                  | libusb_alloc_transfer<br />libusb_free_transfer              |                                                              |
|                  | libusb_submit_transfer<br />libusb_cancel_transfer           |                                                              |
|                  | libusb_transfer_set_stream_id<br />libusb_transfer_get_stream_id |                                                              |
|                  | libusb_control_transfer_get_data<br />libusb_control_transfer_get_setup |                                                              |
|                  | libusb_fill_control_setup<br />libusb_fill_control_transfer<br />libusb_fill_bulk_transfer<br />libusb_fill_bulk_stream_transfer<br />libusb_fill_interrupt_transfer<br />libusb_fill_iso_transfer |                                                              |
| poll             | 结构体                                                       |                                                              |
|                  | libusb_pollfd                                                |                                                              |
|                  | 函数                                                         |                                                              |
|                  | libusb_try_lock_events<br />libusb_lock_events<br />libusb_unlock_events |                                                              |
|                  |                                                              |                                                              |
|                  |                                                              |                                                              |
| 同步设备io       | 就3个函数                                                    |                                                              |
|                  | libusb_control_transfer                                      |                                                              |
|                  | libusb_bulk_transfer                                         |                                                              |
|                  | libusb_interrupt_transfer                                    |                                                              |











## 数据结构

| 结构体                                     | 说明 |
| ------------------------------------------ | ---- |
| libusb_bos_descriptor                      |      |
| libusb_bos_dev_capability_descriptor       |      |
| libusb_config_descriptor                   |      |
| libusb_container_id_descriptor             |      |
| libusb_control_setup                       |      |
| libusb_device_descriptor                   |      |
| libusb_endpoint_descriptor                 |      |
| libusb_interface                           |      |
| libusb_interface_descriptor                |      |
| libusb_iso_packet_descriptor               |      |
| libusb_pollfd                              |      |
| libusb_ss_endpoint_companion_descriptor    |      |
| libusb_ss_usb_device_capability_descriptor |      |
| libusb_transfer                            |      |
| libusb_usb_2_0_extension_descriptor        |      |
| libusb_version                             |      |

https://libusb.sourceforge.io/api-1.0/

# libusb实现与板端的通信



https://xilinx.eetrend.com/blog/2021/100556402.html



# Rockchip RK3399 - linux通过libusb读取usb数据包

新建`hid_keyboard_mouse.sh`脚本：

```shell
#!/bin/bash

gadget=g1

do_start(){
    has_mount=$(mount -l | grep /sys/kernel/config)
    if [[ -z  $has_mount ]];then
        mount -t configfs none /sys/kernel/config
    fi
    cd /sys/kernel/config/usb_gadget

    # 当我们创建完这个文件夹之后，系统自动的在这个文件夹中创建usb相关的内容 ，这些内容需要由创建者自己填写
    if [[ ! -d ${gadget} ]]; then
        mkdir ${gadget}
    else
    	exit 0
    fi
    cd ${gadget}

    #设置USB协议版本USB2.0
    echo 0x0200 > bcdUSB

    #定义产品的VendorID和ProductID
    echo "0x0525"  > idVendor
    echo "0xa4ac" > idProduct

    #实例化"英语"ID：
    mkdir strings/0x409

    #将开发商、产品和序列号字符串写入内核
    echo "76543210" > strings/0x409/serialnumber
    echo "mkelehk"  > strings/0x409/manufacturer
    echo "keyboard_mouse"  > strings/0x409/product

    #创建一个USB配置实例
    if [[ ! -d configs/c.1 ]]; then
        mkdir configs/c.1
    fi

    #定义配置描述符使用的字符串
    if [[ ! -d configs/c.1/strings/0x409 ]]; then
        mkdir configs/c.1/strings/0x409
    fi

    echo "hid" > configs/c.1/strings/0x409/configuration

    #创建功能实例，需要注意的是，一个功能如果有多个实例的话，扩展名必须用数字编号：
    mkdir functions/hid.0   #键盘
    mkdir functions/hid.1   #鼠标
    mkdir functions/hid.2   #触摸屏

    #配置hid描述符
    echo 1 > functions/hid.0/subclass   #标识仅有一个接口描述符
    echo 1 > functions/hid.0/protocol   #标识键盘设备
    echo 8 > functions/hid.0/report_length  #标识该hid设备每次发送的报表长度为8字节
    echo -ne \\x05\\x01\\x09\\x06\\xa1\\x01\\x05\\x07\\x19\\xe0\\x29\\xe7\\x15\\x00\\x25\\x01\\x75\\x01\\x95\\x08\\x81\\x02\\x95\\x01\\x75\\x08\\x81\\x03\\x95\\x05\\x75\\x01\\x05\\x08\\x19\\x01\\x29\\x05\\x91\\x02\\x95\\x01\\x75\\x03\\x91\\x03\\x95\\x06\\x75\\x08\\x15\\x00\\x25\\x65\\x05\\x07\\x19\\x00\\x29\\x65\\x81\\x00\\xc0 > functions/hid.0/report_desc

    echo 1 > functions/hid.1/subclass
    echo 2 > functions/hid.1/protocol
    echo 4 > functions/hid.1/report_length
    echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x03\\x15\\x00\\x25\\x01\\x95\\x03\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x05\\x81\\x03\\x05\\x01\\x09\\x30\\x09\\x31\\x09\\x38\\x15\\x81\\x25\\x7f\\x75\\x08\\x95\\x03\\x81\\x06\\xc0\\xc0 > functions/hid.1/report_desc

    #配置hid描述符
    echo 0 > functions/hid.2/subclass
    echo 0 > functions/hid.2/protocol
    echo 5 > functions/hid.2/report_length  #标识该hid设备每次发送的报表长度为5字节
    echo -ne \\x05\\x01\\x09\\x02\\xa1\\x01\\x09\\x01\\xa1\\x00\\x05\\x09\\x19\\x01\\x29\\x05\\x15\\x00\\x25\\x01\\x95\\x05\\x75\\x01\\x81\\x02\\x95\\x01\\x75\\x03\\x81\\x01\\x05\\x01\\x09\\x30\\x09\\x31\\x15\\x00\\x26\\xff\\x7f\\x35\\x00\\x46\\xff\\x7f\\x75\\x10\\x95\\x02\\x81\\x02\\xc0\\xc0 > functions/hid.2/report_desc

    #捆绑功能实例到配置config.1
    ln -s functions/hid.0 configs/c.1
    ln -s functions/hid.1 configs/c.1
    ln -s functions/hid.2 configs/c.1

    #配置USB3.0/2.0 OTG0的工作模式为Device（设备）：
    #echo peripheral > /sys/devices/platform/ff770000.syscon/ff770000.syscon:usb2-phy@e460/otg_mode

    echo "sleep 3s"
    sleep 3s

    #将gadget驱动注册到UDC上，插上USB线到电脑上，电脑就会枚举USB设备。
    echo fe900000.dwc3 > UDC
}

do_stop() {
    cd /sys/kernel/config/usb_gadget/${gadaget}
    echo "" > UDC
}

case $1 in
    start)
        echo "Start hid gadget "
        do_start
        ;;
    stop)
        echo "Stop hid gadget"
        do_stop
        ;;
    *)
        echo "Usage: $0 (stop | start)"
        ;;
esac

```



https://www.cnblogs.com/zyly/p/17766017.html



# libusb可以实现哪些设备驱动

libusb可以用于实现各种USB设备的用户空间驱动程序，包括但不限于以下类型的设备：

1. **外围设备**：例如打印机、扫描仪、摄像头、键盘、鼠标等。

2. **存储设备**：例如闪存驱动器、硬盘、U盘等。

3. **网络设备**：例如USB网卡、调制解调器等。

4. **音频设备**：例如USB麦克风、扬声器、音频接口等。

5. **视频设备**：例如USB摄像头、视频采集卡等。

6. **传感器设备**：例如温度传感器、湿度传感器、加速度计等。

7. **嵌入式设备**：例如开发板、单片机调试器等。

8. **自定义设备**：任何符合USB规范的自定义设备。

总的来说，只要是符合USB规范的设备，libusb都可以用来进行驱动开发和控制。

## libusb实现鼠标设备驱动说明

要使用libusb实现鼠标设备的用户空间驱动程序，你可以按照以下步骤进行：

1. **初始化libusb**：在程序开始时，调用`libusb_init`函数初始化libusb库。

2. **获取设备列表**：使用`libusb_get_device_list`函数获取系统中已连接的USB设备列表。

3. **遍历设备列表**：遍历设备列表，找到描述鼠标设备的USB设备。可以通过`libusb_get_device_descriptor`函数获取设备的描述符信息，通常鼠标设备的描述符会包含指定的设备类别。

4. **打开鼠标设备**：使用`libusb_open`函数打开找到的鼠标设备，获取一个设备句柄用于后续的操作。

5. **Claim接口**：调用`libusb_claim_interface`函数请求对鼠标设备的接口进行独占性访问。

6. **进行数据传输**：使用`libusb_interrupt_transfer`函数进行中断传输操作，从鼠标设备读取输入数据。通常，鼠标设备会以中断传输的方式发送鼠标移动和点击等事件。

7. **处理数据**：解析从鼠标设备读取的数据，根据鼠标协议解释鼠标移动、点击等事件，并进行相应的处理。

8. **关闭设备和释放资源**：在程序结束时，调用`libusb_release_interface`函数释放对鼠标设备接口的独占性访问，并使用`libusb_close`函数关闭设备。最后调用`libusb_exit`函数关闭libusb库并释放资源。

通过这些步骤，你可以实现一个简单的libusb驱动程序来控制鼠标设备。需要注意的是，鼠标设备的数据格式和通信协议可能因厂商而异，你需要根据具体的鼠标设备规格来解析数据并实现相应的功能。

### 代码

以下是一个简单的C语言示例代码，演示了如何使用libusb实现一个简单的鼠标设备驱动程序来监听鼠标事件：

```c
#include <stdio.h>
#include <stdlib.h>
#include <libusb-1.0/libusb.h>

#define VENDOR_ID 0x046d    // Logitech厂商ID
#define PRODUCT_ID 0xc077   // Logitech无线鼠标产品ID

#define ENDPOINT_ADDR 0x81  // 鼠标数据输入端点地址
#define INTERFACE_NUM 0     // 鼠标设备接口号

#define DATA_SIZE 4         // 鼠标数据包大小

int main() {
    libusb_context *ctx = NULL;
    libusb_device_handle *handle = NULL;
    unsigned char data[DATA_SIZE];
    int transferred;
    int ret;

    // 初始化libusb
    ret = libusb_init(&ctx);
    if (ret < 0) {
        fprintf(stderr, "Failed to initialize libusb\n");
        return 1;
    }

    // 打开鼠标设备
    handle = libusb_open_device_with_vid_pid(ctx, VENDOR_ID, PRODUCT_ID);
    if (handle == NULL) {
        fprintf(stderr, "Failed to open device\n");
        libusb_exit(ctx);
        return 1;
    }

    // Claim接口
    ret = libusb_claim_interface(handle, INTERFACE_NUM);
    if (ret < 0) {
        fprintf(stderr, "Failed to claim interface\n");
        libusb_close(handle);
        libusb_exit(ctx);
        return 1;
    }

    printf("Listening for mouse events...\n");

    // 进入事件监听循环
    while (1) {
        // 从鼠标设备读取数据
        ret = libusb_interrupt_transfer(handle, ENDPOINT_ADDR, data, sizeof(data), &transferred, 0);
        if (ret == 0 && transferred == DATA_SIZE) {
            // 解析鼠标数据
            int x = data[1];
            int y = data[2];
            int button = data[0] & 0x07;

            // 打印鼠标事件
            printf("Mouse event: X=%d, Y=%d, Button=%d\n", x, y, button);
        } else {
            fprintf(stderr, "Error reading mouse data\n");
            break;
        }
    }

    // 释放资源
    libusb_release_interface(handle, INTERFACE_NUM);
    libusb_close(handle);
    libusb_exit(ctx);

    return 0;
}
```

这个示例代码使用了libusb库来监听连接到计算机上的Logitech无线鼠标，并在控制台输出鼠标的移动和按键事件。你可以根据实际需要修改厂商ID、产品ID以及数据解析部分的代码来适配你的鼠标设备。



# 使用了libusb的项目有哪些

基于 libusb 的项目有很多，以下是一些常见的基于 libusb 的项目示例：

1. **usbview**：一个简单的 Linux USB 设备查看器，使用 libusb 实现了对 USB 设备的检测和信息显示功能。

2. **OpenOCD**：一个开源的调试和编程工具，用于嵌入式系统开发。它使用 libusb 与目标设备进行通信，支持多种不同的调试接口和芯片。

3. **dfu-util**：一个命令行工具，用于将固件上传到设备的内部存储器，例如使用 USB 设备固件升级（DFU）模式的设备。它使用 libusb 实现了与设备的通信。

4. **sigrok**：一个开源的信号分析软件套件，用于采集、解码和分析各种测试设备的数据。它使用 libusb 实现了与支持的硬件设备进行通信。

5. **QMK Firmware**：一个开源的键盘固件，用于 DIY 机械键盘。它使用 libusb 实现了与计算机的通信，支持通过 USB 连接到计算机，并支持各种高级键盘功能。

6. **gr-limesdr**：一个开源的软件无线电（SDR）框架，用于与 LimeSDR 系列硬件设备进行通信。它使用 libusb 实现了与 LimeSDR 设备的通信和控制。

7. **NeTV2**：一个开源的 HDMI 输入/输出板，用于视频捕获和处理。它使用 libusb 实现了与计算机的通信和控制，支持从计算机接收命令并将视频流传输到计算机。

这些项目只是基于 libusb 的众多应用之一，libusb 作为一个功能强大且广泛应用的开源库，在各种嵌入式、嵌入式系统、软件无线电和USB通信领域都有着广泛的应用。





# 参考资料

1、官方wiki

https://github.com/libusb/libusb/wiki

2、使用usbfs与内核驱动之间的冲突

https://blog.csdn.net/crazyleen/article/details/7062327

3、Libusb简介及例子

https://blog.csdn.net/hfyutdg/article/details/83896116

4、libusb的嵌入式移植

https://blog.csdn.net/tianruxishui/article/details/37903579

5、libusb函数说明

很好。

https://blog.csdn.net/wince_lover/article/details/70337809