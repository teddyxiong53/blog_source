---
title: dlna相关之miracast
date: 2020-04-28 13:58:08
tags:
	- dlna

---

1

miracast在Linux下的实现，叫做miraclecast。

下载代码：

```
git clone https://github.com/albfan/miraclecast.git
```

需要安装一些依赖，其他的都好说，有报readline找不到，是需要安装这个。

```
sudo apt-get install libreadline-dev
```

buildroot里也有带。

直接在Ubuntu笔记本上运行，没有跑起来。

在buildroot里编译，放板子上试一下。

这个在板子跑不太显示，依赖的东西太多了。暂时不深入研究这个了。





参考资料

1、DIY Wifi投屏器的两种方法（Linux,树莓派）

https://zhuanlan.zhihu.com/p/95128228