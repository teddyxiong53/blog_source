---
title: youtube代理搭建
date: 2018-08-12 12:06:51
tags:
	- 翻墙
typora-root-url:..\
---



我的出发点是，翻墙流量太珍贵，看youtube流量比较单一，选择其他方式来做。



you2php是一款基于php开发的youtube流量代理脚本。

可以用来搭建youtube视频镜像站。

使用you2php的成本非常低，你只需要一个支持php环境的海外主机，上传代码简单配置就可以用了。

you2php对接谷歌官方api。

you2php采用GPL协议开源。

you2php工作原理：

1、you2php读取谷歌服务器上的视频并写入到你的虚拟主机里的内存中，然后转发给你的浏览器。



you2php采用api获取youtube的数据，所以首先要做的就是申请一个youtube data api秘钥。

youtube data api是谷歌的免费api。

1、首先你的要有一个谷歌账户，没有就申请一个。

2、打开这个网站：https://console.developers.google.com/

安装教程的一步步操作就好了。



部署非常顺利。你可以打开这个网址。

https://xhl-youtube.herokuapp.com/

你就在这个网站里进行搜索就好了。就可以进行观看了。

![](/images/youtube代理.png)

# 参考资料

使用Heroku搭建免费YouTube代理

https://gfw-breaker.win/heroku%E4%B8%8A%E6%90%AD%E5%BB%BAyoutube%E4%BB%A3%E7%90%86/

YOU2PHP介绍

https://you2php.github.io/doc/