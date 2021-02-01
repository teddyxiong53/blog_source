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



# like和glob区别

like不区分大小写， glob区分大小写



like：  百分号（%）代表零个、一个或多个数字或字符。下划线（_）代表一个单一的数字或字符。

glob： 星号（*）代表零个、一个或多个数字或字符。问号（?）代表一个单一的数字或字符。



# 内置命令

sqlite的命令，都是以点号开头的，否则当成sql命令处理。



备份

```
.backup [db] 2.db 把db备份到文件，默认是main。
```

列出数据库

```
.databases
```



导出数据库为sql文件

```
.dump [tablename] 如果不指定tablename，那么就是所有的table。
```

导入数据到表里

```
.import 1.db tablename
```

显示所有的索引

```
.indices [tablename]
```

加载插件

```
.load xx
```

打开日志

```
.log on
```

设置null的位置输出为xx字符串

```
.nullvalue xx
```

设置输出到stdout

```
.output stdout
```

输出字符串

```
.print xx
```

执行sql文件脚本

```
.read xx.sql
```

查看table的结构。

```
.schema xx
```

列出所有的table

```
.tables
```

一般打开这个设置，这样内容看起来更好。

```
.headers on
.mode column
```

# 数据类型

一般数据库采用的是固定的静态数据类型。

而sqlite采用的是动态数据类型。

在sqlite里，值的数据类型跟值本身是相关的，而不是跟它的容器（例如列）相关。

所以，可以得到一个结论：

可以在创建table的时候，为column指定数据类型，但是不是必须的。

而且，指定了某种类型，你后续放入其他类型的值，也完全没有关系。

sqlite会根据存入的值自动判断column的类型。

一个column，插入不同的row的时候，可以随意指定值，不同的类型可以的。

```
sqlite> create table test (x,y,z);
sqlite> .tables
test
sqlite> insert into test values (1,2,3);
sqlite> insert into test values ('a', 'b', 'c');
sqlite> select * from test;
x           y           z         
----------  ----------  ----------
1           2           3         
a           b           c 
```

上面，我们的第一次插入，是插入数字，第二次插入，是插入了字符串。

完全没有问题。

这个是因为sqlite使用了更普遍的动态类型系统。

它把数据分别存储为五种类别。

为了跟sql标准兼容，同时实现了亲和类型（Type Affinity）。

## 存储类型

sqlite里的值，被存储为下面5种类型之一：

```
null
integer：整数，带符号。长度可以是1、2、3、4、6、8个字节。
real：浮点数
text：字符串
blob：二进制
```

以integer类型为例。

根据需要，存放在磁盘里，长度是1到8字节之间。

读取到内存里，都统一是8个字节的有符号数。

除了primary key必须是integer类型外，其他的字段没有限制。

## 亲和类型

为了兼容sql标准，也为了跟其他数据库兼容。

sqlite提供了亲和类型的概念。

这个概念的意思是：

你在创建table的时候，指定的column的类型，会被优先选用。除非无法匹配，sqlite会自动选择合适的。

支持5种亲和类型

```
text
numeric
integer
real
blob
```

字段的亲和性，按照下面的规则进行转换

1、如果类型里包含了”int“字符串，那么该字段的亲和类型是integer。

2、如果类型里包含了”char“、”clob”、“text”，那么该字段的亲和类型是text

3、如果类型里包含了blob，对应blob

4、如果类型包含了real、floa、doub、对应real。

5、其余的都是numeric。

可能有的字段的类型，同时符合了上面2条以上的规则。那么就前面的起作用。

```
sqlite> create table test(id integer primary key, x varchar(255), y tinyint);
sqlite> insert into test values (null, 'a', 1);
sqlite> select * from test;
id          x           y         
----------  ----------  ----------
1           a           1         
sqlite> select typeof(id), typeof(x), typeof(y) from test;
typeof(id)  typeof(x)   typeof(y) 
----------  ----------  ----------
integer     text        integer 
```

## 日期时间

sqlite没有单独的用来存放日期时间的存储类型。

但是可以把日期和时间存储为text、real或者integer类型。

```
text类型：
	格式为：YYYY-MM-DD HH:MM:SS.SSS
real类型：
	从公元前4714年11月24日的中午开始算的天数。
integer
	从1970年开始的秒数。
	
```

## 数值比较

比较依赖于存储类型。

规则：

