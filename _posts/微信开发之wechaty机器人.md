---
title: 微信开发之wechaty机器人
date: 2023-01-14 20:57:31
tags:
	- 微信

---



https://github.com/wechaty/wechaty

看了一下，这个居然要基于微信网页版，但是我扫描试了一下，微信网页版已经被限制，那就没法做了。

哦，看到下面又说提供了ipad版本的接入方式。

那就先看看吧。

但是安装npm的内容，有些资源是在github上的。

所以服务器还必须翻墙才行。

```
wget -O ~/.config/clash/config.yaml  <你的订阅地址>
```

但是这样下载下来的是一个base64编码后的内容。

我直接从我的pc上把config.yml文件的内容拷贝过去粘贴进去就好了。

https://maintao.com/2021/use-clash-as-a-proxy/

这个东西就是下载不下来。

https://github.com/stedolan/jq/releases/download/jq-1.6/jq-linux64

算了。我放弃了。

