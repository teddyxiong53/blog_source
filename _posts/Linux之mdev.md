---
title: Linux之mdev
date: 2018-03-07 09:08:00
tags:
	- Linux

---



mdev是mini udev 的缩写。是busybox里的一部分。

文档在busybox/docs/mdev.txt。

mdev有2个基本用途，

* 初始化生成设备

* 动态更新设备。

这2个功能都需要sysfs的支持。

要支持动态更新设备，需要使能kernel的热拔插功能。



一般在初始化脚本里写上这个：

```
mount -t proc proc /proc
mount -t sysfs sysfs /sys
echo /sbin/mdev > /proc/sys/kernel/hotplug
mdev -s #开始扫描
```

更完整的写法，会在上面代码的前面再加上这个。

```
mount -t tmpfs -o size=64k,mode=0755 tmpfs /dev #保证/dev是一个tmpfs文件系统。
mkdir /dev/pts
mount -t devpts devpts /dev/pts
```



# 配置文件

在/etc/mdev.conf。

这个文件可以没有。

有的话，是因为想要修改权限值。

示例：

```
null		0:0 666
zero		0:0 666
urandom		0:0 444

kmem		0:9 000
mem		0:9 640
port		0:9 640

console		0:5 600
ptmx		0:5 660
tty[0-9]*	0:5 660

ttyS[0-9]*	0:20 640

fd[0-9]*	0:11 660

sd[a-z]*	0:6 660
hd[a-z]*	0:6 660

```

你可以写一行全局通配：

```
.* 1:1 777
```

把所有的设备都设置为uid为1的用户的，权限为777 



# 代码分析

`mdev -s`扫描/sys/class/xxx，查找目录下面有dev这个文件的目录。

例如：/sys/class/tty/tty0/dev。这个文件里的内容是：`4:0`。

目录名被当成设备名。



# rules编写

现在要做usb动态插拔的检测。

给的参数是udev的。

看看mdev的怎么进行模仿。

/etc/mdev.conf定义了这些rules

Now it’s time to gain control about the hardware plugged in. The config file /etc/mdev.conf defines what happens, when a device gets plugged in or out.

```
# /etc/mdev.conf
# Fire the setupUSBdev script if a device named ttyUSB* gets plugged:
ttyUSB[0-9]* 0:0 660 @/usr/bin/ladybug/setupUSBdev
```

这个代码表示的含义：

当一个usb串口设备插入的时候，setupUSBdev这个脚本文件执行。

脚本通过环境变量来获取信息。

信息包含这些

```
ACTION=add
SEQNUM=1018
MAJOR=188
MDEV=ttyUSB6
DEVPATH=/class/tty/ttyUSB6
SUBSYSTEM=tty
MINOR=6
PHYSDEVPATH=/devices/pci0000:00/0000:00:0b.0/usb2/2-1/2-1.3/2-1.3:1.6/ttyUSB6
PHYSDEVDRIVER=sierra
PHYSDEVBUS=usb-serial
PWD=/dev
```

