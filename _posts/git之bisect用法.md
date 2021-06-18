---
title: git之bisect用法
date: 2021-06-17 19:17:11
tags:
	- git

---

--

```bash
git log --pretty=oneline
```

```bash
git bisect start HEAD 4d83cf
```

4d83cf是我们希望从这个版本开始查。



参考资料

1、

http://www.ruanyifeng.com/blog/2018/12/git-bisect.html