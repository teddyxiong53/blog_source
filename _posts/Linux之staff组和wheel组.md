---
title: Linux之staff组和wheel组
date: 2018-03-12 13:55:43
tags:
	- Linux

---



看LDD3里的加载脚本，看到了staff组和wheel组这个东西，研究一下。



# wheel组

wheel组的概念继承自unix。

如果你不是wheel组成员，就无法取得root权限进行一些操作。

# 为什么需要wheel组

一般在unix下，即使是系统管理员，也不会用root进行登陆，而是以普通身份登陆，再su登陆成为root用户。

但是，任何人只要知道了root密码，就可以通过su命令成为root用户。这个无意是有安全隐患的。

所以，建立wheel这个特殊的组。

# 怎么加入wheel组

1、编辑/etc/group文件，把新的用户加到wheel组的末尾。

```
wheel::10:root,teddy
```

# 什么是staff

staff是所有普通用户的集合。

