---
title: Linux netlink使用举例
date: 2017-02-18 14:47:10
tags:
	 - Linux
	 - netlink
---
--

netlink的主要用途就是实现内核空间和用户空间的双向通信，下面是一个例子，演示如何使用这个机制。
代码在Linux2.6的内核基础上可以正常运行，在新的内核版本上无法运行，有些结构体有调整了，接口也改了。
目录下的文件如下。

```
Makefile
netlink_2.c -- 用户态的程序
netlink_k.c -- 内核的程序，编译为ko文件。
```
先看netlink_k.c。
```
#include <linux/init.h>
#include <linux/module.h>
#include <linux/timer.h>
#include <linux/time.h>
#include <linux/types.h>
#include <net/sock.h>
#include <net/netlink.h>

#define NETLINK_TEST 25
#define MAX_MSGSIZE 1024
int stringlength(char *s);
void sendnlmsg(char * message);
int pid;
int err;
struct sock *nl_sk = NULL;
int flag = 0;

void sendnlmsg(char *message)
{
	struct sk_buff *skb_1;
	struct nlmsghdr *nlh;
	int len = NLMSG_SPACE(MAX_MSGSIZE);
	int slen = 0;
	if(!message || !nl_sk)
	{
		return ;
	}
	skb_1 = alloc_skb(len,GFP_KERNEL);
	if(!skb_1)
	{
		printk(KERN_ERR "my_net_link:alloc_skb_1 error\n");
	}
	slen = stringlength(message);
	nlh = nlmsg_put(skb_1,0,0,0,MAX_MSGSIZE,0);

	NETLINK_CB(skb_1).pid = 0;
	NETLINK_CB(skb_1).dst_group = 0;

	message[slen]= '\0';
	memcpy(NLMSG_DATA(nlh),message,slen+1);
	printk("my_net_link:send message '%s'.\n",(char *)NLMSG_DATA(nlh));

	netlink_unicast(nl_sk,skb_1,pid,MSG_DONTWAIT);

}

int stringlength(char *s)
{
	int slen = 0;


	for(; *s; s++)
	{
		slen++;
	}

	return slen;
}

void nl_data_ready(struct sk_buff *__skb)
{
	struct sk_buff *skb;
	struct nlmsghdr *nlh;
	char str[100];
	struct completion cmpl;
	int i=10;
	skb = skb_get (__skb);
	if(skb->len >= NLMSG_SPACE(0))
	{
		nlh = nlmsg_hdr(skb);

		memcpy(str, NLMSG_DATA(nlh), sizeof(str));
		printk("Message received:%s\n",str) ;
		pid = nlh->nlmsg_pid;
		while(i--)
		{
			init_completion(&cmpl);
			wait_for_completion_timeout(&cmpl,3 * HZ);
			sendnlmsg("I am from kernel!");
		}
		flag = 1;
		kfree_skb(skb);
	}

}

// Initialize netlink

int netlink_init(void)
{
	nl_sk = netlink_kernel_create(&init_net, NETLINK_TEST, 1,
	                              nl_data_ready, NULL, THIS_MODULE);
	if(!nl_sk)
	{
		printk(KERN_ERR "my_net_link: create netlink socket error.\n");
		return 1;
	}
	printk("my_net_link_3: create netlink socket ok.\n");
	return 0;
}

static void netlink_exit(void)
{
	if(nl_sk != NULL)
	{
		sock_release(nl_sk->sk_socket);
	}

	printk("my_net_link: self module exited\n");
}

module_init(netlink_init);
module_exit(netlink_exit);

MODULE_LICENSE("GPL");
```
再看netlink_2.c。
```
#include <sys/stat.h>
#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <string.h>
#include <asm/types.h>
#include <linux/netlink.h>
#include <linux/socket.h>
#include <errno.h>

#define NETLINK_TEST 25
#define MAX_PAYLOAD 1024 // maximum payload size

int main(int argc, char* argv[])
{
	int state;
	struct sockaddr_nl src_addr, dest_addr;
	struct nlmsghdr *nlh = NULL;
	struct iovec iov;
	struct msghdr msg;
	int sock_fd, retval;
	int state_smg = 0;
	// Create a socket

	sock_fd = socket(AF_NETLINK, SOCK_RAW, NETLINK_TEST);
	if(sock_fd == -1)
	{
		printf("error getting socket: %s", strerror(errno));
		return -1;
	}

	// To prepare binding

	memset(&msg,0,sizeof(msg));
	memset(&src_addr, 0, sizeof(src_addr));
	src_addr.nl_family = AF_NETLINK;
	src_addr.nl_pid = getpid(); // self pid

	src_addr.nl_groups = 0; // multi cast


	retval = bind(sock_fd, (struct sockaddr*)&src_addr, sizeof(src_addr));
	if(retval < 0)
	{
		printf("bind failed: %s", strerror(errno));
		close(sock_fd);
		return -1;
	}

	// To prepare recvmsg

	nlh = (struct nlmsghdr *)malloc(NLMSG_SPACE(MAX_PAYLOAD));
	if(!nlh)
	{
		printf("malloc nlmsghdr error!\n");
		close(sock_fd);
		return -1;
	}

	memset(&dest_addr,0,sizeof(dest_addr));
	dest_addr.nl_family = AF_NETLINK;
	dest_addr.nl_pid = 0;
	dest_addr.nl_groups = 0;

	nlh->nlmsg_len = NLMSG_SPACE(MAX_PAYLOAD);
	nlh->nlmsg_pid = getpid();
	nlh->nlmsg_flags = 0;
	strcpy(NLMSG_DATA(nlh),"Hello you!");

	iov.iov_base = (void *)nlh;
	iov.iov_len = NLMSG_SPACE(MAX_PAYLOAD);
	// iov.iov_len = nlh->nlmsg_len;

	memset(&msg, 0, sizeof(msg));

	msg.msg_name = (void *)&dest_addr;
	msg.msg_namelen = sizeof(dest_addr);
	msg.msg_iov = &iov;
	msg.msg_iovlen = 1;

	printf("state_smg\n");
	state_smg = sendmsg(sock_fd,&msg,0);

	if(state_smg == -1)
	{
		printf("get error sendmsg = %s\n",strerror(errno));
	}

	memset(nlh,0,NLMSG_SPACE(MAX_PAYLOAD));
	printf("waiting received!\n");
	// Read message from kernel

	while(1)
	{
		printf("In while recvmsg\n");
		state = recvmsg(sock_fd, &msg, 0);
		if(state<0)
		{
			printf("state<1");
		}
		printf("In while\n");
		printf("Received message: %s\n",(char *) NLMSG_DATA(nlh));
	}

	close(sock_fd);

	return 0;
}
```
再看Makefile。一次性把ko和用户态程序都编译出来。
```
obj-m := netlink_k.o 
KERNELBUILD := /lib/modules/`uname -r`/build 
default: 
	@echo "BUILE Kmod" 
	@make -C $(KERNELBUILD) M=$(shell pwd) modules 
	gcc -o netlink_2 netlink_2.c 
clean: 
	@echo " CLEAN kmod" 
	@rm -rf *.o 
	@rm -rf .depend .*.cmd *.ko *.mod.c .tmp_versions *.symvers .*.d 
```
执行情况：
1、先insmod netlink.ko
2、另外打开一个shell窗口，执行netlink程序。
3、用dmesg查看输出信息。


