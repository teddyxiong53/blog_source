---
title: nodejs之nedb用法
date: 2022-01-16 12:07:11
tags:
	- nodejs

---

--

mongodb还是比较繁杂。nedb据说是一个简单的版本。

了解一下。

[NeDB](https://github.com/louischatriot/nedb) 是使用 [Node.js](https://nodejs.org/) 实现的一个 NoSQL 嵌入式数据库操作模块， 

可以充当内存数据库，

也可以用来实现本地存储，

甚至可以在浏览器中使用。 

查询方式比较灵活，

支持使用正则、比较运算符、逻辑运算符、索引以及 JSON 深度查询等， 

适用于不需要大量数据处理的应用系统。



在你开发一个程序时，有时可能需要一部分[数据库](https://cloud.tencent.com/solution/database?from=10680)的功能，但又不想单独安装一个，因为安装数据库还是比较麻烦的，也用不到数据库那么丰富的功能，单独安装数据库会感觉比较重

假设下面两个场景：

（1）你正在写一个 Node service，你希望他是可以轻松被打包的，安装独立的数据库不能满足需求

（2）使用 Node Webkit 开发了一个桌面应用，但是不想要求用户安装一个外部数据库

**NeDB** 是一个轻量级数据库，完全使用[javascript](https://cloud.tencent.com/product/sms?from=10680)编写，并且使用了广为使用的 [MongoDB](https://cloud.tencent.com/product/mongodb?from=10680) API 使用方式

NeDB 被打包成一个 Node module，只需要一个简单的 require 便可以使用

NeDB 可以只用作内存数据库，也可以进行数据持久化，你可以把 NeDB 理解为 MongoDB 版的 SQLite



**NeDB的特点**

实现了 MongoDB 的很多特性

（1）CRUD 和 upserts

（2）持久化数据的能力

（3）表达式查询语言，可以使用符号‘.’来查询嵌套文档，支持 正则表达式、比较操作符（$lt, $lte, $gt, $gte, $in, $nin, $exists）、逻辑操作符（$and, $or, $not）

（4）Documents 修改方法 $set, $inc, $push, $pop, $addToSet, $each

（5）提供浏览器版本

**NeDB的性能**

NeDB 不是用来替代像 MongoDB 这样的真实数据库的，所以他的目标不是尽可能的快，而是够用就行

NeDB 可以达到 写 **5000**次/秒、读 **25000**次/秒

如果你的需求超出了这个，那么NeDB便不适合了



初始化

```
var db = new NeDB({
    filename: './user.db',
    autoload: true,
})
```

至此，我们得到了一个数据库对象 *db* 。 接下来，对数据库进行常规操作：插入、查询、更新、删除。





参考资料

1、

https://nodejs.fasionchan.com/zh_CN/latest/database/nedb/index.html

2、轻量级Javascript嵌入式数据库 NeDB

https://cloud.tencent.com/developer/article/1083874
