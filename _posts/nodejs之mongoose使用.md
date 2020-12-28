---
title: nodejs之mongoose使用
date: 2019-03-14 14:17:11
tags:
	- nodejs

---





什么是mongoose？

简单说，就是对nodejs环境里的mongodb数据库的操作进行封装。

可以把数据库里的数据转化为JavaScript对象给我们用。

名词解释：

```
Schema：以文件形式存在的数据库模型骨架。不具备数据库的操作能力。字面含义是概要。
Model：由Schema发布生成的模型，具有抽象属性和行为的数据库操作对象。
Entity：由Model创建的实体。它的操作会影响数据库。

它们之间的关系是：
Schema生成Model。
Model创造Entity。
Model和Entity都可以对数据库造成影响。但是Model比Entity更具有可操作性。
```



# get started

```
var mongoose = require('mongoose');
mongoose.connect('mongodb://localhost/test', {useNewUrlParser: true});

var db = mongoose.connection

db.on('error', function(err) {
    console.log(err)
})
db.once('open', function() {
    console.log('connected ok')
})

// 新建一个Schema
var studentSchema = new mongoose.Schema({
    name: String,
    age: Number
})
// 给Schema增加方法
studentSchema.methods.study = function() {
    console.log(this.name + " is studying")
}
// 新建一个Model
var Student = mongoose.model('Student', studentSchema)

// 新建一个Model实例
var allen = new Student({
    name: "allen",
    age: 10
})
// 调用方法
allen.study()
// 保存
allen.save(function(err, student) {
    if(err) {
        console.log("save error")
        return
    }

})
// 查找所有的Student
Student.find(function(err, students) {
    if(err) {
        console.log(err)
        return
    }
    console.log(students)
})

```



mongodb是一个开源的nosql数据库，相比于mysql那样的关系型数据库，它显得更加轻巧灵活，非常适合在数据规模很大、事务性不强的场合下使用。

同时它也是一个对象数据库。

没有表、行的概念。

也没有固定的模式和结构。

所有的数据以文档的形式存储。文档的格式是json的。



mongoose是什么？

mongoose是mongodb的一个对象模型工具。

基于node-mongodb-native开发的mongodb 的nodejs驱动。

可以在异步环境下执行。

同时也是一个针对mongodb操作的一个对象模型库。

封装了mongodb对文档的增删改查等操作。

让nodejs操作mongodb更加容易。



要掌握mongoose，还是需要花时间的。



这个demo写得不错。

https://github.com/IronPans/mongodb-pratice



虚拟属性

虚拟属性不存放在数据库里。

只是在逻辑上存在。



mongoose的一切都从Schema开始。

一个Schema相当于对应数据库里的一张表。也就是一个collection。

把Schema转成一个Model。

```
var User = mongoose.model('User', UserSchema)
```



# mongoose连接

```
connect函数
可以接收一个callback作为参数，
也使用Promise使用。
```

```
mongoose.connect("mongodb://localhost/test", options, function(err) {

})
或者
mongoose.connect("mongodb:/localhost/test", options).then(
	()=> {
	
	},
	(err)=> {
	
	}
)
```

# Models

Models从从Schema编译得到的构造函数。

Models实例代表着数据库里的document。相当于一行实际的数据。

## 创建一个数据，并保存到数据库

可以用save，也可以用create。

```
var User = mongoose.model('User', userSchema)
var allen = new User({
    name: 'allen',
    age: 10
})
allen.save(function(err) {
    if(err) {
        console.log("save error")
        return
    }
    console.log("save ok")
})


User.create({
    name: 'bob',
    age: 11
}, function(err, user) {
    if(err) {
        console.log("save fail")
        return
    }
    console.log("save ok")
    console.log(user)
})
```

## 查找

```
User.find({name: 'allen'}).where('name').eq('bob').exec(console.log)
```

## 删除

remove已经过时了。

```
collection.remove is deprecated. Use deleteOne, deleteMany, or bulkWrite instead.
```



```
var User = mongoose.model('User', userSchema)
User.remove({name: 'bob'}, function(err) {
    if(err) {
        console.log(err)
    }
   
})
```

## 更新

```
//更新一条数据
var User = mongoose.model('User', userSchema)
User.findOneAndUpdate({name: 'allen'}, {name: 'bob'},{}, function(err) {
    if(err) {
        console.log(err)
        return
    }
    console.log("update ok")
})
```



# 插件

怎么使用插件？

插件是对Schema进行扩展的机制。

例如，我们想要对所有的表，都添加最后修改这样的功能。

借助插件，我们可以很容易做到。

我们需要做的是：

1、定义一个插件，

2、然后应用到每个Schema就可以了。

新建一个lastMod.js文件。

对应代码在这里。

https://github.com/teddyxiong53/nodejs_code/tree/master/mongoose_study/plugin_demo

## 全局插件

对mongoose执行plugin函数。

这样后面所有的Schema就不需要分别去执行插入插件的行为了。

```
var mongoose = require("mongoose")
mongoose.plugin(require("./lastMod"))
var userSchema = new Schema({

})
```



# virtual属性

virtual属性就是不会被持久化到数据库里的属性。

是为了应对这种场景，有些属性需要拼接起来用。但是每次用的时候都拼接一下非常麻烦。

例如下面的fullName。

```
var mongoose = require("mongoose")
var Schema = mongoose.Schema

var personSchema = new Schema({
    name: {
        first: String,
        last: String
    }
})
var Person = mongoose.model('Person', personSchema)
var allen = new Person({
    name: {
        first: "Ray",
        last: "Allen"
    }
})

personSchema.virtual("fullName").get(function() {
    return this.name.first + ' ' + this.name.last;
})
```

# index

这个是建立索引，提高查询的速度。

可以对多个字段建立索引。



# 怎么保证只连接一次

它底层已经做了保证，对一个url，执行多次connect操作，实际只有一次连接的效果。

你连续这样调用。连接回调只有一次。

```
mongoose.connect('mongodb://192.168.1.102/test', { useNewUrlParser: true } )
mongoose.connect('mongodb://192.168.1.102/test', { useNewUrlParser: true } )
mongoose.connect('mongodb://192.168.1.102/test', { useNewUrlParser: true } )
```

# 连接多个mongodb

我们一般使用的mongoose.connect，这种用法，只能连接一个mongodb。

如果要同时连接多个mongodb，则需要使用createConnection这个函数。

# 查找不到，就创建

这个要用findOneAndUpdate这个函数。

```
let doc =  Character.findOneAndUpdate(filter, update, {
  new: true
});
```

返回的是更新之前的。

new这个选项为true，就是找不到就创建的意思。



参考资料

1、官网教程

https://mongoosejs.com/docs/guide.html

2、mongoose中文文档

https://www.kancloud.cn/luponu/mongoose/870695

3、Mongoose开发实战-进阶篇

https://juejin.im/entry/5a0596c5f265da43163c89e4

4、使用express+mongoose对mongodb实现增删改查操作

https://segmentfault.com/a/1190000004873740

5、

https://mongoosejs.com/docs/guide.html#virtuals

6、Mongoose模块化实践

https://blog.csdn.net/weixin_40629244/article/details/104915736

7、nodejs连接多个mongodb数据库

https://blog.csdn.net/m0_37263637/article/details/78963991