---
title: flask之源代码阅读
date: 2019-01-16 15:34:59
tags:
	- flask
---



app_run是入口函数。

调用了werkzeug的run_simple函数。

把自己作为Application参数传递进去了。



参考资料

1、flask 源码解析：应用启动流程

https://cizixs.com/2017/01/11/flask-insight-start-process/