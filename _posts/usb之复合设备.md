---
title: usb之复合设备
date: 2020-11-13 15:32:30
tags:
	- usb
---

--

# 复合型设备

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



# usb通过configfs在rndis和adb、host和device之间切换

在Linux中，您可以使用`configfs`来配置USB功能，包括切换USB设备的功能模式，例如从RNDIS（Remote Network Driver Interface Specification）切换到ADB（Android Debug Bridge）模式，或者从设备模式切换到主机模式。

以下是一个简单的步骤示例，演示如何在`configfs`中切换USB功能：

1. 首先，确保您的Linux内核已启用`configfs`支持。您可以在内核配置中查找以下选项并启用它：
   ```
   CONFIG_CONFIGFS_FS=y
   ```

2. 接下来，加载`configfs`文件系统。您可以使用以下命令：
   ```
   sudo modprobe configfs
   ```

3. 创建USB功能配置的根目录：
   ```
   sudo mkdir /sys/kernel/config/usb_gadget
   cd /sys/kernel/config/usb_gadget
   ```

4. 创建USB设备并配置相关功能。这里我们以RNDIS和ADB为例。首先，创建一个新的USB设备目录：
   ```
   sudo mkdir my_usb_device
   cd my_usb_device
   ```

5. 为USB设备添加描述符文件：
   ```
   sudo mkdir functions/rndis.usb0
   sudo mkdir functions/ffs.adb
   ```

6. 在`configfs`中创建UDC（USB Device Controller）对象，并将设备绑定到UDC：
   ```
   sudo mkdir configs/c.1
   sudo ln -s functions/rndis.usb0 configs/c.1/
   sudo ln -s functions/ffs.adb configs/c.1/
   echo "123456789" | sudo tee functions/rndis.usb0/dev_addr
   echo "192.168.0.2" | sudo tee functions/rndis.usb0/host_addr
   echo ffs_adb > UDC
   ```

7. 这样就完成了USB设备的配置。您可以使用`lsusb`命令来查看USB设备是否正确配置。

8. 要切换USB设备的功能，您可以先解绑当前的UDC对象，然后重新绑定新的UDC对象。例如，要从RNDIS模式切换到ADB模式：
   ```
   sudo sh -c 'echo "" > /sys/kernel/config/usb_gadget/my_usb_device/configs/c.1/UDC'
   sudo sh -c 'echo ffs_adb > /sys/kernel/config/usb_gadget/my_usb_device/configs/c.1/UDC'
   ```

这些是简单的示例步骤，您可以根据具体的需求和场景进行调整和扩展。请注意，在实际应用中，可能需要更多的配置和参数设置。





USB Linux Gadget是一种具有UDC (USB设备控制器)的设备，

可以连接到USB主机，以扩展其附加功能，如串口或大容量存储能力。



一个gadget被它的主机视为一组配置，每个配置都包含一些接口，

从gadget的角度来看，这些接口被称为功能，每个功能代表一个串行连接或一个SCSI磁盘。



Linux提供了许多gadget可以使用的功能。

创建一个gadget意味着决定将有哪些配置以及每个配置将提供哪些功能。

