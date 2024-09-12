---
title: sql练习
date: 2023-01-20 11:05:31
tags:
	- 数据库

---



sql 50道题目练习。这个还可以，其余的资料都是很偏国外的，数据理解起来不方便。

这个是以学校的数据举例，比较贴近中国人的现实生活，理解起来也比较方便。

本来是基于mysql的，我不照抄吧，在sqlite上来练习。

https://zhuanlan.zhihu.com/p/32137597?utm_id=0

这个是对应的markdown文件，看起来排版更好。

https://note.youdao.com/ynoteshare/index.html?id=45d4298f42397bd52ccf6fc716e27ee9&type=note&_time=1674184231260#/

peewee这个ORM的作者有个sqlite-web的程序，跑起来看看是个什么效果。

https://github.com/coleifer/sqlite-web

安装

```
pip3 install  -U sqlite-web
```

启动

```
sqlite_web ./test.db -H 0.0.0.0 -p 1200
```

别说，还挺好用的。

我看看能不能用pywebio来复刻一个。

很容易发现一个bug。就是table里当前只有一个id，你不能把这个id直接删掉，而要另外先新建一个field，然后才能把id这个删掉。

# 环境准备

总共4个table

```
Student
Course
Teacher
SC 成绩
```

用sqlite_web来创建table。

算了。还是用sql语句来创建，并插入初始化的数据。

总共4张表，学生、老师，科目、成绩。

总共3个老师。

12个学生，前面7个编号是连着的，他们有成绩，后面5个的没有成绩。

而在前面7个学生里，前面4个修满了3门课程，而后面3个都各自缺了一门课程。

08号是空缺的。



## setup.sql

为了方便各个数据库的测试，我把所有的字母都转成了小写的。

```
drop table if exists student;
drop table if exists teacher;
drop table if exists course;
drop table if exists sc;

create table student(
    sid varchar(10) primary key,
    sname varchar(10),
    sage datetime,
    ssex varchar(10)
);

insert into student values('01' , '赵雷' , '1990-01-01' , '男');
insert into student values('02' , '钱电' , '1990-12-21' , '男');
insert into student values('03' , '孙风' , '1990-05-20' , '男');
insert into student values('04' , '李云' , '1990-08-06' , '男');
insert into student values('05' , '周梅' , '1991-12-01' , '女');
insert into student values('06' , '吴兰' , '1992-03-01' , '女');
insert into student values('07' , '郑竹' , '1989-07-01' , '女');
insert into student values('09' , '张三' , '2017-12-20' , '女');
insert into student values('10' , '李四' , '2017-12-25' , '女');
insert into student values('11' , '李四' , '2017-12-30' , '女');
insert into student values('12' , '赵六' , '2017-01-01' , '女');
insert into student values('13' , '孙七' , '2018-01-01' , '女');

create table course(
    cid varchar(10),
    cname varchar(10),
    tid varchar(10)
);

insert into course values('01', '语文', '02');
insert into course values('02', '数学', '01');
insert into course values('03', '英语', '03');

create table teacher(
    tid varchar(10),
    tname varchar(10)
);

insert into teacher values('01', '张三');
insert into teacher values('02', '李四');
insert into teacher values('03', '王五');


create table sc(
    sid varchar(10),
    cid varchar(10),
    score decimal(18,1)
);

insert into sc values('01' , '01' , 80);
insert into sc values('01' , '02' , 90);
insert into sc values('01' , '03' , 99);
insert into sc values('02' , '01' , 70);
insert into sc values('02' , '02' , 60);
insert into sc values('02' , '03' , 80);
insert into sc values('03' , '01' , 80);
insert into sc values('03' , '02' , 80);
insert into sc values('03' , '03' , 80);
insert into sc values('04' , '01' , 50);
insert into sc values('04' , '02' , 30);
insert into sc values('04' , '03' , 20);
insert into sc values('05' , '01' , 76);
insert into sc values('05' , '02' , 87);
insert into sc values('06' , '01' , 31);
insert into sc values('06' , '03' , 34);
insert into sc values('07' , '02' , 89);
insert into sc values('07' , '03' , 98);
```

decimal(10,6)，表示数值中共有10位数，其中整数占4位，小数占6位。

# 题目

我把代码都放在这里了。

