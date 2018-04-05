---
title: usb（二）实验环境搭建
date: 2018-04-05 10:20:24
tags:
	- usb

---



为了能够实现不同的usb设备类，需要选择一款通用的usb接口芯片。

PDIUSBD12芯片是一个不错的选择。简称D12 。

这个是飞利浦的芯片。

1、支持usb2.0的全速模式。

2、具有软连接功能。soft connect。

3、有数据指示灯。

4、使用8位并口和mcu进行连接。数字引脚兼容5V逻辑电平

5、内置3.3V的稳压器。

7、内置锁相环。外部使用6MHz的晶振。



D12与mcu的连接。

```
1、Data，8根线。
2、int，低电平中断。
3、A0。这个是控制命令还是数据的。1表示命令，0表示数据。
4、wr、rd两根线。
5、clk
```



因为usb协议规定了操作是有时间限制的，所以调试usb的时候，不能用单步调试。

所以要用串口来观察变量，进行调试。

d12.h的头文件。

```
#define D12_CMD_ADDR 1
#define D12_DATA_ADDR 0

#define D12_DATA P0
#define D12_A0  P3_5
#define D12_WR  P3_6
#define D12_RD  P3_7
#define D12_INT P3_2

#define D12SetCmdAddr() D12_A0 = D12_CMD_ADDR
#define D12SetDataAddr() D12_A0 = D12_DATA_ADDR

#define D12SetWr()  D12_WR = 1
#define D12ClrWr()  D12_WR = 0

#define D12SetRd()  D12_RD = 1
#define D12ClrRd()  D12_RD = 0

#define D12GetIntPin()  D12_INT 

#define D12GetData() D12_DATA 
#define D12SetData(value)  D12_DATA = value

#define D12SetPortIn()  D12_DATA = 0XFF
#define D12SetPortOut()  

#define Read_ID 0xfd

void D12WriteCmd(u8);
u8 D12ReadByte(void);
u16 D12ReadID(void);
```

函数实现：

```
void D12WriteCmd(u8 cmd)
{
	D12SetCmdAddr();
	D12ClrWr();
	D12SetPortOut();
	D12SetData(cmd);
	D12SetWr();
	D12SetPortIn();
}

u8 D12ReadByte(void)
{
	u8  tmp;
	D12SetDataAddr();
	D12ClrRd();
	tmp = D12GetData();
	D12SetRd();
	return tmp;
}
```

有了上面这2个函数，就可以读取D12芯片的id了。

```
u16 D12ReadID(void)
{
	u16 id;
	D12WriteCmd(Read_ID);
	id = D12ReadByte();
	id |= ((u16)D12ReadByte())<<8;
	return id;
}
```

