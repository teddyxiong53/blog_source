---
title: proteus研究
date: 2023-05-29 20:14:11
tags:
	- 电路仿真
---

--

# 资源收集

Proteus8 STM32F4仿真

https://www.zhihu.com/column/c_1231215635280945152

# 安装和破解

我只是需要它的模拟仿真功能。

下载地址

链接：[https://pan.baidu.com/s/1sZFy2ZK1YnUsBHZI0GMs5g](https://link.zhihu.com/?target=https%3A//pan.baidu.com/s/1sZFy2ZK1YnUsBHZI0GMs5g)

提取码：t2ck

用油猴脚本的“网盘直链下载助手脚本”配合IDM可以快速下载。



https://zhuanlan.zhihu.com/p/484917126

# 写一个简单的51 HelloWorld

配合sdcc来做。

就参考这个做。很顺利。用sdcc编译器支持编译运行了。

https://bbs.21ic.com/icview-2885716-1-1.html

# arduino mega2560

这个是新建proteus工程时，可以选择这个内置的板子。

然后代码直接这样就可以。这个代码是让chatgpt生成的。

```
void setup() {
  pinMode(13, OUTPUT);  // 设置Pin 13为输出
}

void loop() {
  digitalWrite(13, HIGH);  // 设置Pin 13为高电平
  delay(1000);             // 延迟1秒
  digitalWrite(13, LOW);   // 设置Pin 13为低电平
  delay(1000);             // 延迟1秒
}

```

头文件都不用写，直接可以编译过运行。

效果是板子上的灯会闪烁。

内置的工具和相关的源代码文件都是在这个目录下面。

D:\Program Files (x86)\Labcenter Electronics\Proteus 8 Professional\Tools



# 进行arduino实验

https://forum.arduino.cc/t/adding-arduino-library-in-proteus-8/270694

http://microprocessor2015.blogspot.com/2015/03/simple-project-proteus-8-with-arduino.html



# esp8266添加

https://www.youtube.com/watch?v=8ALOH3QRptA&ab_channel=ArduinoMagix

对应的文件在这里下载。

https://arduinomagix.blogspot.com/2019/01/how-to-use-nodemcu-in-proteus.html