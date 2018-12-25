---
title: sqlite之数据类型
date: 2018-12-25 15:04:55
tags:
	- 数据库

---



数据库的数据类型，我一直没有理清楚。现在就把sqlite的都理一遍。

sqlite使用了动态类型系统。

值的数据类型跟跟值本身是相关的，而不是跟它的容器相关。



sqlite存储类

1、null。

2、integer。一个带符号整数，根据值的大小，可能占用1、2、3、4、6、8个字节。

3、real。浮点数，8个字节。

4、text。字符串。使用utf-8编码。

5、blob。根据输入进行存储。



sqlite亲和类型Affinity

1、text。

2、numeric。

3、integer。

4、real。

5、none。



亲和类型integer

1、int。

2、integer。

3、tinyint。

4、smallint。

5、mediumint。

6、bigint。

7、unsigned big int

8、int2

9、int8

亲和类型text

1、character(20)

2、varchar(255)

3、varying character(255)

4、nchar(55)

5、native character(70)

6、nvarchar(100)

7、text

8、clob。

亲和类型none

1、blob。

2、no datatype specified。

亲和类型real

1、real。

2、double。

3、double precious。

4、float。

亲和类型numeric

1、numeric。

2、decimal(10，5)

3、boolean。

4、date。

5、datetime。



参考资料

1、SQLite 数据类型

http://www.runoob.com/sqlite/sqlite-data-types.html