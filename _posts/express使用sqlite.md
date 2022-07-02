---
title: express使用sqlite
date: 2021-01-25 10:23:11
tags:
	- express

---

--

https://www.npmjs.com/package/sqlite3

https://github.com/mapbox/node-sqlite3

https://github.com/mapbox/node-sqlite3/wiki/API

先看这里的官方示例。

# api

主要的api，可以分为3类

Main

Database

Statement

## Main

### sqlite3.Database

```
var db = new sqlite3.Database(filename[,mode][,callback])
```

filename可以的取值

```
':memory:'：这个表示使用内存里的数据库。
''：这个表示使用一个匿名的磁盘文件作为数据库。
'1.db'：这个表示使用1.db这个名字作为数据库。
```

mode的取值

```
sqlite3.OPEN_READONLY
sqlite3.OPEN_READWRITE
sqlite3.OPEN_CREATE
默认值是OPEN_READWRITE |OPEN_CREATE
```

callback

```
可选的，
如果提供了，那么会在数据库打开之后被调用。
有一个err参数，如果成功，err为null。
如果失败，err为错误信息。
```

### sqlite3.verbose()

把执行模式设置为verbose，

## Database

这些接口都是对象的方法。

### db.close([callback])

```
回调在关闭结束后调用。
关闭后，会发出一个名为'close'的event。
```

### db.configure

```
有3个选项。
2个函数
trace
profile
一个整数
busyTimeout
```

### db.run

```
db.run(sql[,param][,callback])
sql：sql语句。
param：如果sql语句里带有placeholder的时候，通过这里传递参数。
	参数有三种方式传递：
		直接一个个放。
		放到数组。
		放到对象里。这个看起来最直观，比较好。
		
callback
	可选。如果有。那么在执行过程中，任意一步出错的时候都会调用。
	在执行完成的时候也会被调用。
	回调函数的context是一个Statement对象。也就是说，在callback里的this是Statement对象。
	运行成功时，this里会有2个属性：lastID、changes。
	只有run方法会设置这2个属性。后面的db.get、db.all等方法都不会设置这2个属性。
```

举例

```
db.run('update tbl set name=? where id=?', 'bar', 2)
db.run('update tbl set name=? where id=?', ['bar', 2])

db.run('update tbl set name=$name where id=$id', {
	$id:2,
	$name:'bar'
})
```

### db.get

```
db.get(sql[,param][,callback])
参数跟db.run类似。
callback在第一个结果返回的时候执行。
callback是这样的：callback(err, row)
如果查询结果为空，那么row就是undefined。
否则row是一个对象。
key是数据库表的字段名。
value就是字段值。
```

### db.all

```
db.all(sql[,param][,callback])
跟db.get的不同在于：
callback是在所有查询执行完之后调用。
callback是这样：callback(err, rows)
rows是一个数组，数组的元素是一个个row对象。
```

### db.each

```
db.each(sql[,param][,callback][,complete])
这个意思很明显，就是每条查询都执行一次callback。
complete是在所有的执行之后再调用。
```

all和each的选择

因为all是一次性把数据读取出来，而each是一次次读取。

所以all要占用更多的内容。

这就有点python里迭代器的意思了。



### db.exec

```
db.exec(sql[,callback])
这个函数返回一个db对象本身。
用来做链式调用。

```

### db.prepare

```
db.prepare(sql,[param], [callback])
这个返回的就是一个Statement。

```



## Statement

```
stmt.bind([param...], [callback])
stmt.reset([callback])
stmt.finalize([callback])
stmt.run([param], [callback])
stmt.all([param],[callback])
stmt.each([param], [callback], [complete])

```

# 控制流

https://github.com/mapbox/node-sqlite3/wiki/Control-Flow

提供了2个函数用来做Statement的控制流。

默认是并行执行的。

db.run会等待所有的命令执行完再执行。

```
db.serialize([callback])
db.parallelize([callback])
```

# HelloWorld

新建test.js，里面写入下面的内容：

```
var sqlit3 = require('sqlite3').verbose()
var db = new sqlite3.Database('1.db', function(err) {
    if(err) {
        console.log('create db fail')
    } else {
        console.log('create db ok')
    }
})
db.serialize(function() {
    db.run('create table aaa (info text)')
    var stmt = db.prepare('insert into aaa values (?)')
    for(var i=0; i<10; i++) {
        stmt.run("bb " + i)
    }
    stmt.finalize()
    db.each('select rowid as id, info from aaa', function(err, row) {
        console.log(row.id + ':' + row.info)
    })
})
db.close()
```

上面代码做的事情：

在1.db这个数据库文件里，新建一个叫aaa的表格，表格只有一个字段，就是info（文本类型），先在里面插入10条数据，数据内容为bb 1这样的。

然后读取这个表的内容，并打印出来。

结果是这样：

```
create db ok
1:bb 0
2:bb 1
3:bb 2
4:bb 3
5:bb 4
6:bb 5
7:bb 6
8:bb 7
9:bb 8
10:bb 9
```



这样读取到的result是空的。为什么？

```
db.run('select * from oplog', (result, err)=> {
    console.log('result:' + result)
    console.log('err:' + err)
})
```



这样可以

```
var db = require('./db')
var sql = 'select * from oplog order by id desc'
db.all(sql, [], (err, rows) => {
    if(err) {
        throw err
    }
    rows.forEach((row)=> {
        console.log(row)
    })
})
```



# 完整项目



参考资料

https://www.computerhope.com/issues/ch002076.htm



# 路径问题

我之前是这样写的

```
var db = new sqlite3.Database('./database/db.sqlite');
```

这样使用的时候，出现对应的table找不到。

其实table是存在的。

这个是因为路径引用的问题，导致程序在其他路径去找db.sqlite文件。

而没有找到时，默认创建一个空的。所以空的文件里，当然我们要的表格，

这样来改写就好了。

```
var db = new sqlite3.Database(path.join(__dirname,'/db.sqlite'),
```





# 参考资料

1、

https://developerhowto.com/2018/12/29/build-a-rest-api-with-node-js-and-express-js/

2、

https://www.sqlitetutorial.net/sqlite-nodejs/query/