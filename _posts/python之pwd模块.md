---
title: python之pwd模块
date: 2019-01-10 17:22:51
tags:
	- Python
---



这个模块提供访问unix password database的方法。

密码数据库的entry是7个元素的tuple。

```
name password uid gid gecos dir shell
```

跟pwd.h里的定义是一样的。

```
In [353]: print(pwd.getpwnam(os.path.expandvars("$USER")))
pwd.struct_passwd(pw_name='hlxiong', pw_passwd='x', pw_uid=1000, pw_gid=1000, pw_gecos='hlxiong,,,', pw_dir='/home/hlxiong', pw_shell='/bin/bash')
```



有3个get函数：

```
getpwall()
getpwnam("hlxiong")
getpwuid(1000)
```



grp模块跟pwd模块类型。

函数也是类似的。



参考资料

1、python使用pwd和grp操作unix用户及用户组

https://www.cnblogs.com/breezey/p/6663598.html