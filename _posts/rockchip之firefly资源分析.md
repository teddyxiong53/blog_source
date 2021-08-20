---
title: rockchip之firefly资源分析
date: 2021-08-18 15:18:33
tags:
	- rockchip

---

--

代码放在github上

从这里下载

```
repo init --repo-url=https://github.com/FireflyTeam/repo -u https://github.com/FireflyTeam/manifests
```

只有36个project，不算多。

去代码会失败，我单独去buildroot部分吧。

repo sync buildroot

make一下，看到.config里，默认这个也是有的。

BR2_PACKAGE_IFUPDOWN_SCRIPTS=y

之所以不慢，我估计是没有启动ap方式的配网。



参考资料

https://www.t-firefly.com/doc/product/info/267.html

https://www.codenong.com/cs106544012/