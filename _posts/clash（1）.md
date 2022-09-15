---
title: clash（1）
date: 2022-09-04 11:32:33
tags:
	- 科学上网

---

--

现在把主要的科学上网工具都切换到clash了。感觉这个听不错的。

我在windows 目录找出了这个配置文件。

这个就是配置文件的最简单结构。

# config.yaml

```
mixed-port: 7890
allow-lan: false
log-level: info
external-controller: '127.0.0.1:9090'
secret: ''
ipv6: false

# Will be ignored after profile selection
proxies:
  - name: Debug
    type: socks5
    server: 127.0.0.1
    port: 1080
proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - Debug
rules:
  - 'MATCH,DIRECT'

```

# profiles/xxx.yaml文件

你订阅导入的规则，是生成在这个目录下的。

这些文件可以不完整，通常只需要有：`proxies/proxy-groups/rules`三个字段组成即可：

```
proxies:
  - name: Shadowsocks
    type: socks5
    server: 127.0.0.1
    port: 1080
proxy-groups:
  - name: Proxy
    type: select
    proxies:
      - Shadowsocks
rules:
  - "MATCH,DIRECT"
```



CFW 启动流程如下：

1. 使用基础配置文件 config.yaml 启动 Clash 核心
2. 根据用户上次使用的配置文件（Profiles/xxxxx.yml）进行恢复
3. 恢复用户上次操作的策略情况



# 参考资料

1、官方文档

https://docs.cfw.lbyczf.com/contents/configfile.html#%E6%A0%BC%E5%BC%8F