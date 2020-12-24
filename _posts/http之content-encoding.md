---
title: http之content-encoding
date: 2020-12-23 11:20:30
tags:
- http
---

---

1

Content-Encoding值

　　gzip　　表明实体采用GNU zip编码

　　compress 表明实体采用Unix的文件压缩程序

　　deflate　　表明实体是用zlib的格式压缩的

　　**identity　　表明没有对实体进行编码。当没有Content-Encoding header时， 就默认为这种情况**

　　gzip, compress, 以及deflate编码都是无损压缩算法，用于减少传输报文的大小，不会导致信息损失。 **其中gzip通常效率最高， 使用最为广泛。**



参考资料

1、Content-Encoding值

https://blog.csdn.net/diaoju3333/article/details/101993273