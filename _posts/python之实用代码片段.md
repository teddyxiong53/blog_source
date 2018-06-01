---
title: python之实用代码片段
date: 2017-07-22 23:59:09
tags:
	- python

---

## 格式化打印

特点是用{}来占位。

```
print "Sent: {}".format(data)
```



## 取得某个目录下所有某个后缀的文件

```
import glob
files = glob.glob("./*.jpg")
print files
```

