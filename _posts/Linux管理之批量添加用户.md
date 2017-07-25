---
title: Linux管理之批量添加用户
date: 2017-07-25 23:28:48
tags:

	- Linux管理

---

先把老服务器上的home目录ls一下，把目录名拷贝出来，在notepad++里整理一下。得到一个username.txt文件。如下：

```
aaa
bbb
ccc
```

把这个文件拷贝一份，得到一个secret.txt文件，批量替换，内容如下：

```
aaa:123456
bbb:123456
ccc:123456
```

每一行的格式是：`name:password`。

新建一个add_users.sh脚本，内容如下：

```
#!/bin/sh
cat < username.txt | xargs -n 1 useradd -m
chpasswd < secret.txt
pwconv
echo "add users ok"
```

