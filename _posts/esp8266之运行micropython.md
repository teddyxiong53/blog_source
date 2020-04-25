---
title: esp8266之运行micropython
date: 2018-11-29 15:24:28
tags:
	- esp8266
typora-root-url: ..\
---

1

micropython是使用esp8266的好的方式，同时，esp8266也是支持micropython很好的一个平台。

下面我们就在wemos d1这个板子（esp8266底板上扩展了串口和io引脚）来做这些：

1、烧录镜像。

2、得到一个repl

3、使用webrepl。

4、网络通信。

5、使用硬件外设。

6、控制一些外部设备。



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



```
import machine
machine.freq() # 查看当前的频率。
machine.freq(160000000) # 设置频率为160M。
```

```
import esp
import network
import time
from machine import Timer, Pin, PWM, ADC, SPI,I2C, RTC
import onewire
```



从实用角度来说，写脚本运行才有意义。

```
>>> import os
>>> os.listdir()
['boot.py']
```

怎么查看这个boot.py的内容？

怎样自己写一个脚本放进去运行？



micropython内置了一个文件系统，你可以把文件放进去，这样机器开机的时候，就会自动执行你的脚本。

就像arduio一样。

pyboard上，有一张SD卡。

对于esp8266，则只有内部的flash。

esp8266提供了一个工具，叫web repl。提供了一个web的接口，让我们可以上传文件。

还有一个工具叫rshell。让你可以通过串口或者usb远程访问设备上的文件。

还有一个工具叫mpfshell，这个是专门为esp8266做的工具。跟rshell类似。

还有一个通用的工具，叫ampy，是Adafruit Micropython tool。

我们就使用ampy这个工具，因为简单实用。

安装：`pip install adafruit-ampy`

安装后，你可以用`ampy --help`查看帮助。

基本命令：

```
export AMPY_PORT=/dev/ttyUSB0 #  设置了环境变量，就不用每次都带上-p /dev/ttyUSB0了。
ampy ls
```

但是我执行命令，都是在串口这边打印下面的内容：

```
raw REPL; CTRL-B to exit
```

是需要把minicom这边关闭才行。



现在弄一个实用的项目。做一个wifi温度计。

使用dht11作为传感器。这个的onewire的设备。可以测温度和湿度。

温度范围0到50度，湿度20%到90%。

模组3个引脚：vcc、gnd、data。

micropython内建了对dht的支持。

核心代码就下面这几行：

```
import dht
import machine

PIN_DHT = 14 # gpio14/d5
d = dht.DHT11(machine.Pin(PIN_DHT))
d.measure()
print(d.temprature())
```

完善一下：

```
import dht
import machine
import usocket as socket
import network

SSID="xhl"
SSID_PW="1234567890"



def do_connect():
	wlan = network.WLAN(network.STA_IF)
	wlan.active(True)
	print("before connect")
	if not wlan.isconnected():
		wlan.connect(SSID, SSID_PW)
		while not wlan.isconnected():
			pass
	print("connect ok")
	return wlan.ifconfig()
	
	
def read_dht():
	# PIN_DHT = 14 # gpio14/d5
	# d = dht.DHT11(machine.Pin(PIN_DHT))
	# d.measure()
	# return d.temperature()
	return 25
	
def do_server(ip, port):
	# this \ is necessary, 
	CONTENT = """\
HTTP/1.0 200 OK
Content-Type: applicatoin/json

{
	"data": %d
}
"""
	ai = socket.getaddrinfo(ip, port)
	addr = ai[0][4]
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(addr)
	print("before listen")
	s.listen(1)
	while True:
		print("before accept")
		res = s.accept()
		print("after accept")
		client_s = res[0]
		client_addr = res[1]
		req = client_s.recv(300)
		parts = req.decode("ascii").split(' ')
		print(parts)
		if part[1] == '/temperature':
			client_s.send(bytes(CONTENT % read_dht(), "ascii"))
		client_s.close()
		
def main():
	print("begin")
	ipconfig = do_connect()
	print("IP {}".format(ipconfig[0]))
	do_server(ipconfig[0], 8080)
	
main()

```

现在运行脚本，有不少问题。

首先是报这个。

```
    raise PyboardError('could not enter raw repl')
ampy.pyboard.PyboardError: could not enter raw repl
```

有时候是报下面这个。

```
    raise PyboardError('timeout waiting for first EOF reception')
ampy.pyboard.PyboardError: timeout waiting for first EOF reception
```

对于这个问题，说是可以这样解决：

```
ampy run -n test.py
```

相当于不会阻塞。这个可能是合理的。但是我也看不到日志了。

这样执行也得到预期的效果。

我手动一句句执行，可以收到http请求的数据。



总的来说，这个调试非常不方便。



#  mpfshell使用

既然当前ampy使用非常不方便。

那么尝试一下mpfshell。

地址：https://github.com/wendlers/mpfshell

readme就足够用了。

安装：

```
sudo pip install mpfshell
```

使用：mpfshell。这个会产生一个二级shell。

```
mpfs [/]> help

Documented commands (type help <topic>):
========================================
EOF  cd     exec  get   lcd  lpwd  md    mput  mrm   put   pwd   rm
cat  close  exit  help  lls  ls    mget  mpyc  open  putc  repl
```

然后需要连上板端。有两种方式：网络或者串口。

我们使用串口的方式。

```
mpfs [/]> open ttyUSB0
Connected to esp8266
```

```
mpfs [/]> ls
Remote files in '/':
       boot.py
```

```
mpfs [/]> exec print("hello")
hello
```

这个的确是比ampy要方便一些。

进入到repl

```
输入repl命令就可以进入。
退出是按ctrl+] 。
```

用python2的话，repl就会有很多问题，所以换到python3下面来做。



micropython的一般做法是：

```
写2个文件。
一个boot.py。这个是默认就有的。这里做一下配置。在boot.py最后，调用一下main.py。
一个main.py。这个放主要逻辑。
```

所以，我们用mpfshell。可以这样：

```
open ttyUSB0
put boot.py
put main.py
ls
```

保存成1.txt。

然后：

```
mpfshell -s 1.txt
```

这样就可以省去敲这些命令了。

不行，这个执行完就退出了。只能用来推送。不能用来执行。



我们可以在repl里执行脚本文件。

```
exec(open("test.py.py").read())
```

虽然可以执行，但是没有任何打印。

进入repl。发现test.py里的内容都已经进入到命名空间了。

我可以手动执行do_connect这些函数了。

我先把最后的调用main注释掉。

这样就可以手动来调用main了。

这个是我目前发现最好的调试方式了。

调试采集温度可以上来。



# upycraft

其实早就有更好的调试方法了。

就是借助upycraft这个micropython专用ide，比msfshell要方便，但是原理是一样的。

都是靠exec来做的。

下载地址在这里：

https://dfrobot.gitbooks.io/upycraft_cn/5.1%20%E9%85%8D%E5%A5%97%E8%B5%84%E6%BA%90.html



minicom的退出方法：先按ctrl+A，再按x。







# 参考资料

1、MicroPython入坑记（二）刷固件（ESP8266 ESP32）

https://www.cnblogs.com/yafengabc/p/8681380.html

2、Quick reference for the ESP8266

http://docs.micropython.org/en/latest/esp8266/quickref.html

3、运行您的首个脚本

https://docs.singtown.com/micropython/zh/latest/pyboard/pyboard/tutorial/script.html

4、如何在20元小板子上跑Python

https://zhuanlan.zhihu.com/p/24644526

5、DHT11温湿度传感器模块使用方法和驱动代码实现

https://www.cnblogs.com/lulipro/p/10815338.html

