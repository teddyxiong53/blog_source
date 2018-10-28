---
title: Python之hyper模块
date: 2018-10-28 14:05:13
tags:
	- python

---





http2相当于http1.1的改进有：

1、速度更快。

2、带宽占用更低。

3、连接管理。

hyper就是一个Python写的http2的client。

下面的测试代码要基于一个测试网站来做。http://nghttp2.org/httpbin/

但是我们填写host的时候，要写nghttp2.org。

后面的资源写“/httpbin/get”这种。不然主机解析不到的。

这个是类似之前的httpbin.org的网站的。

最简单的代码这样写：

```
import hyper

conn = hyper.HTTP20Connection('nghttp2.org') 
conn.request("GET", "/httpbin/get")
resp = conn.get_response()
print(resp.read())
```

运行结果：

```
b'{"args":{},"headers":{"Host":"nghttp2.org","Via":"2 nghttpx"},"origin":"59.63.206.245","url":"https://nghttp2.org/httpbin/get"}\n'
```

hyper不需要依赖其他组件。



hyper的主要类有：

```
__all__ = [
    HTTPConnection,
    HTTP20Response,
    HTTP20Push,
    HTTP20Connection,
    HTTP11Connection,
    HTTP11Response,
]
```



# 参考资料

1、官方文档

https://hyper.readthedocs.io/en/latest/

