---
title: express使用mysql数据库
date: 2021-01-27 14:01:11
tags:
	- express

---

--

一般express都是用mongodb的比较多。

https://github.com/xiugangzhang/video.github.io

这个项目里是用的mysql。还比较全面，可以从这里学习一下mysql的实用用法。

以models/user.js为例进行分析。

没有用orm。数据库表格是靠sql文件执行来创建的。

我简化一下。

有一个单独的db.js，用来处理跟数据库的连接。

```
exports = module.exports = {
	function query(sql, p,c ) {
		//这个用来执行sql语句。
		//3个参数：
			参数1：sql语句。string类型。
			参数2：参数，可以没有。
			参数3：回调函数。
	}
}
```

这样创建一个数据库连接池

```
// 数据库配置
let config = {
    connectionLimit : 500,
    host : _config.host,
    database : _config.database,
    user : _config.user,
    password : _config.password
};

// 创建一个数据库连接池
let pool = mysql.createPool(config)
```

从连接池里拿出一个连接进行查询操作。

```
// 从数据库连接池中取出可以使用的链接
    pool.getConnection(function (err, connection) {
        connection.query(sql, params, function (err, rows) {
            // 使用完毕放回去连接池中，然后释放链接
            connection.release();
            callback.apply(null, arguments);
        });
    })
```



定义一个User构造函数，跟数据库的表是对应关系。



```javascript
funtion User(user) {
    this.id = user.id
    this.username = user.username
    this.pwd = user.pwd
}
```

获取所有用户

```javascript
User.getAllUsers = function(callback) {
	db.query('select * from users', function(err, result) {
        if(err) {
            return callback(err, null)
        }
        callback(null, result)
    })
}
```

用名字获取用户

```
User.getUserByName = function(username, callback) {
	db.query('select * from users where username = ?', [username], function(err, result) {
		if(err) {
			return callback(err, null)
		} 
		callback(null, result[0])
	})
}
```

用id获取用户

```
User.getUserById = 
```

删除用户

```
User.deleteUserById
```

保存用户，这个是prototype方法

```
User.prototype.save = function(callback) {
	db.query('insert into users values (null, ?, ?)', 
	[this.name, this.pwd],
	function(err, result) {
		if(err) {
			return callback(err, null)
		}
		callback(null, result.insertId > 0)
	}
	)
}
```

修改用户信息

```
User.prototype.update = function(callback) {
	db.query('update users set pwd = ?', [this.pwd], function(err, result) {
	
	}
}
```



