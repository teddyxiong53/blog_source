---
title: webapi接口
date: 2021-02-02 16:33:11
tags:
	- web

---

--

# 概念辨析

说到web api，可能是指2个不同的东西：

1、浏览器提供的操作bom和dom的接口。document.getElementById就是一个web api。

https://developer.mozilla.org/zh-CN/docs/Web/API

2、网站提供的功能接口。

下面我们主要讨论网站提供的功能接口。



Web API 是Web 应用程序接口。

包含了广泛的功能，

Web 应用通过API接口，

可以实现存储服务、消息服务、计算服务等能力，

利用这些能力可以进而开发出强大功能的web应用。



这些服务的共同点是它们都提供简单的API来访问海量数据，

并且可能**催生孤立信息间的不可预知的交叉应用。**



# Web API和MVC框架比较

Web API是一种数据请求框架，是基于HTTP协议的服务，能够直接返回用户的数据请求。

MVC是建站的一种框架，倾向于返回用户的页面请求。

Web API 可以根据请求报文来返回的相应数据格式。包括JSON和XML。

而单独做数据请求和MVC做页面请求可以让Web前端和后台更好的解耦，能够减少开发难度。

MVC主要是用于前端页面的生成，最终的目的是生成HTML，

Web API主要应用于对外部服务的接口，如提供给APP调用和用于前端AJAX访问。



对外公开 Web API 时，必须首先思考将怎样的信息或数据经由怎样的 API 对外公开。

接下来就让我们来考虑一下如何决定对外公开的功能和端点，以及 Web API 的端点该如何设计。

从本章开始，我们将讲解 API 具体的设计规则及方法。



# API 端点的设计思想

在 Web API 的语境里，端点是指用于访问 API的 URI。

一般而言，因为 API 将各种不同的功能进行了封装，所以会拥有多个不同的端点。

实现不同的功能就需要分别赋予其不同的端点，即访问这些功能的 API 所需的 URI。

比如，在设计获取用户信息的 API 时，可以分配如下 URI，API 用户可以通过访问端点使用 API 提供的功能。

```
https://api.example.com/v1/users/me
```

要探讨什么是优秀的 URI 设计，有一个非常重要的原则，如下所示。

```
容易记忆，URI 包含的功能一目了然。
```

API 是供计算机程序机械地访问的，但是还需要人眼看上去也易于理解，

设计出便于开发人员理解的端点，可以有效降低开发人员搞错 API 端点或错误使用 API的概率。

这不仅可以提高开发人员的生产效率，还有助于提升 API 的口碑。

设计优美的 URI 的方法，我们可以总结出如下几个普适又重要的原则。

 短小便于输入的 URI
 人可以读懂的 URI
 没有大小写混用的 URI
 修改方便的 URI
 不会暴露服务器端架构的 URI
 规则统一的 URI



“修改方便”即英语中所说的“Hackable”。“修改方便的 URI”指的是能将某个URI 非常容易地修改为另一个 URI。假设我们需要获取某种商品（item，根据 API类型的不同而发生变化），该 API 的端点如下所示。

```
http://api.example.com/v1/items/12346
```

从以上 URI 能直观地看出该商品 ID 为 123456，并且可以猜测只要修改这一ID，就能访问到其他商品的信息。

# 最佳实践

## RESTful API 设计指南

网络应用程序，分为前端和后端两个部分。当前的发展趋势，就是前端设备层出不穷（手机、平板、桌面电脑、其他专用设备......）。

因此，必须有一种统一的机制，方便不同的前端设备与后端进行通信。

这导致API构架的流行，甚至出现"API First"的设计思想。

RESTful API是目前比较成熟的一套互联网应用程序的API设计理论。

