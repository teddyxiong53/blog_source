---
title: mysql（1）
date: 2021-02-02 15:17:11
tags:
	- 数据库

---

--

数据库（Database）是按照数据结构来组织、存储和管理数据的仓库。

每个数据库都有一个或多个不同的 API 用于创建，访问，管理，搜索和复制所保存的数据。

我们也可以将数据存储在文件中，但是在文件中读写数据速度相对较慢。

所以，现在我们使用关系型数据库管理系统（RDBMS）来存储和管理大数据量。

所谓的关系型数据库，是**建立在关系模型基础上**的数据库，借助于**集合代数**等数学概念和方法来处理数据库中的数据。

- 1.数据以表格的形式出现
- 2.每行为各种记录名称
- 3.每列为记录名称所对应的数据域
- 4.许多的行和列组成一张表单
- 5.若干的表单组成database

# 数据库操作

```
#创建数据库
create database test;
# 删除数据库
drop database test if exists;
# 选择数据库
use test;
```

# 数据类型

大致可以分为3种：

数值。

时间。

字符串。

## 数值类型

数值类型包括：

1、严格数值。integer、smallint、decimal、numeric。

2、近似数值。float、real、double 。

int是integer的别名。dec是decimal的别名。

还支持tinyint、mediumint、bigint类型。

## 时间

date：3个字节。范围从公元1000元1月1日到9999年12月31日。日期值。格式YYYY-MM-DD

time：3字节。格式；HH:MM:SS

year：1字节。1901年到2155年。格式YYYY。

datetime：8字节。

timestamp：4字节。到2038年溢出。

## 字符串类型

char：0到255字节。定长字符串。

varchar：0到65535字节。变长字符串。

tinyblob：0到255字节。二进制字符串。

tinytext：0到255字节。短文本字符串。

blob：0到65535字节。

text：0到65535字节。

mediumblob：0到1600万字节。

mediumtext：0到1600万字节。

longblob：0到42亿字节。

longtext：0到42亿字节。

注意：

char(30)的30表示字符的格式，不是字节格式。

# table操作

## 创建

```
create table if not exists `xxx` {
	`aaa` int unsigned auto_increment,
	`bbb` varchar(100) not null,
	primary key (`aaa`)
	
} engine=InnoDb default charset=utf8;
```

## 删除

```
drop table xxx;
```

## 增加数据

```
insert into xxx ( bbb) values ( 'abc');
```

## 查询数据

```
select * from xxx;
```



# 触发器是什么

现在看这个代码，里面有用到一些特别的sql语句。

https://github.com/AllenOris/CloudDisk

```
let query = "set @path='';" +
        "call download(?, ?, @path);" +
        "select @path as path;";
```

在csdn里搜索“mysql set call“。就找到触发器这个主题的。看看。

我对mysql其实一直没有掌握。

主要我都是随便写着玩，没有动力去深入。

一次性看太多资料，也看不进去。

所以还是看代码，碰到问题点，就深入进去搞清楚，这样逐步来掌握。



# MySQL的存储过程

call实际对应的是存储过程。实际是调用层次过程。

调用存储过程的前提是先创建，create procedure 

mysql的存储过程是从mysql5.0开始增加的特性。

主要的优点是：提高执行效率，封装sql代码。

特别是封装sql代码这一条，对于复杂业务很有用。不然需要在php等代码里写一堆复杂的sql语句。

有了存储过程，就可以把把业务逻辑封装到存储过程里。

不仅便于维护，也提高了执行效率。

## 简单示例

下面以创建一个简单的无参存储过程为例。

以mysql里自带的test数据库作为测试对象。

```
> use test;

```







参考资料

1、

https://blog.csdn.net/gaokcl/article/details/83182002

2、

https://blog.csdn.net/qq_33157666/article/details/87877246

# mysql代码分析

MySQL 是一款开源的关系型数据库管理系统，它使用了 C 和 C++ 进行编写。MySQL 的代码分析可以涉及多个方面，包括了解其架构、核心模块、SQL 查询处理流程等。

以下是对 MySQL 代码分析的一般性概述：

1. **代码结构**：
   - MySQL 的代码主要包含了服务器端和客户端两部分。服务器端代码包括了各种模块，如存储引擎、SQL 查询处理、连接管理、权限控制等；客户端代码包括了用于连接 MySQL 服务器的各种库和工具。
   - 服务器端的代码主要位于 `sql/` 目录下，客户端的代码主要位于 `client/` 目录下。

2. **核心模块**：
   - 存储引擎：MySQL 的存储引擎是一个重要的模块，它负责实际的数据存储和检索操作。MySQL 支持多种存储引擎，如 InnoDB、MyISAM、Memory 等，每种存储引擎都有自己的特点和适用场景。
   - SQL 查询处理：MySQL 的 SQL 查询处理模块负责解析、优化和执行 SQL 查询语句。这涉及了词法分析、语法分析、查询优化器、执行计划生成等多个步骤。

3. **SQL 查询处理流程**：
   - MySQL 的 SQL 查询处理流程通常包括了以下几个步骤：词法分析、语法分析、语义分析、查询优化、执行计划生成、执行计划执行等。在执行过程中还涉及了锁管理、事务管理、日志记录等操作。

4. **数据库连接和线程管理**：
   - MySQL 的服务器端负责管理客户端的连接和请求，并且为每个连接分配一个线程进行处理。这涉及了连接池管理、线程池管理、请求队列管理等操作。

5. **权限控制和安全性**：
   - MySQL 通过权限控制和安全策略保护数据库的安全性。这涉及了用户认证、权限管理、数据加密、安全连接等操作。

6. **错误处理和日志记录**：
   - MySQL 提供了丰富的错误处理和日志记录机制，用于记录数据库的运行状态、错误信息和警告信息，以便于故障排查和性能优化。

对 MySQL 代码的深入分析需要对数据库系统的原理和实现有一定的了解，以及具备 C 和 C++ 编程的技能。可以通过阅读 MySQL 的官方文档、查看源代码、参考开发手册等方式进行学习和研究。





# 参考资料

1、

https://www.runoob.com/mysql/mysql-tutorial.html