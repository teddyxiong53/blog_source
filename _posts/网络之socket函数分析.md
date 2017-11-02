---
title: 网络之socket函数分析
date: 2017-11-02 22:00:07
tags:
	- 网络

---



# 服务端

1、bind函数。

这个是把一个int类型的socket跟一个sockaddr进行绑定。



2、listen函数。

listen函数使得一个socket从主动变为被动。

backlog是指处理多个连接时，可以让多少个进行排队。



3、accept函数。

输入的是前面listen的那个sock。得到的是另外一个sock值。

后续的recv和send都是用得到的sock来进行的。



