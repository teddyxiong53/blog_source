---
title: arduino（四）nodemcu
date: 2018-04-16 14:44:41
tags:
	- arduino
typora-root-url: ..\
---



板子类型太多了。我手里的这款arduino兼容板是nodemcu的。

官网在这里：http://www.nodemcu.com

特色是可以用lua进行开发。

固件的代码在这里：

https://github.com/nodemcu/nodemcu-firmware



# 什么是nodemcu

nudemcu是基于esp8266的一块板子，它提供了一个固件，支持在这个固件上用lua进行编程。

固件是基于esp8266 non-os SDK 2.2.0版本做的，提供了一个文件系统，基于spiffs。

# 特点

1、基于lua5.1.4。没有debug和os模块。

2、异步事件驱动。

3、支持超过65个内置模块。

4、固件分为支持浮点和不支持浮点两种。



# 编程模型

编程模型类似Node.js。这也是nodemcu得名的原因。

这句话的内涵是，大量使用了回调函数来做异步。



# 烧录测试

我买板子的时候，卖家给我发的资料里，已经有现成的固件了。

我用这个工具，打开D:\work\arduino\NodeNcu+入门指导\关于Nodemcu 入门指导\软件\nodemcu-flasher(固件烧录工具)\nodemcu-flasher-master\Win64\Release\ESP8266Flasher.exe。

我选择这个固件：

D:\work\arduino\NodeNcu+入门指导\关于Nodemcu 入门指导\固件\Nodemcu官方固件\nodemcu_integer_0.9.6-dev_20150704.bin

点击Flash就可以启动烧录，不用复位硬件之类的操作。

到这个目录下，D:\work\arduino\NodeNcu+入门指导\关于Nodemcu 入门指导\软件\ESPlorer

双击ESPlorer.bat打开应用。

这个bat文件里就一句话：

```
java -jar "ESPlorer.jar" 
```

因为是一个jar文件里的main函数是入口。

设置波特率为9600 ，其余的串口设置都是一般我们用的设置。

点击open。这个时候需要按一下板子上的复位键。然后open成功。

我在这个工具里的编辑区域写入这些代码：

```
gpio.mode(0,gpio.OUTPUT)
print(gpio.read(0),"\n")
gpio.write(0,gpio.LOW)
print(gpio.read(0),"\n")
tmr.delay(1000000)
gpio.write(0, gpio.HIGH)
print(gpio.read(0),"\n")
```

然后保存为test.lua文件。它默认的保存行为就是保存，并且运行，所以你在串口上可以看到打印：

```

> dofile('test.lua')
1	

0	

1	
```

你也可以在print按钮旁边的区域输入lua命令，点击send。

```
> print("hello")
hello
> 
```

这个工具上还有很多的按钮，都点一点看看。

点击reset按钮。

```

NodeMCU 0.9.6 build 20150704  powered by Lua 5.1.4
lua: cannot open init.lua
> 
Communication with MCU...
Got answer! AutoDetect firmware...
Communication with MCU established.
NodeMCU firmware detected.
=node.heap()
35128
```

另外有一个ESP8266 LuaLoader的工具，作用差不多。也试用一样。

其实这些都是不怎么好用的。我用SecureCRT，把串口打开，就可以像在shell下工作一样来做了。



# 定制

这个网站，可以让你自己定制自己的firmware。

https://nodemcu-build.com/index.php

它会给你编译出一个bin文件，发送到你的邮箱里。



# 安信可和乐鑫的关系

安信可是乐鑫的客户。安信可二次开发了不少的文件，在乐鑫的基础上改的。

安信可还基于eclipse开发了一个IDE环境。方便在windows下进行乐鑫sdk的编译。



# spiffs

从名字上看，这个是一个文件系统，是在spi flash的基础上做的 。

spiffs的设计灵感来自于yaffs。

spiffs就是为了单片机而设计的，单片机上一般没有复杂的堆管理能力。spiffs只需要一定的ram缓冲区就可以工作。

一般spi flash尺寸为512KB到8MB。

块一般是64K，页一般是4K。

这个文件系统的代码在这里：

https://github.com/pellepl/spiffs



# 继续基于串口和lua进行试验

根据官方网站上的简单例子进行测试。

## 测试wifi连接

```
> print(wifi.sta.getip())
nil
> wifi.setmode(wifi.STATION)
> wifi.sta.config("aa","88889999")
> print(wifi.sta.getip())
192.168.0.11    255.255.255.0   192.168.0.1
> 
```

## 作为web server

```
srv=net.createServer(net.TCP) 
srv:listen(80,function(conn) 
    conn:on("receive",function(conn,payload) 
    print(payload) 
    conn:send("<h1> Hello, NodeMcu.</h1>")
    end) 
end)
```

然后我们在电脑的浏览器输入：http://192.168.0.11/。就可以得到。

```
Hello, NodeMcu.
```



# 硬件引脚

板子引出了30个引脚。

左边，从上到下。

```
A0：
G:
VV:
S3：
S2：
S1：
SC:
S0：
SK:
G:
3V:
EN:
RST:
G:
VIN:
```

右边，从上到下。

```
D0:
D1：
D2：
D3：
D4：
3V:
G:
D5：
D6：
D7：
D8：
RX:
TX:
G:
3V:
```

![](/images/arduino（四）nodemcu-引脚定义.png)

我现在控制gpio16的电平，然后用万用表来量一下，看看是否有效。

```
gpio.mode(16,gpio.OUTPUT)
gpio.write(16,gpio.HIGH)
gpio.write(16,gpio.LOW)
```

但是报错了。

```
> gpio.mode(16,gpio.OUTPUT)
stdin:1: gpio 16 does not exist
```

我就看gpio1的吧。它跟gnd是挨着的。

```
gpio.mode(1,gpio.OUTPUT)
gpio.write(1,gpio.HIGH)
gpio.write(1,gpio.LOW)
```

我设置了没有用。一直是高电平。

我看看gpio0的。

```
gpio.mode(0,gpio.OUTPUT)
gpio.write(0,gpio.HIGH)
gpio.write(0,gpio.LOW)
```



# 内存测试

关于NodeMCU的内存测试

https://blog.csdn.net/qq_37258787/article/details/79942561

# NodeMcu网络服务器搭建

https://blog.csdn.net/FENGYULU_0701/article/details/139823822

# ota

https://blog.csdn.net/CATTLE_L/article/details/104715498

# 参考资料

1、github

https://github.com/nodemcu/nodemcu-firmware

2、官方文档

https://nodemcu.readthedocs.io

3、关于乐鑫，安信可固件使用问题，说明汇总

https://blog.csdn.net/simpleswing/article/details/77000885

4、SPIFFS技术手册

https://blog.csdn.net/zhangjinxing_2006/article/details/75050611

5、NodeMCU教程 GPIO操作与引脚映射

https://blog.csdn.net/leytton/article/details/51646624

