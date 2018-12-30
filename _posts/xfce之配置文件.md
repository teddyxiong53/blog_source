---
title: xfce之配置文件
date: 2018-12-30 09:46:25
tags:
	- xfce

---



在~/.config目录下。

vscode的配置文件也放在这里。在Code目录下。settings.json放在这里。



代码库在这里。

https://github.com/xfce-mirror



下载terminal的源代码。分析一下。

编译。报错。需要先安装这个。

```
sudo apt-get install  xfce4-dev-tools
```

配置。

```
./autogen.sh
./configure
```

还是不行。

```
checking pkg-config is at least version 0.9.0... yes
checking for gtk+-3.0 >= 3.20.8... not found
*** The required package gtk+-3.0 was not found on your system.
*** Please install gtk+-3.0 (atleast version 3.20.8) or adjust
*** the PKG_CONFIG_PATH environment variable if you
*** installed the package in a nonstandard prefix so that
*** pkg-config is able to find it.
```

需要安装gtk3.0的。

```
sudo apt-get install libgtk-3-dev 
sudo apt-get install pkg-config 
```

要编译还挺麻烦的。我不编译了。

