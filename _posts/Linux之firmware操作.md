---
title: Linux之firmware操作
date: 2022-04-28 19:35:01
tags:

	- Linux

---

--

硬件市场的激烈竞争, 使得制造商连一点用于设备控制固件的 EEPROM 的成本都不愿意花费。

因此固件一般发布在和硬件配套的驱动包中，由操作系统（其实是驱动程序）负责传送固件到设备。

获取固件的正确方法是当需要时从用户空间获取它。

一定不要试图从内核空间直接打开包含固件的文件，

那是一个易出错的操作, 因为它把策略(以文件名的形式)包含进了内核。

正确的方法是使用固件接口:

```
/* fw 参数指向以下结构体:*/
struct firmware {
    size_t size;
    u8 *data;
};
int request_firmware
void release_firmware(struct firmware *fw);
```

固件子系统使用 sysfs 和热插拔机制工作。当调用 request_firmware时, 函数将在 /sys/class/firmware 下创建一个以设备名为目录名的新目录，其中包含 3 个属性:

- loading ：这个属性应当被加载固件的用户空间进程设置为 1。当加载完毕, 它将被设为 0。被设为 -1 时，将中止固件加载。
- data ：一个用来接收固件数据的二进制属性。在设置 loading 为1后, 用户空间进程将固件写入这个属性。
- device ：一个链接到 /sys/devices 下相关入口项的符号链接。



参考资料

1、

https://www.kernel.org/doc/html/v4.13/driver-api/firmware/request_firmware.html

2、

https://blog.csdn.net/lizuobin2/article/details/53675443