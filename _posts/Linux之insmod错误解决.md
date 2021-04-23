---
title: Linux之insmod错误解决
date: 2021-04-21 10:46:07
tags:
	- Linux

---

--

用system函数调用insmod，出现了File exists的错误。

但是我明显没有插入过这个模块。

但是在出现错误后，先rmmod，再insmod，确实就可以成功。

用system函数来调用insmod，总感觉不是太健壮。

看看有没有直接载入模块的C函数。

有，init_module和finit_module都可以。

insmod/rmmod use the functions `init_module` and `delete_module` to do this,



modules.alias

这个文件是如何生成的？



如果想让内核启动过程中自动加载某个模块该怎么做呢？

最容易想到的方法就是到/etc/init.d/中添加一个启动脚本，

然后在/etc/rcN.d/目录下创建一个符号链接，

这个链接的名字以S开头，

这内核启动时，就会自动运行这个脚本了，

这样就可以在脚本中使用modprobe来实现自动加载。

但是我们发现，内核中加载了许多硬件设备的驱动，

而搜索/etc目录，却没有发现任何脚本负责加载这些硬件设备驱动程序的模块。

那么这些模块又是如何被加载的呢？



每一个设备都有Verdon ID, Device ID, SubVendor ID等信息。

而每一个设备驱动程序，必须说明自己能够为哪些Verdon ID, DevieceID, SubVendor ID的设备提供服务。

以PCI设备为例，它是通过一个pci_device_id的数据结构来实现这个功能的。

例如：RTL8139的pci_device_id定义为：

```
static struct pci_device_id rtl8139_pci_tbl[] = {
{0x10ec, 0x8139, PCI_ANY_ID, PCI_ANY_ID, 0, 0, RTL8139 },
{0x10ec, 0x8138, PCI_ANY_ID, PCI_ANY_ID, 0, 0, RTL8139 },
......
}
MODULE_DEVICE_TABLE (pci, rtl8139_pci_tbl);
```

上面的信息说明，

凡是Verdon ID为0x10EC, 

Device ID为0x8139, 0x8138的PCI设备

(SubVendor ID和SubDeviceID为PCI_ANY_ID，表示不限制。)，

都可以使用这个驱动程序(8139too)。



在模块安装的时候，depmod会根据模块中的rtl8139_pci_tbl的信息，

生成下面的信息，保存到/lib/modules/`uname-r`/modules.alias文件中，

其内容如下：

```
alias pci:v000010ECd00008138sv*sd*bc*sc*i* 8139too
alias pci:v000010ECd00008139sv*sd*bc*sc*i* 8139too
......
```

v后面的000010EC说明其Vendor ID为10EC，

d后面的00008138说明Device ID为8139，

而sv,和sd为SubVendor ID和SubDevice ID，后面的星号表示任意匹配。



另外在/lib/modules/`uname-r`/modules.dep文件中

还保存这模块之间的依赖关系，其内容如下：

```
(这里省去了路径信息。)
8139too.ko:mii.ko
```



在内核启动过程中，总线驱动程序会会总线协议进行总线枚举

(总线驱动程序总是集成在内核之中，不能够按模块方式加载，你可以通过make menuconfig进入Bus options，这里面的各种总线，你只能够选择Y或N，而不能选择M.)，

并且为每一个设备建立一个设备对象。

每一个总线对象有一个kset对象，每一个设备对象嵌入了一个kobject对象，kobject连接在kset对象上，这样总线和总线之间，总线和设备设备之间就组织成一颗树状结构。

当总线驱动程序为扫描到的设备建立设备对象时，会初始化kobject对象，并把它连接到设备树中，同时会调用kobject_uevent()把这个(添加新设备的)事件，以及相关信息(包括设备的VendorID,DeviceID等信息。)

通过netlink发送到用户态中。

**在用户态的udevd检测到这个事件，就可以根据这些信息**，打开/lib/modules/`uname-r`/modules.alias文件，

根据

```
alias pci:v000010ECd00008138sv*sd*bc*sc*i* 8139too
```

得知这个新扫描到的设备驱动模块为8139too。

于是modprobe就知道要加载8139too这个模块了，同时modprobe根据 modules.dep文件发现，8139too依赖于mii.ko，如果mii.ko没有加载，modprobe就先加载mii.ko，接着再加载 8139too.ko。



# depmod

分析可载入模块的相依性。

供modprobe在安装模块时使用。

在构建嵌入式系统时，需要由这个命令来生成相应的文件，由modprobe使用。



在 linux桌面系统中，当你编译了新的驱动，

为了能够用modprobe ***加载模块, 

你需要先将模块拷贝到/lib/modules /2.6.31-20-generic目录下，

然后运行sudo depmod -a将模块信息写入modules.dep，modules.dep.bin，modules.alias.bin，modules.alias和 modules.pcimap文件中。

如，我编译了一个新的wifi驱动r8192se_pci.ko，将其拷贝到/lib /modules/2.6.31-20-generic/wireless下，

然后到/lib/modules/2.6.31-20-generic运行 depmod -a，

之后可以在任意目录运行modprobe r8192se_pci。



一般通过hotplug的设备会通过module.alias 中的信息来加载device对应的driver



