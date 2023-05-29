---
title: ipv6（一）
date: 2018-02-13 20:08:37
tags:
	- ipv6

---



# 概念

ipv6，有128位，就是16字节。

这个地址空间可以容纳巨大数量的机器。

# 发展历史

1、1992年，一些关于互联网地址系统的建议在IETF上提出，在年底形成了白皮书。

2、1993年，IETF成立了一个临时的工作组来解决下一代的ip的问题。

3、到1996年，一系列的ipv6相关的RFC发表了出来。 因为ipv4和ipv6的地址格式不同，在将来相当长的一段时间内，都会两者共存。

4、2003年1月，IETF发布了ipv6测试网络。目的是为了测试ipv4如何向ipv6进行迁移。这个测试叫做6bone，目前已经有数十个国家加入到这个测试中。

5、2011年开始，pc和服务器都开始内置ipv6支持。

6、2012年6月6日，国际互联网协会举行了世界ipv6启动纪念日，这一天，全球ipv6开始启动。Google 、Facebook等公司宣布，开始永久性支持ipv6 。



# ipv6的地址构成

ipv6有3种表示方法：

## 冒分十六进制法

分8段，一段2个字节。

aaaa:bbbb:cccc:dddd:eeee:ffff:0000:1111

一段内部，如果是以0开头，0是可以省略的。

## 0位压缩表示法

有些情况下，可能有很多的0，这些0就可以省略不写，留着空位就好。

把0压缩成`::`。`::`只能出现一次。

```
FF01：0：0：0：0：0：1101 --> FF01：:1101
```

## 内嵌ipv4地址表示法

为了实现ipv4和ipv6的互通，ipv4地址会嵌入到ipv6地址里。表示是这样的：

```
x:x:x:x:x:x:d.d.d.d
```

前面12个字节，用冒分的十六进制，后面的4个字节，用点分十进制。

实际例子是这样：

```
::192.168.0.1
```

# 报文内容





# 地址类型

跟ipv4一样，也分为单播、组播、广播这3种。

## 单播



# 过渡技术

1、双协议栈技术。同时按照ipv4和ipv6 。

2、隧道技术。必要时将ipv6数据包封装在ipv4的数据包里。这个应对的场景是一个运行ipv6的局域网，但是骨干网是ipv4的，这个局域网为了跟外界通信，就要采取这种方式。这个技术在初期使用比较多。

3、nat。

# ipv6的优势

1、更大的地址空间。

2、使用更小的路由表。提高了路由的速度。

3、 增加了增强的组播。

4、加入了自动配置的支持。这样局域网的管理就更加简单。

5、更加安全。

6、允许扩充。

7、更好的头部格式。



目前大部分的服务器，都没有internet类型的ipv6地址。所以主要要解决的问题就是：

在ipv6 only的网络下去访问ipv4 only的服务器。

服务器要兼容ipv6需要做很多硬件和软件的升级。

ipv6在设计之初就充分考虑了ipv4和ipv6的兼容性。

运营商会提供一个中间节点。使用DNS64/NAT64等技术。

负责协议的转换和地址的转换。打通ipv4和ipv6之间的链路。



使用域名方式访问服务器

```
大部分app都是这样。
```



使用ip地址访问服务器

```
需要分区域的游戏会使用这种方法。
```



# Linux怎样支持ipv6

# 检查ipv6支持

你可以访问这个网站，<http://test-ipv6.com/>，来检测你的宽带是否支持ipv6.

网上常见的路由器固件比如openwrt、padavan、LEDE等常见的路由器固件都是支持IPv6的。

不过需要格外注意的是，通过路由器获取IPv6地址时，**只有获取到原生IPv6地址才能用于上网**。

国内三大运营商的IPv6地址分配情况分别是：

电信为240e开头的（240e::/20）；移动为2409开头的（2409:8000::/20）；联通为2408开头的（2408:8000::/20）。

**如果获取到的是fe80开头的地址，是不能拿来上网的。**

整体而言，目前国内大部分地区的家庭宽带和4G网络基本都已用上IPv6协议，但部分家庭路由器对IPv6的支持欠佳。

# 编程连接ipv6的服务器

## tcp编程

要在Python中使用Socket编程连接到IPv6地址，可以使用`socket`模块中的`socket.AF_INET6`来创建IPv6套接字对象。然后，使用`socket.connect()`方法来建立与目标IPv6地址的连接。

