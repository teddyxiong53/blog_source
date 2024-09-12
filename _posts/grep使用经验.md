---
title: grep使用经验
date: 2020-03-24 14:01:11
tags:
	- Linux

---



服务器是多核，但是普通的grep，还是单核的，速度比较慢。

怎么利用多核？

```
alias mygrep='find . -type f -print0  | xargs -0 -P `nproc` grep'
```

使用rg这个新的工具。自然就是多线程的。




参考资料

1、

https://unix.stackexchange.com/questions/197352/how-to-start-multi-threaded-grep-in-terminal