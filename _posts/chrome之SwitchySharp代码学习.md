---
title: chrome之SwitchySharp代码学习
date: 2019-01-20 15:00:32
tags:
	- chrome

---



update_url这个有什么用？

```
__MSG_manifest_iconTitle__、__MSG_manifest_appDescription__、__MSG_manifest_appName__
这些是根据系统的语言来自动选择的。
```

在messages.json里，有这样的定义：

```
    "manifest_appName":{
        "message":"Proxy SwitchySharp"
    },
```



js的test函数，用来检测字符串算法匹配某个规则。

```
var str = "visit w3cschool";
var patt1 = new RegExp("w3cschool");
var result = patt1.test(str);
console.log(result);
```



这个还是复杂了点，暂时不看了。

