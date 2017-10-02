---
title: Linux之login shell的特点
date: 2017-10-02 14:35:59
tags:
	- Linux

---



Linux的login shell和普通shell的不同在于：

```
	if (isloginsh) {
		const char *hp;

		state = 1;
		read_profile("/etc/profile");
 state1:
		state = 2;
		hp = lookupvar("HOME");
		if (hp) {
			hp = concat_path_file(hp, ".profile");
			read_profile(hp);
			free((char*)hp);
		}
	}
```

login shell会执行/etc/profile和~/.profile脚本。

