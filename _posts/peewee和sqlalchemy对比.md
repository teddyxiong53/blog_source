---
title: peewee和sqlalchemy对比
date: 2022-10-30 18:19:33
tags:
	- 数据库

---

--

觉得sqlalchemy比较复杂。文档很难读。

我做简单项目，不用这么复杂的东西。刚好看到有peewee这个东西，是轻量级的。

对比看看区别是什么。



**Peewee**：一个轻量的、有表现力的ORM——支持postgresql、mysql和sqlite。

用python（2.6+，3.2+）编写，内置了对sqlite、mysql和postgresql的支持，以及hstore等特殊扩展；



# 生成model.py

虽然两种工具都提供了使用model.py生成数据库的方式，

可以很方便的用于数据库的迁移。

但是平时做的最多的还是对已有的数据库进行操作。

```
python -e mysql -u 用户名 -P -H localhost -p 3306 数据库名 >models.py
```

SQLAlchemy输出的数据库结构更加完整，

Peewee模型的输出是不包括视图的，

如果需要需要再加一个-v的命令；

SQLAlchemy默认输出所有的视图、索引，除非加上“--noviews --noconstraints --noindexes”。

可以看出peewee的轻量，你需要的我在输出，没说要的我就不输出了。



Peewee安全性低，在生成的models.py文件中，peewee生成的文件中，直接将用户输入的用户名和密码明文的作为配置语句，

即如果我是一个黑客，我可以通过你的models.py文件就知道你的数据库的密码是什么。

SQLAlchemy的models.py中只有对应的表和字段信息，并没有连接数据库的配置信息，需要再后续的程序中再进行配置，使其应用更加灵活。

当然 peewee只是轻量服务，给自己用足够了，不需要考虑这么多的安全问题。



http://docs.peewee-orm.com/en/latest/peewee/example.html



# 参考资料

1、两个ORM的pk初体验：Peewee VS SQLAlchemy

https://blog.csdn.net/qq_33293040/article/details/110387660