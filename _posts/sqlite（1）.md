---
title: sqlite（1）
date: 2018-12-25 14:38:55
tags:
	- 数据库

---



sqlite的优点

1、不需要一个单独的服务器进程。

2、不需要配置。

3、数据存储在一个单一的文件里。

4、很小。

5、完全兼容ACID事务。线程安全。

6、符合sql语言标准。

7、完全用ansi C编写。

8、跨平台。



不支持的特性：

1、不支持右连接，只支持左连接。

2、对表的修改，有些不支持。例如不支持列修改。

3、view是只读的。

4、权限只是os的文件权限。没有更多的权限管理。



sql命令分类：

1、数据定义语言。DDL

create、alter、drop。

2、数据操作语言。DML

insert、update、delete

3、数据查询语言。DQL。

select。








参考资料

1、sqlite教程

http://www.runoob.com/sqlite/sqlite-intro.html