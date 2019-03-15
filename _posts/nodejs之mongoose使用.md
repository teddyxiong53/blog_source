---
title: nodejs之ejs学习
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



最简单的连接的代码：

```
var mongoose = require('mongoose')
var db = mongoose.connect("mongodb://localhost:27017/test")

var con = mongoose.connection

con.on("error", function(e) {
    console.log("connect to mongodb fail")
    console.log(e)
})

con.on("open", ()=> {
    console.log("open mongodb ok")
})
```



完整一点的例子。

```
var mongoose = require('mongoose')
var db = mongoose.connect("mongodb://localhost:27017/test")

var con = mongoose.connection

con.on("error", function(e) {
    console.log("connect to mongodb fail")
    console.log(e)
})

con.on("open", ()=> {
    console.log("open mongodb ok")
    //定义一个Schema
    let Schema = mongoose.Schema({
        category: String,
        name: String
    })
    Schema.methods.eat = function() {
        console.log("eat " + this.name)
    }
    //继承一个Schema
    let Model = mongoose.model("fruit", Schema)
    //生成一个document
    let apple = new Model({
        category: "apple",
        name: "apple"
    })
    //存放数据
    apple.save((err, apple)=> {
        if(err) {
            console.log(err);
            return
        }
        apple.eat()
        //查找数据
        Model.find({name: "apple"}, (err, data)=> {
            console.log(data)
        })
    })
})
```



参考资料

1、Mongoose学习参考文档——基础篇

https://cnodejs.org/topic/504b4924e2b84515770103dd

2、深入浅出mongoose

https://www.villainhr.com/page/2016/05/11/%E6%B7%B1%E5%85%A5%E6%B5%85%E5%87%BAmongoose

3、Connections

https://mongoosejs.com/docs/connections.html