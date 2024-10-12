---
title: 海报和logo制作
date: 2024-03-08 19:32:17
tags:
	- 活动

---

--

因为要社团活动要组织，需要做一些logo和海报。

把相关的研究情况记录下来。

方便后续查阅。

# 当前主要方式

就是使用讯排设计来做。

这个是开源免费的，是国人个人开发者做的。

简单直观，对我来说够用了。

主要元素：

* 网上找一张景点的图片。
* 公司logo素材，透明背景。
* 微信群的二维码。
* 然后一句文案。



# logo制作

这个在线找logo制作网站，截图下来用。

后面是让其他人用adobe illustrator做成矢量图了。

# 海报制作

谷歌搜索：海报生成器 github



这个每次活动都会需要一个新的，所以最好是自己掌握一个比较快速的出图方案。

这个方案还行，但是就是字体只能最原始的那种。这个做的海报太呆板了。

https://github.com/psoho/fast-poster

可以直接在线来试一下。

https://fastposter.net/demo/open/

这个的star还比较多。更新也频繁。

https://github.com/palxiao/poster-design

还有一个在线的demo：这个很好，我就用这个做了海报。

https://design.palxp.cn/home

我的图片里因为有文字，所以需要先到这个网站把文字快速去掉。

https://picwish.cn/remove-unwanted-object

# 公告制作

https://www.canva.cn/

这个免费的。用来做简单还不也不错的。

简单清晰，没有什么套路。

# webp文件logo转成透明png logo

```
ffmpeg -i amlogic.webp -vf "colorkey=0xFFFFFF:0.1:0" amlogic.png
```

