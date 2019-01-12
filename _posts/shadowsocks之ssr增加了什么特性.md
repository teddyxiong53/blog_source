---
title: shadowsocks之ssr增加了什么特性
date: 2019-01-12 16:05:59
tags:
	- shadowsocks
---



加入了混淆插件。

就是obfs

可以选择的有：

plain

http-simple



代码在这里。

https://github.com/ToyoDAdoubiBackup/shadowsocksr



从setup.py里看。

```
 packages=['shadowsocks', 'shadowsocks.crypto', 'shadowsocks.obfsplugin'],
```



参考资料

1、SSR服务端配置说明

http://rt.cn2k.net/?p=328

2、ShadowsocksR 配置

https://www.zfl9.com/ssr.html

3、ShadowsocksR 协议插件文档

https://github.com/iMeiji/shadowsocks_install/wiki/ShadowsocksR-%E5%8D%8F%E8%AE%AE%E6%8F%92%E4%BB%B6%E6%96%87%E6%A1%A3