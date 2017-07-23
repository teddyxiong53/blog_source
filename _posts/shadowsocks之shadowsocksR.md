---
title: shadowsocks之shadowsocksR
date: 2017-07-23 01:12:40
tags:
	- shadowsocks

---

现在我的shadowsocks翻墙非常不稳定。不得不寻求改进的方法。网上看到shadowsocksR这个，是从shadowsocks衍生而来。加入了一些高级特性。这个作者是breakwa11。在Google+上比较活跃。

下面安装试用一下。

# 1. 下载代码

用SecureCRT连接到vps上。

```
git clone -b manyuser https://github.com/shadowsocksr/shadowsocksr.git
```

下载过程比较慢。在`Resolving deltas`这一步卡了很久。我选择用wget来下载压缩包。



下载下来的代码，根目录shadowsocksr 是多用户版本，一般是给站长用的。个人用户出于简单考虑，先不用。



# 2. 启动服务

```
./server.py -c /etc/shadowsocks.json -d start -O auth_sha1_v4 -o http_simple
```

试了，好像不行。

我下载了对应的SSR Android客户端，还是效果很不好。也许不能怪这个。

下载windows版本的客户端看看。感觉作者给的下载地址也是在各种捉迷藏，估计也是被逼的。

还是不行。

看来现在这条路走不通了。









