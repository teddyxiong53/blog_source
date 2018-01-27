---
title: alpine（六）安装桌面环境
date: 2018-01-26 22:04:05
tags:
	- alpine

---



我觉得xfce的桌面环境不错，就安装这个了。

1、配置。

```
setup-xorg-base
```

2、安装xfce4.

```
apk add xfce4
```

3、

```
apk add xf86-video-intel
```

4、

```
apk add xf86-input-mouse xf86-input-keyboard
```

5、startx。然后可以顺利进入到桌面环境了。



# 安装浏览器

1、直接add firefox是不行的。要这样：

```
apk add firefox-esr-dev
```

