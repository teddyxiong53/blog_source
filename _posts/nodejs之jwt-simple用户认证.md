---
title: nodejs之jwt-simple用户认证
date: 2020-09-07 13:46:17
tags:
	- js

---

1

jwt是json web token的缩写。

前后端分离后，**后端只承担api的功能，**

传统的使用session的认证方法带来很大的不便：

例如移动端app和PC端不能共用cookie等。



首先第一件事是让客户端通过账号密码交换token，可以使用post，此处假设已经得到了用户名和密码。

验证用户名和密码通过后，返回一个包含JWT的响应。



JSON Web Token（缩写 JWT）是目前最流行的跨域认证解决方案，本文介绍它的原理和用法。

互联网服务离不开用户认证。一般的流程是这样的：

1、用户提交username和password。

2、服务端验证通过后，在当前session里存放相关数据。例如role、time等。

3、服务端向用户返回一个session_id，写入到用户的cookie里。

4、后续用户的每一个请求，都会通过cookie把session_id发送给服务器。

5、服务器收到session_id，查找到对应的session，就可以验证用户是身份。



上面这种验证方式的问题是，扩展性不好。

如果是服务器集群，或者的跨域的服务导向架构，就要求session数据共享。每台服务器都要能够读取session。

举例来说，A网站和B网站是同一家公司的关联业务。

现在要求，用户只需要登陆其中一个网站，在跳转到另外一个网站的时候，要能够自动登陆。

这个应该怎么实现呢？

一个解决方案是session数据持久化。把session写入到数据库或者其他的持久层。

各种服务收到请求后，都向持久层请求数据。

这个方案的优点是架构清晰。缺点是工程量比较大。另外持久层如果挂了，就会单点失败。

另外一种方案是，服务端索性就不保存session数据了。

所有的数据都保存在客户端。每次请求都发送给服务器。

jwt就是这种方案的一种实现。



jwt的原理是，服务器认证后，生成一个json对象，发送给用户。

就像下面这样：

```
{
	"username": "allen",
	"role": "admin",
	"expire": "xxx"
}
```

在随后的通信里，用户每次都把这个json对象发送给服务器。

服务器就完全靠这个json对象来认证用户。

为了防止用户篡改数据，服务器在生成这个对象的时候，会加上签名。

服务器就不需要保存任何的session数据了。这样就便于服务器进行扩展。

实际上的jwt数据是这个样子。

```
xxx.yyy.zzz
```

用点号分割为3个部分。分别是：

1、header。

2、payload。

3、signature。

header部分是一个json对象。描述jwt的元数据。

一般是下面这样：

```
{
	"alg": "HS256",
	"typ": "JWT"
}
```

alg表示签名算法。默认是HMAC SHA256，简写为HS256。

typ表示这个token的类型。

然后，把上面的字符串用base64url转成字符串。

payload部分也是一个json对象。用来存放实际需要传递的数据。

jwt规定了7个官方字段。

```
iss：签发人。issuer。
exp：过期时间。
sub：主题。
aud：受众。audience。
nbf：生效时间。Not BeFore
iat：签发时间。Issued At
jti：编号。jwt ID
```

除了上面这7个官方的字段，你可以自定义。例如下面这样：

```
{
"name":"allen",
"admin": true
}
```

jwt默认是不加密的，任何人都可以读取。所以不用把敏感信息放在里面。

payload部分也用base64url进行转化为字符串。



signature是对header和payload进行前面，防止篡改。

首先，需要指定一个秘钥，这个密钥只有服务器才只能，不能告诉用户。

然后，用下面的公式进行签名。

```
hs256(base64url(header) + "." + base64url(payload), secret)
```

base64url跟普通的base64算法有点区别。

Base64 有三个字符`+`、`/`和`=`，在 URL 里面有特殊含义，所以要被替换掉：`=`被省略、`+`替换成`-`，`/`替换成`_` 。这就是 Base64URL 算法。



jwt的使用方式

客户端收到服务器返回的jwt数据，可以存放在cookie里，也可以存放在localStorage里。

然后，客户端每次跟服务端通信，都带上这个jwt。

可以放在cookie里，好处是可以自动发送。坏处是不能跨域。

所以更好的做法是放在http header里的Authorization里。



# 实例演示

下载这个代码

https://github.com/shawnwz/passport-js-jwt

```
先安装：
npm i
然后启动：
npm start
```

这样服务端就启动了。

用户这边，用postman来做。

先是post 到http://192.168.56.101:8000/api/users/这个地址。

post内容是一个json对象：

```
{
    "user": {
        "email": "1073167306@qq.com",
        "password": "test"
    }
}
```

得到的返回值是：

```
{
    "user": {
        "_id": "5f57545a0cd72306b8b93024",
        "email": "1073167306@qq.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjEwNzMxNjczMDZAcXEuY29tIiwiaWQiOiI1ZjU3NTQ1YTBjZDcyMzA2YjhiOTMwMjQiLCJleHAiOjE2MDQ3NDI3NDcsImlhdCI6MTU5OTU1ODc0N30.HdVDrIdQl72mpiVw4dyf7ivw2pPZlyWaoHHRdP-_OqU"
    }
}
```

然后是获取当前用户。

```
GET http://192.168.56.101:8000/api/users/current
```

需要填写2个header。

```
Authorization 填写：Token eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjEwNzMxNjczMDZAcXEuY29tIiwiaWQiOiI1ZjU3NTQ1YTBjZDcyMzA2YjhiOTMwMjQiLCJleHAiOjE2MDQ3NDI3NDcsImlhdCI6MTU5OTU1ODc0N30.HdVDrIdQl72mpiVw4dyf7ivw2pPZlyWaoHHRdP-_OqU
```

```
Content-Type 填写：application/json
```

返回结果：

```
{
    "user": {
        "_id": "5f57545a0cd72306b8b93024",
        "email": "1073167306@qq.com",
        "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IjEwNzMxNjczMDZAcXEuY29tIiwiaWQiOiI1ZjU3NTQ1YTBjZDcyMzA2YjhiOTMwMjQiLCJleHAiOjE2MDQ3NDMwNTIsImlhdCI6MTU5OTU1OTA1Mn0.7_5TV901DyG2ksYmfRKJc5tOJQha9qtvIZLg9cFnxjk"
    }
}
```



分析一下服务端的代码。

```
const jwt = require('express-jwt');
```



参考资料

1、在Nodejs中使用JWT做用户认证

https://www.jianshu.com/p/3c3de39ff8f0

2、JSON Web Token 入门教程

http://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html

3、JWT 和一个例子 Node + passport.js

https://zhuanlan.zhihu.com/p/100645782