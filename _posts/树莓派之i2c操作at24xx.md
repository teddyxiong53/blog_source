---
title: 树莓派之i2c操作at24xx
date: 2018-02-28 13:29:51
tags:
	- 树莓派
	- i2c

---



为了配合理解linux的i2c driver，我在树莓派上对一块at24xx的eeprom芯片进行操作。

为了操作简单，使用dip封装的at24xx，可以直接插到面包板上用。

sda和scl的上拉电阻用10K的。地址线都接地。

# 安装i2c-tools工具

为了方便后面的调试，我们安装i2c-tools工具。

```
sudo apt-get install i2c-tools
```

这个工具有4个工具组成：

```
1、i2cdetect。
2、i2cdump。
3、i2cget
4、i2cset。
```

工具的用法。

```
i2cget  i2cbus chip-address [data-address [mode]]
```





# 树莓派的i2c驱动加载

1、用lsmod查看当前有没有加载i2c的驱动。发现没。

2、用命令临时加载。

```
sudo modprobe i2c-bcm2708 
```

查看lsmod，有了：

```
pi@raspberrypi:/etc/modprobe.d$ lsmod
Module                  Size  Used by
i2c_bcm2708             4834  0
```

如果要卸载掉。用这个。-r表示remove。

```
sudo modprobe -r i2c-bcm2708 
```

3、如果希望后面自己开机默认就加载。

在/etc/modules文件里加入：

```
i2c-bcm2708
i2c-dev
```

同时要把/etc/modprobe.d/rapi-blacklist.conf里的相关内容去掉。

我就不加载了。

4、查看当前I2C的速度。

```
pi@raspberrypi:~$ sudo cat /sys/module/i2c_bcm2708/parameters/baudrate 
0
```

发现是0。这个是可以修改。但是修改要在modprobe的时候通过参数传递进去。

```
modprobe i2c_bcm2708 baudrate=10000
```

这个修改也可以改成永久的。

在/etc/modprobe.d目录下，增加一个mycfg.conf文件。里面写入：

```
options i2c_bcm2708 baudrate=10000
```

这样重启后就可以生效。

但是我加载了i2c_bcm2708之后，/dev目录下没有产生i2c节点。

看了一下，是需要在/boot/config.txt里，把配置打开。

```
# Uncomment some or all of these to enable the optional hardware interfaces
#dtparam=i2c_arm=on
#dtparam=i2s=on
dtparam=spi=on
```

要把i2c的也打开。

当然你也可以用raspi-config这个脚本来进行直观的配置来打开。都是改到config.txt文件里的。

改了后，reboot树莓派。

再加载模块。用i2cdetect查看。有了。

```
pi@raspberrypi:~$ i2cdetect -l
i2c-1   i2c             3f804000.i2c                            I2C adapter
pi@raspberrypi:~$ 
```







树莓派的i2c信息。

```
pi@raspberrypi:/sys/class/i2c-dev/i2c-1$ tree
.
├── dev
├── device -> ../../../i2c-1
├── name
├── power
│   ├── autosuspend_delay_ms
│   ├── control
│   ├── runtime_active_time
│   ├── runtime_status
│   └── runtime_suspended_time
├── subsystem -> ../../../../../../../class/i2c-dev
└── uevent

3 directories, 8 files
pi@raspberrypi:/sys/class/i2c-dev/i2c-1$ cat dev
89:1
pi@raspberrypi:/sys/class/i2c-dev/i2c-1$ cat device
cat: device: Is a directory
pi@raspberrypi:/sys/class/i2c-dev/i2c-1$ cat name
bcm2835 I2C adapter
pi@raspberrypi:/sys/class/i2c-dev/i2c-1$ cat uevent 
MAJOR=89
MINOR=1
DEVNAME=i2c-1
pi@raspberrypi:/sys/class/i2c-dev/i2c-1$
```



```
pi@raspberrypi:/sys/class/i2c-adapter/i2c-1$ tree
.
├── delete_device
├── device -> ../../3f804000.i2c
├── i2c-dev
│   └── i2c-1
│       ├── dev
│       ├── device -> ../../../i2c-1
│       ├── name
│       ├── power
│       │   ├── autosuspend_delay_ms
│       │   ├── control
│       │   ├── runtime_active_time
│       │   ├── runtime_status
│       │   └── runtime_suspended_time
│       ├── subsystem -> ../../../../../../../class/i2c-dev
│       └── uevent
├── name
├── new_device
├── of_node -> ../../../../../firmware/devicetree/base/soc/i2c@7e804000
├── power
├── subsystem -> ../../../../../bus/i2c
└── uevent

9 directories, 12 files
pi@raspberrypi:/sys/class/i2c-adapter/i2c-1$ cat name 
bcm2835 I2C adapter
pi@raspberrypi:/sys/class/i2c-adapter/i2c-1$ cat uevent 
OF_NAME=i2c
OF_FULLNAME=/soc/i2c@7e804000
OF_COMPATIBLE_0=brcm,bcm2835-i2c
OF_COMPATIBLE_N=1
OF_ALIAS_0=i2c1
pi@raspberrypi:/sys/class/i2c-adapter/i2c-1$ 
```



参考资料

1、Linux I2C工具查看配置I2C设备

https://blog.csdn.net/zjy900507/article/details/78655384