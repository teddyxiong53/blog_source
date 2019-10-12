---
title: python之scapy
date: 2019-09-21 15:35:48
tags:
	- python

---

1

在寻找自己构造ping包的工具时，发现了scapy这个工具。感觉很强大。学习一下。

安装：

```
pip install scapy
```

安装后，就可以使用了。scapy是一个命令行工具。可以进行交互使用。

交互式使用：直接在命令行输入scapy命令即可。

而在脚本里使用。则需要这样进行导入：

```
from scapy.all import *
```

基本命令：

```
ls()
	查看支持的所有内容。
ls(IP)
	查看ip包结构。
lsc()
	查看支持的命令。
```



构造报文

查看报文内容

发送报文 send

接收报文 sniff

发送和接收报文 sr

读取cap内容



基本操作：

```
# 构造一个IP数据包。
a = IP(ttl=10)
a.dst = "192.168.56.101"
```

斜杠操作符。可以表示协议栈组合。

```
>>> IP()
<IP  |>
>>> IP()/TCP()
<IP  frag=0 proto=tcp |<TCP  |>>
>>> Ether()/IP()/TCP()
<Ether  type=IPv4 |<IP  frag=0 proto=tcp |<TCP  |>>>
>>> IP()/TCP()/"GET / HTTP/1.0\r\n\r\n"
<IP  frag=0 proto=tcp |<TCP  |<Raw  load='GET / HTTP/1.0\r\n\r\n' |>>>
```

官网里提到的这句话，正是我现在需要的功能。

One that pings a whole network and gives the list of machines answering. 



构造ping包

```
def ping_once(host):
    ip_id = randint(1,65535)
    icmp_id = randint(1, 65535)
    icmp_seq = randint(1, 65535)
    packet = IP(dst=host, ttl=64, id=ip_id)/ICMP(id=icmp_id, seq=icmp_seq)/b'rootkit'
    ping = sr1(packet, timeout=2, verbose=False)
    if ping:
        print("ping {} ok".format(host))
        # sys.exit(3)
        return True
    return False
```



参考资料

1、Python Scapy使用方法

https://blog.csdn.net/Matcha_996731821/article/details/86159911

2、scapy使用入门

https://blog.csdn.net/thinkmore1314/article/details/9469763

3、官网文档

https://scapy.readthedocs.io/en/latest/