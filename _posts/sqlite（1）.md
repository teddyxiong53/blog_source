---
title: sqlite（1）
date: 2018-12-25 14:38:55
tags:
	- 数据库

---

--

# 简介

当谈及轻量级数据库管理系统时，SQLite是一个备受推崇的选择。它被设计为零配置、无服务器的、自给自足的数据库引擎。下面是一些关于SQLite的要点：

| 特点    | 描述                                          |
| ------- | --------------------------------------------- |
| 类型    | 嵌入式数据库管理系统                          |
| 语言    | C语言编写，但支持多种编程语言的接口           |
| 存储    | 单个磁盘文件                                  |
| 配置    | 无需配置，零管理成本                          |
| 容量    | 没有理论上的最大数据库大小限制                |
| 跨平台  | 支持多种操作系统，包括Windows、Linux、macOS等 |
| ACID    | 支持ACID事务，保证数据完整性和一致性          |
| SQL标准 | 遵循ANSI SQL标准                              |
| 扩展性  | 支持常见的SQL功能，如JOIN、触发器、视图等     |
| 高性能  | 轻量级设计，快速读写操作                      |
| 开源    | 遵循开源许可证                                |

SQLite的轻量级、易用性和广泛的应用领域使其成为许多项目的首选数据库引擎。

# 发展历史

| 时间   | 事件                                                   |
| ------ | ------------------------------------------------------ |
| 2000年 | 第一个公开发布的版本，由D. Richard Hipp创建            |
| 2004年 | 发布了SQLite 3.0，引入了新的存储引擎和其他改进         |
| 2005年 | SQLite成为Mozilla Firefox浏览器的内置数据库            |
| 2010年 | 发布了SQLite 3.7，引入了写入排序和其他性能优化         |
| 2013年 | 发布了SQLite 3.8，引入了部分索引和其他功能             |
| 2014年 | SQLite成为Android平台的默认数据库引擎                  |
| 2018年 | 发布了SQLite 3.24，引入了Window Functions等高级SQL功能 |
| 2020年 | 发布了SQLite 3.31，引入了增强的FTS5全文搜索和其他改进  |
| 2021年 | 发布了SQLite 3.35，引入了R-tree索引和其他新功能        |
| 2022年 | 继续发布新的版本，不断改进和完善功能                   |

SQLite在其长期的发展过程中持续保持着稳健的增长，并逐步成为了许多应用和系统的首选数据库引擎之一。

# 作者简介

SQLite的创始人是D. Richard Hipp（简称Richard Hipp）。

他是美国计算机科学家，于1999年创建了SQLite数据库引擎。

Richard Hipp出生于1955年，拥有计算机科学学位。

他是SQLite的主要设计者和开发者，致力于推动SQLite的发展和改进。

除了SQLite之外，他还参与了其他开源项目的开发，并持续致力于计算机科学领域的研究和创新。

# sqlite代码架构分析

SQLite的代码架构是相当精巧的，以下是对其主要组成部分的简要分析：

| 组件               | 描述                                                         |
| ------------------ | ------------------------------------------------------------ |
| **核心引擎**       | 包括解析器、查询优化器、执行引擎等，负责处理SQL语句的解析、优化和执行。这部分代码是SQLite的核心，负责实现数据库的基本功能。 |
| **存储引擎**       | 负责处理数据的读写操作，将数据写入磁盘并从磁盘读取数据。SQLite使用B树作为其默认的存储结构，但也支持其他类型的存储引擎，如R-tree等。 |
| **SQL解析器**      | 负责将SQL语句解析成对应的语法树，并进行语法分析和语义分析。解析器将SQL语句转换为内部数据结构，以便后续的优化和执行。 |
| **查询优化器**     | 负责对查询进行优化，以提高查询性能。优化器会根据查询的特性和索引情况，选择合适的执行计划，并进行各种优化操作，如条件下推、索引选择等。 |
| **执行引擎**       | 负责执行优化后的查询计划，从存储引擎中读取数据并进行相应的操作。执行引擎会按照查询计划的要求，逐步执行查询并生成结果。 |
| **线程管理**       | 负责处理多线程并发访问的问题，保证数据库的线程安全性。SQLite使用轻量级的线程模型，并通过读写锁来控制并发访问。 |
| **数据库文件格式** | 定义了SQLite数据库文件的存储格式，包括文件头、页面布局、数据结构等。数据库文件格式决定了SQLite的持久化存储方式，以及数据的组织和访问方式。 |
| **扩展接口**       | 提供了用于扩展SQLite功能的接口，允许用户编写自定义的函数、聚合器、虚拟表等，并将其集成到SQLite中。这些扩展可以通过动态链接库的方式加载和调用。 |

