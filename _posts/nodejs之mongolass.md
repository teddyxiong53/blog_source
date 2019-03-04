---
title: nodejs之mongolass
date: 2018-12-25 15:41:55
tags:
	- nodejs

---



mongolass是一个mongodb的驱动库。用在nodejs上的。

安装：

```
npm install -g mongolass
```

使用：

```
const Mongolass = require("mongolass")
const mongolass = new Mongolass()
mongolass.connect("mongodb://localhost:27017/test")

const User = mongolass.model('User')

User.find()
    .select({name:1, age: 1})
    .sort({name: -1})
    .exec()
    .then(console.log)
    .catch(console.error)
```

然后node test.js运行即可。当前查询到的空的。

用自己的Schema。

这个故意放了一个错误。

```
const Mongolass = require("mongolass")
const mongolass = new Mongolass()
const Schema = Mongolass.Schema

mongolass.connect("mongodb://localhost:27017/test")

const UserSchema = new Schema('UserSchema', {
    name: {
        type: 'string'
    },
    age: {
        type: 'number'
    }
})

const User = mongolass.model('User', UserSchema)

User.insertOne({name: 'allen', age: 'xxx'})//这里给错误数据。
    .exec()
    .then(console.log)
    .catch(function(e) {
        console.error(e)
    })
```





是n-blog的作者写的。此人是石墨文档的。



参考资料

1、Mongolass——一个类 mongoose 的 MongoDB 驱动库

https://cnodejs.org/topic/56e01c7a255ed94c6e4c2724

2、

https://zhuanlan.zhihu.com/p/24308524