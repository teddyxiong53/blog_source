---
title: mongodb命令行操作
date: 2018-12-23 15:03:27
tags:
	- 数据库

---



命令行的基本用法

```
# mongo
> help
> show dbs
> db  查看当前使用的是哪个数据库。默认是test。
> use myblog
> show collections 查看有哪些表。
> db.users.find() 查看表里的内容。
> db.dropDatabase() 删除这个数据库。
```

数据库操作

```
use xxx
```

如果存在xxx这个数据库，则切换到它。否则创建xxx这个数据库。

删除数据库

是删除当前数据库。

```
db.dropDatabase()
```

```
> db.dropDatabase()
{ "dropped" : "xxx", "ok" : 1 }
```

插入数据。yyy是collection的名字。

```
db.yyy.insert({'name':'allen', 'age': 10})
```

查看collection情况。

```
> show collections
system.indexes
yyy
```

查询

```
> db.yyy.find()
{ "_id" : ObjectId("5f58a70ce7c8a14d1b4bd270"), "name" : "allen", "age" : 10 }
```

更新。把age改为20

```
> db.yyy.update({'name':'allen'},{'age':'20'})
WriteResult({ "nMatched" : 1, "nUpserted" : 0, "nModified" : 1 })
```

查询看看改动有没有生效。不符合预期。把name属性给去掉了。

所以update的时候，后面的需要写完整。

```
> db.yyy.find()
{ "_id" : ObjectId("5f58a70ce7c8a14d1b4bd270"), "age" : "20" }
```

update的完整是4个参数：

```
update(cond, new, upsert, multi)
参数1：表示要更新的内容的条件。
参数2：新的内容。
参数3：upsert表示如果找不到，是否把新的插入进去。默认是不插入的。bool类型
参数4：表示如果找到多条，是否都更新。默认只更新第一条。bool类型。
```

删除collection的记录。

```
db.yyy.remove(cond, justOne)
参数1：过滤条件。
justOne：是否只删除第一条。默认为true。
```

```
> db.yyy.remove({'age': '20'})
WriteResult({ "nRemoved" : 1 })
```

删除collection里的所有的数据。这样：

````
db.yyy.remove({})
````

查询条件

```
db.yyy.find({'age': {$lt:50}}) 小于50的
$lte
$gt
$gte
$ne
```

与关系

```
就是条件里同时列出多条属性就是与的关系。
db.yyy.find({k1:v1, k2:v2})
```

或关系

```
db.yyy.find({
	$or: [
		{k1:v1}, {k2:v2}
	]
})
```

type

这个是用来查询属性为某种类型的条件。例如查询title为string类型的记录。

```
db.yyy.find({'title': {$type:2}})
```

type的值对应表格

```
Double  1
String 2
Object 3 
...
```

limit方法

limit方法接受一个数字参数。

表示读取的记录条数。

用在find后面链式调用。

skip

跟limit相反，表示跳过最前面的几个条数。



sort方法

对数据进行排序。一个参数：1表示升序，-1表示降序。

也是在find后面调用。



索引

索引对于提高查询效率是非常重要的。

如果没有索引，mongodb必须读取collection里所有的document。

这个效率是非常低的。

索引是特殊的数据结构。存储在一个易于遍历读取的数据集合里。

索引是对数据库表中一列或者多列进行排序的一种结构。

要使用索引，第一步就是创建索引，使用ensureIndex方法。

```
db.yyy.ensureIndex({"name":1}) 1表示安装名字的升序建立索引。
```

可以指定多个字段建立索引。

```
db.yyy.ensureIndex({'name':1, 'age':-1})
```



聚合 aggregate

聚合主要用来处理数据，例如求取平均值，求和。返回计算的结果。



参考资料

1、

https://www.w3cschool.cn/mongodb