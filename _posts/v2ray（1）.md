---
title: v2ray（1）
date: 2018-06-30 16:41:41
tags:
	- 翻墙

---



ssr目前情况很不好。要开拓新的翻墙手段。



先下载windows客户端。

https://github.com/2dust/v2rayN

都是vs工程，需要自己编译的。

不过这个编译很顺利。



运行后，从doub.io上找到一个vmess地址，选择从剪切板导入。

鼠标移到图标上，显示“未找到v2ray文件”。

在这里找到解决方法。

https://www.ssrshare.com/threads/v2ray-for-windows.38/

是说

```
V2rayN无法独立运行，需要下载V2ray原版文件，将其解压到相同文件夹即可
```

地址在这里。

https://github.com/v2ray/v2ray-core/releases



现在因为长城宽带不能通过ssr翻墙，所以只能再研究一下v2ray的了。

project V是一个工具集合。

它可以帮组你打造专属的基础通信网络。

project v的核心工具叫V2RAY。

主要负责网络协议和功能的实现。

与其他的project v互通。

v2ray可以单独运行。



默认是10808这个端口。

但是如果你在proxy插件里设置这个端口号，那么不行。

tortoisegit里，需要设置位10809才行。

浏览器里也是要10809这个端口。



# 参考资料

1、V2RayN 使用教程

https://v2ray66.com/post/8/