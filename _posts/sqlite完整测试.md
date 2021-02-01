---
title: sqlite完整测试
date: 2018-12-25 21:08:17
tags:
	- 数据库

---



写一个test.sql文件。内容如下：

```
create table company(
	id int primary key not null,
	name text not null,
	age int not null,
	address char(50),
	salary real
);

create table department (
	id int primary key not null,
	dept char(50) not null,
	emp_id int not null
);
```

生成数据库文件。

````
sqlite3 test.db < test.sql
````

查看数据库。

```
teddy@teddy-ubuntu:~/work/test/sqlite$ sqlite3 test.db 
SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .databases
seq  name             file                                                      
---  ---------------  ----------------------------------------------------------
0    main             /home/teddy/work/test/sqlite/test.db                      
sqlite> .tables
company     department
```

查看表结构。

```
sqlite> .schema company
CREATE TABLE company(
        id int primary key not null,
        name text not null,
        age int not null,
        address char(50),
        salary real
);
```

删除表。

```
drop table company
```

重新建立数据库文件。

修改test.sql内容如下：

```
drop table if exists company;
drop table if exists department;


create table company(
	id int primary key not null,
	name text not null,
	age int not null,
	address char(50),
	salary real
);

create table department (
	id int primary key not null,
	dept char(50) not null,
	emp_id int not null
);

insert into company (id, name, age, address, salary)
values (1, "aaa", 21, "a city", 100);

insert into company (id ,name, age, address, salary)
values (2, "bbb", 22, "b city", 200);

insert into company (id, name, age, address, salary)
values (3, "ccc", 23, "c city", 300);

insert into company (id, name, age, address, salary)
values (4, "ddd", 24, "d city", 400);

insert into company (id ,name, age, address, salary)
values (5, "eee", 25, "e city", 500);

insert into company (id, name, age, address, salary)
values (6, "fff", 26, "f city", 600);
```

现在我们已经准备了基本数据，下面对这些数据进行操作。

# select操作

```
sqlite> .header on
sqlite> .mode column
sqlite> select * from company;
id          name        age         address     salary    
----------  ----------  ----------  ----------  ----------
1           aaa         21          a city      100.0     
2           bbb         22          b city      200.0     
3           ccc         23          c city      300.0     
4           ddd         24          d city      400.0     
5           eee         25          e city      500.0     
6           fff         26          f city      600.0  
```

只读取部分属性。

```
select name, age from company;
```

## where 子句

选取年龄大于22岁且工资大于300的。

```
select * from company where age >= 22 and salary >= 300;
```

选取名字里含有a的。

```
select * from company where name like "a%";
下面也可以。
select * from company where name like "a*"; 
```

选取年龄是22或者24之间的。

```
select * from company where age in (22,24);
```

选取年龄不是22且不是24的。

````
select * from company where age not in(22, 24);
````

选取年龄在22到24之间的。

```
select * from company where age between 22 and 24;
```

## 子查询

```
select * from company where age > (select age from company where salary > 400);
```

# update 操作

把6号员工的工资加到650 。

```
update company set salary = 650 where id = 6;
```



# delete操作

把6号员工删掉。

```
delete from company where id = 6;
```

# like子句

有2个通配符。

%：表示0个、1个或者多个字符。

下划线：一个字符。

例子：

```
where salary like "200%" 以200开头的任意值。
"%200%" 里面有200的任意值。
"_00%" 第二位和第三位为0的。
```

# GLOB子句

GLOB必须大写。是大小写敏感的。

通配符有2个：

星号：

问号：

跟我们一般用的是一个意思。



# limit子句

从偏移2的位置，读取2条。

```
 select * from company limit 2 offset 2;
```



# order子句

按工资降序排列。

```
select * from company order by salary desc;
```

可以同时按多个属性进行排序。

```
select * from company order by salary,name desc;
```



# group by

对数据进行分组。

group by在where之后，在order by之前。



# having子句

位置是这样的：

```
SELECT
FROM
WHERE
GROUP BY
HAVING
ORDER BY
```



# distinct关键字

用来消除相同项目。

```
select distinct name from company;
```



# 约束

约束是在数据列上强制执行的规则。

常用的约束有：

```
not null
default
unique
primary key
check
```



# join子句

join子句用来连接多个数据库里的记录。

join是通过共同值来结合2个表里的字段的手段。

sql定义了三种主要的连接：

1、交叉连接。

2、内连接。

3、外连接。

现在我们把department的表里填入数据。

```
insert into department values (1, "RD", 1);
insert into department values (2, "MKT", 2);
insert into department values (3, "FINANCE", 3);
```

3个部门，当前1号、2号、3号员工指定到这3个部门。

## 交叉连接

```
sqlite> select emp_id, name, dept from company cross join department;
emp_id      name        dept      
----------  ----------  ----------
1           aaa         RD        
2           aaa         MKT       
3           aaa         FINANCE   
1           bbb         RD        
2           bbb         MKT       
3           bbb         FINANCE   
1           ccc         RD        
2           ccc         MKT       
3           ccc         FINANCE   
1           ddd         RD        
2           ddd         MKT       
3           ddd         FINANCE   
1           eee         RD        
2           eee         MKT       
3           eee         FINANCE   
1           fff         RD        
2           fff         MKT       
3           fff         FINANCE 
```

## 内连接

```
sqlite> select emp_id, name, dept from company inner join department on company.id=department.emp_id;
emp_id      name        dept      
----------  ----------  ----------
1           aaa         RD        
2           bbb         MKT       
3           ccc         FINANCE 
```

## 外连接

注意，outer join，前面要加left。

```
sqlite> select emp_id, name, dept from company outer join department on company.id =department.emp_id;
Error: RIGHT and FULL OUTER JOINs are not currently supported
sqlite> select emp_id, name, dept from company left outer join department on company.id =department.emp_id;
emp_id      name        dept      
----------  ----------  ----------
1           aaa         RD        
2           bbb         MKT       
3           ccc         FINANCE   
            ddd                   
            eee                   
            fff   
```

# unions子句

unions子句用来合并两个或者多个select语句的结果。

不反悔任何重复的行。

多个select的列数需要相同。