SQLite的代码结构相对清晰，模块化程度高，这使得其易于理解和扩展。同时，SQLite的设计也充分考虑了性能和效率，使得其在资源受限的环境下能够提供稳定和高效的数据库服务。

# sqlite的benchmark数据

SQLite的性能表现可以通过各种基准测试（Benchmark）进行评估。这些基准测试通常涉及一系列标准化的操作，例如插入、查询、更新和删除数据，以及对事务处理能力的评估等。

以下是SQLite的一些常见基准测试的结果（以TPS为单位，即每秒事务数）：

| 基准测试                              | 结果（TPS）   |
| ------------------------------------- | ------------- |
| 插入性能测试（Insert Benchmark）      | 1000 - 10000+ |
| 查询性能测试（Query Benchmark）       | 5000 - 50000+ |
| 更新性能测试（Update Benchmark）      | 2000 - 20000+ |
| 删除性能测试（Delete Benchmark）      | 1000 - 10000+ |
| 事务处理测试（Transaction Benchmark） | 1000 - 20000+ |

这些结果取决于多种因素，包括硬件配置、数据库大小、索引设置、操作类型等。值得注意的是，SQLite通常在轻量级应用和嵌入式系统中表现出色，但在高并发和大规模数据处理方面可能不如一些专门的服务器数据库引擎。

# sqlite的代码量

SQLite的代码量相对较小，这也是其被称为“嵌入式”数据库的原因之一。SQLite的核心引擎和主要功能都包含在一个相对较小的代码库中，这使得它易于理解、维护和集成到各种应用中。

截至最近的统计数据，SQLite的核心代码库（不包括测试和文档）大约有约 230,000 行 C 代码。这个数字可能会随着时间的推移而略有变化，但总体上来说，SQLite的代码量是相对较小的，这也符合其轻量级、嵌入式的设计理念。

# sqlite命令

SQLite是一个命令行工具，可以用来管理SQLite数据库。以下是一些常用的SQLite命令：

1. **连接数据库**：使用`.open`命令连接到现有数据库文件或创建一个新的数据库文件。
   ```sql
   .open database_name.db
   ```

2. **退出SQLite**：使用`.exit`或`.quit`命令退出SQLite命令行工具。
   ```sql
   .exit
   ```

3. **显示表格**：使用`.tables`命令列出当前数据库中的所有表格。
   
   ```sql
   .tables
```
   
4. **显示模式**：使用`.mode`命令设置输出模式，例如列、列头、HTML等。
   
   ```sql
   .mode column
```
   
5. **显示列头**：使用`.header`命令设置是否显示列头。
   ```sql
   .header on
   ```

6. **执行SQL语句**：可以直接输入SQL语句执行查询、插入、更新等操作。
   ```sql
   SELECT * FROM table_name;
   ```

7. **执行脚本**：使用`.read`命令执行一个包含SQL语句的脚本文件。
   ```sql
   .read script.sql
   ```

8. **查看帮助**：使用`.help`命令获取SQLite命令行工具的帮助信息。
   ```sql
   .help
   ```

这些命令可以让你在SQLite命令行中执行各种操作，管理数据库文件并执行SQL查询。

# sqlite的优点

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



# sql命令分类：

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

SQLite支持以下基本数据类型：

1. **NULL**: 存储NULL值。
2. **INTEGER**: 整数，可以存储带符号的整数，取决于存储大小。
3. **REAL**: 浮点数，用于存储浮点数值。
4. **TEXT**: 字符串，用于存储文本字符串。
5. **BLOB**: 二进制数据，用于存储二进制对象。

SQLite是一种动态类型系统，允许在同一列中存储不同类型的值。此外，SQLite还支持以下特殊的数据类型：

6. **DATE**: 存储日期，但不提供内置的日期类型。通常将日期存储为文本或整数。
7. **TIME**: 存储时间，类似于日期，通常将时间存储为文本或整数。
8. **DATETIME**: 存储日期和时间的组合，通常将日期和时间组合存储为文本或整数。
9. **BOOLEAN**: 存储布尔值，通常将布尔值存储为整数（0表示false，1表示true）或文本（'true'或'false'）。

