---
title: 蓝牙之socket编程
date: 2018-11-27 15:04:35
tags:
	- 蓝牙

---



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



参考资料

1、bluetooth开发（二）------基于rfcomm通信编程之服务器端

https://blog.csdn.net/wang_zheng_kai/article/details/23330329