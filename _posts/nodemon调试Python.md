---
title: nodemon调试Python
date: 2023-01-19 10:05:31
tags:
	- Python

---



nodejs里的nodemon用来调试nodejs代码很方便，修改保存后自动重新执行。

nodemon其实是个通用工具。可以用来调试其他语言的脚本编写。

例如Python的。

```
nodemon --exec python3 test.py
```