1、null最小。

2、integer和real小于text和blob。

3、text小于blob。

4、text之间用ASCII码比较。

5、blob的比较，用memcmp来做。

# 数据库操作

创建数据库

```
sqlite3 test.db
```

附加数据库

```
这个是这样的场景：
我们已经打开了一个数据库A，然后需要访问另外一个数据库B。
就需要把B附加到A的操作。
命令这样写：

attach b.db as b_db
取消是：
detach b_db

但是并不常用。
```

备份和恢复

```
.backup backup.db
//中间进行一下对当前数据库的修改。
.restore backup.db
```

还可以用sql脚本文件来做备份和恢复。

```
备份
sqlite3 test.db .dump > test.db.sql
恢复
sqlite3 test.db < test.db.sql
```

# 表的操作

## 创建table

```

```

如果autoincrement自增的字段，必须是integer类型，必须是主键。

unique关键字用于约束字段的唯一性。

default关键字指定默认值。

如果要设置默认时间日期，需要使用datetime函数。

```
default (datetime('now', 'localtime'))
```

## 内置表

sqlite数据库里有一个名为sqlite_master的内置表。

它定义了数据库的模式，并记录了所有已经创建的表的信息。

这张表的结构是：

```
sqlite> .schema sqlite_master
CREATE TABLE sqlite_master (
  type text,
  name text,
  tbl_name text,
  rootpage integer,
  sql text
);
```

我们要查询当前数据库里所有的table。除了使用sqlite的内置命令`.tables`之外，还可以用sql语句

```
select name from sqlite_master where type='table' order by name;
```

索引在sqlite_master里的type是index。

sqlite_master是只读的。

它会被create table / create index /drop table /drop index这些命令自动更新。

临时表不会出现在sqlite_master里。

临时表及其索引和触发器，存放在另外一个叫sqlite_temp_master里。

另外还有一个sqliet_sequence的内置表。

这个表用来保存其他表的rowid的最大值。

## 把表清空

```
delete from xx;
还需要把sqlite_sequence里的seq复位
update sqlite_sequence set seq=0 where name='xx'
```

## 删除表

```
drop table xx;
```

## 修改表

改表名

```
alert table xx rename to yy;
```

给表增加一个列。

```
alert table xx add column aa text;
```

## 复制表

```
//只复制数据
insert into xx selec * from yy;

//只复制schema
create table xx as select * from yy where 0;

//复制数据和schema
create table xx as select * from yy;
```

# 约束

约束是用来确保数据库里的数据的准确性和可靠性。

sqlite里支持的约束有：

```
not null
default
unqiue
primary key：
check
foreign key：外键约束，默认不支持，需要手动开启。
```

可以多个字段组合起来做主键，这个叫复合主键。

```
create table test (
	name,
	email,
	password,
	primary key(name, email)
)
```

## check

这个会在插入的时候，检查值是否符合要求。check失败，则插入失败。

```
salary real check(salary > 0)
```

sqlite不允许在alert的时候，修改约束。

只能在create的时候，把约束写好。

## foreign key

sqlite从2009年的3.6.19版本，开始支持foreign key

外键用于关联2个表。

这也是关系型数据库的主要特点之一。

sqlite的外键默认是关闭的。需要在运行的时候，手动打开。

使用pragma语句来打开。

```
pragma foreign_keys=on;
```

以博客程序为例子。

一个文章topic，对应了一个作者user。

topic里就有一个外键，是user的id。

创建外键的基本语法

```
create table users (
	id integer autoincremnt primary key,
	name
)
create table topics (
	topic_id,
	constraint	fk_user_id foreign_key (user_id) references users(id)
)
```

# 索引index

索引用来对数据进行排序。

这样可以加快搜索和排序的速度。

本质是一种特殊的查找表。

是一个指向表里面数据的指针。

有这些特点：

1、索引改善了读取的性能。但是降低了写入的性能。

2、索引可能占用大量空间。

3、可以指定多个列来一起构成一个索引，叫复合索引。

4、索引的创建和删除，对表没影响。

5、索引可以指定唯一性，也就是唯一索引。

基本语法

```
//单列索引
create index xx_index on xx (email);

//唯一索引
create unique index xx_index on xx (email);

//复合索引
create index xx_index on xx (name, email);
```

## 自动创建索引

数据库默认为给有primary key约束和unique约束的列，创建索引。

