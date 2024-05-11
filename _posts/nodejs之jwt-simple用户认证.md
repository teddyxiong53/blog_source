---
title: nodejs之jwt-simple用户认证
date: 2020-09-07 13:46:17
tags:
	- js

---

--

jwt是json web token的缩写。

前后端分离后，**后端只承担api的功能，**

传统的使用session的认证方法带来很大的不便：

例如移动端app和PC端不能共用cookie等。



首先第一件事是让客户端通过账号密码交换token，可以使用post，此处假设已经得到了用户名和密码。

验证用户名和密码通过后，返回一个包含JWT的响应。



JSON Web Token（缩写 JWT）是目前==最流行的跨域认证解决方案==，本文介绍它的原理和用法。

互联网服务离不开用户认证。

一般的流程是这样的：

1、用户提交username和password。

2、服务端验证通过后，在当前session里存放相关数据。例如role、time等。

3、服务端向用户返回一个session_id，写入到用户的cookie里。

4、后续用户的每一个请求，都会通过cookie把session_id发送给服务器。

5、服务器收到session_id，查找到对应的session，就可以验证用户是身份。



上面这种验证方式的问题是，扩展性不好。

如果是服务器集群，或者的跨域的服务导向架构，就要求session数据共享。

每台服务器都要能够读取session。

举例来说，A网站和B网站是同一家公司的关联业务。

现在要求，用户只需要登陆其中一个网站，在跳转到另外一个网站的时候，要能够自动登陆。

这个应该怎么实现呢？

==一个解决方案是session数据持久化。==

把session写入到数据库或者其他的持久层。

各种服务收到请求后，都向持久层请求数据。

这个方案的优点是架构清晰。

缺点是工程量比较大。另外持久层如果挂了，就会单点失败。

**另外一种方案是，服务端索性就不保存session数据了。**

**所有的数据都保存在客户端。每次请求都发送给服务器。**

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

**服务器就不需要保存任何的session数据了。这样就便于服务器进行扩展。**

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



# jwt的使用方式

客户端收到服务器返回的jwt数据，可以存放在cookie里，也可以存放在localStorage里。

然后，客户端每次跟服务端通信，都带上这个jwt。

可以放在cookie里，好处是可以自动发送。坏处是不能跨域。

**所以更好的做法是放在http header里的Authorization里。**



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

# 简介

JWT（JSON Web Token）是一种开放标准（RFC 7519），

用于在网络应用之间==传递声明式的身份信息。==

它是一种轻量级、可自包含的认证方式，通常用于在客户端和服务器之间安全地传输信息。

JWT由三部分组成，分别是头部（Header）、载荷（Payload）和签名（Signature）：

1. **头部（Header）**：头部通常由两部分组成，令牌的类型（比如JWT）和使用的签名算法（比如HMAC SHA256或RSA）。例如：`{"alg": "HS256", "typ": "JWT"}`。

2. **载荷（Payload）**：载荷包含了一些声明（claim），声明是关于实体（通常是用户）和其他数据的声明。声明可以是注册的声明、公共声明和私有声明。例如：`{"sub": "user123", "exp": 1619446104}`。其中`sub`是主题，表示令牌的主体，而`exp`表示令牌的过期时间。

3. **签名（Signature）**：签名是由头部、载荷和一个密钥（secret）使用指定的算法计算而得。签名用于验证消息的完整性，以及消息发送者的身份。==签名通常是使用Base64编码的字符串，==用于验证令牌的真实性。

JWT的工作流程通常是这样的：用户登录成功后，服务器生成一个JWT，然后将其返回给客户端。

客户端在随后的请求中将JWT包含在HTTP头部的Authorization字段中发送给服务器。

服务器接收到JWT后，会验证JWT的有效性，并根据其中的声明来进行相应的操作。

JWT的优点包括了跨平台、可扩展性强、自包含性和安全性高等。

它广泛应用于身份认证和授权，比如在Web应用程序、移动应用程序和微服务架构中。

# HTTP头部的Authorization字段

HTTP头部的Authorization字段用于在HTTP请求中传递身份验证信息。

它通常用于对受保护的资源进行访问时，向服务器提供身份验证凭据。

Authorization字段的值通常由两部分组成，

即身份验证方案（Authentication Scheme）和凭据（Credentials），之间用空格分隔。

常见的身份验证方案包括基本认证（Basic Authentication）、摘要认证（Digest Authentication）、Bearer Token认证等。

例如，Bearer Token认证的Authorization字段的格式通常是这样的：

```
Authorization: Bearer <token>
```

其中 `<token>` 是一个JWT令牌或其他形式的访问令牌。服务器在接收到这样的请求时，会提取Authorization字段中的令牌，然后对令牌进行验证，以确定请求的发送者是否有权限访问所请求的资源。

在使用基本认证时，Authorization字段的格式如下：

