---
title: 蓝牙之Linux命令行工具
date: 2018-12-13 17:34:35
tags:
	- 蓝牙

---



```
• hciconfig 
• hciattach
• hcitool 
• rfkill  
• rfcomm  
• sdptool  
• rctest 
• l2test
```



```
mknod /dev/rfcomm0 c 216 1
chmod 666 /dev/rfcomm0
```

然后树莓派上安装minicom。设置串口为/dev/rfcomm0.

把这个设置保存为bt。

```
root@raspberrypi:~# minicom bt
minicom: cannot open /dev/rfcomm0: No such device or address
```

现在还不行。还需要设置。

rfcomm.conf用来把/dev/rfcomm0跟蓝牙地址进行绑定。

可以用rfcomm命令来做这个事情。

```
rfcomm bind /dev/rfcomm0 [MAC] [channel]
```

我的就是：

```
rfcomm bind /dev/rfcomm0 B8:27:EB:AA:E4:60 
```

解除绑定：

```
rfcomm release /dev/rfcomm0
```

查看绑定：

```
root@raspberrypi:/etc/bluetooth# rfcomm show /dev/rfcomm0
rfcomm0: B8:27:EB:AA:E4:60 channel 1 clean 
```



然后是添加sdp协议通道。方便起见，我们把所有的协议都添加了。

```
sdptool add --channel=1 DID SP DUN LAN FAX OPUSH FTP HS HF SAP NAP GN PANU HID CIP CTP A2SRC A2SNK SYNCML NOKID PCSUITE SR1
```



现在再打开minicom，还是有问题。

我发现我弄错了。

rfcomm绑定，是绑定远端的地址，而不是本机地址。

```
rfcomm bind /dev/rfcomm0 B4:0B:44:F4:16:8D
```

还是出错。



# 参考资料

1、crifan

https://www.crifan.com/files/doc/docbook/bluetooth_intro/release/pdf/bluetooth_intro.pdf

2、linux下使用蓝牙设备 bluetooth hciconfig hcitool

http://www.360doc.com/content/12/0218/15/8157643_187595684.shtml

3、LINUX中的rfcomm命令工具的使用

https://blog.csdn.net/sdlcgxcqx/article/details/3616256

4、Linux下Bluetooth的使用

https://blog.csdn.net/hzl6255/article/details/32352365/

5、Manually using Bluetooth

http://wiki.openmoko.org/wiki/Manually_using_Bluetooth