---
title: golang环境配置相关
date: 2020-11-14 17:03:17
tags:
	- go语言

---

1

# go get通过ssr翻墙

不翻墙根本没法用。

我主要在windows下用。

新建goget.bat。放到PATH路径下。例如我放到D:\go_sdk\go1.15\bin

```
@echo off

set http_proxy=socks5://127.0.0.1:1080
set https_proxy=socks5://127.0.0.1:1080

go get -u -v %*

echo ...

pause
```

然后执行：

```
goget golang.org/x/crypto
```

测试一下，可以正常下载了。



# go get提示没有gcc

有些是需要编译的。

那就用mingw安装gcc。

http://win-builds.org/doku.php/download_and_installation_from_windows

从这里下载。是一个下载器。会自动帮你安装一些东西。



这个其实是不小的坑，首先是64位的mingw，不能是32位，否则会报错，其次mingw里面ld.exe版本不能低于2.26，否则会报错

我把报错信息也复制一份，便于大家能搜索到这篇文章

使用32位的报错：cc1.exe: sorry, unimplemented: 64-bit mode not compiled in

使用低版本MinGW的报错：ld.exe: unrecognized option '--high-entropy-va'

解决方案就是直接去下别人release的文件即可，注意版本不要太低（我下的是8.1.0），也省去了mingw-get的时间浪费（不挂梯子好像非常慢？）

直接下载这个压缩包的就好了。

https://sourceforge.net/projects/mingw-w64/files/Toolchains%20targetting%20Win64/Personal%20Builds/mingw-builds/8.1.0/threads-posix/sjlj/x86_64-8.1.0-release-posix-sjlj-rt_v6-rev0.7z/download



参考资料

1、go-get 利用 socks5 代理翻墙下载

https://ybilly.com/2018/07/03/go-get%E5%88%A9%E7%94%A8ss%E7%9B%B4%E6%8E%A5%E7%BF%BB%E5%A2%99/

2、VSCode调试go语言出现：exec: "gcc": executable file not found in %PATH%

https://www.cnblogs.com/zsy/p/5958170.html

3、【环境安装】Windows安装go-flutter-desktop桌面应用框架的环境

https://blog.csdn.net/ReimuYk/article/details/108773425