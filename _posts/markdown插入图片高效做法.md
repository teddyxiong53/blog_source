---
title: markdown插入图片高效做法
date: 2020-11-27 10:07:30
tags:
	- markdown
---

1

如何高效在markdown里插入图片，保证在不同的地方都可以正常浏览。这个是一个值得研究的问题。

本地图片法

这个用相对路径，如果只是markdown文件，其实还可以接受。

但是生成html静态网页，不好处理。

这个写的时候，很方便，用typora，可以无感进行粘贴插入。写作体验非常好。

网络图片法

这个依赖网络。不管对于托管的网页，这个不是问题。

但是就是插入图片，能不能高效进行？

base64法

把图片转成base64，直接放入markdown文件里面。

这个不太好。太影响阅读感觉了。



最好的方式，还是网络法。但是要找到快速的插入图片的操作方式。



用 Markdown 写文章最苦恼的其实就是图片链接了，iPic 是一个为图片生成外链的神器，支持将图片匿名上传到微博图床（免费）、付费后还支持更多图床（七牛、Flickr、Imgur 等），但是免费的新浪图床就已经很好用了！



现在的typora版本，已经支持默认把图片上传到picgo了。

**PicGo: 一个用于快速上传图片并获取图片 URL 链接的工具**

PicGo 本体支持如下图床：

- `七牛图床` v1.0
- `腾讯云 COS v4\v5 版本` v1.1 & v1.5.0
- `又拍云` v1.2.0
- `GitHub` v1.5.0
- `SM.MS V2` v2.3.0-beta.0
- `阿里云 OSS` v1.6.0
- `Imgur` v1.6.0

哪个图床稳定且免费呢？

先安装picgo再看 。

阿里云的oss，对象存储服务。是收费的，不过不贵。

先不考虑。

看了一圈，觉得七牛云可能还比较靠谱一点。

在配置七牛的“确认存储区域”的时候，如果没有选项需要输入值，直接输入区域名称是不行的，需要输入对应的代码。华东 z0, 华北 z1，华南 z2，北美 na0，东南亚 as0



现在用picgo，图片是上传上去了。

生成的连接，是这样：

http://teddyxiong53.gitee.io/playopenwrt/20201127110236.png

找不到。

关键就是设置访问网址。

算了，我不用七牛云了。

网上搜索到可以用gitee来做图床，我说呢，github可以，gitee应该可以模仿这个功能。

需要先在picgo里面，搜索gitee。找到gitee uploader插件，安装。

然后就可以看到图床设置里多了gitee这一项。

然后是到gitee里新建一个仓库，我就叫playopenwrt_pic。

https://gitee.com/teddyxiong53/playopenwrt_pic

得到的链接是这样的，可以正常访问。速度还可以。

../images/playopenwrt_pic/20201127112513.png



插入图片的问题，就这样解决了。

而且typora还可以集成picgo的自动上传功能。这样就更加方便了。





参考资料

1、picgo安装

https://picgo.github.io/PicGo-Doc/zh/guide/

2、盘点国内免费好用的图床

https://zhuanlan.zhihu.com/p/35270383

3、使用picGo和码云搭建个人图床

https://blog.csdn.net/DeftTOT/article/details/105069329