我以前写过一篇[《理解RESTful架构》](http://www.ruanyifeng.com/blog/2011/09/restful.html)，探讨如何理解这个概念。

### 一、协议

API与用户的通信协议，总是使用HTTPs协议。

### 二、域名

应该尽量将API部署在专用域名之下。

```
https://api.example.com
```

如果确定API很简单，不会有进一步扩展，可以考虑放在主域名下。

```
https://example.org/api/
```

### 三、版本（Versioning）

应该将API的版本号放入URL。

```
https://api.example.com/v1/
```

另一种做法是，将版本号放在HTTP头信息中，但不如放入URL方便和直观。Github采用这种做法。

### 四、路径（Endpoint）

路径又称"终点"（endpoint），表示API的具体网址。

在RESTful架构中，每个网址代表一种资源（resource），

所以网址中不能有动词，

只能有名词，

**而且所用的名词往往与数据库的表格名对应。**

一般来说，

数据库中的表都是同种记录的"集合"（collection），

**所以API中的名词也应该使用复数。**

举例来说，

有一个API提供动物园（zoo）的信息，

还包括各种动物和雇员的信息，

则它的路径应该设计成下面这样。

```
https://api.example.com/v1/zoos
https://api.example.com/v1/animals
https://api.example.com/v1/employees
```

### 五、HTTP动词

对于资源的具体操作类型，由HTTP动词表示。

常用的HTTP动词有下面五个（括号里是对应的SQL命令）。

- GET（SELECT）：从服务器取出资源（一项或多项）。
- POST（CREATE）：在服务器新建一个资源。
- PUT（UPDATE）：在服务器更新资源（客户端提供改变后的完整资源）。
- PATCH（UPDATE）：在服务器更新资源（客户端提供改变的属性）。
- DELETE（DELETE）：从服务器删除资源。

下面是一些例子。

```
GET /zoos：列出所有动物园
POST /zoos：新建一个动物园
GET /zoos/ID：获取某个指定动物园的信息
PUT /zoos/ID：更新某个指定动物园的信息（提供该动物园的全部信息）
PATCH /zoos/ID：更新某个指定动物园的信息（提供该动物园的部分信息）
DELETE /zoos/ID：删除某个动物园
GET /zoos/ID/animals：列出某个指定动物园的所有动物
DELETE /zoos/ID/animals/ID：删除某个指定动物园的指定动物
```

### 六、过滤信息（Filtering）

如果记录数量很多，服务器不可能都将它们返回给用户。API应该提供参数，过滤返回结果。
下面是一些常见的参数。

```
?limit=10：指定返回记录的数量
?offset=10：指定返回记录的开始位置。
?page=2&per_page=100：指定第几页，以及每页的记录数。
?sortby=name&order=asc：指定返回结果按照哪个属性排序，以及排序顺序。
?animal_type_id=1：指定筛选条件
```

参数的设计允许存在冗余，即允许API路径和URL参数偶尔有重复。比如，`GET /zoo/ID/animals 与 GET /animals?zoo_id=ID` 的含义是相同的。

### 七、状态码（Status Codes）

服务器向用户返回的状态码和提示信息，常见的有以下一些（方括号中是该状态码对应的HTTP动词）。

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

### 八、错误处理（Error handling）

如果状态码是4xx，就应该向用户返回出错信息。一般来说，返回的信息中将error作为键名，出错信息作为键值即可。

```
{
    error: "Invalid API key"
}
```

### 九、返回结果

针对不同操作，服务器向用户返回的结果应该符合以下规范。

```
GET /collection：返回资源对象的列表（数组）
GET /collection/resource：返回单个资源对象
POST /collection：返回新生成的资源对象
PUT /collection/resource：返回完整的资源对象
PATCH /collection/resource：返回完整的资源对象
DELETE /collection/resource：返回一个空文档
```

### 十、Hypermedia API

RESTful API最好做到Hypermedia，

即返回结果中提供链接，连向其他API方法，

使得用户不查文档，也知道下一步应该做什么。

比如，当用户向api.example.com的根目录发出请求，会得到这样一个文档。

```
{"link": {
  "rel":   "collection https://www.example.com/zoos",
  "href":  "https://api.example.com/zoos",
  "title": "List of zoos",
  "type":  "application/vnd.yourformat+json"
}}
```

### 十一、其他

（1）API的身份认证应该使用[OAuth 2.0](http://www.ruanyifeng.com/blog/2014/05/oauth_2_0.html)框架。
（2）服务器返回的数据格式，应该尽量使用JSON，避免使用XML。



参考资料

1、

https://www.kancloud.cn/amamatthew/api/417704

2、

https://baike.baidu.com/item/Web%20API/4102287