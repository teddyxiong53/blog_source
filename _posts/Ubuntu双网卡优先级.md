---
title: Ubuntu双网卡优先级
date: 2020-12-14 17:29:30
tags:
- ubuntu
---

1

修改一下默认网关就可以了。

当前是这样，所以优先走了eth0的。这个没有代理，所以下载pypi的包非常慢。

```
root@thinkpad:~# route 
内核 IP 路由表
目标            网关            子网掩码        标志  跃点   引用  使用 接口
default         172.16.2.254    0.0.0.0         UG    0      0        0 eth0
default         192.168.1.1     0.0.0.0         UG    600    0        0 wlan0
link-local      *               255.255.0.0     U     1000   0        0 wlan0
172.16.2.0      *               255.255.255.0   U     0      0        0 eth0
172.17.0.0      *               255.255.0.0     U     0      0        0 docker0
192.168.1.0     *               255.255.255.0   U     600    0        0 wlan0
```

可以看到最上面的是eth0的。

我希望走wlan0的。

很简单，把eth0的default gw删除就好了。

```
sudo route del default gw 172.16.2.254 
```

然后再执行pip命令，就可以看到流量都是走wlan0。速度一下子就上去了。





参考资料

1、

https://blog.csdn.net/z515878963/article/details/81184068