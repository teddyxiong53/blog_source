---
title: nodejs之validator
date: 2021-10-26 19:55:33
tags:
	- nodejs

---

--

该库仅验证和清理字符串。

如果您不确定您的输入是否为字符串，请使用 input + '' 对其进行强制转换。

传递字符串以外的任何内容都会导致错误

可以验证的功能有：

```
validator.contains("abc", "ab", {ignoreCase:true})
validator.isAfter("2022") 
	看是否在某个日期之后，第二个参数默认是now。
isAlpha("a", "zh-cn")
isAlphanumeric("1")
isAscii("123")
isBase32("aa")
```



参考资料

1、

https://www.npmjs.com/package/validator