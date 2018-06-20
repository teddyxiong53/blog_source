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



一句话来概括的话：

REST是所有web应用都应该遵守的架构设计原则。

7个http方法：

get、post、put、delete、

patch、head、options。



web技术的四大基石：

1、uri。

2、http。

3、hypertext。包括html和json、xml。

4、mime。



web技术的发展阶段：

1、静态内容阶段。

2、cgi阶段。

3、脚本语言阶段。php/asp/jsp等。

4、瘦客户端应用阶段。这个阶段出现了独立于web服务器的应用服务器。在服务端生成所有的动态内容。

5、RIA应用阶段。Rich Internet App。典型的RIA技术就是dhtml+ajax。

6、移动web应用阶段。基于html5开发。





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



# 实现细节

1、使用https协议。

2、尽量把api部署在专用域名下。例如https://api.xxx.com

3、应该把api的版本号放入到url。例如https://api.xxx.com/v1

4、路径。endpoint。表示api的具体网址。

在restful架构中，每个网址表示一种资源，所以网址中不能有动词。只能有名词。

而且用的名词一般是跟数据库的内容对于。一般都是复数的。

例如一个api提供动物园的信息。包括动物和员工。

所以路径设计如下：

```
https://api.xxx.com/v1/zoos
https://api.xxx.com/v1/animals
https://api.xxx.com/v1/employees
```

5、http动词。

对于资源的具体操作类型，用http动词来表示。

举例：

```
GET /zoos ：列出所有动物园
POST /zoos ：新建一个动物园
GET /zoos/ID: 获取某个指定动物园的信息
DELETE /zoos/ID/animals/ID: 删除某个动物园的指定的动物。
```

6、过滤信息。

如果记录的内容很多，服务器不可能把它们都返回给用户，api应该提供参数，过滤返回结果。

常见的如下：

```
?limit=10 :指定返回的记录的数量。
?offset=10：从第10条开始。
?page=2&per_page=100: 指定第几页，以及每页的记录的数目。
?animal_type_id=1:指定筛选条件。
```

7、状态码。

```
200 OK - [GET]：服务器成功返回用户请求的数据，该操作是幂等的（Idempotent）。
201 CREATED - [POST/PUT/PATCH]：用户新建或修改数据成功。
202 Accepted - [*]：表示一个请求已经进入后台排队（异步任务）
204 NO CONTENT - [DELETE]：用户删除数据成功。
400 INVALID REQUEST - [POST/PUT/PATCH]：用户发出的请求有错误，服务器没有进行新建或修改数据的操作，该操作是幂等的。
401 Unauthorized - [*]：表示用户没有权限（令牌、用户名、密码错误）。
403 Forbidden - [*] 表示用户得到授权（与401错误相对），但是访问是被禁止的。
404 NOT FOUND - [*]：用户发出的请求针对的是不存在的记录，服务器没有进行操作，该操作是幂等的。
406 Not Acceptable - [GET]：用户请求的格式不可得（比如用户请求JSON格式，但是只有XML格式）。
410 Gone -[GET]：用户请求的资源被永久删除，且不会再得到的。
422 Unprocesable entity - [POST/PUT/PATCH] 当创建一个对象时，发生一个验证错误。
500 INTERNAL SERVER ERROR - [*]：服务器发生错误，用户将无法判断发出的请求是否成功。
```





# 参考资料

1、

http://www.infoq.com/cn/articles/understanding-restful-style/

2、RESTful API 设计指南

http://www.ruanyifeng.com/blog/2014/05/restful_api.html