这些数据类型可以满足大多数应用程序的需求，并且可以通过适当的约束和转换来处理更复杂的数据。



==一般数据库采用的是固定的静态数据类型。==

而sqlite采用的是动态数据类型。

在sqlite里，值的数据类型跟值本身是相关的，而不是跟它的容器（例如列）相关。

所以，可以得到一个结论：

==可以在创建table的时候，为column指定数据类型，但是不是必须的。==

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

==这个是因为sqlite使用了更普遍的动态类型系统。==

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

==为了兼容sql标准，也为了跟其他数据库兼容。==

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

# sqlite内置的函数

SQLite内置了许多函数，可以用于各种数据操作和计算。以下是一些常见的SQLite内置函数：

1. **数学函数**：如`ABS()`（绝对值）、`ROUND()`（四舍五入）、`MAX()`（最大值）、`MIN()`（最小值）、`SUM()`（求和）等。

2. **字符串函数**：如`LENGTH()`（字符串长度）、`UPPER()`（将字符串转换为大写）、`LOWER()`（将字符串转换为小写）、`SUBSTR()`（提取子字符串）等。

3. **日期和时间函数**：如`DATE()`（获取当前日期）、`TIME()`（获取当前时间）、`DATETIME()`（获取当前日期和时间）、`JULIANDAY()`（将日期转换为儒略日数）等。

4. **聚合函数**：如`AVG()`（平均值）、`COUNT()`（计数）、`GROUP_CONCAT()`（连接组内的字符串）等，用于在查询结果集上执行聚合操作。

5. **条件函数**：如`IFNULL()`（如果第一个参数不为空则返回该参数，否则返回第二个参数）、`COALESCE()`（返回参数列表中第一个非空值）等。

6. **类型转换函数**：如`CAST()`（将值转换为指定数据类型）、`CONVERT()`（将值转换为指定数据类型）等。

7. **正则表达式函数**：如`REGEXP`、`REGEXP_MATCH()`、`REGEXP_REPLACE()`等，用于进行正则表达式匹配和替换操作。

8. **全文搜索函数**：如`FTS3/4/5`模块提供的全文搜索函数，如`MATCH()`、`SNIPPET()`、`OFFSET()`等。

9. **几何函数**：如`ST_DISTANCE()`（计算两个几何对象之间的距离）、`ST_INTERSECTS()`（检查两个几何对象是否相交）等，需要在SQLite中启用扩展以使用。

这些函数覆盖了许多常见的数据操作和计算需求，可以在SQLite查询中直接调用使用。

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

SQLite使用锁机制来处理多个并发事务对数据库的访问。它实现了一个轻量级的锁定系统，具有以下几种类型的锁：

1. **共享锁（SHARED）**：允许多个事务同时读取同一资源，但阻止其他事务写入该资源。多个共享锁可以同时存在，互相不会阻塞。

2. **排它锁（EXCLUSIVE）**：阻止其他事务读取或写入相同的资源，只有一个事务可以持有排它锁。在SQLite中，如果事务需要进行写入操作，它必须首先获取排它锁。

3. **保留锁（RESERVED）**：事务请求一个排它锁，但是只有在其他共享锁释放后才会升级为排它锁。这种锁通常用于预留资源，等待条件满足时再执行写操作。

4. **待定锁（PENDING）**：事务等待另一个事务释放锁的状态。当一个事务请求排它锁，但其他事务持有共享锁时，该事务会进入待定状态。

5. **游标锁**：在SQLite中，每个游标（或称为数据库句柄）都有一个相关联的锁。游标锁用于控制对特定行或页面的访问。

SQLite的锁机制通过锁定数据库中的页面来实现，因此它被称为“页面级锁定”。这种锁定方式相对简单高效，并且能够处理大量的并发事务。但是，由于SQLite是一个嵌入式数据库，通常在单用户或轻量级多用户环境下使用，因此它的锁机制可能不如一些专门的服务器数据库引擎那样复杂或高级。



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



# sqlite的各种限制

最大的db文件可以到多大？

存储的数据最大可以是多少？

可以支持同时多少个连接？

通过`.limit`命令可以查看。

