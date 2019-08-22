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



为什么需要mongodb？跟mysql的不同是什么？



# index



#模糊匹配

```
$in
	在某个范围内。
$nin
	不在某个范围内。
$or
$not

```



参考资料

1、什么是MongoDB ?

http://www.runoob.com/mongodb/mongodb-intro.html

2、

https://www.cnblogs.com/caihuafeng/p/5494336.html

3、MongoDB索引原理

http://www.mongoing.com/archives/2797

4、mongo-查询（2）——比较/$in/$nin/$or/$not

https://www.cnblogs.com/yuechaotian/archive/2013/02/04/2891506.html