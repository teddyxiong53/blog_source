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

使用了libusb的项目有：

usbutils：Linux的usb工具包。

btstack：轻量级蓝牙协议栈。

libuvc

提供这些语言的binding

pyusb



这种新的协议的问题一般是采用后者来实现，因为内核主线是不会采纳不通用的驱动代码的。所以为了不一直为所有的版本内核都添加自己的驱动，可以在用户空间直接USB通信。这才是大家都好的结局。

 这个时候大家猛然发现已经在内核中实现的基于printer协议的打印驱动程序也可以采用这个方法直接在用户空间USB通信实现，这样就可以完全和系统无关了，内核只要有usb通信协议就好了。上半场已经捋顺了，下面说说下半场。

方向明确了，如何实现，这时候大家发现了libusb，libusb可以实现用户空间直接和usb设备直接通信。这样大家都采用了基于libusb的免驱模式，如实说就是免掉内核中的驱动模式。



Linux 平台上的usb驱动开发，主要有内核驱动的开发和基于libusb的无驱设计。

*libusb是基于用户空间的usb库。libusb* 设计了一系列的外部*API* 为应用程序所调用，通过这些*API*应用程序可以操作硬件，从*libusb*的源代码可以看出，这些*API* 调用了内核的底层接口，和*kernel driver*中所用到的函数所实现的功能差不多，**只是*libusb*更加接近*USB* 规范。使得*libusb*的使用也比开发内核驱动相对容易的多。**





usb驱动分为通过usbfs操作设备的用户空间驱动，内核空间的内核驱动。两者不能同时进行，否则容易引发对共享资源访问的问题，死锁！使用了内核驱动，就不能在usbfs里驱动该设备。

libusb中须要先detach内核驱动后，才能claim interface，否则claim会返回的vice busy的错误。

如果你不dettach，也不claim interface，也能使用libusb对设备进行访问，但是，容易导致内核usbfs瘫痪，这是不允许的。

# 简介

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