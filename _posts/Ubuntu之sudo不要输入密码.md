---
title: Ubuntu之sudo不要输入密码
date: 2018-03-18 19:40:57
tags:
	- Ubuntu

---



总是需要用sudo做一些事情，频繁输入密码特别烦。

解决方式是这样的：

```
sudo visudo
在最后一行加上（最后一行，这一点很关键。不能可能被其他的配置覆盖掉的。我之前加在中间，总是不生效。原来后面还有配置覆盖了）。
teddy ALL=(ALL) NOPASSWD: ALL
```

改完即刻生效。这样teddy这个用户sudo就不用再输入密码了。

