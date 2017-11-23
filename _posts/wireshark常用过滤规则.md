---
title: wireshark常用过滤规则
date: 2016-11-05 16:29:06
tags:
	- wireshark
---
wireshark的过滤规则有两种，一种是抓包的过滤规则，一种是显示内容的过滤规则。
这两种规则的写法不太一样。
# 1. 抓包过滤规则
这个过滤规则在选择抓包网卡时填写。
常用的有这些：
1. 只抓取http包
```
tcp port 80
```
2. 只抓取arp包
```
ether proto 0x0806
```
3. 只抓取与某个主机的通信
```
host www.baidu.com
```
4. 只抓取icmp 
```
icmp
```

可以用的连接词有：and 、or、not。



# 2. 显示的常用过滤规则

1.过滤源ip和目标ip
```
ip.src==192.168.0.10
ip.dst==192.168.0.1
ip.addr==192.168.0.10  --这个是表示源地址和目标地址都是192.168.0.10的。
==可以用eq关键字来替代
```
2.过滤指定端口
```
tcp.port==80 --这个是把源端口和目标端口都设置为80
tcp.srcport==80
tcp.dstport==80
```
3.协议过滤
这个比较简单。直接把协议的名字填进去就可以了。
```
http
```
4.http模式过滤
```
http.request.method=="GET" --这个是过滤GET请求。
http contains "GET"
http contains "HTTP/1.1 200 OK" && http contains "Content-Types: "
```
5.多个条件的关系
```
与关系：用and关键字
或关系：用or关键字。
排除：用not或者!来做。例如不要arp数据，就"!arp"
大于 gt或者>
小于 lt 或者<
不等于 ne 或者!=
```
6.过滤mac地址
```
eth.dst
eth.src
eth.addr
用法跟ip地址类似。
```
7.包长度过滤
```
udp.length == 26
```



# 3.其他操作

1、导出图片、视频、音频文件。

这个一般是在http的包里面。

```
1、选中对应的包。
2、在下面的框里面的JPEG File Interchange Format上右键。选择导出字节分组流。然后在弹出的对话框里面，选all file。然后保存为test.jpg。就可以了。
```