https://gitee.com/teddyxiong53/sql-practice

按题目依次编号为01.sql、02.sql这样。

做其他操作之前，要先进入到sqlite的命令行：

```
sqlite3 ./test.db

> .read setup.sql
# 执行后面的查询文件
> .read 01.sql
```



下面都使用https://liaoxuefeng.com/books/sql/sql-online/index.html 这个在线sql环境来进行。

```
13个学生

3门课程

3个老师

一个成绩表格
只有前面7个学生的成绩。
1到4号是有3门课的成绩。
5号：只有1和2课程的成绩。
6号：只有1和3的成绩。
7号：只有2和3的成绩。
```



## 查询01课程比02课程成绩高的学习的信息以及课程分数

```
select *
from (select sid, score from sc where sc.cid = '01') as t1,
(select sid, score from sc where sc.cid = '02') as t2
where t1.sid = t2.sid
and t1.score > t2.score ;
```

### 查询同时有01课程和02课程的学生的情况

```
select *
from (select sid, score from sc where sc.cid = '01') as t1,
(select sid, score from sc where sc.cid = '02') as t2 
where t1.sid = t2.sid;
```

### 查询有01课程但是可能没有02课程的学生的情况

```
select *
from (select sid, score from sc where sc.cid='01') as t1 
left join
(select sid, score from sc where sc.cid='02') as t2 
on t1.sid=t2.sid;

```

### 查询没有01课程但是有02课程的学生

```
select * from sc 
where sc.cid not in 
(select sid from sc where sc.cid = '01')
and sc.cid = '02';
```



## 平均成绩>=60分的学生的id、name和平均score

```
select student.*, t1.avgscore
from student inner join (
    select sc.sid, avg(sc.score) as avgscore from sc 
    group by sc.sid
    having avg(sc.score)>=60
) as t1 on student.sid = t1.sid;
```

## 查询在sc表格里有成绩的学生的信息

```
select distinct student.* from student,sc 
where student.sid = sc.sid;
```

## 查询所有同学的学生编号、学生姓名、选课总数、所有课程的总成绩(没成绩的显示为null)

```
select student.sid, student.sname, t1.sumscore, t1.coursecount
from student, (
    select sc.sid, sum(sc.score) as sumscore, count(sc.cid) as coursecount
    from sc 
    group by sc.sid 
) as t1 
where student.sid = t1.sid;
```

##  查有成绩的学生信息

```
select * from student
where exists(
    select * from sc where student.sid = sc.sid
);

```

## 查询「李」姓老师的数量

```
select count(*) from teacher
where teacher.tname like '李%';
```

## 查询学过「张三」老师授课的同学的信息

```
select student.*
from teacher, course, student, sc 
where teacher.tname = '张三'
and teacher.tid = course.tid 
and course.cid = sc.cid 
and sc.sid = student.sid;
```

## 查询没有学全所有课程的同学的信息

### 方法1

```
select student.*
from sc, student
where sc.sid = student.sid 
group by sc.sid
having count(*) < (select count(*) from course);

```

这个方法会有个问题，就是没法查询到什么课程都没有学的学生。

### 方法2

使用笛卡尔积的方法。

```
select distinct student.*
from 
(select student.sid, course.cid from student, course) as t1
left join
(select sc.sid, sc.cid from sc) as t2 
on t1.sid=t2.sid and t1.cid=t2.cid,student 
where t2.sid is null 
and t1.sid=student.sid ;
```

这个在在线环境里跑起来会出错。

## 查询至少有一门课跟01学生所学相同的学生信息

```
select distinct student.*
from sc, student
where sc.cid in 
(select cid from sc where sc.sid='01')
and sc.sid = student.sid;

```

这里的distinct是必须要的。

不然就会有很多重复的。



# 找一个在线的sql练习环境

https://liaoxuefeng.com/books/sql/sql-online/index.html

https://liaoxuefeng.com/books/sql/rdbms/index.html

# 数据分析师使用sql的场景举例，给出sql语句例子

数据分析师使用 SQL 的场景非常多样，以下是一些常见的场景及对应的 SQL 语句示例：

### 1. 提取特定数据
**场景**：从用户表中提取所有活跃用户的信息。
```sql
SELECT *
FROM users
WHERE status = 'active';
```

