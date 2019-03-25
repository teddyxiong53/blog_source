---
title: boost之less_than_comparable
date: 2019-03-25 16:25:32
tags:
	- cpp

---



在实际的编程过程中，我们有时候需要进行运算符重载，以便进行类之间的比较。

但是，进行运算符重载，是一件乏味有比较容易出错的事情。

而且，一般只要我们实现了小于比较，其他的重载都可以通过小于来推导出来。

用boost的less_than_comparable就可以帮我们只需要重载小于比较，就可以自动帮我们完成其他的比较。





参考资料

1、boost::less_than_comparable

https://blog.csdn.net/huangjh2017/article/details/74357003