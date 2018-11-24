---
title: Linux之curl命令
date: 2018-11-24 10:32:51
tags:
	- Linux
---



现在用libcurl做东西，需要先用curl命令来验证问题，所以需要对这个命令有全面的认识。

我还是都基于http://httpbin.org来做测试。

curl这个名字的含义是：Command line Url viewer。







# 常用命令

获取网页内容，直接加网址就好了。会把内容输出到stdout。

```
curl http://httpbin.org
```

保存网页内容到文件。

```
curl http://httpbin.org -o 1.html
```

如果用-O选项，则不需要跟文件名，是用网页的名字做文件名。

可以同时跟多个-O选项，这样就可以同时下载多个网页。

断点续传。用-C选项。

```
curl -C - -O http://httpbin.org/index.html
```

限速。

```
curl --limit-rate 1000B -O http://httpbin.org/index.html
```

使用用户名和密码。

```
curl -u username:password http://www.xxx.com
```

但是这样会把密码暴露在命令行的历史里。可以只指定username。让curl提示你输入密码。

```
curl -u username http://www.xxx.com
```

从ftp服务器下载文件。

```
curl -u username:password -O ftp://xxx.com/index.html
```

如果给的ftp是一个路径而不是文件名，则只是罗列文件，而不是下载目录下所有的文件。

上传文件到ftp服务器。

```
curl -u username:password -T 1.txt ftp://xxx.com
```

同时上传多个文件。

```
curl -u username:password -T "{1.txt, 2.txt}" ftp://xxx.com
```

设置代理。

```
curl -x 127.0.0.1:1080 http://google.com
```

只解析返回的header数据。

```
curl -I http://httpbin.org
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/curl$ curl -I http://httpbin.org
HTTP/1.1 200 OK
Connection: keep-alive
Server: gunicorn/19.9.0
Date: Sat, 24 Nov 2018 03:03:44 GMT
Content-Type: text/html; charset=utf-8
Content-Length: 10122
Access-Control-Allow-Origin: *
Access-Control-Allow-Credentials: true
Via: 1.1 vegur
```

下载有数字规律的文件。

```
curl http://example.com/pic[1-24].jpg
```



# 带url参数的用法

curl默认是用get方式来请求数据的。

get方式，是把参数加在url后面的。

```
curl http://httpbin.org/get?a=1&b=2
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/curl$ curl "http://httpbin.org/get?a=1&b=2"
{
  "args": {
    "a": "1", 
    "b": "2"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Connection": "close", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/7.54.0"
  }, 
  "origin": "183.11.39.123", 
  "url": "http://httpbin.org/get?a=1&b=2"
}
```

而post方式，则是这样：

```
curl --data "a=1&b=2" http://httpbin.org/post
```

```
hlxiong@hlxiong-VirtualBox:~/work/test/curl$ curl --data "a=1&b=2" http://httpbin.org/post
{
  "args": {}, 
  "data": "", 
  "files": {}, 
  "form": {
    "a": "1", 
    "b": "2"
  }, 
  "headers": {
    "Accept": "*/*", 
    "Connection": "close", 
    "Content-Length": "7", 
    "Content-Type": "application/x-www-form-urlencoded", 
    "Host": "httpbin.org", 
    "User-Agent": "curl/7.54.0"
  }, 
  "json": null, 
  "origin": "183.11.39.123", 
  "url": "http://httpbin.org/post"
}
```

还可以把文件内容作为数据传递过去。1.txt里内容就是`a=1&b=2`。这个命令效果跟上面一样。

```
curl --data @1.txt http://httpbin.org/post
```

# 其他选项

```
-A：指定Agent
```

指定证书。

```
curl --cacert /etc/ssl/certs/xx.perm https://xxx.com
```

指定方法。

```
curl -X PUT http://httpbin.org/put
curl -X POST http://httpbin.org/post
curl -X DELETE http://httpbin.org/delete
curl -X GET http://httpbin.org/get
```







# 参考资料

1、CURL常用命令

http://www.cnblogs.com/gbyukg/p/3326825.html

2、cheat curl看到的内容

3、curl命令的基本使用

https://www.cnblogs.com/yinzhengjie/p/7719804.html