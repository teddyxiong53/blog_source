---
title: mongodb（1）
date: 2018-12-24 13:47:27
tags:
	- 数据库

---



mongodb是c++写的。

是一个基于分布式文件存储的数据库。

在高负载的情况下，可以通过添加更多的节点来实现扩展。

把数据存储为一个文档，文档格式类似json对象。



mongodb的应用案例



基本概念

跟关系型数据库不同，有些东西术语改了。看这个对比就知道了。

| sql术语     | mongodb术语 | 说明                               |
| ----------- | ----------- | ---------------------------------- |
| table       | collection  | 表                                 |
| row         | document    | 行                                 |
| column      | field       | 列                                 |
| table join  | 没有        |                                    |
| primary key | primary key | 主键，mongodb自动把_id字段作为主键 |

_id是ObjectId。





有几个默认就带了的数据库。

admin

local

config



参考资料

1、什么是MongoDB ?

http://www.runoob.com/mongodb/mongodb-intro.html