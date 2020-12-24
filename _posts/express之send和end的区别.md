---
title: express之send和end的区别
date: 2020-12-21 11:43:30
tags:
- express
---

1

## 官方说明:

- res.end()	终结响应处理流程。
- res.send()	发送各种类型的响应。

## 1.res.end（[data] [，encoding]）

结束响应过程。这个方法实际上来自Node核心，特别是http.ServerResponse的response.end（）方法。

用于在没有任何数据的情况下快速结束响应。如果需要响应数据，请使用res.send（）和res.json（）等方法。

```
res.end();
res.status(404).end();
```

## 2.res.send([body])

发送HTTP响应。

所述body参数可以是一个Buffer对象，一个String，对象，或一个Array。例如：

```
res.send(new Buffer('whoop'));
res.send({ some: 'json' });
res.send('<p>some html</p>');
res.status(404).send('Sorry, we cannot find that!');
res.status(500).send({ error: 'something blew up' });
```



## 总结:

1. 参数类型的区别:

- res.end() 参数为: a Buffer object / a String

- res.send() 参数为: a Buffer object / a String / an object / an Array

  

  2.发送服务器内容不同

- **res.end() 只接受服务器响应数据,如果是中文则会乱码**

- res.send() 发送给服务端时,会自动发送更多的响应报文头,其中包括 Content-Tpye: text/html; charset=uft-8,所以中文不会乱码

参考资料

1、nodeJs中res.end和res.send 区别

https://my.oschina.net/rlqmy/blog/1927522