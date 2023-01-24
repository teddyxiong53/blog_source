---
title: sql的各种join理解
date: 2023-01-20 14:19:31
tags:
	- 数据库

---



sql join子句可以2个或者多个table的row连接起来。

基于这些table的共同的column。

最简单最常见的join是 inner join。

inner join是从多个table返回所有满足条件的row。

举个例子是这样：

```
select teacher.id, teacher.name, teacher.age
from teacher
join student on student.teacher_id=teacher.id;
```

先了解一下这4种join的基本概念

```
inner join
	如果table里有至少一个match，则返回row
left join
	即使right table没有一个匹配的，也把left table的所有行返回。
right join
	跟left join刚好相反。
full join
	只要其中一个table存在match，则返回行。
```



参考资料

1、

https://www.runoob.com/sql/sql-join.html