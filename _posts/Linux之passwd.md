---
title: Linux之passwd
date: 2018-03-20 22:23:28
tags:
	- Linux

---



Linux的passwd的格式定义是在C库里做的。

在头文件pwd.h里。

```
struct passwd
{
	char *pw_name;
	char *pw_passwd;
	uid_t pw_uid;
	gid_t pw_gid;
	char *pw_gecos;
	char *pw_dir;
	char *pw_shell;
};
```

总共7个成员变量。