```
              length 1000000000    // 字符串或BLOB的最大长度10亿，一行的最大长度
          sql_length 1000000000    // sql语句最大长度
              column 2000    // 列数，可以在编译时才可以将最大列出改为32767
          expr_depth 1000    // 表达式树的最大深度，SQLite将表达式解析到树中进行处理。
     compound_select 500    // 复合SELECT语句中的最大术语数
             vdbe_op 25000    // 虚拟机程序中用于实现SQL语句的最大指令数
        function_arg 127    // 一个函数的最大参数个数
            attached 10        // ATTACH语句，附加数据库最大值为125
 like_pattern_length 50000    // LIKE模式匹配算法或GLOB模式的最大长度
     variable_number 250000    // 任何参数的索引号
       trigger_depth 1000    // 触发递归的最大深度
      worker_threads 0        // 可以启动的辅助工作线程的最大数量
```



参考资料

1、

https://blog.csdn.net/weixin_39465823/article/details/106348850

# sqlite_master表

这个表是sqlite数据库内置的。可以用来查询数据库里是否存在某个表格。

SELECT * from sqlite_master where name = 'posts'



`sqlite_master`是SQLite系统表之一，

用于存储数据库的元数据信息，

包括表格、索引、视图和触发器等对象的定义。

它是SQLite内部使用的系统表，

用户可以通过查询这个表来获取数据库中的元数据信息。

以下是`sqlite_master`表的基本结构：

| 列名     | 类型    | 描述                                 |
| -------- | ------- | ------------------------------------ |
| type     | TEXT    | 对象类型（如表、索引、视图、触发器） |
| name     | TEXT    | 对象名称                             |
| tbl_name | TEXT    | 表名称（如果适用）                   |
| rootpage | INTEGER | 根页码（如果适用）                   |
| sql      | TEXT    | 对象的创建SQL语句                    |

通过查询`sqlite_master`表，你可以了解数据库中包含的所有表格、索引、视图和触发器，以及它们的定义和其他相关信息。例如，你可以执行以下查询来获取所有表格的名称：

```sql
SELECT name FROM sqlite_master WHERE type='table';
```

或者，你可以执行以下查询来获取指定表格的创建SQL语句：

```sql
SELECT sql FROM sqlite_master WHERE type='table' AND name='your_table_name';
```

这些查询可以帮助你了解数据库的结构和对象之间的关系，以便进行进一步的操作和分析。

# 写入文件的性能问题

往sqlite里插入一条数据，会导致整个文件重新写入到磁盘吗？加入数据库文件非常大，那岂不是会导致严重的性能问题？



在 SQLite 中，往数据库插入一条数据通常不会导致整个文件重新写入到磁盘。SQLite 使用一种称为写入-回放（write-ahead logging，WAL）的日志机制来处理数据的插入、更新和删除操作。

在默认的WAL模式下，当进行数据插入操作时，SQLite 会将新数据追加到一个称为WAL文件（Write-Ahead Log）的日志文件中，而不是直接修改原始数据库文件。这个日志文件记录了对数据库进行的修改操作。

然后，SQLite 会将这些修改操作应用到原始数据库文件的副本中，生成一个新的数据库文件。这个过程称为回放（replay），它只会涉及到被修改的数据页和相关的索引页，而不会重新写入整个文件。

这种写入-回放机制的优势在于它可以减少磁盘写入的次数，提高了写操作的性能和并发性。只有在某些条件下（如WAL文件大小达到阈值），SQLite 才会执行一次称为checkpoint的操作，将修改应用到原始数据库文件中，并清空WAL文件。

因此，对于单条数据的插入操作，SQLite 通常只会涉及到WAL文件和相关的数据页，而不会导致整个数据库文件重新写入到磁盘。这对于大型数据库文件而言是一种性能优化，因为它减少了磁盘写入的开销。

然而，如果数据库文件非常大，可能会导致WAL文件增长到较大的大小，并且在checkpoint时需要较长的时间来将修改应用到原始数据库文件中。这可能会对性能产生一定的影响。在这种情况下，可以考虑调整WAL模式的参数、定期执行checkpoint操作或者使用其他的优化策略来减轻性能问题。

总之，SQLite 的写入-回放机制可以有效地处理数据的插入操作，避免了整个文件的重写，但在处理大型数据库文件时，仍需要注意性能方面的考虑。



## 这种机制的工作原理是什么？是往后面的磁盘位置写入修改的数据吗

SQLite 的写入-回放（WAL）机制的工作原理如下：

