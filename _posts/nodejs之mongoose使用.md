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







参考资料

1、官网教程

https://mongoosejs.com/docs/guide.html

2、mongoose中文文档

https://www.kancloud.cn/luponu/mongoose/870695

3、Mongoose开发实战-进阶篇

https://juejin.im/entry/5a0596c5f265da43163c89e4