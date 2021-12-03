---
title: httpbin网站分析
date: 2017-09-24 11:00:30
tags:
	- http

---



1、httpbin网站是一个测试网站。用来测试各种http请求和响应。

2、网址是：http://httpbin.org/

3、可以测试的项目有：cookie、ip、headers和登陆验证等等。

4、对于web开发很有用。

5、是基于Python+flask编写的开源项目。

6、源码地址在<https://github.com/Runscope/httpbin>

7、是学习爬虫技术的好站点。

8、有点像一个蜜罐，不怕你去折腾它。

9、你可以用各种语言来对它进行访问。



# 接口列表：

```
/    主页
/ip  返回你的ip地址
/user-agent 返回你的浏览器的agent名字。
/headers 返回header字典
/get 返回get数据。
/post 返回post数据。
/patch  返回patch数据
/put 返回put数据。
/delete 返回delete数据
/gzip  返回gzip编码的数据
/deflate 返回deflate编码的数据
/status/:code 返回指定的http状态码
/response-headers 返回指定的回复header
/redirect/:n  302重定向n次
/redirect-to?url=foo  302重定向到foo这地址
/relative-redirect/:n 相对重定向n次
/cookies  返回cookie数据
/cookies/set?name=value 设置一条或者多条cookie数据
/cookies/delete?name 删除cookie数据
/basic-auth/:user/:passwd http基本授权
/hidden-basic-auth/:user/:passwd 404错误授权

```



# Python简单使用

```
import requests

s = requests.Session()
print s.get("http://httpbin.org/ip").text
print s.get("http://httpbin.org/get").json()
print s.post("http://httpbin.org/post", {"key": "value"}, headers={'user-agent':'xhl'}).text
```

# 用postwoman来调试



# 代码分析

我们在本地搭建一个环境。

```
 docker run -p 80:80 kennethreitz/httpbin
```

这个会下载docker的运行环境。

然后自动运行。

我们用这个就可以访问到本地的httpbin了。

http://192.168.190.137/



不借助docker直接在本地运行的方法：

1、下载代码。

2、在代码目录下：

```
sudo python setup.py install
```

这个会下载一些依赖的东西进行安装。

3、运行。

```
python
>>> import httpbin
用help查看信息。发现用法是下面的这样的
>>> httpbin.app.run(port=5000, host='0.0.0.0') #如果要用80端口，就要用sudo来运行Python。
```

运行打印：

```
>>> httpbin.app.run(port=5000, host='0.0.0.0')  
 * Serving Flask app "httpbin.core" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
192.168.190.1 - - [20/Jun/2018 23:40:37] "GET / HTTP/1.1" 200 -
192.168.190.1 - - [20/Jun/2018 23:40:37] "GET /flasgger_static/swagger-ui.css HTTP/1.1" 200 -
192.168.190.1 - - [20/Jun/2018 23:40:37] "GET /flasgger_static/swagger-ui-bundle.js HTTP/1.1" 200 -
192.168.190.1 - - [20/Jun/2018 23:40:37] "GET /flasgger_static/swagger-ui-standalone-preset.js HTTP/1.1" 200 -
192.168.190.1 - - [20/Jun/2018 23:40:37] "GET /flasgger_static/lib/jquery.min.js HTTP/1.1" 200 -
192.168.190.1 - - [20/Jun/2018 23:40:38] "GET /spec.json HTTP/1.1" 200 -
192.168.190.1 - - [20/Jun/2018 23:40:55] "GET /static/favicon.ico HTTP/1.1" 200 -
```

# express实现httpbin

https://github.com/sheharyarn/httpbin-node



# php版本

https://github.com/zhanghuid/httpbin