这样自动创建的索引叫隐式索引。

## 删除索引

```
drop index xx;
```

## 索引不适合的情况

1、较小的表

2、经常插入和更新的表。

3、有大量null值的列。

4、频繁操作的列。

5、较少可能值的列。

# 触发器

sqlite的触发器是数据库的回调函数。

在某些操作的时候，自动执行。

触发器一般的用途：

1、保证数据的一致性。例如在insert或者update的时候，对数据进行统一转化。

2、计算列的值或者更新时间戳。

3、表A的变化时，触发表B的活动。例如更新删除数据时，写入审计表里。

4、验证输入是否合法。

## 创建

```
create trigger xx [before|after] event_name
on table_name
[for each row]
[when condition]
begin
	//这里写代码。
end;
```

before和after，指定是在操作之前还是操作之后执行。

event_name可以是：insert、delete、update。

sqlite目前只支持`for each row`的触发器。

没有`for each statement`的触发器。

# 日期和时间函数

```
date
time
datetime
julianday
strftime
```

最常用的就是这一个

```
datetime('now')
```

测试这些函数

```
sqlite> select time('now');
06:17:37
sqlite> select date('now');
2021-01-29
sqlite> select datetime('now');
2021-01-29 06:18:30
```

这个是utc时间。需要校正为北京时间。

```
sqlite> select datetime('now', '+8 hour');
2021-01-29 14:19:08
```

用localtime也可以。

```
sqlite> select datetime('now', 'localtime');
2021-01-29 14:19:24
```



# 锁机制

sqlite基于锁来实现并发控制。

以保证数据的安全和完整性。

sqlite的锁是粗粒度的。

所以效率没有其他的数据库高。但是实现简单。

当有连接在写数据的时候，数据库被锁住，直到写事务完成。

在这个期间，所有其他的对数据库的读写都被阻塞。

sqlite在3.7.0版本开始引入WAL技术。这个可以解决读写互斥的问题。

## 锁状态

sqlite的数据库连接状态有5个：

1、unlocked。没有锁。

2、shared。共享锁。

3、reserved。预留锁。

4、pending。未决锁。

5、exclusive。排他锁。



## 死锁

在使用事务的情况下，sqlite的所禁止存在死锁的可能性。



# 和mysql的比较



# 事务

事务是dbms最核心 技术。

关于事务处理的技术很多，这里只讨论跟sqlite事务实现的一些原理。

sqlite的事务，跟大型的dbms相比，其实比较简单。

哪些对象在事务下运行？

事务的生命周期，就是什么时候开始，什么时候结束，什么时候影响别的连接（这一点对于并发性非常重要）

一个连接（connection）包含多个statement。

每个connection有一个跟数据库关联的b-tree和一个pager。

pager在连接中起着非常重要的作用。

pager负责管理：

1、事务。

2、锁。

3、内存缓存。

4、crash recovery。

一般来说，一个事务的生命周期跟一个statement差不多。

默认情况下，事务自动提交。

你可以通过commit来手动提交。



## 读事务

我们先看看select语句执行时，锁的状态变化过程。

一个连接执行select语句，触发一个事务。

锁的状态变化：

1、首先是unlocked

2、然后是shared。

3、事务提交后，变回unlocked。

看下面的例子。伪代码。

```
db = open('test.db')
db.exec('begin')
db.exec('select * from topics')
db.exec('select * from users')
db.exec('commit')
db.close()
```

上面的情况，因为明确使用了begin和commit来包裹里面的select语句。

所以，这2个select是在一个事务下执行。

所以，对应的锁的变化过程是：

```
unlocked -> pending -> shared -> unlocked
```

如果去掉begin和commit。那么锁的变化是这样的：

```
unlocked -> pending -> shared -> unlocked -> pending -> shared -> unlocked
```

## 写事务





https://www.kancloud.cn/kangdandan/sqlite/64351



# 参考资料

1、sqlite教程

http://www.runoob.com/sqlite/sqlite-intro.html

2、Sqlite3 like和glob的区别

https://blog.csdn.net/majiakun1/article/details/50635121

3、Sqlite 基本概念及使用概述

这个很好，条理清晰。

https://blog.konghy.cn/2018/07/30/sqlite/

4、SQLite权威指南

https://www.kancloud.cn/wizardforcel/the-definitive-guide-to-sqlite/154144