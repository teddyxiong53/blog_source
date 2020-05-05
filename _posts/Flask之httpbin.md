---
title: Flask之httpbin
date: 2018-11-24 11:41:51
tags:
	- Flask
---



httpbin是一个很有用的网站，而且也不复杂，所以值得研究。

httpbin涉及到的flask知识其实不错。大部分内容都是swagger的注释。

直接用pycharm从github下载到本地来阅读。

为了方便表示，肯定是直接在本目录运行比较好。

直接这样：

```
python3 ./core.py
```

会报错：

```
ImportError: attempted relative import with no known parent package
```



要这样来运行才可以：

```
python3 -m httpbin.core
```



参考资料

1、[译][python]ImportError:attempted relative import with no known parent package

<https://blog.csdn.net/nigelyq/article/details/78930330>