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



参考资料

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