1. 数据插入：当进行数据插入操作时，SQLite 将新数据追加到一个称为WAL文件（Write-Ahead Log）的日志文件中，而不是直接修改原始数据库文件。这个日志文件记录了对数据库进行的修改操作。

2. 数据页修改：同时，SQLite 会将这些修改操作应用到原始数据库文件的副本中，生成一个新的数据库文件。这个过程通常涉及到被修改的数据页和相关的索引页。SQLite 使用页级别的锁定机制来保证并发修改的正确性。

3. 回放操作：在读取数据库时，SQLite 首先检查WAL文件，然后将WAL文件中的修改操作应用到原始数据库文件中，生成一个最新的视图。这个过程称为回放（replay），它只会涉及到被修改的数据页和相关的索引页，而不会重新写入整个文件。

4. Checkpoint：WAL文件会一直增长，直到达到一定大小或满足一些特定条件。在某些情况下，SQLite 会执行一次称为checkpoint的操作。checkpoint 将修改应用到原始数据库文件中，并清空WAL文件，以便重用。

关于数据的存储位置，具体实现可能会有所不同，但一般情况下，WAL文件会被存储在与数据库文件相同的目录中。原始数据库文件和WAL文件是分开存储的，它们所在的磁盘位置可能是相邻的，但不是完全相同的位置。

通过将修改操作记录在WAL文件中，并在后续读取时应用这些修改，SQLite 实现了一种高效的写入-回放机制，以提高写操作的性能和并发性。这种机制避免了频繁地重写整个数据库文件，减少了磁盘写入的次数，从而提高了性能和数据的一致性。

## wal文件在哪里？平时只能看到一个sqlite的文件。

在 SQLite 中，默认情况下，WAL文件与数据库文件存储在同一个目录下，并使用与数据库文件相同的名称，但扩展名为`.wal`。

例如，如果你的数据库文件名为`mydatabase.db`，那么对应的WAL文件将会是`mydatabase.db-wal`。这个WAL文件是用于记录写入-回放日志的文件。

在平时的文件浏览器或命令行界面中，你可能只能看到一个单独的SQLite数据库文件，即`mydatabase.db`。WAL文件通常是隐藏的，不会直接显示在文件列表中。

要查看WAL文件，你可以尝试在文件浏览器中启用显示隐藏文件和文件扩展名选项。或者，你可以使用命令行工具（如`ls`、`dir`等）来列出目录中的所有文件，包括隐藏文件。

需要注意的是，WAL文件是临时文件，用于记录写入-回放日志。在SQLite的正常操作中，WAL文件会不断增长并在checkpoint操作后被清空。因此，WAL文件的大小通常不会太大，除非在特殊情况下（如长时间运行未执行checkpoint），它可能会增长到较大的大小。

如果你希望关闭WAL模式，可以在连接到SQLite数据库时使用PRAGMA语句执行如下操作：

```sql
PRAGMA journal_mode = DELETE;
```

这将禁用WAL模式，并将SQLite切换回传统的回滚日志模式。在这种模式下，SQLite会直接修改原始数据库文件，而不使用WAL文件。



# sqlite C语言编程示例

以下是一个简单的SQLite C语言编程示例，演示了如何创建一个数据库、创建一个表格、插入数据、查询数据，并关闭数据库连接。

```c
#include <stdio.h>
#include <sqlite3.h>

int main() {
    sqlite3 *db;
    char *err_msg = 0;

    // 打开数据库连接
    int rc = sqlite3_open("test.db", &db);
    if (rc) {
        fprintf(stderr, "无法打开数据库: %s\n", sqlite3_errmsg(db));
        return 1;
    } else {
        fprintf(stdout, "成功打开数据库\n");
    }

    // 创建表格
    const char *sql_create_table = "CREATE TABLE IF NOT EXISTS test_table ("
                                   "id INTEGER PRIMARY KEY AUTOINCREMENT,"
                                   "name TEXT NOT NULL,"
                                   "age INT NOT NULL);";

    rc = sqlite3_exec(db, sql_create_table, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "无法创建表格: %s\n", err_msg);
        sqlite3_free(err_msg);
    } else {
        fprintf(stdout, "成功创建表格\n");
    }

    // 插入数据
    const char *sql_insert_data = "INSERT INTO test_table (name, age) VALUES ('Alice', 30), ('Bob', 25);";

    rc = sqlite3_exec(db, sql_insert_data, 0, 0, &err_msg);
    if (rc != SQLITE_OK) {
        fprintf(stderr, "插入数据失败: %s\n", err_msg);
        sqlite3_free(err_msg);
    } else {
        fprintf(stdout, "成功插入数据\n");
    }

    // 查询数据
    const char *sql_select_data = "SELECT * FROM test_table;";
    sqlite3_stmt *stmt;

    rc = sqlite3_prepare_v2(db, sql_select_data, -1, &stmt, 0);
    if (rc == SQLITE_OK) {
        while (sqlite3_step(stmt) == SQLITE_ROW) {
            int id = sqlite3_column_int(stmt, 0);
            const unsigned char *name = sqlite3_column_text(stmt, 1);
            int age = sqlite3_column_int(stmt, 2);
            printf("ID: %d, Name: %s, Age: %d\n", id, name, age);
        }
        sqlite3_finalize(stmt);
    } else {
        fprintf(stderr, "查询数据失败: %s\n", sqlite3_errmsg(db));
    }

    // 关闭数据库连接
    sqlite3_close(db);

    return 0;
}
```

