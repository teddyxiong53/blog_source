---
title: tcp和udp的server和client实例代码
date: 2017-02-18 17:32:33
tags:
---
tcp_server.c
```
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main()
{
	//ignore all error to make code simple and clean
	//1. get a sock, like a file
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	if(sock < 0) {printf("sock create failed \n"); exit(1);}
	
	//2. get server_addr struct 
	struct sockaddr_in server_addr, client_addr;
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(5000);
	server_addr.sin_addr.s_addr = INADDR_ANY;
	memset(&server_addr.sin_zero, 0, sizeof(server_addr.sin_zero));
	//3. bind sock and server addr
	int ret = bind(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
	//4. listen this sock
	ret = listen(sock, 1024);
	if(ret) {printf("sock bind or listen failed \n"); exit(1);}
	int connected_sock;
	static int stop = 0;
	int sin_size = 0;
	while(!stop)
	{
		sin_size = sizeof(struct sockaddr_in);
		//5. accept
		connected_sock = accept(sock, (struct sockaddr *)&client_addr, &sin_size);
		printf("get connect from:(%s, %d)\n", inet_ntoa(client_addr.sin_addr), ntohs(client_addr.sin_port));
		char recv_data[1024] = {0};
		//6. recv and proc
		while(1)
		{
			char *send_data = "welcome to here";
			memset(recv_data, 0, 1024);
			send(connected_sock, send_data, strlen(send_data), 0);
			int recv_bytes = recv(connected_sock, recv_data, 1024, 0);
			if(recv_bytes <= 0)
			{
				close(connected_sock);
				break;
			}
			recv_data[recv_bytes] = '\0';
			if(strcmp(recv_data, "q") == 0)
			{
				printf("quit current connection \n");
				close(connected_sock);
				break;
			}
			else if(strcmp(recv_data, "exit") == 0)
			{
				printf("stop server \n");
				close(connected_sock);
				stop = 1;
				break;
			}
			else
			{
				printf("receive data:[%s] \n", recv_data);
				
			}
		}
	}
	close(sock);
	return 0;
}
```

tcp_client.c
```
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main()
{
	//1. get sock 
	int sock = socket(AF_INET, SOCK_STREAM, 0);
	//2. get server addr
	struct sockaddr_in server_addr = {};
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(5000);
	server_addr.sin_addr.s_addr = inet_addr("127.0.0.1"); 
	//3. use sock to connect the server
	int ret = connect(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
	int recv_bytes = 0;
	char recv_data[1024] = {0};
	char send_data[1024] = {0};
	int send_bytes = 0;
	while(1)
	{
		memset(recv_data, 0, 1024);
		memset(send_data, 0, 1024);
		scanf("%s", send_data);
		printf("input str:%s \n", send_data);
		if(strcmp(send_data, "q") == 0)
		{
			printf("exit client \n");
			break;
		}
		send_bytes = send(sock, send_data, strlen(send_data), 0);
		if(send_bytes != strlen(send_data))
		{
			printf("send err \n");
			break;
		}
		#if 0
		recv_bytes = recv(sock, recv_data, 1024, 0);
		if(recv_bytes <= 0)
		{
			break;
		}
		recv_data[recv_bytes] = '\0';
		printf("recv data:%s \n", recv_data);
		#endif
	}
	printf("-------exit------------\n ");
	close(sock);
}
```


运行测试：
1、编译：
`gcc tcp_server.c -o tcp_server`
`gcc tcp_client.c -o tcp_client`
2、测试
先运行tcp_server，再运行tcp_client。tcp_client输入的字符会在tcp_server打印打出来。



一些注意的点：
1、`INADDR_ANY`的现实意义是：一台服务器由多个网卡，网卡可能还会经常变动，这个值的意义在于表示，不管网卡怎么变动，只要是发到这个服务器上5000这个端口（代码里指定的）的，不管从哪个网卡进来的，我都要处理。
2、accept和recvfrom的len参数都是指针，需要先定义一个变量出来取地址，不然有问题的。



下面看udp的。
udp_server.c
```
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main()
{
	//1. get sock
	int sock = socket(AF_INET, SOCK_DGRAM, 0);
	if(sock < 0)
	{
		printf("create socket failed \n");
		exit(1);
	}
	//2. get server_addr
	struct sockaddr_in server_addr = {}, client_addr = {};
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(5001);
	server_addr.sin_addr.s_addr = INADDR_ANY;
	
	//3. bind sock and server_addr
	int ret = bind(sock, (struct sockaddr *)&server_addr, sizeof(struct sockaddr));
	int stop = 0;
	int recv_bytes = 0;
	char recv_data[1024] = {};
	int addr_size = sizeof(struct sockaddr);
	while(!stop)
	{
		//4. recv 
		recv_bytes = recvfrom(sock, recv_data, 1024-1, 0, (struct sockaddr *)&client_addr, addr_size);
		#if 0 //should not add this code here  
		if(recv_bytes <= 0)
		{
			printf("recvfrom error, now exit \n");
			break;
		}
		#endif
		recv_data[recv_bytes] = '\0';
		if(strcmp(recv_data, "exit") == 0)
		{
			printf("recv exit , now exit \n");
			break;
		}
		printf("recv data:%s \n", recv_data);
	}
	close(sock);
}
```
tpc_client.c。
```
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>

int main()
{
	//1. get sock
	int sock = socket(AF_INET, SOCK_DGRAM, 0);
	//2. get server_addr
	struct sockaddr_in server_addr = {};
	server_addr.sin_family = AF_INET;
	server_addr.sin_port = htons(5001);
	server_addr.sin_addr.s_addr = inet_addr("127.0.0.1");
	char send_data[1024] = {};
	int send_bytes = 0;
	int addr_size = sizeof(struct sockaddr);
	while(1)
	{
		memset(send_data, 0, 1024);
		scanf("%s", send_data);
		printf("input_str:%s \n", send_data);
		if(strcmp(send_data, "exit") == 0)
		{
			printf("udp client exit \n");
			break;
		}
		//3. sendto
		send_bytes = sendto(sock, send_data, 1024-1, 0, (struct sockaddr *)&server_addr, addr_size);
		if(send_bytes <= 0)
		{
			printf("send error \n");
			break;
		}
		
	}
	close(sock);
}
```
编译运行与tcp的类似。

send函数返回0，只会在send数据长度是0的时候发生，这个时候，说明所有数据都发送完了。
