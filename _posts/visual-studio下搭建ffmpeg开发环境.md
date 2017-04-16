---
title: visual studio下搭建ffmpeg开发环境
date: 2017-02-26 14:03:30
tags:
	- ffmpeg
	- visual studio
---
要学习一下写播放器，感觉Linux下的各种依赖库安装太麻烦，所以还是选择在windows下来做。
# 1. 下载必要的库和头文件
下载地址：`https://ffmpeg.zeranoe.com/builds/`。下载速度很快。
我们需要下载dev版本和shared版本。
dev版本是为了得到lib文件和头文件。shared版本是为了得到dll文件。
lib文件和dll文件的区别在于：lib文件是编译阶段需要，而dll文件是运行时需要。
我的visual studio是2015版本的。安装目录在`D:\Program Files (x86)\Microsoft Visual Studio 14.0`。
visual studio现在也免费了，很好，免去破解的麻烦了。
我的电脑是64位的，所以我下载的ffmpeg的资源都是64位的。

# 2. 新建工程并进行设置
新建一个c++的控制台程序。就叫testffmpeg。自动生成的源文件是testffmpeg.cpp。
我们从ffmpeg的源代码目录下的`doc/exmaples`目录找到metadata.c文件，把里面的内容拷贝到testffmpeg.cpp里。
然后从ffmpeg-dev的目录下把include和lib两个目录拷贝到testffmpeg.cpp所在目录下。
在testffmpeg.cpp所在目录新建一个dll目录，从ffmpeg-shared目录下把bin目录下的所有dll文件拷贝到dll目录下。
编译发现会出现符号找不到的错误。
发现是C++编译导致的，要重新建立一个空的工程，写.C文件。
编译，还是提示符号找不到。原因是lib库没有找到。我已经设置了项目的目录里包含了。
解决方法是在项目上右键==>添加==>新建筛选器，就命名为lib。
然后在lib上右键==>添加==>现有项。把lib文件都添加进来，再编译，就ok了。

# 3. 运行
现在运行，会提示计算机丢失AVformat-57.dll。








