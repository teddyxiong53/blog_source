---
title: usb（三）鼠标键盘实现
date: 2018-04-05 10:48:51
tags:
	- usb

---



下面实现一个usb鼠标的功能。

在前面一章，我们已经实现了读取usb设备的id的功能了。还缺一个写字节的函数。

```
void D12WriteByte(u8 val)
{
	D12SetDataAddr();
	D12ClrWr();
	D12SetPortOut();
	D12SetData(val);
	D12SetWr();
	D12SetPortIn();
}
```

但板子重新上电的时候，必须模拟一个usb拔下的动作。

因此，我们要在程序开始的地方，需要把D12内部的上拉电阻点开。这个可以通过命令来完成。

然后延时一会儿，再把上拉电阻连接上。这样就可以模拟一个插入的动作。

主机就可以看检测到了。

D12的设置模式的命令是0xF3 。后面跟2个字节的数据写入。

第一个字节是配置字节，第二个字节是时钟分频系数。

```
void UsbDisconnect(void)
{
	D12WriteCmd(D12_SET_MODE);
	D12WriteByte(0x06);
	D12WriteByte(0x47);
	DelayMs(1000);
}
void UsbConnnect(void)
{
	D12WriteCmd(D12_SET_MODE);
	D12WriteByte(0x16);
	D12WriteByte(0x47);
}
```

# usb的中断处理

当D12芯片完成一个操作后，就会产生一个中断。

导致中断的情况有：

1、usb总线复位。

2、D12进入挂起状态。

3、收到数据。

4、发送完数据。

中断就是产生低电平。

具体是什么中断，还需要读取D12的中断寄存器来得知。

中断寄存器是一个字节，定义如下：

```
0：端点0输出。
1：端点0输入。
2：端点1输出。
3：端点1输入
4：端点2
5：
6：总线复位。
7：挂起状态改变。
```

我们可以用查询引脚电平的方式来做。

```
void func(void)
{
	while(D12GetIntPin() == 0) {
		D12WriteCmd(READ_INT_REG);
		int = D12ReadByte();
		if(int & 0x80) {
			UsbBusSuspend()
		}
		if(int & 0x40) {
			
		}
	}
}
```

我们把设备插到电脑上，可以从串口观察到打印。

显示端点0已经产生了中断。

主机到底发了什么数据给端点0呢？

下面我们要添加函数来 读取这数据。

```
//选择对应的端点
void D12SelectEndpoint(u8 point)
{
	D12WriteCmd(0x00 + point);
}

u8 D12ReadEndpointBuffer(u8 point, u8 len, u8 *buf)
{
	u8 i,j;
	D12SelectEndpoint(point);
	D12WriteCmd(D12_READ_BUFFER);
	D12ReadByte();//这个字节数据是保留的，不用
	j = D12ReadByte();//这个是接收到的数据长度。
	if(j>len) {
		j = len;//
	}
	print_str("read endpoint:");
	print_int(point/2);//除以2才是真正的端点值
	print_str("buffer:");
	print_int(j);
	print_str("bytes \n");
	for(i=0; i<j; i++) {
		D12ClrRd();
		*(buf+i) = D12GetData();
		D12SetRd();
		print_hex(*(buf+i));
		if((i+1)%16 == 0) {
			print_str("\n");
		}
	}
	return j;
}
```

我们从打印中可以看出通信过程如下：

1、主机给设备发来8个字节的数据。

2、设备在第一次接收到数据后，会停顿一段时间，这时候，主机一直在请求输入。但是程序目前还没有返回数据，所以D12芯片一直在回答NAK。就是说数据还没有准备好。

3、主机经过一段时间的等待，不耐烦了，发送了一次总线复位，然后又发来8个字节。

4、总共经过3次尝试，主机只好放弃，然后弹出usb无法识别的提示。



请求的这8个字节是什么内容呢？是在请求设备描述符。

我们自己造一个设备描述符。但是怎么把它返回给主机呢？

是通过控制端点0来返回的。

```
void D12ValidateBuffer(void)
{
	D12WriteCmd(D12_VALIDATE_BUFFER);
}

u8 D12WriteEndpointBuffer(u8 point, u8 len, u8 *buf)
{
	u8 i;
	D12SelectEndpoint(point);
	D12WriteCmd(D12_WRITE_BUFFER);
	D12WriteByte(0);//这个必须写0
	D12WriteByte(len);
	D12SetPortOut();
	for(i=0;i<len; i++) {
		D12ClrWr();
		D12SetData(*(buf+i));
		D12SetWr();
	}
	D12SetPortIn();
	D12ValidateBuffer();
	return len;
}
```



