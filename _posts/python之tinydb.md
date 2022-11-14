---
title: python之tinydb
date: 2022-10-29 12:06:33
tags:
	- python

---

--

在nodejs里，有nedb这样的小型文档数据库，看看python里有没有类似的东西。

有的，就是tinydb。

# 资源收集

这些一些对tinydb进行的改写和扩展。

https://tinydb.readthedocs.io/en/latest/extensions.html

# 基本介绍

## tinydb的优点

* tiny。代码只有1800行，其中注释40%，所以大概就是1000行代码。
* 基于document。类似mongodb。
* 简单。提供简单干净的api。
* 纯python编写。
* 在python3.5+和pypy上可以工作。
* 可扩展。
* 100%测试覆盖。

## 不建议使用的场景

* 并发访问。
* 需要给table创建index的场景。
* ACID 保证

# get started

安装

```
pip install tinydb
```

创建一个db

```
from tinydb import TinyDB, Query
db = TinyDB('db.json')
```

插入数据：

```
db.insert({
	'type': 'apple',
	'count': 7
})
db.insert({
	'type': 'peach',
	'count': 3
})
```

insert函数返回的是插入的数据id。

查看所有的数据

```
db.all()
```

也可以用for进行遍历。

```
for item in db:
	print(item)
```

用search查询

```
Fruit = Query()
db.search(Fruit.type == 'peach')
db.search(Fruit.count > 5)
```

更新

```
db.update({
	'count': 10,
}, Fruit.type == 'apple')
```

删除

```
db.remove(Fruit.count < 5)
```

清空数据

```
db.truncate()
```

# 高级用法

## storage

在进一步深入之前，我们需要先看看tinydb的storage机制。

默认是使用python的json模块来保存数据。

你可以自己替换storage机制。

## query

有两种方式来构造query

方法一：

```
from tinydb import Query
User = Query()
db.search(User.name == 'allen')
```

用点号`.`来级联。

如果属性名字不是合法的python符号的话，例如含有`-`。那么就要用``User['country-code']`这种dict的方式来做了。

上面这种方式是ORM方式。

还可以用传统的方式。

```
from tinydb import where
db.search(where('username') == 'allen')
```

传统方式，反而是通过ORM实现的。



## advance query



# table

如果没有指定table，那么默认是插入到一个叫`_default`的table里。



# 参考资料

1、官网文档

https://tinydb.readthedocs.io/en/latest/intro.html