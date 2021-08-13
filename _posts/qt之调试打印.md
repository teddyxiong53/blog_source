---
title: qt之调试打印
date: 2021-08-03 16:09:33
tags:
	- qt

---

--

现在调试tslib的。发现里面是这样进行打印的

```
qCDebug(qLcTsLib) << "Initializing tslib plugin" << key << specification;
```

在文件上面，还有这样一个定义，

```
Q_LOGGING_CATEGORY(qLcTsLib, "qt.qpa.input")
```

感觉是可以通过环境变量来动态打开调试的。

找了一下，的确是可以。这样执行一下就好了。

```
export QT_LOGGING_RULES="*.debug=false;qt.qpa.input=true"
```



参考资料

1、

https://blog.csdn.net/xiaoyan_yt/article/details/89517194