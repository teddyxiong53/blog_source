---
title: 授权之basic-auth
date: 2019-05-14 11:29:11
tags:
	- 授权

---



对于授权这一块，我不太了解。现在看看。

RFC7235定义了http basic auth的规则。

交互过程是这样的：

1、客户端向服务器发起请求

```
GET / HTTP/1.1
Host: www.xx.com
```

2、服务端返回认证要求。是401

```
HTTP/1.1 401 Unauthorized
Server: xxx
WWW-Authenticate: Basic xxx
Content-Type: text/html; charset=utf-8
```

3、客户端收到401，会弹出一个登陆窗口。

4、用户把用户名、密码填入。点击确定。Baisc后面的字符串是用户名和密码经过base64加密后得到的。

```
GET / HTTP/1.1
Host: www.xx.com
Authorization: Basic xxxxxxxxxxxxxxxxxxxx
```

5、服务器拿到用户名和密码，进行判断，看看是否合法。

合法则返回200 



nodejs实验

```
var http = require("http")
var auth = require("basic-auth")
// time safe compare
var compare = require("tsscmp")


var server = http.createServer(function(req, res) {
    var credentials = auth(req)
    console.log(credentials)
    if(!credentials || !check(credentials.name, credentials.password)) {
        res.statusCode = 401
        res.setHeader('WWW-authenticate', 'Basic realm="teddy"')
        res.end('Access denied')
    } else {
        res.end('Access granted')
    }
})
function check(name, password) {
    var valid = true
    valid = compare(name, 'teddy')&&valid
    valid = compare(password, 'teddy')&&valid
    return valid
}

server.listen(3000)
```





参考资料

1、HTTP 身份验证

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Authentication

2、HTTP认证模式：Basic and Digest Access Authentication

https://www.cnblogs.com/XiongMaoMengNan/p/6671206.html