---
title: Linux之udev规则文件
date: 2017-08-05 14:48:45
tags:
	- Linux
---

--

udev的工作是靠kernel发出的uevent来驱动的，如果是删除的uevent，就会删除对应的节点。如果是增加设备的uevent，就会增加对应的节点。

规则文件是放在/etc/udev/rules.d目录下的。下面的文件命名规则是：xx-yy.rules。xx是数字，yy是字母，后缀都是rules。

执行时，先看数字，后看字母，后执行的会覆盖先执行的。

每一行代表一个规则，由多个键值对。

一个例子

```
SUBSYSTEM=="udc",ACTION=="change",DRIVER=="configfs-gadget",RUN+="/usr/bin/usbdevice %E{DEVPATH}"
```



```
常用匹配键：
    * KERNEL     - 匹配设备在内核中的命名
    * SUBSYSTEM  - 匹配设备(在sysfs中)的subsystem名
    * DRIVER     - 匹配设备对应的驱动名
    * ATTR       - 匹配设备在sysfs中属性
    * KERNELS    - 匹配设备及其父亲在内核中的命名
    * SUBSYSTEMS - 匹配设备及其父亲(在sysfs中)的subsystem名
    * DRIVERS    - 匹配设备及其父亲对应的驱动名
    * ATTRS      - 匹配设备及其父亲在sysfs中属性
      注：父亲表示直到最上层的所有祖先

常用赋值键：
    * NAME - 设备节点名
    * SYMLINK - 指向设备节点的符号连接列表
```



多个相同设备会出现相同的产品号和相同的设备号，系统就无法与其中的一个设备进行绑定

为了解决多设备问题，可以利用usb串口id进行区分两个设备

执行这个命令：

```
udevadm info --attribute-walk --name=/dev/ttyUSB0
```

简单一点这样：

```
udevadm info /dev/ttyUSB0
```

现在需要达到的目的，就是插在某个口上的设备，只要不换口，就固定为某个名字。不管中间是否有插拔，不管电脑是否重启。

```
ID_PATH=pci-0000:00:14.0-usb-0:2.1:1.0
```

这个字符串，具体怎么理解？

我把usb，从一个口插到另外一个口上后，可以发现数字上是有一点变化的。

```
E: ID_PATH=pci-0000:00:14.0-usb-0:2.1:1.0
E: ID_PATH=pci-0000:00:14.0-usb-0:2.4:1.0
```



```
SUBSYSTEM=="tty", ENV{ID_PATH}=="pci-0000:00:14.0-usb-0:1.1:1.0", MODE:="0666", SYMLINK+="S420_powerRelay"
```

SYMLINK+="S420_powerRelay" 这个不要写成SYMLINK+="/dev/S420_powerRelay"

这样会生成到：

```
/dev/dev/S420_powerRelay"
```



所以， 可以将devpath 属性作为区分每个设备的关键词

# 分析一行配置

```
ACTION=="add", SUBSYSTEM=="usb", ATTRS{idVendor}=="1234", ATTRS{idProduct}=="5678", RUN+="/path/to/script.sh"
这一行分析
```

这行 udev 规则的含义如下：

- `ACTION=="add"`：这个条件表示当设备被添加到系统时触发规则，即设备插入时执行规则动作。
- `SUBSYSTEM=="usb"`：这个条件表示匹配 USB 子系统的设备，即只有 USB 设备才会触发规则。
- `ATTRS{idVendor}=="1234"`：这个条件表示设备的 `idVendor` 属性必须等于 "1234"，即匹配特定的 USB 设备的 Vendor ID。
- `ATTRS{idProduct}=="5678"`：这个条件表示设备的 `idProduct` 属性必须等于 "5678"，即匹配特定的 USB 设备的 Product ID。
- `RUN+="/path/to/script.sh"`：这个规则动作指定在匹配的设备上运行脚本 `/path/to/script.sh`。

综合起来，这条规则的意思是当一个 USB 设备插入系统并且其 Vendor ID 为 "1234"，Product ID 为 "5678" 时，会执行 `/path/to/script.sh` 脚本。

这个规则可以用于特定 USB 设备的自动化处理。当匹配的设备插入系统时，系统会自动执行指定的脚本，以便进行一些特定的操作或配置，例如挂载设备、启动相关服务、执行备份等。

# ACTION有哪些取值

在 udev 规则中，`ACTION` 是一个用于匹配设备操作的条件之一。它可以使用不同的取值来指定特定的设备操作类型。以下是常见的 `ACTION` 取值：

