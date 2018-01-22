---
title: Ubuntu之Hash Sum mismatch
date: 2018-01-22 18:23:01
tags:
	- Ubuntu

---



执行apt-get update的时候，一直碰到这个问题：

```
W: Failed to fetch http://security.debian.org/dists/jessie/updates/main/binary-amd64/Packages  Hash Sum mismatch

W: Failed to fetch http://deb.debian.org/debian/dists/jessie/main/binary-amd64/Packages  Hash Sum mismatch

```

上面给的是Debian上的打印。Ubuntu也是类似的。

出现这个问题的原因，应该就是ISP提供商的透明缓存导致的。

解决办法是绕过缓存。翻墙的手段对这个也是管用的。

但是好像解决不了我的当前问题，我的是在docker里，docker里设置代理无法做到。

