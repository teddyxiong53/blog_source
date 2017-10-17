---
title: mqtt之协议抓包分析
date: 2017-10-11 22:24:27
tags:
	- mqtt

---



环境设置如下：

1、mosquitto运行在Ubuntu虚拟机上。ip地址为192.168.190.128。

2、wireshark安装的win7的物理机上。

3、win7上下载paho的eclipse客户端。下载地址在：https://repo.eclipse.org/content/repositories/paho-releases/org/eclipse/paho/org.eclipse.paho.ui.app/1.1.1/ 。解压后就可以使用。

如果下载不下来，可以在51cto上找到。

这篇文章和https://wenku.baidu.com/view/bdbc5cb45901020206409c10.html 这篇文章一起看。

# 1.环境预备

1、在Ubuntu下启动mosquitto。

2、win7下打开eclipse paho mqtt utility工具。

3、win7 打开wireshark。选择对应的虚拟网卡，并且在网卡的过滤器那里设置：tcp and port 1883。这样就只会抓mqtt包。



# 2. 分析connect消息

在eclipse paho里填入下面的信息：

服务器地址：`tcp://192.168.190.128:1883`

客户机标识：`test-mqtt`（这个随便写）

然后点击连接。我们可以看到wireshark里已经产生了一系列的包了。

看到很多是tcp包。我们把显示这里也过滤一下，只看mqtt的。可以看到当前总共有5个mqtt消息。

依次是：2个connect消息。1个connect ack。1个ping request和1个ping response。

ping是定时在做的。不管。

我们看connect消息的内容。

```
10 15 00 04 4d 51 54 54 04 02 00 3c 00 09 74 65 73 74 2d 6d 71 74 74
```

我们逐个字节分析：

10：代表connect消息类型。

15：代表remaining length。21个字节。

00：

04：跟上面一个字节00连起来表示长度4个字节。

4d 51 54 54 ：表示MQTT的ASCII码。

04：版本。4表示3.1.1版本。

02：连接标志。

00 3c：表示keep alive的时间是60秒。

00 09：表示后面的内容的长度。是9个字节，就是test-mqtt的字节数。

74 65 73 74 2d 6d 71 74 74：test-mqtt的ASCII码。

# 3. 分析connect ack消息

这个很短。

```
20 02 00 00 
```

20：表示是connect ack消息。

02：表示后面的长度是2个字节。

00 ：保留的，没有含义。

00 ：连接成功的。

错误有6种：

00：连接成功。

01：连接拒绝。不可接受的版本。

02：client id 服务器不接受。

03：服务器连接不到。

04：用户名密码错误。

05：没有授权。

# 4. ping request和response分析

既然目前产生了这2个消息，我们就顺便看看。

request：

```
c0 00
```

就2个字节。

response：

```
d0 00
```

回复也是2个字节。



# 5. pub消息分析

我们接下来在eclipse paho里填入下面的内容：

主题：test-msg

服务质量：至少一次。“已保留”和“16进制”都不勾选。

消息：1234

然后点击发布。

可以抓到publish message和publish ack的2个包。

publish message：

```
32 10 00 08 74 65 73 74 2d 6d 73 67 00 01 31 32 33 34
```

32：表示publish message类型。

10：表示长度是16个字节。后面所有内容的长度。

00 08：表示后面的内容的长度是8个字节。就是test-msg的长度。

74 65 73 74 2d 6d 73 67： test-msg的ASCII码。

00 01：消息的id。

31 32 33 34：消息的内容。



publish ack：

```
40 02 00 01
```

40：表示publish ack消息。

02：表示后面的字节数是2个字节。

00 01：表示消息id。



我现在比较关注长度超过127的实际情况是怎样的。我把消息内容写成连续140个字符'a'。发布。抓包看。

内容不细看了。

长度显示是：98 01 。这个计算是这样的。01当成高字节。98把bit7的不要。然后拼起来就是0118就是十进制的152个字节。



# 6. sub消息分析

到这里，因为我的Ubuntu虚拟机编译安装mosquitto有问题，导致mosquitto_sub和mosquitto_pub工具不能用。我的mosquitto服务器转而在树莓派上运行。

在win7上是eclipse paho上。订阅里，添加主题rpi0和rpi1，rpi0的服务质量设置为0，rpi1的设置为1。

点击订阅按钮。可以看到抓到包了。

sub request的内容：

```
82 10 00 01 00 04 72 70 69 30 00 00 04 72 70 69 31 01
```

82：表示sub request。后面的2表示，二进制是0010，qos的是01。

10：表示消息长度是16字节。

00 01：表示message id是0001。

00 04：长度为4个字节。

72 70 69 30：rpi0的ASCII码。

00：表示qos是0 。

00 04：表示4字节。

72 70 69 31 ：rpi1的ASCII码。

01：表示qos是1 。

再看sub ack的包的内容。很简单。

```
90 04 00 01 00 01
```

90：表示sub ack消息。

04：表示4个自己。

00 01：message id。

00：表示qos是0。

01：表示qos是1。如果失败，返回是128 。



# 7. 取消订阅消息unsub分析

我们接着上面的，把rpi0和rpi1都退订。

unsub request

```
a2 0e 00 02 00 04 72 70 69 30 00 04 72 70 69 31
```

a2：表示类型是取消订阅。

0e：表示后面的内容总长度是13个字节。

00 02：message id。

00 04 ：表示后面的内容长度是4个字节。

72 70 69 30：rpi0.

00 04 ：表示后面的内容长度是4个字节。

72 70 69 31：rpi1.



unsub ack内容：

```
b2 02 00 02 00 00 
```

b2：表示unsub ack消息。

02：表示后面内容长度是2个字节。

00 02 ：message id。

00 00 ：不知道是什么，多余的。

# 8. qos为2的消息发布过程分析

qos为2的通信过程比其他情况要复杂。总共分为4步：

1、client给server发pub message。

2、server给client回复pub receive。

3、client给server发pub release。

4、server给client回复pub complete。

消息内容本身都很简单。不细看了。



