---
title: 网络之tcp粘包问题
date: 2019-11-27 13:25:06
tags:
	- 网络
---

1

只有tcp有粘包问题，udp是没有的。

根本原因是nagle算法要尽量避免小包阻塞网络，所以一般要求达到一定的数据量才真正往外发送。

tcp是基于流的协议。

应用层必须以消息为单位提取数据。

粘包问题，主要就是接收方不知道消息的边界，不知道一次性应该提取多少数据造成的。

假设客户端分别发了D1和D2这2个数据包给服务端。

因为服务端一次读取的字节数是不确定的，所以可能存在下面这4种情况：

```
1、服务端分两次读取到完整的D1和D2，没有粘包和拆包。
	这个是最理想的情况。
2、服务端一次读到了完整的D1和D2，D1和D2粘到一起了。
	这个就是粘包。
3、服务端第一次读取到D1和D2_1（D2的一部分），第二次读取到D2_2（D2剩下的部分）。
	这个就是拆包。
4、服务端第一次读取到D1_1（D1的一部分），第二次读取到了D1剩下的部分和完整的D2.
```



我们用代码演示。

#1

server.py

```
from socket import *
ip_port = ('127.0.0.1', 8080)
server = socket(AF_INET, SOCK_STREAM)
server.bind(ip_port)
server.listen(5)

conn,addr = server.accept()
data1 = conn.recv(10)
data2 = conn.recv(10)

print('--->', data1.decode('utf-8'))
print('--->', data2.decode('utf-8'))

conn.close()
```

client.py

```
from socket import *
ip_port = ('127.0.0.1', 8080)
BUFSIZE = 1024
s = socket(AF_INET, SOCK_STREAM)
res = s.connect(ip_port)
s.send('hello'.encode('utf-8'))
s.send('world'.encode('utf-8'))
```

得到的结果：

```
('--->', u'helloworld')
('--->', u'')
```

可以看到D1和D2粘到了一起了。

# 2

之是把server.py里的

```
data1 = conn.recv(10)
data2 = conn.recv(10)
```

改成：

```
data1 = conn.recv(2) //第一次只收2个字节。
data2 = conn.recv(10)
```

结果：

```
('--->', u'he')
('--->', u'lloworld')
```

这就是收到了D1的一部分，第二次收到了D1的剩余部分和D2 。



问题的关键在于，要让接收端知道需要收多少字节。



解决方案有：

```
1、定长包。
	如果包长不够，用无效字节填上。
	优点是简单，缺点是无效数据降低效率。
2、尾部标记。
	例如http就是这种。
3、头部标记长度。
	这个是最好的方式。
	
```

具体代码操作上，是怎么做呢？

分两次发？分两次收？

发可以一次发，收，还是需要先提前只收包头长度，用这个长度做依据再收数据。收完就交给函数去处理。



这个主要是客户端关注。

关键是两层循环：

外层：网络接收循环。

内层：解析循环。



```
char tmp[];
Buffer buffer;
// 网络循环：必须在一个循环中读取网络，因为网络数据是源源不断的。
while(1){
    // 从TCP流中读取不定长度的一段流数据，不能保证读到的数据是你期望的长度
    tcp.read(tmp);
    // 将这段流数据和之前收到的流数据拼接到一起
    buffer.append(tmp);
    // 解析循环：必须在一个循环中解析报文，应对所谓的粘包
    while(1){
        // 尝试解析报文
        msg = parse(buffer);
        if(!msg){
            // 报文还没有准备好，糟糕，我们遇到拆包了！跳出解析循环，继续读网络。
            break;
        }
        // 将解析过的报文对应的流数据清除
        buffer.remove(msg.length);
        // 业务处理
        process(msg);
    }
}
```



参考资料

1、粘包问题及解决

https://www.cnblogs.com/zhouxuchong/p/11576275.html

2、如何解决tcp通信中的粘包问题？

https://blog.csdn.net/m0_37829435/article/details/81747488

3、c/c++网络编程 对象的传输 以及 TCP粘包处理 解析

https://blog.csdn.net/luoti784600/article/details/12646405

4、炮打TCP - 关于一而再再而三的粘包拆包问题的大字报

https://github.com/ideawu/FUCK_TCP