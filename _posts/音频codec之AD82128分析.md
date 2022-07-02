---
title: 音频codec之AD82128分析
date: 2022-02-16 20:00:25
tags:
	- 音频

---

--

现在使用ad82128这个codec做功放，需要进行功耗优化，所以把相关细节梳理一下。

先把datasheet读一遍。有90页左右。

Volume control (+24dB~-103dB, 0.125dB/step)

Programmed 3D surround sound 

 Anti-pop design

Supports I2C control without clock 

Support hardware and software reset 

寄存器表格

```
0x00
0x01
0x02
	都是控制寄存器
0x03
	master volume
	从+12dB到-103dB，step值是0.5dB
	0x00表示+12dB。
	0xe6表示-103dB
0x04
0x05
0x06
0x07
0x08
0x09
	这些都是channel volume
	从channel1到channel6
0x0c
	控制寄存器
0X0D, 0X0E ,0X0F,0X10,0X11,0X12, 0X13,0X14 : 
	Channel configuration registers
	DRC这些控制。
0x1A
0x1B
0x1C
	控制寄存器
0X1D ~0X2D : 
	User-defined coefficients registers
0X33 : State control 8
0X35/0X36: Volume fine tune
0X37 : Device number and Version number
0X38 : level meter clear
0X39 : Power meter clear
0X5A : I2S output selection
0X5E : Analog gain
	For 12V application, setting +9.5dB is suggested.
0X69 : TDM word length selection
0X6A : TDM offset
	0到255个bclk
0X6B : PWM frequency selection

```



codec  probe流程

```
1、regulator_bulk_enable，然后sleep 10ms
2、
```



参考资料

