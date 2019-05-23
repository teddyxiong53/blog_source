---
title: http之认证之basic-auth
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



# nginx配置

对应的module是ngx_http_auth_basic_module。

默认会安装的。

在sites-enabled目录下的default文件里，在location里加上这个：

```
location / {
    auth_basic "xxx";
    auth_basic_user_file conf/htpasswd;
    autoindex on;
    
    try_files $uri $uri/ =404;
}
```

然后生成密码。

```
hlxiong@hlxiong-VirtualBox:/etc/nginx$ openssl passwd -crypt 123456
N06xh3ETHkhFE
```

新建conf目录。下面新建htpasswd。（这个就是什么default文件里指定的密码文件目录）

可以随意命名。和上面配置的对得上就好了。

把用户名和加密的密码写上。

```
teddy:N06xh3ETHkhFE
```

然后重启nginx，访问网站就好了。

# basic认证的问题

```
1、basic认证用发送用户名和密码。只使用了base64的方式对用户名和密码进行了加密。这样基本就等于没有加密。
2、即使密码你用其他方式加密过。不然也可以利用你的密码去访问服务器。
3、而且，很多用户是一个密码打天下。导致密码泄露的问题变得更加严重。
4、basic认证没有提供任何针对代理和作为中间人的中间节点的防护措施。中间人可以修改报文。
5、basic不支持对称认证，客户端无法认证服务器，服务器很可能是钓鱼网站。
```



参考资料

1、HTTP 身份验证

https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Authentication

2、HTTP认证模式：Basic and Digest Access Authentication

https://www.cnblogs.com/XiongMaoMengNan/p/6671206.html

3、nginx用户认证配置（ Basic HTTP authentication）

http://www.ttlsa.com/nginx/nginx-basic-http-authentication/