---
title: express（1）
date: 2021-01-27 17:00:11
tags:
	- express

---

--

这个做一些总结性的东西。

多个static目录。这样就可以在public目录之外放文件。

```
var target1 = path.join(__dirname,'./public');
var target2 = path.join(__dirname,'./upload');
app.use(express.static(target1));
app.use(express.static(target2));
```

