---
title: nodejs之express接收文件上传
date: 2019-06-18 11:49:37
tags:
	- nodejs
---

1

客户端用postman进行上传。

上传地址：http://172.16.2.102:3000/upload

先写headers。里面就填写

Content-Type: multipart/form-data

然后写body。选择为form-data

下面key，最右边点击下拉三角形，可以选择File，然后随便上传一个文件。

点击send。

```
teddy@teddy-ThinkPad-SL410:~/work/dossos/fake_server$ node http_server.js 
undefined
Error: Multipart: Boundary not found
```

我的服务端报错了。

说没有找到边界符号。

需要这样写才行：

```
Content-Type: multipart/form-data;boundary=123
```

123是随便给的一个数字。

这样就不会报错了。

然后body这个标签下，文件需要加上key，我就写“file”。

我在服务端，没法通过req.file来获取到上传的文件。是为什么？



我用multer是一直没法获取到req.file。

换一种方式吧。

用formidable来做。

```
MultipartParser.end(): stream ended unexpectedly: state = START_BOUNDARY
```

感觉是关闭连接太早了导致的。

我自己写一个html文件看看。这个不能上传。

再换一种方式进行上传看看。



就下面的代码，打印出来看看就好了。

```
const http = require('http')

const server = http.createServer((req, res) => {
  let arr = []

  req.on('data', (buffer) => {
    arr.push(buffer)
  })

  req.on('end', () => {
    let buffer = Buffer.concat(arr)

    console.log(buffer.toString())
  })
})

server.listen(3000)
```



参考资料

1、Express使用Multer实现文件上传

https://blog.csdn.net/kaelyn_X/article/details/78822006

2、Postman Post请求上传文件

https://blog.csdn.net/maowendi/article/details/80537304

3、postman 请求文件上传遇到的问题

https://blog.csdn.net/qq_30711653/article/details/88717471

4、nodejs使用http模块编写上传图片接口测试客户端

https://www.jianshu.com/p/88e39ebde95c

5、Nodejs教程16：POST文件上传

https://blog.csdn.net/chencl1986/article/details/88210892