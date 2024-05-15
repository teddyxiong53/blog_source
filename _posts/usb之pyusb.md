---
title: usb之pyusb
date: 2024-05-14 14:46:11
tags:
	- usb
---

--

`pyusb`是一个Python库，用于与USB设备进行通信。

它提供了一种简单而有效的方法来访问和控制USB设备，

使得在Python中进行USB设备的开发变得更加容易。

以下是`pyusb`库的一些主要特点和用法：

- **跨平台性：** `pyusb`可在多个操作系统上运行，包括Windows、Linux和macOS等。
  
- **USB设备访问：** 可以使用`pyusb`来枚举已连接的USB设备、获取设备描述符、配置设备、发送控制命令等。

- **简单易用：** `pyusb`提供了简单的API，使得在Python中进行USB通信变得更加容易。

- **支持USB原生层级：** `pyusb`直接与USB原生层级进行交互，允许开发人员直接控制设备的底层功能。

- **与其他Python库兼容：** `pyusb`可以与其他Python库结合使用，例如在图形界面应用程序中与Tkinter或PyQt结合使用。

- **开源：** `pyusb`是开源项目，可以根据需要进行定制和扩展。

下面是一个简单的示例，展示了如何使用`pyusb`库来枚举已连接的USB设备：

```python
import usb.core

# 枚举所有USB设备
def enumerate_usb_devices():
    # 使用pyusb库查找所有USB设备
    devices = usb.core.find(find_all=True)
    # 遍历并输出每个设备的描述信息
    for device in devices:
        print("设备信息：")
        print("  设备厂商ID: 0x{:04x}".format(device.idVendor))
        print("  设备产品ID: 0x{:04x}".format(device.idProduct))
        print("  设备类别: {}".format(device.bDeviceClass))
        print("  设备子类别: {}".format(device.bDeviceSubClass))
        print("  设备协议: {}".format(device.bDeviceProtocol))
        print("  设备配置数量: {}".format(device.bNumConfigurations))
        print()
    
# 示例用法
if __name__ == "__main__":
    enumerate_usb_devices()
```

这只是`pyusb`库的一个简单示例。你可以使用`pyusb`来执行更高级的USB设备操作，如发送控制命令、读取设备数据等。

# 从readme总结的内容

PyUSB为Python 3提供了对主机的通用串行总线（USB）系统的轻松访问。

在0.4版本之前，PyUSB曾经是libusb上的一个瘦包装器。

从1.0版本开始，事情发生了很大的变化：

现在PyUSB是一个API丰富，后端中立的Python USB模块，易于使用。

PyUSB主要在Linux和Windows上开发和测试，

但它也应该在任何运行Python >= 3.8，

ctypes和至少一个内置后端的平台上正常工作。

PyUSB支持libusb 1.0、libusb 0.1和OpenUSB。其中，libusb 1.0目前被推荐用于大多数用例。

与用C编写的0.x版本不同，1.0版本是用Python编写的。这使得没有C背景的Python程序员能够更好地理解PyUSB的工作原理。

1.0版本实现了前端-后端方案。

这将API与系统特定的实现细节隔离开来。

两层之间的粘合剂是 `IBackend` 接口。

PyUSB附带了libusb 1.0、libusb 0.1和OpenUSB的内置后端。

如果你愿意，你可以写自己的后端。

与USB设备通信从未如此简单！USB是一个复杂的协议，但PyUSB对于大多数常见配置都有很好的默认值。

如果底层后端支持的话，PyUSB支持*isochronous* 传输。

首先，让我们给予一个关于PyUSB模块的概述。PyUSB模块在 `usb` 包下，包含以下模块：

| Content | Description                                                  |
| ------- | ------------------------------------------------------------ |
| core    | The main USB module. USB主模块。                             |
| util    | Utility functions. 工具函数。                                |
| control | Standard control requests. 标准控制请求。                    |
| legacy  | The 0.x compatibility layer. 0.x兼容层。                     |
| backend | A subpackage containing the builtin backends. 包含内置后端的子包。 |

例如，要导入 `core` 模块，请键入以下内容：

```
>>> import usb.core
>>> dev = usb.core.find()
```



```
import usb.core
import usb.util

dev = usb.core.find(idVendor=0xfffe, idProduct=0x0001)

if dev is None:
    raise ValueError('deivce not found')
dev.set_configuration()

cfg = dev.get_active_configuration()

intf = cfg[(0,0)]
def my_custom_match(e):
    return usb.util.endpoint_direction(e.bEndpointAddress) == usb.util.ENDPOINT_OUT
ep = usb.util.find_descriptor(
    itf,
    custom_match=my_custom_match
)
assert ep is not None
ep.write('test')

```



前两行导入PyUSB包模块。

 `usb.core` 是主模块， `usb.util` 包含实用功能。

下一个命令搜索我们的设备，如果找到了，返回一个实例对象。

如果没有，返回 `None` 。

之后，我们设置要使用的配置。

请注意，没有提供指示我们需要什么配置的参数。

正如您将看到的，许多PyUSB函数对于大多数常见设备都有默认值。

在这种情况下，配置集是找到的第一个配置集。



PyUSB中的每个函数在出现错误时都会引发异常。

除了Python标准异常之外，PyUSB还为USB相关错误定义了 `usb.core.USBError` 。

您还可以使用PyUSB日志功能。

它使用logging模块。

要启用它，请使用以下级别名称之一定义环境变量 `PYUSB_DEBUG` ： `critical` 、 `error` 、 `warning` 、 `info` 或 `debug` 。

默认情况下，消息被发送到sys.stderr。

如果需要，可以通过定义 `PYUSB_LOG_FILENAME` 环境变量将日志消息重定向到文件。

如果它的值是一个有效的文件路径，消息将被写入它，否则它将被发送到 `sys.stderr` 。



https://github.com/pyusb/pyusb