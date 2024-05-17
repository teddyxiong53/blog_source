---
title: 蓝牙之socket编程
date: 2018-11-27 15:04:35
tags:
	- 蓝牙

---

--

# python版本

在进行蓝牙通信时，可以使用蓝牙套接字（Bluetooth socket）进行编程。

类似于传统的网络编程中的套接字，蓝牙套接字也提供了一种在蓝牙设备之间进行数据传输的方法。

以下是使用Python进行蓝牙套接字编程的简单示例：

```python
import bluetooth

# 搜索附近的蓝牙设备
devices = bluetooth.discover_devices(lookup_names=True)

# 打印已发现的设备信息
for addr, name in devices:
    print("Device:", name, " - ", addr)

# 选择要连接的设备
selected_device = devices[0]  # 假设选择第一个设备

# 创建蓝牙套接字
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)

# 连接到选定的设备
sock.connect((selected_device[0], 1))  # 1是RFCOMM通道号

# 发送数据
sock.send("Hello, Bluetooth!")

# 接收数据
data = sock.recv(1024)
print("Received:", data)

# 关闭套接字连接
sock.close()
```

在上面的示例中，首先搜索附近的蓝牙设备，然后选择要连接的设备。接下来，创建一个蓝牙套接字，并使用RFCOMM协议（通常用于蓝牙串口通信）连接到选定的设备。发送数据后，等待接收来自远程设备的响应，并最终关闭套接字连接。

需要注意的是，这只是一个简单的示例，实际应用中可能需要更多的错误处理和异常处理。此外，蓝牙通信的特性可能因设备和操作系统的不同而有所不同，因此在实际应用中可能需要更多的定制和调整。

# C语言版本

直接编译，会报bluetooth.h找不到。

需要安装蓝牙开发库。

```
sudo apt-get install libbluetooth-dev
```

```
#include <sys/socket.h>
#include <bluetooth/bluetooth.h>
#include <bluetooth/rfcomm.h>

#include <unistd.h>
#include <stdio.h>

int main()
{
	struct sockaddr_rc local_addr = {0};
	struct sockaddr_rc remote_addr = {0};
	char buf[1024] = {0};
	int opt = sizeof(remote_addr);
	int s = socket(PF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM);
	if(s < 0) {
		printf("create bt socket fail\n");
		exit(-1);
	}
	local_addr.rc_family = AF_BLUETOOTH;
	local_addr.rc_bdaddr = *BDADDR_ANY;
	local_addr.rc_channel = 1;
	int ret = bind(s, (struct sockaddr *)&local_addr, sizeof(local_addr) );
	if(ret < 0) {
		printf("bind failed\n");
		exit(-1);
	}
	ret = listen(s, 5);
	if(ret < 0) {
		printf("listen fail\n");
		exit(-1);
	}
	int client = accept(s, (struct sockaddr *)&remote_addr, &opt);
	if(client < 0) {
		printf("accept fail\n");
		exit(-1);
	}
	ba2str(&remote_addr.rc_bdaddr, buf);
	printf("accept connection from:%s \n", buf);
	memset(buf, 0, sizeof(buf));
	int bytes_read;
	while(1) {
		bytes_read = read(client, buf, sizeof(buf));
		if(bytes_read > 0) {
			printf("received:%s\n", buf);
			if(strcmp(buf, "goodbye") == 0) {
				printf("client is down\n");
				break;
			}
			memset(buf, 0, sizeof(buf));
		}
	}
	close(client);
	close(s);
	return 0;
}
```



# 参考资料

1、bluetooth开发（二）------基于rfcomm通信编程之服务器端

https://blog.csdn.net/wang_zheng_kai/article/details/23330329