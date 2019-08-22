---
title: chromium了解
date: 2018-02-06 19:40:37
tags:
	- 浏览器

---



研究chrome浏览器，接触到chromium这个东西，了解一下。

简单说，chromium和chrome都是谷歌的，chromium是开源的，chrome不是。

国内的搜狗浏览器等，就是基于chromium来做的。

chrome也是基于chromium，chromium是引擎。chrome是实际产品。

chrome相当于是chromium的一个参考设计。

chromium的基础是webkit。采用bsd协议开源。所以大家可以免费商用。



图标上，chromium是蓝色的。chrome是彩色的。

还有一个chromium os呢。



官网在这里：http://www.chromium.org/Home。



直接有chromium浏览器。下载试用一下。



现在下载代码看一下，自己编译看看。

源代码有1.2G。就从github上下载压缩包就好了。

到这里下载工具。

https://chromium.googlesource.com/chromium/tools/depot_tools/+/refs/heads/master

解压后，把路径添加到PATH里。

安装依赖：

```
source build/install-build-deps.sh
```

安装碰到了问题，暂时不做了。



参考资料

1、