# mdev禁止热插拔

mdev导致的自动加载驱动，有没有办法指定参数？

以dhd的驱动为例。

/sys/module/dhd目录下。

有这些内容：

```
/sys/module/dhd # ls
coresize    initsize    notes       refcnt      taint
holders     initstate   parameters  sections    uevent
```

parameters目录下，放的就是参数文件。

```
/sys/module/dhd/parameters # ls
clm_path              dhd_oob_gpio_num      nvram_path
clockoverride         disable_proptx        op_mode
dhd_console_ms        firmware_path         passive_channel_skip
dhd_doflow            info_string
dhd_dpcpoll           instance_base
```



在mdev.conf里，当前有这样一行

```
$MODALIAS=.*    root:root 660 @modprobe "$MODALIAS"
```

这一行具体怎么起作用？



mdev有2个主要作用：

1、初始化生成。

2、动态更新。

都需要sysfs支持，并且sysfs需要挂载在/sys目录下。

为了实现动态更新，你需要使能内核的热插拔。

如果有procfs，你在初始化脚本里这样写：

```
[0] mount -t proc proc /proc
[1] mount -t sysfs sysfs /sys
[2] echo /sbin/mdev > /proc/sys/kernel/hotplug
[3] mdev -s
```

如果没有procfs，就这样写：

```
[1] mount -t sysfs sysfs /sys
[2] sysctl -w kernel.hotplug=/sbin/mdev
[3] mdev -s

```



```
> Since loading the modules might trigger new MODALIAS events you
> need your hotplugger to handle those. You can use this line in
> mdev.conf:
> 
>   $MODALIAS=.*    root:root       0660    @modprobe -b "$MODALIAS"
```



modprobe参数

```
-b, --use-blacklist         Apply blacklist to resolved alias.
```



MODALIAS要和驱动中一致，马上能看到。

这条规则指的是：

**当收到的环境变量中含有MODALIAS，那么加载MODALIAS代表的模块。**

我有点明白了，这个是靠内核里把MODALIAS这个环境变量放进来的。

在uevent函数里，有这样的语句：

```
add_uevent_var(env, "MODALIAS=%s%s", PLATFORM_MODULE_PREFIX,
			pdev->name);
```

热插拔肯定要保留，因为还有U盘这些东西。

modules.dep具体是怎么起作用的？





加载内核驱动的通常流程：

1.先将.ko文件拷贝到/lib/module/`uname -r`（内核版本号）/kernel/driver/...目录下，

  根据具体用途的区别分为net、ide、scsi、usb、video、parport、md、block、ata等等。

2.运行depmod -a，更新模块依赖新，主要是更新modules.dep文件

3.运行modprobe加载内核模块



对内核模块来说，黑名单是指禁止某个模块装入的机制

在 /etc/modprobe.d/ 中创建 .conf 文件，使用 blacklist 关键字屏蔽不需要的模块，例如如果不想装入 pcspkr 模块：

/etc/modprobe.d/blacklist.conf
blacklist pcspkr



我加上了dhd这个模块，为什么还是被加载进来了？

看busybox里的modprobe的参数，没有说blacklist相关的。

是因为这个是扩展选项，busybox默认没有配置。

```
//config:config FEATURE_MODPROBE_BLACKLIST
//config:	bool "Blacklist support"
//config:	default y
//config:	depends on MODPROBE && !MODPROBE_SMALL
//config:	help
```



参考资料

http://lists.busybox.net/pipermail/busybox/2015-March/082666.html



https://blog.csdn.net/xxxxxlllllxl/article/details/9302803

linux中blacklist.conf解读

https://blog.51cto.com/xjsunjie/2379819

# /etc/init.d/rc.modules

这个在rcS里开头的位置调用。

通过读取/etc/modules里的内容。

执行modprobe操作。

/etc/modules里的内容是这样的：

```
dwc3
dwc_otg
# media modules
media_clock
firmware
video_framerate_adapter
decoder_common
stream_input
```

rc.modules的内容：

```
1、判断/etc/modules是否存在。
2、执行depmod命令，不带任何参数。
3、逐行读取/etc/modules内容，执行modprobe。
```



# 参考资料

1、

https://stackoverflow.com/questions/5947286/how-to-load-linux-kernel-modules-from-c-code

2、

https://stackoverflow.com/questions/29183713/how-to-trigger-a-kernel-module-from-shell

3、

https://www.cnblogs.com/sky-heaven/p/13280047.html

4、ARM64内核系统调用详解（基于kernel-4.9）

https://blog.csdn.net/rikeyone/article/details/79919019

5、

https://www.cnblogs.com/image-eye/archive/2011/08/19/2145858.html

6、编译linux内核以及depmod的使用

https://www.cnblogs.com/pengdonglin137/p/3633967.html

7、

https://docs.oracle.com/cd/E37670_01/E41138/html/ol_modparams.html

8、

https://stackoverflow.com/questions/11031554/kernel-module-parameters-changes-using-sys-module

9、

https://blog.csdn.net/luckyapple1028/article/details/44261391

10、自动处理可载入模块命令 modprobe

https://blog.csdn.net/freeking101/article/details/80870678?utm_source=blogxgwz7