### 2. 聚合数据
**场景**：计算每个产品的销售总额。
```sql
SELECT product_id, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY product_id;
```

### 3. 数据连接
**场景**：获取用户及其对应订单的详细信息。
```sql
SELECT u.user_id, u.name, o.order_id, o.order_date
FROM users u
JOIN orders o ON u.user_id = o.user_id;
```

### 4. 计算增长率
**场景**：计算某产品在过去一年的销售增长率。

```sql
SELECT 
    (SUM(CASE WHEN order_date >= '2023-01-01' THEN sales_amount ELSE 0 END) -
     SUM(CASE WHEN order_date < '2023-01-01' THEN sales_amount ELSE 0 END)) /
    SUM(CASE WHEN order_date < '2023-01-01' THEN sales_amount ELSE 1 END) * 100 AS sales_growth_rate
FROM sales;
```

### 5. 数据筛选和排序
**场景**：找到销售额最高的前10个产品。
```sql
SELECT product_id, SUM(sales_amount) AS total_sales
FROM sales
GROUP BY product_id
ORDER BY total_sales DESC
LIMIT 10;
```

### 6. 查找重复数据
**场景**：查找重复的用户邮箱。
```sql
SELECT email, COUNT(*) AS count
FROM users
GROUP BY email
HAVING COUNT(*) > 1;
```

### 7. 时间序列分析
**场景**：按月统计用户注册数量。
```sql
SELECT DATE_TRUNC('month', registration_date) AS month, COUNT(*) AS user_count
FROM users
GROUP BY month
ORDER BY month;
```

### 总结
这些示例展示了数据分析师在日常工作中如何利用 SQL 来提取、聚合和分析数据。熟练掌握这些查询可以帮助分析师从数据中获得有价值的洞察。

# 如何使用SQL进行数据清洗？

使用 SQL 进行数据清洗是数据分析过程中的重要步骤，以下是一些常用的方法和示例：

### 1. 删除重复数据
**场景**：查找并删除重复的记录。
```sql
DELETE FROM table_name
WHERE id NOT IN (
    SELECT MIN(id)
    FROM table_name
    GROUP BY column1, column2
);
```

### 2. 处理缺失值
**场景**：查找缺失值并替换为默认值。

```sql
UPDATE table_name
SET column_name = 'default_value'
WHERE column_name IS NULL;
```

### 3. 标准化数据格式
**场景**：将日期格式统一为 `YYYY-MM-DD`。
```sql
UPDATE table_name
SET date_column = TO_DATE(date_column, 'MM/DD/YYYY')
WHERE date_column IS NOT NULL;
```

### 4. 修剪多余空格
**场景**：去除字符串字段的前后空格。
```sql
UPDATE table_name
SET column_name = TRIM(column_name);
```

### 5. 数据类型转换
**场景**：将字符串类型的数字转换为整数。
```sql
UPDATE table_name
SET numeric_column = CAST(string_column AS INTEGER)
WHERE string_column IS NOT NULL AND string_column <> '';
```

### 6. 过滤异常值
**场景**：删除不合逻辑的记录，例如负数销售额。
```sql
DELETE FROM sales
WHERE sales_amount < 0;
```

### 7. 合并相似记录
**场景**：将相似的记录合并，例如不同拼写的同一产品。
```sql
UPDATE products
SET product_name = 'Standard Product Name'
WHERE product_name IN ('Prod1', 'prod1', 'Prod_1');
```

### 8. 创建清洗后的新表
**场景**：将清洗后的数据存入新表。
```sql
CREATE TABLE cleaned_data AS
SELECT DISTINCT *
FROM original_data
WHERE column_name IS NOT NULL;
```

### 总结
使用 SQL 进行数据清洗可以帮助确保数据的准确性和一致性。通过上述方法，可以有效地处理重复数据、缺失值、格式标准化等问题，为后续的数据分析打下良好的基础。



# 几千行的sql查询语句是怎么样的？

几千行的 SQL 查询语句通常是为了处理复杂的数据分析、报表生成或数据迁移等任务。这类查询可能包含多个子查询、联接、聚合、排序和条件筛选等。以下是一个简化的示例，展示一个复杂查询的结构，但具体内容可能会根据实际数据库设计和需求有所不同。

