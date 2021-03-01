---
title: usb之复合设备
date: 2020-11-13 15:32:30
tags:
	- usb
---

--

复合型设备：

具有两种usb设备功能的一种设备，

无论是相同的设备功能，还是不同的设备功能，

只要同时具有两种以上的功能就是复合型设备。

现在就把hid keyboard and usb mass storage复合起来，组成一个设备。



首先要说的是既然是复合型设备，那么就有多个interface，

**这里有两个设备，那么就需要两个interface，**

需要几个设备描述符呢，一个就够了，

那配置描述符呢，也只需要一个就好了，

那需要几个端点描述符呢，这个嘛，我就不知道了（开玩笑，你在总结你不知道），这个就得讲讲usb的几种传输模式了。



在usb里面一共有四种传输：

控制传输、中断传输、批量传输、等时传输。

控制和批量端点用于异步的数据传输，驱动需要他们就立马工作。

中断和等时端点是周期性的，即在固定时间段连续的传输数据。

是不是有点熟悉，的确，前面总结过的，在这里再提提。

所以有几个端点，还是得看你在用哪种传输模式，

hid keyboard和usb mass storage他们使用的传输方式是中断传输和批量传输。



中断传输：interrupt in ,在这里只需要interrupt in就ok了，既只要一个端点，至于interrupt out就不用管了。

批量传输：bulk in和bulk out，**由于u盘是双向的，当然需要有两个端点哦，**毕竟他们通信要有来回才行啊。



所以要复合hid keyboard和usb mass storage就需要三个端点。

好了，前面说来复合型设备的描述符分别是：

`设备描述符*1+配置描述符*1+端点描述符*3`



那么到这里就完了吗，

如果只是usb mass storage，在加一个端点就完了，

但是这里是Hid,还需要一个子类，

在hid里面还有很多子类，那么就需要区分他们，不然host不知道你是哪家的，

好比有很多人叫张三，但是这个世界那么多是张三，你知道他应该是哪家的呢，还是只有slave主动说

自己是谁方便。

现在配置是设备描述符*1+配置描述符*1+端点描述符*3+**子类描述符**，

**但是描述符排列是有顺序的，写完一个在写另外一个。**



例如我们公司常用，

键盘 + 自定义HID  （HID Keyboard  + 自定义 Human Interface Device），如下图，在设备管理器可以看到

![img](../images/random_name/2018041313483541)

本来，一般这两种东西都是分别存在于两个HID 设备上，分两个硬件，如USB 键盘  和 USB 鼠标，但是，现在却存在于同一个硬件中。看上面的图应该非常直观。

用UsbTreeView 可以非常直观的看到



在hid 协议中，无论是单设备还是复合设备，操作系统都会根据设备的interface 设备描述符认为是独立的，即：

我们公司的产品复合设备是 - 键盘 + 自定义HID  （HID Keyboard  + 自定义 Human Interface Device），那么就会存在两个inerface ,

 则操作系统就会认为 上面 是两个独立的单设备，

无论是Windows或则是Linux 还是 Android 都会这样子识别。

因此，在编程时，获取设备的接口时就需要注意，要操作的设备号是哪个。



可以发现Android的各个方法与Linux 的libusb 的同名函数的参数相识，

因此，可以看出Android usb 底层应该是libusb,





参考资料

1、USB-HID设备中的复合设备

https://blog.csdn.net/gd6321374/article/details/79919917

2、USB复合设备（mass storage&hid）

https://blog.csdn.net/plauajoke/article/details/8537740