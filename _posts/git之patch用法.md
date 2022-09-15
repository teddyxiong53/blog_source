---
title: git之patch用法
date: 2022-09-06 15:52:33
tags:
	- git

---

--

现在要对buildroot仓库本身打较多的patch，要摸索出一个可以反复多次打patch，切后续继续修改patch也比较方便的操作方式。

大概对10几个package进行了分散修改。

其中某些package可能后面再次修改。

还可能新增某些package的修改。

假设就是10个package的修改。分解成10个提交。

提交都要写log。直接简单描述就好了。

提交完之后，后面第三个patch对应的内容有修改，其实这些package改动都是相互独立的。

我只需要重新生成第三个patch，替换原有的就好了。

就这么操作。



参考资料

1、

https://blog.csdn.net/liuhaomatou/article/details/54410361