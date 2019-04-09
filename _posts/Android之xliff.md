---
title: Android之xliff
date: 2019-04-09 14:05:30
tags:
	- Android

---



有时候在string.xml文件里，会看到这种写法。

```
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
```

这个xliff是什么东西？

xliff是Xml Localization Interchange File Format。xml本地化数据交互格式。

用来标记不应该翻译的消息部分。

```
<resources xmlns:xliff="urn:oasis:names:tc:xliff:document:1.2">
	<string name="title_connected_to">
		connect to <xliff:g id="device_name">%1$s</xliff:g>
	</string>
</resources>
```





参考资料

1、Android资源文件中xliff标签的使用

https://blog.csdn.net/isee361820238/article/details/53463866

