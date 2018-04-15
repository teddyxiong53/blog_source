---
title: openwrt（九）插件使用
date: 2018-04-11 22:09:08
tags:
	- openwrt

---



# adblock

默认开启的。我试了一下，的确是有效果的。研究一下实现。



# ssr

这个插件是内置的。不需要你自己去安装。

通过网页启动服务。ps查看到是这样的进程。

```
 /usr/bin/ssr-local -c /var/etc/shadowsocksr_s.json -u -l 1080 -f /var/run/ssr-local.pid
```

看看配置文件内容。

```
root@LEDE:/etc# cat /var/etc/shadowsocksr.json 
{
    
    "server": "127.0.0.1",
    "server_port": 8388,
    "local_address": "0.0.0.0",
    "local_port": 1234,
    "password": "hello!!",
    "timeout": 60,
    "method": "rc4-md5",
    "protocol": "origin",
    "obfs": "plain",
    "obfs_param": "",
    "fast_open": false
}
```

是本地的server。没法翻墙的。

我找一个有用的配置设置进去看看。

设置完之后，可以看到json配置文件内容就是改后的。

然后手机连接上来就可以上网了。

