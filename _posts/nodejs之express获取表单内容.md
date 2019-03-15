---
title: nodejs之express获取表单内容
date: 2019-03-04 14:55:03
tags:
	- nodejs
---



用bodyParser就可以了。

```
var app = express()
app.use(bodyParser.urlencoded({extended: true}))

app.post("/vote", function(req, res, next) {
    console.log("name:", req.body.name)
```



参考资料

1、

https://blog.csdn.net/wang1006008051/article/details/78191532

2、how to get data passed from a form in Express (Node.js)

https://stackoverflow.com/questions/9304888/how-to-get-data-passed-from-a-form-in-express-node-js