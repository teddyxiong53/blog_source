---
title: Linux命令之tcpdump
date: 2017-08-08 22:54:52
tags:

	- Linux命令

---

1

tcpdump是一个抓包工具。抓包的时候，最好把网卡设置为混杂模式，这就需要root权限。

# 常用命令

普通情况下，直接启动tcpdump将监视第一个网络接口上所有流过的数据包。

```
tcpdump
```

抓包的结果，就直接在当前控制台打印出来。



基本选项：

```
-i wlan0：指定网卡，interface缩写。
src host 192.168.0.10 指定本机的哪个网卡。
dst host 114.114.114.114 指定目标主机。
src port 1234 本机端口
dst port 80  目标端口

可以使用and or not这些逻辑条件。
-w xx 结果写入到文件xx里。而不是打印在控制台。
```



抓mqtt包

```
tcpdump -AX -i wlan0   tcp port 39486 -w mqtt.cap
```

39486 这个是本地的端口号，对方的端口号是1883 。

可以写目的端口号，是这样：

```
tcpdump -AX -i wlan0   dst port 1883 -w mqtt.cap
```







 根据以上分析，可以通过改善tcpdump上层的处理效率来减少丢包率，下面的几步根据需要选用，每一步都能减少一定的丢包率
 1. 最小化抓取过滤范围，即通过指定网卡，端口，包流向，包大小减少包数量
 2. 添加-n参数，禁止反向域名解析
 3. 添加-B参数，加大OS capture buffer size
 4. 指定-s参数, 最好小于1000
 5. 将数据包输出到cap文件
 6. 用sysctl修改SO_REVBUF参数，增加libcap缓冲区长度:/proc/sys/net/core/rmem_default和/proc/sys/net/core/rmem_ma



# 基本用法

查看进出host的包

```
tcpdump host 192.168.1.10 -i wlan0
```

查看目标是host的包

```
tcpdump dst 192.168.1.10 -i wlan0
```

查看来源是host的包

```
tcpdump src 192.168.1.10 -i wlan0
```

查看net下面的包

```
tcpdump net 192.168.1.0/24 -i wlan0
```

把icmp包的内容用16进制打印出来。

```
tcpdump -X icmp -i lwan0
```

查看指定端口的包

```
tcpdump port 80 -i wlan0
```

查看指定来源端口的包。

```
tcpdump src port 80 -i wlan0
```

查看指定协议的包

```
tcpdump icmp -i wlan0
```

显示所有的ipv6的包。

```
tcpdump ip6 -i wlan0
```

上面这个的测试，可以用ping6工具来ping一个ipv6地址。

查看一个范围的端口。

```
tcpdump portrange 21-23
```

查看指定大小的包。

```
tcpdump less 32 -i wlan0
tcpdump greater 64 -i wlan0
tcpdump <= 128 #这个不行
```

抓包写入文件。

```
tcpdump -w 1.txt -i wlan0
```

读取文件

```
tcpdump -r 1.txt
```

# 高级用法

逻辑

用单词或者符合都可以。尽量不用符合，用单词，因为命令行可能解释不对。

```
and &&
or ||
not !
```

一个基本的选项组合

```
tcpdump -ttnnvvS
```

不解析主机名和端口号。使用绝对seq num，用可读的时间戳。

这个是在树莓派上抓取我的手机访问80端口的包。注意and是必须的，不然就提示语法错误。

```
tcpdump -i wlan0 -ttnnvvS src 192.168.1.104 and dst port 80
```

抓一个网络到另外一个网络的包。

```
tcpdump -i wlan0 -ttnnvvS src net 192.168.1.0/24 and dst net 172.16.2.0/23 or 10.0.0.0/8
```

查看目标host所有非icmp的包。

```
tcpdump -i wlan0 dst 192.168.1.104 and not icmp
```

使用单引号。

```
tcpdump -i wlan0 'src 192.168.1.104 and (dst port 80 or 443)'
```

# 剥离tcp flags

下面都是过滤rst包。两种写法等效。后面一种直观。

```
tcpdump 'tcp[13] & 4!=0'
tcpdump 'tcp[tcpflags] == tcp-rst'
```

