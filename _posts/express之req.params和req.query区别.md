---
title: express之req.params和req.query区别
date: 2021-01-18 16:21:11
tags:
	- express

---

--

req.body明显一点，这个是在form里提交的东西。

而req.params和req.query则需要说明一下，这2个都是在url里传递的。

# req.params

这个是对于这样的路由的：

```
app.get('/:id', function(req,res) {
	console.log(req.params['id'])
})
```

url里是这样的：

```
http://xx/123
```

# req.query

这样路由是这样：

```
app.get('/', function(req, res) {
	console.log(req.query)
})
```

url是这样：

```
http://xx/?id=123
```



参考资料

1、node中req.params,req.query,req.body三者的细微区别

https://blog.csdn.net/MyNameIsXiaoLai/article/details/85319479