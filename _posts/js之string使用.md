---
title: js之string使用
date: 2021-05-27 19:08:25
tags:
	- js
---

--

string的replace方便不会改变原字符串。

我就踩到这个坑了。

```
var text = "aaa"
text.replace('aaa', 'bbb')
console.log(text) //这个还是aaa
//要得到bbb
//需要这样
var text2 = text.replace('aaa', 'bbb')
console.log(text2)
```



参考资料

1、