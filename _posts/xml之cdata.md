---
title: xml之cdata
date: 2019-04-28 15:48:25
tags:
	- xml

---



cdata是Character DATA的缩写。

被这个包裹的不会被解析。

格式是这样：

```
<![CDATA[xx]]>
```

xx就是我们要填入的内容。

cdata不能嵌套。

xx里不能出现“]]>”。不然会出现解析错误。



参考资料

1、XML 中的 ﹤![CDATA[ ]]>，及其解析

https://blog.csdn.net/qq_33266987/article/details/54288051