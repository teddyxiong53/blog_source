---
title: 叮当音箱之mydingdang（1）
date: 2018-11-27 21:04:57
tags:
	- 智能音箱

---



自己把叮当写一遍。简化来写。

参数基于json来做。进来都放在一个目录下。

现在的目录情况是这样：

```
teddy@teddy-ubuntu:~/work/mydingdang$ tree
.
├── client
│   ├── config.py
│   ├── dingdangpath.py
│   ├── __init__.py
│   └── stt.py
├── config
│   └── profile.json
└── dingdang.py
```

现在需要加入vocabcompiler.py。这一个就引出了不少的东西了。

现在就把不懂的都发散开去，一一弄懂。写系统不是我的主要目的，通过写的方式，来发现自己不懂的点，把这些点弄懂才是关键。



