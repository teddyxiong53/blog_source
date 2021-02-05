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



参考资料

1、

https://www.runoob.com/mysql/mysql-tutorial.html