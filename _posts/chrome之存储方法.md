---
title: chrome之存储方法
date: 2019-01-21 10:47:12
tags:
	- chrome

---

有3种方式：

```
1、html5的localStorage。不管。
2、chrome.storage接口
3、chrome.cookies接口。
```



chrome.storage接口

需要声明：

```
"permissions": [
    "storage"
]
```

提供了3种存储空间类型：

```
1、sync。
	同一个谷歌账号会同步。
2、local。
	只在当前设备。
3、managed。
	只读存储。插件只能读取。只有域管理员可以写。
```

存储机制是存储格子的机制，只能一个一个写入，并发性能不高。

以sync方式为例，看看怎么进行操作。

```
存储一个或者多个数据
	chrome.storage.sync.set({color:"white"}, function(items) {
        document.body.style.backgroundColor = items.color;
	});
获取数据
	var defaultConfig = {color:"white", showImage:true};
	chrome.storage.sync.get(defaultConfig, function(items) {
        document.getElementById("color").value = items.color;
	});
删除
	chrome.storage.sync.remove
清空
	chrome.storage.sync.clear
```



参考资料

1、Chrome浏览器扩展开发系列之八：Chrome扩展的数据存储

https://www.cnblogs.com/champagne/p/4826611.html