基本操作如下所示：

```
# -*- coding:utf-8 -*-
import MySQLdb

try:
	conn = MySQLdb.connect(host='localhost', user='root', passwd='XXXX', port=3306, charset='utf8')
	#创建游标
	cur = conn.cursor()
	#先删掉，方便反复运行测试。
	cur.execute('drop database  if exists testpydb')
	#创建数据库
	cur.execute('create database if not exists testpydb')
	#切换到数据库
	conn.select_db('testpydb')
	#创建表
	cur.execute('create table student(id int, name varchar(20), age int)')
	#插入单条数据
	cur.execute('insert into student value(1,"Allen",20)')
	#插入多条数据
	cur.execute('insert into student values (2, "Bob",20),(3, "Carl",21),(4,"David",22)')
	#更新数据
	cur.execute('update student set age=23 where name="Allen" ')
	#删除数据
	cur.execute('delete from student where name="Carl" ')
	#查找数据
	count = cur.execute('select * from student')
	print "总数是:" 
	print count
	result = cur.fetchone()
	print "查找一条:"
	print result 
	#这个条数给多了没关系。不会报错。
	results = cur.fetchmany(5)
	print "查找多条"
	for r in results:
		print r
	
	#关闭游标
	cur.close()
	#提交
	conn.commit()
	#断开数据库连接
	conn.close()
	
except MySQLdb.Error, e:
	print "MySQLdb error %d:%s" %(e.args[0], e.args[1])
	
```

