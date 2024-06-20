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



# codec的pvdd和dvdd分别是什么

在音频编解码器（codec）中，PVDD和DVDD分别指的是模拟电源和数字电源。具体来说：

- **PVDD（Power Voltage for Analog section）**：这是提供给编解码器内部模拟电路部分的电源电压。这些模拟电路通常包括模拟输入和输出放大器、ADC（模数转换器）、DAC（数模转换器）等。模拟电路对电源噪声非常敏感，因此通常需要稳定、低噪声的电源。

- **DVDD（Digital Voltage for Digital section）**：这是提供给编解码器内部数字电路部分的电源电压。这些数字电路通常包括数字信号处理单元、控制接口（如I2C、SPI）等。数字电路对电源噪声的敏感度相对较低，但仍需要稳定的电源以确保可靠工作。

### 两者的区别
1. **电源噪声敏感度**：
   - **PVDD**：对噪声敏感，需要低噪声电源。
   - **DVDD**：对噪声相对不太敏感，但仍需稳定。

2. **电路类型**：
   - **PVDD**：用于模拟电路（如ADC、DAC、放大器）。
   - **DVDD**：用于数字电路（如DSP、控制接口）。

3. **电源电压**：
   - **PVDD**：通常与模拟电路的工作电压相匹配，可能较高。
   - **DVDD**：通常与数字电路的工作电压相匹配，可能较低。

### 连接和布局建议
- **分离电源**：为了减少电源噪声的互相干扰，模拟和数字电源通常需要分开提供，并且在PCB布局时，模拟和数字地（GND）也应尽量分离，最终在一点接地。
- **滤波和去耦**：在PVDD和DVDD引脚附近添加适当的去耦电容（如0.1µF和10µF），以滤除高频噪声和稳定电源。

确保PVDD和DVDD的正确供电和布局，对于音频编解码器的性能和稳定性非常重要。详细的电源和布局建议可以参考AD82128的数据手册中的相关章节。
