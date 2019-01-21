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



现在继续看。

```
ProfileManager
	就是各种代理模式的管理。
	依赖了Setting模块。这个是保存设置的模块。
	有4种模式：
		直连
		手动
		自动
		系统
		
```



从options.html来看，这个是主要界面。

对应的js文件是options.js。

background是main.html。

里面包含了profileManager.js等文件。就相当于在window里，产生了ProfileManager对象。

在包含模块的时候，同时进行了初始化。

```
var ProfileManager = {};
...
ProfileManager.init();
```



我们还是先从popup.html开始看吧。

这里是一切开始的地方。

不是，应该是background是最前面的，不是说background是跟随浏览器一起启动的吗？

按照main.html的包含顺序。

```
<script src="assets/scripts/settings.js" type="text/javascript"></script>
    <script src="assets/scripts/i18n.js" type="text/javascript"></script>
    <script src="assets/scripts/plugin.js" type="text/javascript"></script>
    <script src="assets/scripts/profileManager.js" type="text/javascript"></script>
    <script src="assets/scripts/ruleManager.js" type="text/javascript"></script>
    <script src="assets/scripts/main.js" type="text/javascript"></script>
    <script src="assets/scripts/utils.js" type="text/javascript"></script>
```

首先是settings.js里的init执行。这个模块里没有init函数。

i18n的有初始化，且调用了。

plugins这个里面读取了参数。

```

```

