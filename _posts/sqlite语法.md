---
title: sqlite语法
date: 2018-12-25 15:18:55
tags:
	- 数据库

---



sqlite不区分大小写，但是有一些命令是区分的。例如GLOB和glob。

注释。单行和多行如下。

```
--这是单行注释
/*
	这个是多行注释。
*/
```



我下面的测试材料，是一个叫test.db的数据库。里面就一张表，叫user。属性有id和name。

里面就两条数据。

````
sqlite> select * from user;
1|allen
2|bob
````



# 运算符

1、算术。

2、比较。

3、逻辑。

4、位运算。



重点看逻辑的。

```
and
between
exists
in
not in
like
glob
not 
or
is null
is
is not
|| 连接
unique

```



语句：

```
以关键字开始，以分号结束。
```



and和or子句

```

```



参考资料

1、SQLite 语法

http://www.runoob.com/sqlite/sqlite-syntax.html