```
Authorization: Basic <credentials>
```

其中 `<credentials>` 是经过Base64编码的用户名和密码的组合，用冒号分隔，例如：`username:password`。

需要注意的是，虽然Base64编码可以对凭据进行简单的编码，但它并不等同于加密。因此，在传输敏感信息时，应始终使用HTTPS来加密通信，以确保凭据的安全性。

总之，Authorization字段提供了一种标准的机制，用于在HTTP请求中传递身份验证信息，从而实现对受保护资源的访问控制。

# Python jwt使用举例

以下是一个简单的Python示例，演示如何使用PyJWT库创建和验证JWT令牌：

首先，确保你已经安装了PyJWT库。你可以通过以下命令来安装：

```
pip install PyJWT
```

接下来，让我们创建一个JWT令牌并验证它：

```python
import jwt
from datetime import datetime, timedelta

# 密钥，用于签名和验证JWT令牌
secret_key = "your_secret_key"

# 有效载荷（Payload），包含了要包含在JWT令牌中的信息
payload = {
    "user_id": 123,
    "username": "user123",
    "exp": datetime.utcnow() + timedelta(days=1)  # 设置过期时间为一天后
}

# 创建JWT令牌
jwt_token = jwt.encode(payload, secret_key, algorithm="HS256")

print("JWT Token:", jwt_token)

# 验证JWT令牌
try:
    decoded_payload = jwt.decode(jwt_token, secret_key, algorithms=["HS256"])
    print("Decoded Payload:", decoded_payload)
except jwt.ExpiredSignatureError:
    print("JWT Token has expired.")
except jwt.InvalidTokenError:
    print("Invalid JWT Token.")
```

在这个示例中，我们首先导入了PyJWT库。然后，我们定义了一个密钥（secret_key），用于签名和验证JWT令牌。接着，我们创建了一个有效载荷（payload），其中包含了一些用户信息和过期时间。然后，我们使用`jwt.encode()`函数将有效载荷编码为JWT令牌，并打印出来。最后，我们使用`jwt.decode()`函数验证JWT令牌，并解码其中的有效载荷。

请注意，这只是一个简单的示例。在实际应用中，你可能需要更复杂的逻辑来处理身份验证和授权，并根据需要定制有效载荷的内容。

# 配合flask用jwt来做一个完整的demo

好的，下面是一个使用Flask和PyJWT库来实现基本JWT身份验证的示例：

首先，确保你已经安装了Flask和PyJWT库：

```
pip install Flask PyJWT
```

然后，创建一个名为`app.py`的Python文件，内容如下：

```python
from flask import Flask, request, jsonify
import jwt
from functools import wraps
from datetime import datetime, timedelta

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# 用户数据库，实际应用中应该是真实的用户数据库
users = {
    'user123': 'password123'
}

# 用户登录接口
@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Authorization required!'}), 401

    username = auth.username
    password = auth.password

    if users.get(username) == password:
        # 生成JWT令牌
        token = jwt.encode({'username': username, 'exp': datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])
        return jsonify({'token': token.decode('utf-8')})
    else:
        return jsonify({'message': 'Invalid username or password!'}), 401

# 身份验证装饰器
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return jsonify({'message': 'Token is missing!'}), 401

        try:
            # 验证JWT令牌
            data = jwt.decode(token, app.config['SECRET_KEY'])
        except:
            return jsonify({'message': 'Token is invalid!'}), 401

        return f(*args, **kwargs)

    return decorated

# 受保护的路由
@app.route('/protected', methods=['GET'])
@token_required
def protected():
    return jsonify({'message': 'Protected endpoint!'})

if __name__ == '__main__':
    app.run(debug=True)
```

在这个示例中，我们首先导入了Flask、PyJWT库以及一些其他必要的模块。然后，我们创建了一个Flask应用，并设置了一个随机的密钥作为配置。接着，我们定义了一个虚拟的用户数据库（在实际应用中应该是真实的用户数据库），然后创建了一个用于用户登录的接口`/login`。

用户登录接口接收用户名和密码，并根据数据库中的用户信息生成JWT令牌。如果登录成功，将返回JWT令牌；否则，返回相应的错误消息。

我们还定义了一个名为`token_required`的装饰器，用于验证JWT令牌。这个装饰器用于保护受保护的路由`/protected`，只有在提供有效的JWT令牌时才允许访问该路由。

最后，我们定义了一个受保护的路由`/protected`，并应用了`token_required`装饰器来保护它。

你可以运行这个示例，并使用POST请求来模拟用户登录，然后使用JWT令牌来访问受保护的路由。

# 参考资料

1、在Nodejs中使用JWT做用户认证

https://www.jianshu.com/p/3c3de39ff8f0

2、JSON Web Token 入门教程

http://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html

3、JWT 和一个例子 Node + passport.js

https://zhuanlan.zhihu.com/p/100645782