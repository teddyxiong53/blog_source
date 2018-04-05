---
title: shell之实用命令
date: 2018-02-01 10:53:02
tags:
	- shell

---

###找出当前目录下最占用空间的子目录

```
du -h --max-depth=1 ./
```

###同时查找多种文件

```
find -name "Makefile" \
-o -name "*.mk" \
-o -name "*.sh" \
| xargs grep -nwr "generic\-package"
```

### 排除几种文件

```
find -type f ! -name "*.c" \
-type f ! -name "*.h" \
-type f ! -name "*.cmd" \
-type f ! -name "*.java" \
 | xargs grep -nwr "PLATFORM_VERSION_CODENAME"
```

### 查找拷贝

```

```