下面是一个简单的示例代码，演示了如何连接到IPv6地址：

```python
import socket

# 创建IPv6套接字对象
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# 目标IPv6地址和端口
ipv6_addr = '2001:db8::1'  # 替换为目标IPv6地址
port = 8888  # 替换为目标端口

# 连接到目标IPv6地址
sock.connect((ipv6_addr, port))

# 在连接成功后，可以进行读写操作
# 例如，发送数据
data = 'Hello, World!'
sock.send(data.encode())

# 接收响应数据
response = sock.recv(1024)
print(response.decode())

# 关闭套接字连接
sock.close()
```

在代码中，首先创建了一个IPv6套接字对象`sock`，然后通过`sock.connect()`方法连接到目标IPv6地址和端口。连接成功后，可以使用`sock.send()`方法发送数据，使用`sock.recv()`方法接收响应数据。最后，记得关闭套接字连接。

请根据实际情况替换代码中的目标IPv6地址和端口，并根据需要进行适当的错误处理和异常处理。

## http编程

要在Python中使用HTTP编程连接到IPv6地址，可以使用`http.client`模块中的`HTTPConnection`类，并通过`socket.AF_INET6`创建IPv6套接字对象。

下面是一个示例代码，演示了如何使用HTTPConnection连接到IPv6地址：

```python
import http.client

# 目标IPv6地址和端口
ipv6_addr = '2001:db8::1'  # 替换为目标IPv6地址
port = 80  # 替换为目标端口

# 创建IPv6套接字对象
sock = socket.socket(socket.AF_INET6, socket.SOCK_STREAM)

# 创建HTTPConnection对象并连接到目标IPv6地址
conn = http.client.HTTPConnection(ipv6_addr, port, source_address=(sock, 0, 0, 0))

# 发送HTTP请求
conn.request('GET', '/')

# 获取HTTP响应
response = conn.getresponse()

# 打印响应状态码和内容
print('Response Status:', response.status)
print('Response Content:', response.read().decode())

# 关闭连接
conn.close()
```

在代码中，首先创建了一个IPv6套接字对象`sock`，然后使用`HTTPConnection`类创建了一个HTTP连接对象`conn`，并通过`source_address`参数指定了套接字对象。然后，使用`conn.request()`方法发送HTTP请求，并使用`conn.getresponse()`方法获取HTTP响应。最后，打印响应的状态码和内容，并关闭连接。

请根据实际情况替换代码中的目标IPv6地址和端口，并根据需要进行适当的错误处理和异常处理。

# ipv6的使用场景

IPv6在以下几个方面得到广泛应用：

1. 网络通信：IPv6被设计用于替代现有的IPv4协议，以解决IPv4地址耗尽的问题。IPv6在互联网通信中扮演着重要角色，提供了更大的地址空间和更好的网络连接性能。

2. 云计算和数据中心：IPv6在云计算和数据中心环境中得到广泛采用。大规模的云服务提供商和数据中心运营商使用IPv6来支持更多的主机和设备连接，提供更好的可扩展性和性能。

3. 物联网（IoT）：随着物联网设备的普及，IPv6成为了连接大量物联网设备的关键技术。IPv6的地址空间足够大，可以为每个物联网设备分配一个唯一的全局地址，从而实现设备间的直接通信和远程管理。

4. 移动通信：IPv6在移动通信领域的应用越来越重要。随着移动设备的增多和移动网络的发展，IPv6可以提供更多的地址，更好地支持移动设备的连接和移动性管理。

5. 内部网络：许多组织和企业在内部网络中开始采用IPv6，以提供更多的IP地址和更好的网络性能。IPv6可以支持更多的终端设备和服务，并提供更好的网络安全性和管理能力。

总的来说，IPv6在全球范围内的网络通信、云计算、物联网、移动通信和内部网络等领域都有广泛的应用。随着IPv4地址耗尽的压力不断增加，IPv6的重要性和应用范围将进一步扩大。



# OpenThread介绍



# 参考资料

1、

https://www.jianshu.com/p/1312e98cd35b

2、Linux下IPV6详细介绍及配置实例

<https://baijiahao.baidu.com/s?id=1597058589536595545&wfr=spider&for=pc>

3、支持ipv6的路由器有哪些？

<https://www.zhihu.com/question/21982242>