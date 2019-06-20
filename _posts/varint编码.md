---
title: varint编码
date: 2019-06-19 14:20:37
tags:
	- 编码
---

1

看protobuf是使用了varint编码。那么varint编码具体是怎么操作的？

为什么需要varint？

标准的int类型，需要4个字节。

而如果你的int的值在256以内，其实一个字节就可以了。另外3个字节的空间就是浪费的。

varint是一种紧凑的表示数字的方法。

用一个字节或者多个字节来表示一个整数。

每个字节的最高bit位，现在有了特殊含义。

如果最高bit为1，表示后面的一个字节也是这个数字的组成部分。

如果最高bit为0，则这个数字就结束了。

所以，小于128的数字，可以用一个字节来表示。

对于很大的数字，就需要5个字节才能表示了。

但是从统计的角度来说，出现很大数字的概率要低很多。

而且提供了fixed32、fixed64、double来解决这个问题。

protobuf采用了小端编码。



对于sint32和sint64，protobuf采用了zigzag编码。

zigzag编码是把有符号数映射为无符号数。

这样可以保证绝对值较小的负数，仍然有较小的varint编码值。

对照表是这样：

```
负数           编码为
0             0
-1            1
1             2
-2            3

```

对应的公式为：

```
(n<<1)^(n>>(N-1)) N可以为32和64
```

这个位移采用的是算术位移。

位移分两种：逻辑位移和算术位移。

逻辑位移很简单，全部补零就好了。

算术位移，左移很简单，还是补零。右移就根据正数和负数不同了。正数补零，负数补1 。



protobuf序列化之后，产生的二进制数据，一个单元内部，可以划分为6个部分：

1、msb 标志。

2、tag。

3、wire type。

4、len。

5、value。

6、padding。



protobuf本质还是键值对。

key = tag << 3 | wire_type

key的最低3个bit是wire_type。

编码后的数据类型，只有4种。所以3个bit来表达够用了。

1、varint。对应0

2、64 bit。对应1。

3、length-delimited。对应2 。对于string类型、数组类型、自定义class类型。

4、32 bit。对应5 。





参考资料

1、Varint编码

https://www.cnblogs.com/jacksu-tencent/p/3389843.html?utm_source=tuicool

2、图解Protobuf编码

这篇文章很好，图片特别好。

https://blog.csdn.net/zxhoo/article/details/53228303

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