### 示例：复杂 SQL 查询

```sql
WITH EmployeeSales AS (
    SELECT 
        e.employee_id,
        e.name,
        d.department_name,
        SUM(s.sales_amount) AS total_sales
    FROM 
        employees e
    JOIN 
        departments d ON e.department_id = d.department_id
    JOIN 
        sales s ON e.employee_id = s.employee_id
    WHERE 
        s.sale_date BETWEEN '2023-01-01' AND '2023-12-31'
    GROUP BY 
        e.employee_id, e.name, d.department_name
),
TopSales AS (
    SELECT 
        employee_id,
        name,
        department_name,
        total_sales,
        RANK() OVER (PARTITION BY department_name ORDER BY total_sales DESC) AS sales_rank
    FROM 
        EmployeeSales
)
SELECT 
    ts.name,
    ts.department_name,
    ts.total_sales
FROM 
    TopSales ts
WHERE 
    ts.sales_rank <= 5
ORDER BY 
    ts.department_name, ts.sales_rank;
```

### 解释

1. **CTE (Common Table Expressions)**：
   - `EmployeeSales` CTE：计算每位员工在特定时间段内的总销售额。
   - `TopSales` CTE：为每个部门的销售额进行排名。

2. **联接**：
   - 将 `employees`、`departments` 和 `sales` 表连接，以获取所需的信息。

3. **聚合和分组**：
   - 使用 `SUM` 和 `GROUP BY` 计算每位员工的总销售额。

4. **窗口函数**：
   - 使用 `RANK()` 为每个部门的员工按销售额排序。

5. **最终选择**：
   - 从 `TopSales` 中选择前五名销售员工并按部门和排名排序。

### 复杂查询的特点

- **结构清晰**：使用 CTE 可以使查询结构更清晰，易于理解。
- **性能考虑**：复杂查询可能涉及多个表和大量数据，需注意性能优化。
- **可维护性**：长查询应保持可读性，可以通过分解成多个部分（如 CTE 或子查询）来提高可维护性。

### 总结

几千行的 SQL 查询通常应用于复杂的数据处理任务，结构化的方式（如使用 CTE 和分解查询）能够提高可读性和维护性。具体的查询会因业务需求而异，可能会涉及更复杂的逻辑和条件。



# 参数化查询为什么可以避免sql注入

参数化查询能够有效避免 SQL 注入的原因主要有以下几点：

### 1. **分离数据与代码**
- 参数化查询将 SQL 代码与用户输入的数据分开处理。在执行查询时，SQL 代码已经被数据库解析，用户输入的数据仅作为参数传递。这种分离确保了输入不会被当作 SQL 代码执行。

### 2. **预编译语句**
- 在参数化查询中，SQL 语句首先被编译，然后再将参数传递给预编译的语句。这意味着数据库在执行时已经知道了 SQL 语句的结构，不会受到输入内容的影响。

### 3. **输入转义**
- 参数化查询会自动对用户输入进行适当的转义，确保特殊字符（如单引号、分号等）不会被解释为 SQL 代码的一部分。这使得恶意输入无法改变原本的查询逻辑。

### 4. **防止恶意输入**
- 通过参数化查询，即使用户输入恶意 SQL 代码，数据库也只会将其视为数据，而不是可执行的 SQL 语句。例如，输入 `"1 OR 1=1"` 不会影响查询的逻辑，而只是作为一个参数值。

### 示例

假设有一个 SQL 查询如下：

```sql
SELECT * FROM users WHERE id = 'user_input';
```

如果 `user_input` 是用户提供的输入，攻击者可能输入 `1 OR 1=1`，导致查询变为：

```sql
SELECT * FROM users WHERE id = '1 OR 1=1';
```

这样就可以绕过身份验证，获取所有用户的数据。

使用参数化查询后，代码将变为：

```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_input,))
```

在这种情况下，`user_input` 的内容会作为参数处理，数据库将其视为普通数据，而不作为 SQL 代码执行。

### 总结

通过分离 SQL 代码与用户输入、预编译语句以及自动转义，参数化查询有效地防止了 SQL 注入攻击，确保了数据库操作的安全性。



```
# 使用 Python 的 sqlite3 示例
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

# 参数化查询
user_id = 1
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```



# 参考资料

1、

