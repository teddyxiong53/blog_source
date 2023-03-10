---
title: Android刷机之fastboot
date: 2020-04-08 10:21:51
tags:
	- Android

---



fastboot 主要是用来与bootloader的USB通讯的PC命令行工具。

他一般主要也用来向bootloader传送刷机文件进行文件分区重烧。 

因此在使用时，必须有一个PC机并且USB线要始终联着。

所以这种方式称为线刷。  

用fastboot需要bootloader 支持，所以不是每一家公司产品都支的这个功能的。



```
  fastboot flashing unlock    #6.0以上设备 设备必须解锁，开始刷机（这个不同的手机厂商不同）
  fastboot erase {partition}  # 擦除分区
  fastboot  erase  frp    # 擦除 frp 分区，frp 即 Factory Reset Protection，用于防止用户信息在手机丢失后外泄
  fastboot  flash  boot  boot.img    # 刷入 boot 分区
  fastboot  flash  system  system.img    # 刷入 system 分区
  fastboot  flash  recovery  recovery.img    # 刷入 recovery 分区
  fastboot flashall    #烧写所有分区，注意：此命令会在当前目录中查找所有img文件，将这些img文件烧写到所有对应的分区中，并重新启动手机。
  fastboot  format  data    # 格式化 data 分区
  fastboot  flashing lock    # 设备上锁，刷机完毕
  fastboot  continue    # 自动重启设备
  fastboot reboot# 重启手机
  fastboot reboot-bootloader# 重启到bootloader 刷机用
  fastboot devices  ## 发现手机，显示当前哪些手机通过fastboot连接了
```



```
创建包含boot.img，system.img，recovery.img文件的zip包。
执行：fastboot update {*.zip}
```

# u-boot里的fastboot代码

在uboot里搜索fastboot，可以找到这些文件。

```
./include/fastboot.h
./include/net/fastboot.h
./cmd/fastboot
./cmd/fastboot.c
./net/fastboot.c
./doc/README.android-fastboot-protocol
./doc/README.android-fastboot
./drivers/usb/gadget/f_fastboot.c
```

## ./doc/README.android-fastboot

当前的实现是一个最小实现，

只支持：

```
erase 命令
oem format 命令
flash命令
只支持emmc设备。
```

fastboot依赖了usb download gadget。

所以需要选配这些：

```
CONFIG_USB_GADGET_DOWNLOAD
CONFIG_G_DNL_VENDOR_NUM
CONFIG_G_DNL_PRODUCT_NUM
CONFIG_G_DNL_MANUFACTURER
```

需要一个大的buffer，用来放下载的数据。

有2个对应的配置项。

```
ONFIG_FASTBOOT_BUF_ADDR 
CONFIG_FASTBOOT_BUF_SIZE
```





# 应用层里的fastboot工具



fastboot的 waiting for device是这样打印出来的。

```
usb_handle *open_device(void)
{
    static usb_handle *usb = 0;
    int announce = 1;

    if(usb) return usb;

    for(;;) {
        usb = usb_open(match_fastboot);
        if(usb) return usb;
        if(announce) {
            announce = 0;
            fprintf(stderr,"< waiting for device >\n");
        }
        sleep(1);
    }
}
```



# adb与fastboot的区别

Android设备和PC之间的协议通信，除了`fastboot`协议还有使用`adb`协议。

- `adb`用于Android设备系统起来后的调试，允许访问Android系统。
- `fastboot`用于Android设备开发过程中刷写镜像使用以及Android设备起不来进入fastboot模式救砖使用，对于线刷来说(Android设备与PC机通过USB线连接)。
- 两个协议都是将Android设备配置为USB Gadget，PC做为USB Host，通过USB进行通信，只是一个走的是`adb`协议，一个走的是`fastboot`协议，两者之间的角色定位不同。



# 参考资料

1、

https://www.jianshu.com/p/d960a6f517d8

2、刷写设备

https://source.android.com/setup/build/running

3、

https://www.androidsage.com/

4、

https://wowothink.com/5ade33b8/