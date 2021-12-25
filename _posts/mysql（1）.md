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

# 参考资料

1、

https://www.runoob.com/mysql/mysql-tutorial.html