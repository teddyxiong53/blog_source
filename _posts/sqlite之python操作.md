---
title: sqlite之python操作
date: 2018-12-25 14:18:55
tags:
	- 数据库

---



看看python如何操作sqlite。

```
import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()
cursor.execute("drop table if exists user ")
cursor.execute("create table user (id varchar(20) primary key, name varchar(20))")
cursor.execute("insert into user (id, name) values (\'1\', \'allen\')")
print cursor.rowcount
cursor.close()
conn.commit()

conn.close()
```