Configfs(请参阅[Configfs—用户空间驱动的内核对象配置](https://www.cnblogs.com/wanglouxiaozi/p/15179719.html))非常适合告诉内核上述决定。

本文档是关于如何实现这一点的。它还描述了如何将configfs集成到gadget中。



# 配置步骤

## 首先是挂载：

```
mount -t configfs none /sys/kernel/config
```

## 然后是创建gadget

```
mkdir /sys/kernel/config/usb_gadget/g1
```

g1可以替换为你想要设置的gadget的名字。

然后我们进入到g1的目录下，写入下面这2个id，要改成跟自己实际厂商对应的id。

```
echo 0x1234 > idVendor
echo 0x2345 > idProduct
```

gadget还需要它的序列号、制造商和产品字符串。

为了有一个地方存储它们，必须为每种语言创建一个字符串子目录，例如:

```
mkdir strings/0x409
```

0x409表示英文目录。一般只要这个就够了。

然后在这个0x409目录下执行：

```
echo "12346780" > serialnumber
echo "xx" > manufacturer
echo "yy" > product
```

## 创建配置

还是在g1目录下：

```
mkdir configs/<name>.<number>
```

name可以是合法的文件名即可。number是配置的编号。

```
mkidr configs/c.1
```

每个配置也需要它的字符串，所以必须为每种语言创建一个子目录，例如:

```
mkdir configs/c.1/strings/0x409
```

然后指定配置字符串：

```
echo <configuration> > configs/c.1/strings/0x409/configuration
```

也可以为配置设置一下属性：

```
echo 120 > configs/c.1/MaxPower
```

## 创建功能

```
mkdir functions/<name>.<instance name>
```

name对应一个允许的功能的名字。

instance name是文件系统允许的任意字符串。

例如：

```
mkdir functions/ncm.usb0 
```

ncm对应usb_f_ncm.ko。

每个函数都提供其特定的属性集，具有只读或读写访问权限。如适用，需要酌情写入。更多信息请参考Documentation/ABI/testing/configfs-usb-gadget。

## 关联功能及其配置

此时，许多gadget被创建出来，

每个gadget都有一些指定的配置和一些可用的功能。

剩下的就是指定哪个功能在哪个配置中可用(同一个功能可以在多个配置中使用)。

这是通过创建符号链接来实现的:

```
ln -s functions/<name>.<instance name> configs/<name>.<number>
```

例如：

```
ln -s functions/ncm.usb0 configs/c.1
```

## 启用gadget

以上所有步骤的目的是组成gadget的配置和功能。

示例目录结构可能看起来像这样：

```
  .
  ./strings
  ./strings/0x409
  ./strings/0x409/serialnumber
  ./strings/0x409/product
  ./strings/0x409/manufacturer
  ./configs
  ./configs/c.1
  ./configs/c.1/ncm.usb0 -> ../../../../usb_gadget/g1/functions/ncm.usb0
  ./configs/c.1/strings
  ./configs/c.1/strings/0x409
  ./configs/c.1/strings/0x409/configuration
  ./configs/c.1/bmAttributes
  ./configs/c.1/MaxPower
  ./functions
  ./functions/ncm.usb0
  ./functions/ncm.usb0/ifname
  ./functions/ncm.usb0/qmult
  ./functions/ncm.usb0/host_addr
  ./functions/ncm.usb0/dev_addr
  ./UDC
  ./bcdUSB
  ./bcdDevice
  ./idProduct
  ./idVendor
  ./bMaxPacketSize0
  ./bDeviceProtocol
  ./bDeviceSubClass
  ./bDeviceClass
```

这样的gadget必须最终启用，以便USB主机能够枚举它。

为了启用gadget，它必须绑定到UDC (USB设备控制器)：

```
$ echo <udc name> > UDC
```

其中<udc name>是在/sys/class/udc/*，例如：

```
$ echo s3c-hsotg > UDC
```

## 禁用gadget

```
echo "" > UDC
```

## 清理





https://www.cnblogs.com/wanglouxiaozi/p/15131949.html



# USB gadget 具体是什么



configfs是基于ram的文件系统，与sysfs的功能有所不同。

sysfs是基于文件系统的==kernel对象视图==，

虽然某些属性允许用户读写，但对象是在kernel中创建、注册、销毁，由kernel控制其生命周期。

而configfs是一个基于文件系统的==内核对象管理器==（或称为config_items），

config_items在用户空间通过mkdir显式的创建，使用rmdir销毁，

==在mkdir之后会出现对应的属性==，可以在用户空间对这些属性进行读写，

与sysfs不同的是，==这些对象的生命周期完全由用户空间控制==，kernel只需要响应用户空间的操作即可。

configfs和sysfs两者可以共存，但不能相互取代。

早期的USB只支持单一的gadget设备，使用场景较为简单，

随后加入了composite framework，用来支持多个function的gadget设备，

多个function的绑定在内核中完成，若需要修改，则需要修改内核，不灵活也不方便。



Linux3.11版本引入了基于configfs的usb gadget configfs。

usb gadget configfs重新实现了复合设备层，使用者可以在用户空间配置和组合内核的function，灵活的构成USB复合设备，极大了提高了工作效率。



usb gadget configfs模块的初始化函数为gadget_cfs_init。

该函数调用后，会向configfs注册一个子系统，子系统使用configfs_subsystem结构体描述。

子系统中又可分为组，使用config_group描述，

组内又有成员，使用config_item描述。

usb gadget configfs就是configfs子系统中的一个成员，成员的名称为"usb_gadget"，

成员的类型使用config_item_type描述，成员类型中包含了初始化函数gadgets_ops。

因此usb gadget configfs子系统最终通过调用gadgets_make进行初始化。

==当加载libcomposite.ko模块后，会在/sys/kernel/config/目录下生成一个usb_gadget目录。==



下面是usb gadget configfs定义的几种config_item_type和configfs_group_operations。

当在/sys/kernel/config/usb_gadget/目录下实例化一个新的gadget实例（g1）时，

首先调用gadget_root_type，

在g1目录下生成bDeviceClass、bDeviceSubClass、bDeviceProtocol、bMaxPacketSize0、idVendor、idProduct、bcdDevice、bcdUSB、UDC属性文件，

使用者可以在用户空间进行配置；

接着调用functions_type，

在g1目录下生成functions目录，绑定function驱动后，

会在该目录下导出function驱动的属性文件，供使用者修改；

然后调用config_desc_type，在g1目录下生成configs目录；

随后调用gadget_strings_strings_type，在g1目录下生成strings目录，

包含了使用字符串表示的英语ID，开发商、产品和序列号等信息。

最后调用os_desc_type，在g1目录下生成os_desc目录，包含了操作系统信息，一般不需要设置。





如下图所示，当用户空间执行echo fe800000.dwc3 > /sys/kernel/config/usb_gadget/g1/UDC时，

内核会调用USB gadget configfs的gadget_dev_desc_UDC_store函数。

gadget_dev_desc_UDC_store函数的主要工作是将usb_gadget_driver和底层的USB控制器绑定，

==usb_gadget_driver相当于一个桥梁，==

==桥的两端分别是function驱动和UDC驱动。==

执行流程如下：

判断输入的USB控制器名称，

==若输出为空或者是none，则解除usb_gadget_driver和底层USB控制器的绑定。==

反之调用usb_udc_attach_driver函数进行匹配USB设备控制器。

遍历udc_list链表，查找fe800000.dwc3 USB设备控制器。

找到对应的USB设备控制器，则保存绑定的usb_gadget_driver，即configfs_driver_template。

回调configfs_composite_bind函数。

其主要的工作内容如下：

分配端点的usb_request、分配缓冲区、设置usb_request的回调函数、复位所有端点，并将gadget的端点数量清零。
function驱动保存对应的配置，并回调function驱动的bind函数，对于uac2则回调 afunc_bind 函数。
如果使用os_string，则需要分配os_string requset。
调用UDC驱动接口usb_gadget_udc_start使能USB设备控制器。
调用UDC驱动接口usb_udc_connect_control连接USB主机控制器，这样USB主机就能识别并枚举USB设备。





https://blog.csdn.net/u011037593/article/details/123698241

https://www.cnblogs.com/blogs-of-lxl/p/16815102.html

# 参考资料

1、USB-HID设备中的复合设备

https://blog.csdn.net/gd6321374/article/details/79919917

2、USB复合设备（mass storage&hid）

https://blog.csdn.net/plauajoke/article/details/8537740