---
title: fswebcam代码分析
date: 2017-04-22 21:08:07
tags:
	- video
---
先把代码拷贝到树莓派上，配置编译。出现如下错误：
```
configure: error: GD graphics library not found
```
是需要安装GD库。
安装方法：
```
sudo apt-get install libgd2-xpm-dev
```
安装总是不成功。我直接下载源代码进行编译安装。
源代码下载地址：
```
https://github.com/libgd/libgd/releases
```
默认配置，编译完，安装好。
再看fswebcam的编译。
```
configure: error: GD does not have JPEG support!
```





# 参考资料

1、

https://github.com/fsphil/fswebcam/issues/4