- `add`：表示设备被添加到系统，即设备插入时触发规则。
- `remove`：表示设备从系统中移除，即设备拔出时触发规则。
- `change`：表示设备的属性或状态发生变化，即设备状态变化时触发规则。
- `move`：表示设备的位置或路径发生变化，即设备移动时触发规则。
- `bind`：表示设备与驱动程序绑定，即设备与驱动程序关联时触发规则。
- `unbind`：表示设备与驱动程序解绑，即设备与驱动程序解除关联时触发规则。

这些取值用于指定在特定设备操作发生时应该触发的规则动作。根据实际需求，可以选择适当的 `ACTION` 取值来匹配所需的设备操作类型，并执行相应的规则动作。

# SUBSYSTEM有哪些取值

在 udev 规则中，`SUBSYSTEM` 是一个用于匹配设备子系统的条件之一。它用于指定规则应该应用于哪个设备子系统。以下是一些常见的 `SUBSYSTEM` 取值：

- `block`：表示块设备子系统，如硬盘、SSD、U盘等。
- `char`：表示字符设备子系统，如串口、终端设备等。
- `usb`：表示USB设备子系统。
- `net`：表示网络设备子系统，如以太网卡、Wi-Fi网卡等。
- `sound`：表示音频设备子系统。
- `input`：表示输入设备子系统，如键盘、鼠标、触摸板等。
- `video`：表示视频设备子系统，如摄像头、显示器等。
- `tty`：表示终端设备子系统，如终端控制台。
- `raw`：表示原始设备子系统。

除了上述常见的子系统，还有许多其他设备子系统可以在规则中使用。可以通过查看 `/sys/class/` 目录来确定系统上可用的设备子系统列表。

通过指定适当的 `SUBSYSTEM` 取值，可以将规则应用于特定的设备子系统，并执行相应的规则动作。这样可以实现针对特定类型设备的自定义操作和配置。

# 除了ACTION， SUBSYSTEM，还有什么配置项

除了 `ACTION` 和 `SUBSYSTEM`，在 udev 规则中还有其他常用的配置项。以下是一些常见的配置项：

- `KERNEL`：用于匹配设备的内核名称。可以使用通配符或正则表达式来匹配多个设备。
- `ATTR` 或 `ATTRS`：用于匹配设备的属性。可以指定设备的某个属性名称和对应的属性值来进行匹配。
- `ENV` 或 `ENVIRON`：用于匹配设备的环境变量。可以指定环境变量名称和对应的值来进行匹配。
- `DRIVERS`：用于匹配设备所使用的驱动程序。
- `TAG`：用于给设备打上标签，以便后续规则的匹配和处理。
- `MODE`：用于设置设备节点的权限模式。
- `SYMLINK`：用于创建设备节点的符号链接。
- `OWNER`：用于设置设备节点的所有者。
- `GROUP`：用于设置设备节点的所属组。
- `RUN` 或 `PROGRAM`：用于在匹配到的设备上运行外部脚本或程序。
- `RUN{key}`：用于在匹配到的设备上设置和传递自定义的环境变量。

这些配置项可以根据实际需求进行组合和使用，以实现对特定设备的操作、配置和管理。通过在规则中使用这些配置项，可以根据设备的属性、环境变量、驱动程序等信息，对设备进行更精确的匹配和处理。



# ACTION=="remove", GOTO="default_end"

在 udev 规则中，`GOTO` 是一个特殊的动作，用于控制规则的执行流程。当满足特定条件时，使用 `GOTO` 可以跳过当前规则并跳转到指定的标签位置继续执行。

在你提供的规则中，`ACTION=="remove", GOTO="default_end"` 表示当设备被移除时触发规则，并跳转到标签为 "default_end" 的位置继续执行后续规则。

这意味着当某个设备被移除时，系统会按顺序逐个匹配规则，当匹配到这条规则时，将跳过后续的规则并直接执行标签为 "default_end" 的位置处的规则。

通过使用 `GOTO`，可以根据特定的条件在规则中创建分支和跳转，以便根据需要执行不同的操作或跳过一些规则。这提供了更灵活的控制流程和规则的执行顺序。



# 参考资料

1、udev规则

http://blog.chinaunix.net/uid-26808060-id-4339831.html

2、Linux udev规则编写

https://blog.csdn.net/xiaoliu5396/article/details/46531893

3、

https://blog.csdn.net/zhangyuehuan/article/details/52946841

4、Ubuntu系统USB自定义名称与设备号绑定方法

https://blog.csdn.net/qq_31329259/article/details/112232180

5、【Ubuntu】绑定串口号

这个是我要的。

https://blog.csdn.net/qq_37946291/article/details/98881357