By the way: [This document](http://www.kernel.org/doc/pending/hotplug.txt) from Rob Landley (author of mdev) explains more about obtaining information from hot-plugged devices.

```bash
#!/bin/sh
# Create device files for sierra wirless modems
 
# Device Types
WIRELESS="sierra"
logger "Mdev $ACTION event for $PHYSDEVDRIVER @ $MDEV"
 
#check if PHYSDEVDRIVER is set
if [ "$PHYSDEVDRIVER" = "" ]; then
# No idea why we receive two events for each new device....
exit
fi
 
# catch device driver
if [ "$PHYSDEVDRIVER" = "$WIRELESS" ]; then
logger -t $0 "Wireless Modem ($MDEV) detected"
# get highest node file
HIGHEST=`ls /dev/sierrattyUSB* | tail -1 | tr -cd '[[:digit:]]'`
logger -t $0 "Actual highest dev File = $HIGHEST"
if [ "$HIGHEST" = "" ]; then
Logger -t $0 "$MDEV is the first node. It get's /dev/sierrattyUSB0"
ln -sf /dev/${MDEV} /dev/sierrattyUSB0
else
NEXT=$(($HIGHEST + 1))
Logger -t $0 "Next DevFile ist # $NEXT"
ln -sf /dev/${MDEV} /dev/sierrattyUSB${NEXT}
fi
fi
```

# 基本用法

Usage: mdev [-s] | [-df]

mdev -s is to be run during boot to scan /sys and populate /dev.
mdev -d[f]: daemon, listen on netlink.
        -f: stay in foreground.

```
Bare mdev is a kernel hotplug helper. To activate it:
        echo /sbin/mdev >/proc/sys/kernel/hotplug

It uses /etc/mdev.conf with lines
        [-][ENV=regex;]...DEVNAME UID:GID PERM [>|=PATH]|[!] [@|$|*PROG]
where DEVNAME is device name regex, @major,minor[-minor2], or
environment variable regex. A common use of the latter is
to load modules for hotplugged devices:
        $MODALIAS=.* 0:0 660 @modprobe "$MODALIAS"

If /dev/mdev.seq file exists, mdev will wait for its value
to match $SEQNUM variable. This prevents plug/unplug races.
To activate this feature, create empty /dev/mdev.seq at boot.

If /dev/mdev.log file exists, debug log will be appended to it.
```

我们为什么要使用mdev -df的方式运行呢？

```
./S10mdev:12:   start-stop-daemon -S -b -m -p $PIDFILE -x /sbin/mdev -- -df
```

这个是busybox里的默认配置行为。



# 跟udev对比

\1.  udev 和mdev 是两个使用uevent 机制处理热插拔问题的用户空间程序，两者的实现机理不同。udev 是基于netlink 机制的，它在系统启动时运行了一个deamon 程序udevd，通过[监听](https://so.csdn.net/so/search?q=监听&spm=1001.2101.3001.7020)内核发送的uevent 来执行相应的热拔插动作，包括创建/删除设备节点，加载/卸载驱动模块等等。

\2.  mdev 是基于uevent_helper 机制的，它在系统启动时修改了内核中的uevnet_helper 变量（通过写/proc/sys/kernel/hotplug），值为“/sbin/mdev”。这样内核产生uevent 时会调用uevent_helper 所指的用户级程序，也就是mdev，来执行相应的热拔插动作。

\3. udev 使用的netlink 机制在有大量uevent 的场合效率高，适合用在PC 机上；而mdev 使用的uevent_helper 机制实现简单，适合用在嵌入式系统中。

\4. uevent_helper 的初始值在内核编译时时可配置的，默认值为/sbin/hotplug。如果想修改它的值，写/proc/sys/kernel/hotplug 文件就可以了，例如： echo “/sbin/mdev” > /proc/sys/kernel/hotplug

\5.  在mdev和udev共存的系统中，需要建立规则，避免mdev和udev重复执行。

# 自动挂载SD卡的行为

如下是自动挂载和卸载的脚本：

```
/etc/sd_card_inserting
        #!/bin/sh
        mount -t vfat /dev/mmcblk0p1 /mnt/sd


/etc/sd_card_removing
        #!/bin/sh
        sync
        umount /mnt/sd
```



```
以下是系统初始化脚本中一个典型的使用mdev 的代码片段：
    [1] mount -t sysfs sysfs /sys
    [2] echo /bin/mdev > /proc/sys/kernel/hotplug
    [3] mdev -s
```

```
你可以使用 mdev 的可选配置文件，以控制设备节点的 所有者 和 权限。
The file has the format:
这个文件的格式如下：
    <device regex> <uid>:<gid> <octal permissions>
For example:
例如：
    hd[a-z][0-9]* 0:3 660
```



```
如果你想 mdev 在找到匹配行时可以执行自定义的命令，那么文件格式如下：
the format:
    <device regex> <uid>:<gid> <octal permissions> [<@|$|*> <command>]
The special characters have the meaning:
特殊字符的意义如下：
   @ Run after creating the device.
    @ 在创建设备节点后运行命令。
    $ Run before removing the device.
    $ 在删除设备节点前运行命令。
    * Run both after creating and before removing the device.
    * 在创建设备节点后和删除设备节点前都运行命令。
```

不如直接升级adb工具。





```
采用以下的实例mdev配置写法在我的arm 板子上并没有完全奏效，实验发现我的版本的mdev只会匹配第一条DEVNAME并执行他的规则，匹配第一个后就不在去检查后面的规则，比如@@两个对于mmcblk0p1的规则永远只执行第一个

touch /dev/mdev.log 会保存mdev的log ，对比busybox中的源码提示rule matched, line -1(没有查到命令)

最终的mdebv.conf

mmcblk[0-9]p[0-9] 0:0 666 */etc/hotplug/sdcard_hotplug $ACTION

#!/bin/sh
if [ $1 == "add" ]; then
echo "acttion = $ACTION dev= $MDEV" >> /mnt/tt.log
mkdir /mnt/sdcard
mount /dev/mmcblk[0-9]p[0-9] /mnt/sdcard
elif [ $1 == "remove" ]; then
echo "acttion = $ACTION dev= $MDEV" >> /mnt/tt.log
umount -l /mnt/sdcard
rm /mnt/sdcard -rf
fi
```

# nonexistent directory错误

```
# echo /sbin/mdev > /proc/sys/kernel/hotplug
-/bin/sh: can't create /proc/sys/kernel/hotplug: nonexistent directory
```

解决使用mdev时“cannot create /proc/sys/kernel/hotplug:nonexistent directory”错误

确保编译内核时编译如下选项：

CONFIG_PROC_FS=y

CONFIG_PROC_SYSCTL=y

**CONFIG_HOTPLUG=y**

**CONFIG_NET=y**



原因是Device Drivers > Generic Driver Options > Support for uevent helper 选项没有打开



```
static void open_mdev_log(const char *seq, unsigned my_pid)
{
	int logfd = open("mdev.log", O_WRONLY | O_APPEND);
```



# 参考资料

1、

https://quirk.ch/2010/01/how-to-set-up-mdev-rules-for-busybox

2、udev和mdev hotplug

https://blog.csdn.net/longwang155069/article/details/52702305

3、linux中的热插拔和mdev机制

https://www.cnblogs.com/pengdonglin137/p/3824710.html

4、

https://blog.csdn.net/shenhuxi_yu/article/details/106833735

5、

https://blog.csdn.net/dongliqiang2006/article/details/4504932