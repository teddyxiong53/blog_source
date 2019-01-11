---
title: python之获取文件名、函数名、行数
date: 2019-01-11 17:00:59
tags:
	- Python
---



可以这样：

```
logging.debug("%s %s %d", __file__, sys._getframe().f_code.co_name, sys._getframe().f_lineno)
```

可以用装饰器的方法。


参考资料

1、python 获取当前位置所在的函数名和行号

https://blog.csdn.net/shanliangliuxing/article/details/7717407

2、python_获取当前代码行号_获取当前运行的类名和函数名的方法

https://blog.csdn.net/qiqiyingse/article/details/70766993