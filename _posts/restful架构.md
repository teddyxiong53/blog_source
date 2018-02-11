---
title: restful架构
date: 2018-02-08 21:29:37
tags:
	- restful

---



# 1. 什么是restful架构

这个词的准确写法应该是REST ful。

REST是REpresentational State Transfer。字面含义是表现层状态转化。

这个词是Roy Thomas Fielding在2000年的时候，在他的博士论文里提出的。

Fielding是个非常重要的任务。他是http协议的主要作者、Apache Web Server的作者之一、Apache基金会的第一人主席。

他的论文的目的是，在符合架构原理的前提下，理解和评估以网络为基础的APP的架构设计，得到一个很好的通用架构。

REST这个词拆开了看，也让人一下子弄不清楚具体的含义。

表现层状态转化。表现层是指什么？其实是指资源（Resource）的表现层。

什么是资源？资源是网络上的一个实体。一段文本、一张图片、一首歌、一种服务，都是一个具体的实体。

你可以用uri来指向一个资源。

uri就是资源独一无二的ID。

所谓上网，就是互联网上一系列的资源的互动。

资源是一种信息实体，它可以有多种表现形式。

我们把资源具体呈现出来的形式，就叫做资源的表现层。

比如说，文本可以用txt格式表现，也可以用html格式、xml格式、json格式。甚至可以用二进制。

uri只代表了资源的实体，并不代表它的表现形式。

所以，有些网址最后的html后缀其实是多余的。因为这个html是属于表现层的内容。

uri应该只代表资源的位置。而不是它的表现形式。

它的具体表现形式，应该在http request里的Accept和Content-Type这2个字段里指定。

访问一个网站。就代表了client和server的一个互动过程。

在这个过程中，一定会有数据和状态的变化。

而http协议，是一个无状态协议。这意味着，所有的状态都保存在server端。

如果client想要操作server，一定是通过某种手段，让server端发送了状态转移。

而client能够采取的手段，只能是http协议。具体说就是post、get、put、delete这4个词。

post：增。

delete：删。

post：改。

get：查。



简单来说，restful架构包含这些点：

1、每一个uri代表了一个资源。

2、client通过4个http动词，对server进行操作。



网站应用程序，分为前端和后端两个部分，当前的发展趋势就是前端的设备层出不穷，手机、电脑、平板等等。

所以，要有一种统一的机制来处理不同的前端设备。这就导致了API架构的流行。

甚至出了“API First”的设计思想。

restfull API是目前比较成熟的一套互联网APP的API设计理论。

# restful的一些设计误区

1、uri里包含动词。

我们上面说了，uri代表的是资源，它应该是一个名词。

例如某个uri叫/post/show/1，这个就是错的。

应该是get /post/1 这样才是 妥当的。

有些操作是http动词表现不了的。你就应该把动作当成一种资源。

例如，网上转账。从账户1向账户2转账500元。

错误的写法是这样：

```
POST /accounts/1/transfer/500/to2
```

而应该吧动词transfer改成名词，transaction。资源不能是动词，但是可以是一种服务。

```
POST /transaction HTTP/1.1
host: xx.xx.xx.xx
from=1&to=2&amount=500
```

2、在uri里带了版本号。

例如这样：

```
http://www.xxx.com/app/1.0/foo
http://www.xxx.com/app/1.1/foo
```

因为不同的版本，可以理解为同一种资源的不同表现形式。

所以应该用同一个uri。

这个区别可以在http头部里的Accept字段里做。

```
Accept: vnd.xxx.com.foo+json; version=1.0
```







