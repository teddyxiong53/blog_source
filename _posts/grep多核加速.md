---
title: grep多核加速
date: 2021-08-18 14:40:33
tags:
	- grep

---

--

服务器是多核，但是普通的grep，还是单核的，速度比较慢。

怎么利用多核？

```
alias mygrep='find . -type f -print0  | xargs -0 -P `nproc` grep'
```



参考资料

https://unix.stackexchange.com/questions/197352/how-to-start-multi-threaded-grep-in-terminal