过滤syn包。

```
tcpdump 'tcp[13] & 2!=0'
tcpdump 'tcp[tcpflags] == tcp-syn'
```

syn和ack都设置了的包。

```
tcpdump 'tcp[13]=18'
```

过滤urg包。

```
tcpdump 'tcp[13] & 32!=0'
tcpdump 'tcp[tcpflags] == tcp-urg'
```

过滤ack包。

```
tcpdump 'tcp[13] & 16!=0'
tcpdump 'tcp[tcpflags] == tcp-ack'
```

过滤push包。

```
tcpdump 'tcp[13] & 8!=0'
tcpdump 'tcp[tcpflags] == tcp-push'
```

过滤fin包。

```
tcpdump 'tcp[13] & 1!=0'
tcpdump 'tcp[tcpflags] == tcp-fin'
```



过滤ssh连接包。不管是哪个端口是ssh，都可以抓到。

```
tcpdump 'tcp[(tcp[12]>>2):4] = 0x5353482D'
```

# 指定协议

```
tcpdump udp
tcpdump proto 17 #这个也是udp协议的意思。
```



# 复杂命令

```
tcpdump port http or port ftp or port smtp or port imap or port pop3 or port telnet -lA | egrep -i -B5 'pass=|pwd=|log=|login=|user=|username=|pw=|passw=|passwd= |password=|pass:|user:|username:|password:|login:|pass |user '
```

这个命令，可以把http、ftp、smtp、telnet等的密码登陆行为抓取到。

可以看到明文密码。

是一条很有用的命令。

在路由器上执行，就可以获取到在路由器上执行登陆操作的密码。

-A表示用ASCII码打印输出，对于web应用很有用。

egrep是grep的增强版本，就像vim是vi的增强版本一样。

它的-i表示忽略大小写。-B5表示在匹配行之前，多打印5行。

然后就搜索里面的user和password相关的关键词。



```
tcpdump -w - |pv -bert >/dev/null
```

这个命令可以监控实时的网速。



从tcpdump抓包文件里，找出统计信息。

```
tcpdump -nr capture.file | awk '{print }' | grep -oE '[0-9]{1,}.[0-9]{1,}.[0-9]{1,}.[0-9]{1,}' | sort | uniq -c | sort -n
```



-s0这个选项，表示包的长度没有限制。对于你要抓一个大的文件，是有用的。





抓get

```
tcpdump -s 0 -A -vv 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x47455420'
```

抓post

```
tcpdump -s 0 -A -vv 'tcp[((tcp[12:1] & 0xf0) >> 2):4] = 0x504f5354'
```

拿到http url

```
tcpdump -s 0 -v -n -l | egrep -i "POST /|GET /|Host:"
```



抓post 密码

```
tcpdump -s 0 -A -n -l | egrep -i "POST /|pwd=|passwd=|password=|Host:"
```

抓到cookie

```
tcpdump -nn -A -s0 -l | egrep -i 'Set-Cookie|Host:|Cookie:'
```

抓邮件信息。

```
tcpdump -nn -l port 25 | grep -i 'MAIL FROM\|RCPT TO'
```

我在微信里写了邮件发送，没有抓到。



参考资料

1、tcpdump 抓包工具使用

https://www.cnblogs.com/yorkyang/p/7654647.html

2、tcpdump丢包分析

https://blog.csdn.net/blade2001/article/details/41543297

3、tcpdump 很详细的

实际上就是man手册的翻译。

http://blog.chinaunix.net/uid-11242066-id-4084382.html

4、A tcpdump Tutorial with Examples — 50 Ways to Isolate Traffic

https://danielmiessler.com/study/tcpdump/

5、HOWTO :: SNIFFING PLAIN TEXT USERNAMES AND PASSWORD CREDENTIALS USING TCPDUMP LINUX COMMAND LINE TOOL

https://www.lexo.ch/blog/2012/09/howto-sniffing-plain-text-usernames-and-password-credentials-using-tcpdump-linux-command-line-tool/

6、Tcpdump Examples

https://hackertarget.com/tcpdump-examples/