在这个示例中，我们首先打开一个名为"test.db"的数据库连接，然后创建一个名为"test_table"的表格，表格包含id、name和age字段。接着插入两条数据，然后查询并输出所有数据。最后关闭数据库连接。

# sqlite python编程示例

以下是一个简单的SQLite Python编程示例，演示了如何创建一个数据库、创建一个表格、插入数据、查询数据，并关闭数据库连接。

```python
import sqlite3

# 连接到数据库（如果不存在则创建）
conn = sqlite3.connect('test.db')

# 创建游标对象
cur = conn.cursor()

# 创建表格
cur.execute('''CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INT NOT NULL)''')

# 插入数据
cur.execute("INSERT INTO test_table (name, age) VALUES (?, ?)", ('Alice', 30))
cur.execute("INSERT INTO test_table (name, age) VALUES (?, ?)", ('Bob', 25))

# 提交事务
conn.commit()

# 查询数据
cur.execute("SELECT * FROM test_table")
rows = cur.fetchall()
for row in rows:
    print("ID:", row[0], "Name:", row[1], "Age:", row[2])

# 关闭游标和连接
cur.close()
conn.close()
```

在这个示例中，我们首先使用`sqlite3.connect()`函数连接到一个名为"test.db"的数据库，如果数据库不存在，则会自动创建一个新的数据库文件。然后我们使用`cursor()`方法创建一个游标对象，通过游标对象执行SQL语句来操作数据库。

我们创建一个名为"test_table"的表格，表格包含id、name和age字段。接着我们插入两条数据，然后使用`fetchall()`方法查询所有数据，并遍历打印每一条数据。

最后，我们使用`close()`方法关闭游标对象和数据库连接。

# 用sqlite和flask写一个简单的blog系统

下面是一个简单的用SQLite和Flask写的博客系统的示例代码：

```python
from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# 设置数据库文件路径
DATABASE = 'blog.db'

# 创建表格
def create_table():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS posts (
                   id INTEGER PRIMARY KEY AUTOINCREMENT,
                   title TEXT NOT NULL,
                   content TEXT NOT NULL)''')
    conn.commit()
    conn.close()

# 添加博客文章
def add_post(title, content):
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)", (title, content))
    conn.commit()
    conn.close()

# 获取所有博客文章
def get_posts():
    conn = sqlite3.connect(DATABASE)
    cur = conn.cursor()
    cur.execute("SELECT * FROM posts ORDER BY id DESC")
    posts = cur.fetchall()
    conn.close()
    return posts

# 主页路由
@app.route('/')
def index():
    posts = get_posts()
    return render_template('index.html', posts=posts)

# 添加博客文章路由
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        add_post(title, content)
        return redirect(url_for('index'))
    return render_template('add.html')

if __name__ == '__main__':
    create_table()
    app.run(debug=True)
```

在这个示例中，我们使用了Flask框架来创建一个简单的博客系统。首先，我们定义了一个`create_table()`函数来创建名为`posts`的表格，该表格用于存储博客文章的标题和内容。然后，我们定义了`add_post()`函数来添加新的博客文章，以及`get_posts()`函数来获取所有博客文章。接着，我们定义了两个路由，`index()`用于显示所有博客文章，`add()`用于添加新的博客文章。最后，我们在`if __name__ == '__main__':`语句中调用`create_table()`函数来创建表格，并启动Flask应用。



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