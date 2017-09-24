---
title: python的requests库分析
date: 2017-01-04 21:09:24
tags:
	- python
---
requests是基于urllib写的，是第三方库，不是python自带的。它在使用上比urllib要更加方便，更加适合在python中使用。
安装就用`pip install requests`来安装。

先看一个最简单的使用例子。

```
#!/usr/bin/python

import requests
r = requests.get(url='http://www.baidu.com')
print r.status_code
r = requests.get(url='http://dict.baidu.com/s', params={'wd':'python'})
print r.url
```
这个例子只用到了GET方法，POST等其他方法的接口跟这个都是类似的。

使用requests里的函数后，都会返回一个response的对象。







