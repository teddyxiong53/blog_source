---
title: mqtt之安全
date: 2017-10-12 21:28:12
tags:
	- mqtt
	- 安全

---



物联网的网络安全问题是一个很重要的问题。但是当前其实做得很不好。

对于物联网的安全，受到这些限制：

1、加密算法对设备计算能力有要求，而物联网设备计算能力不强。

2、物联网设备的网络环境不太好。

mqtt又可以为我们做些什么呢？

1、网络层。

如果有条件，可以通过vpn或者专线来连接设备和mqtt server。提高网络传输的安全性。

2、传输层。

使用TLS加密。可以防止中间人攻击。

3、应用层。

mqtt提供了client id和username、password机制。



mqtt基于tcp，默认是不加密的。

mqtt原生支持了TLS加密。

参考这篇文章。

http://ms.csdn.net/share/5DD3BA82E6E7975B611433FF88433D38_1_IPHONE_APP



# mosquitto配置用户名和密码

## 1.先看看mosquitto的配置文件

有这些：

```
pi@raspberrypi:/etc/mosquitto$ tree
.
├── aclfile.example
├── mosquitto.conf.example
├── pskfile.example
└── pwfile.example
```

这4个都是示例文件，我们可以参考他们的格式来进行配置，不要直接用。因为里面内容很多，容易陷进去。

aclfile：acl是Access Control List的缩写。就是用来指定哪些主题是可读/可写的。哪些用户可以pub哪些主题。可以sub哪些主题。

mosquitto.conf：主要配置文件。其他的都是辅助它的。

pskfile：psk是pre-shared-key的意思。表示预设共享密码的意思。这个文件貌似没有什么太大用途。

pwfile：这个是用mosquitto_passwd工具得到的加密的密码文件。

举例：

```
pi@raspberrypi:/etc/mosquitto$ sudo mosquitto_passwd -c mypw test1
Password: 
Reenter password: 
pi@raspberrypi:/etc/mosquitto$ ls
aclfile.example  mosquitto.conf.example  mypw  pskfile.example  pwfile.example
pi@raspberrypi:/etc/mosquitto$ vi mypw 
  1 test1:$6$5Of0HGUKengGdrIZ$Y8/SSL+WtxF663gdj6gxkC52opNFuQ51G1yhWLI1D7M46Jepq2Kq+GOgLjIBnOkc9kYgS+sLrP3ZM64qWI8M6g==
```

## 2.自己配置用户名和密码

跟用户名密码相关的配置项是3个：

1、allow_anonymous：默认是true。所以我们可以匿名连接上来。

2、password_file：指定密码文件。

3、acl_file：指定访问控制文件。

