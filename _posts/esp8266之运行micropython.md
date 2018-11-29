---
title: esp8266之运行micropython
date: 2018-11-29 15:24:28
tags:
	- esp8266
typora-root-url: ..\
---



我在我的Ubuntu笔记本上做这个实验。

先把ch340的usb转串口驱动安装好。

下载esp8266的MicroPython的bin文件。

https://micropython.org/download/#esp8266

然后安装esptool这个刷机工具。

```
 sudo pip install esptool
```

擦除所有flash。这个是必要的，不然会导致刷完后无限重启。

```
sudo esptool.py --port /dev/ttyUSB0 erase_flash 
```

过程如下：要sudo权限。

```
teddy@teddy-ThinkPad-SL410:~/work/esp8266$ sudo esptool.py --port /dev/ttyUSB0 erase_flash 
esptool.py v2.5.1
Serial port /dev/ttyUSB0
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
MAC: 84:f3:eb:93:30:1e
Uploading stub...
Running stub...
Stub running...
Erasing flash (this may take a while)...
Chip erase completed successfully in 9.3s
Hard resetting via RTS pin...
teddy@teddy-ThinkPad-SL410:~/work/esp8266$ 
```



```
sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266.bin
```

```
teddy@teddy-ThinkPad-SL410:~/work/esp8266$ sudo esptool.py --port /dev/ttyUSB0 --baud 460800 write_flash --flash_size=detect 0 esp8266.bin
esptool.py v2.5.1
Serial port /dev/ttyUSB0
Connecting....
Detecting chip type... ESP8266
Chip is ESP8266EX
Features: WiFi
MAC: 84:f3:eb:93:30:1e
Uploading stub...
Running stub...
Stub running...
Changing baud rate to 460800
Changed.
Configuring flash size...
Auto-detected Flash size: 4MB
Flash params set to 0x0040
Compressed 604872 bytes to 394893...
Wrote 604872 bytes (394893 compressed) at 0x00000000 in 9.0 seconds (effective 539.8 kbit/s)...
Hash of data verified.

Leaving...
Hard resetting via RTS pin...
```

然后用minicom连上就可以使用了。



# 参考资料

1、MicroPython入坑记（二）刷固件（ESP8266 ESP32）

https://www.cnblogs.com/yafengabc/p/8681380.html