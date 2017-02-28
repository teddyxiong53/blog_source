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


# 2. 新建工程并进行设置


