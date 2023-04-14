---
title: Linux之date命令
date: 2019-01-09 16:28:22
tags:		
	- Linux

---



```
date +fmt
```

fmt写法：

```
%s: 从1970年以来的秒数。
%S：秒数，0到59。
只打印年月日
date -I

```

-I选项：是iso8601标准。

```
hlxiong@hlxiong-VirtualBox:/usr/include/openssl$ date -I
2019-01-09
hlxiong@hlxiong-VirtualBox:/usr/include/openssl$ date -Ihours
2019-01-09T16+08:00
hlxiong@hlxiong-VirtualBox:/usr/include/openssl$ date -Iminutes
2019-01-09T16:32+08:00
hlxiong@hlxiong-VirtualBox:/usr/include/openssl$ date -Iseconds
2019-01-09T16:32:42+08:00
```

-R选项：是rfc2822标准。

```
hlxiong@hlxiong-VirtualBox:/usr/include/openssl$ date -R
Wed, 09 Jan 2019 16:33:49 +0800
```



设置一个时间

```
date -s '2025-03-20 10:00:00'
```



