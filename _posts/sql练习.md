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

```

drop table if exists Student;
drop table if exists Teacher;
drop table if exists Course;
drop table if exists SC;

create table Student(
    SId varchar(10) primary key,
    Sname varchar(10),
    Sage datetime,
    Ssex varchar(10)
);

insert into Student values('01' , '赵雷' , '1990-01-01' , '男');
insert into Student values('02' , '钱电' , '1990-12-21' , '男');
insert into Student values('03' , '孙风' , '1990-05-20' , '男');
insert into Student values('04' , '李云' , '1990-08-06' , '男');
insert into Student values('05' , '周梅' , '1991-12-01' , '女');
insert into Student values('06' , '吴兰' , '1992-03-01' , '女');
insert into Student values('07' , '郑竹' , '1989-07-01' , '女');
insert into Student values('09' , '张三' , '2017-12-20' , '女');
insert into Student values('10' , '李四' , '2017-12-25' , '女');
insert into Student values('11' , '李四' , '2017-12-30' , '女');
insert into Student values('12' , '赵六' , '2017-01-01' , '女');
insert into Student values('13' , '孙七' , '2018-01-01' , '女');

create table Course(
    CId varchar(10),
    Cname varchar(10),
    TId varchar(10)
);

insert into Course values('01', '语文', '02');
insert into Course values('02', '数学', '01');
insert into Course values('03', '英语', '03');

create table Teacher(
    TId varchar(10),
    Tname varchar(10)
);

insert into Teacher values('01', '张三');
insert into Teacher values('02', '李四');
insert into Teacher values('03', '王五');


create table SC(
    SId varchar(10),
    CId varchar(10),
    score decimal(18,1)
);

insert into SC values('01' , '01' , 80);
insert into SC values('01' , '02' , 90);
insert into SC values('01' , '03' , 99);
insert into SC values('02' , '01' , 70);
insert into SC values('02' , '02' , 60);
insert into SC values('02' , '03' , 80);
insert into SC values('03' , '01' , 80);
insert into SC values('03' , '02' , 80);
insert into SC values('03' , '03' , 80);
insert into SC values('04' , '01' , 50);
insert into SC values('04' , '02' , 30);
insert into SC values('04' , '03' , 20);
insert into SC values('05' , '01' , 76);
insert into SC values('05' , '02' , 87);
insert into SC values('06' , '01' , 31);
insert into SC values('06' , '03' , 34);
insert into SC values('07' , '02' , 89);
insert into SC values('07' , '03' , 98);
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



## 查询01课程比02课程成绩高的学习的信息以及课程分数

看第一题，就发现sqlite跟mysql不同的地方。

sqlite创建的table名字跟sql语句里是一样的。所以是有大写的。

而mysql的table名字是全部小写了。

所以为了方便参考答案，我看看能不能给table设置一个alias。

看这个，sqlite有alias机制，但是都是临时的。

https://www.runoob.com/sqlite/sqlite-alias.html

所以，我还是把sql里的table名字改成小写的吧。

```

```



# 参考资料

1、

