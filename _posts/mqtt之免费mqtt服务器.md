---
title: mqtt之免费mqtt服务器
date: 2020-05-13 13:43:08
tags:
	- mqtt

---

1

eqmx

安装：

```
curl https://repos.emqx.io/install_emqx.sh | bash
```

启动：

```
emqx start
```

查询状态：

```
emqx_ctl status
```

查看dashboard，地址是ip:18083



图形界面客户端有哪些？

因为我的json字符串太长了，如果在命令行下面用，都要进行反斜杠转义，太麻烦。所以要一个图形界面工具。

mqtt.fx这个工具似乎不错。下载地址：

http://www.jensd.de/apps/mqttfx/1.7.1/

跨平台的。是基于java写的工具。



参考资料

1、

