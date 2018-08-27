---
title: 用树莓派操作IC卡
date: 2017-04-16 17:44:09
tags:
	- 树莓派
	- RFID
typora-root-url: ..\
---
拿着树莓派，总想着折腾点什么，觉得用来读写IC卡是个不错的选择。我在网上买了一块RC522的小板子，送了两张空白卡。我看看能不能把我的门禁钥匙给复制一份。

# 1. 先连接电路
参考下面的图来连接就好：
![](/images/rpi_rc522_conn.jpg)
这个连接方法也可以在MFRC522-python代码的readme.md里找到。

连接好的图是这样的：
![](/images/photo/rpi/rpi_rc522.jpg)

# 2. 树莓派配置
默认树莓派没有打开spi，需要手动配置来打开。
先输入：`sudo raspi-config`。选择Advanced Options，进去把SPI打开，退出。
下载查看一下：
```
pi@raspberrypi:~$ ls /dev/spidev0.
spidev0.0  spidev0.1  
```
可以看到spi设备了。

# 3. 下载需要的软件
SPI-Py
```
git clone https://github.com/lthiery/SPI-Py.git
cd SPI-Py
sudo apt-get install -t jessie python-dev
(或者sudo apt-get install -t wheezy python-dev)
sudo python setup.py install
```
MFRC522：
```
$ git clone https://github.com/mxgxw/MFRC522-python.git
$ cd MFRC522-python
$ sudo python Read.py
```
现在把一张卡放到感应区上，可以看到出现下面的打印：
```
pi@raspberrypi:~/work/nfc/src/mfrc522/MFRC522-python$ ./Read.py 
Welcome to the MFRC522 data read example
Press Ctrl-C to stop.
Card detected
Card read UID: 41,13,49,91
Size: 8
Sector 8 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Card detected
Card read UID: 41,13,49,91
Size: 8
Sector 8 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Card detected
Card read UID: 41,13,49,91
Size: 8
Sector 8 [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
Card detected
Card read UID: 41,13,49,91
```
到这里，环境就基本跑起来了。下面就是要分析一下刚刚安装的工具的代码。
理解了其中的工作原理，才能为我们实现自己的功能打下基础。


SPI-Py这个就是用C语言实现了一个可以给Python调用的SPI读写模块，是个工具，不用过多关注。

我们从MFRC522的Read.py开始读代码。这里就是一个死循环，调用了MFRC522.py里的函数。
所以核心是MFRC522.py。这个文件就一个类：MFRC522。






