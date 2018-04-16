---
title: arduino（五）arduino源码分析
date: 2018-04-16 16:23:09
tags:
	- arduino

---



前面稍为看了一下esp8266的代码是如何编译链接的。但是都是在esp8266的目录下。那边把情况更加复杂化了。

我们现在就从一个Blink程序开始看，不涉及esp8266，就以最简单的arduino Uno的为例。看看是哪些目录的哪些文件一起链接得到的最终的文件。看看这些文件的层次关系是什么。

主要文件是在D:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino 这个目录下面。

我们仔细看看这个下面的内容。下面总共44个文件。没有子目录。

```
abi.cpp：里面就2个函数。avr架构需要的。
Arduino.h：声明了一些函数。
binary.h：二进制的01定义。#define B10101000 168 全是这种宏定义。
CDC.cpp：要使能usb才编译。
Client.h：Stream的子类。
HardwareSerial.cpp
HardwareSerial.h
HardwareSerial_private.h
HardwareSerial0.cpp
HardwareSerial1.cpp
HardwareSerial2.cpp
HardwareSerial3.cpp
hooks.c
IPAddress.cpp：IPAddress类。
IPAddress.h
main.cpp ：这里是入口。
new.cpp ：定义了new和delete。
new.h
PluggableUSB.cpp
PluggableUSB.h
Print.cpp
Print.h
Printable.h
Server.h
Stream.cpp
Stream.h
Tone.cpp
Udp.h
USBAPI.h
USBCore.cpp
USBCore.h
USBDesc.h
WCharacter.h
WInterrupts.c
wiring.c
wiring_analog.c
wiring_digital.c
wiring_private.h
wiring_pulse.c
wiring_pulse.S
wiring_shift.c
WMath.cpp
WString.cpp
WString.h
```

我们从main.cpp开始看，这里是入口。

```
int main(void)
{
	init();//这里就是avr单片机的一些寄存器设置。
	initVariant();//用户可以自己定义。默认这里弱定义了一个空函数。
#if defined(USBCON)
	USBDevice.attach();
#endif
	setup();
	for (;;) {
		loop();
		if (serialEventRun) serialEventRun();
	}     
	return 0;
}
```

所以其实很简单，没什么可说的。

new.cpp里的内容。原来就是这么弄的啊。

```
void *operator new(size_t size) {
  return malloc(size);
}

void *operator new[](size_t size) {
  return malloc(size);
}

void operator delete(void * ptr) {
  free(ptr);
}

void operator delete[](void * ptr) {
  free(ptr);
}
```

主要值得注意的就是c++的机制。

我要理清楚，Serial.print，怎么连接到串口的寄存器操作上去的。

这个我还是依据esp8266的来看。

1、在HardwareSerial.h了。

```
extern HardwareSerial Serial;
```

先看Serial的begin函数，一般用这个来设置波特率。

```
    void begin(unsigned long baud)
    {
        begin(baud, SERIAL_8N1, SERIAL_FULL, 1);
    }
    同名函数，实际上是这个。void begin(unsigned long baud, SerialConfig config, SerialMode mode, uint8_t tx_pin);
```

这个函数在HardwareSerial.cpp里实现。

```
void HardwareSerial::begin(unsigned long baud, SerialConfig config, SerialMode mode, uint8_t tx_pin)
{
    if(uart_get_debug() == _uart_nr) {
        uart_set_debug(UART_NO);
    }

    if (_uart) {
        free(_uart);
    }

    _uart = uart_init(_uart_nr, baud, (int) config, (int) mode, tx_pin);//关键是这一行。
    _peek_char = -1;
}
```

uart_init在uart.c里实现。

然后主要看write函数。

```
size_t HardwareSerial::write(uint8_t c)
{
    if(!_uart || !uart_tx_enabled(_uart)) {
        return 0;
    }

    uart_write_char(_uart, c);
    return 1;
}
```

write参数是一个u8的参数。怎么跟print挂钩的。

因为HardwareSerial是Stream的子类，Stream是Print的子类。

Print类里有个虚函数：

```
virtual size_t write(uint8_t) = 0;
```

那就是这里对接的了。





# 参考资料

1、Arduino工程源码分析

https://blog.csdn.net/conquerusb/article/details/69262896

