---
title: Mycroft（一）
date: 2018-03-06 20:01:07
tags:
	- 智能音箱

---



Mycroft是一个开源的智能音箱方案。

官网在这里。

https://mycroft.ai



# 下载安装

```
git clone https://github.com/MycroftAI/mycroft-core.git
cd mycroft-core
./dev_setup.sh
```

安装脚本会做：

1、安装依赖文件。

2、安装virtualenv。

我下载压缩文件包到我的树莓派上。

运行会报错。

我把dev_setup.h里这里注释：

```
#install_deps

#git config commit.template .gitmessage
```

我的依赖文件都是好的。git也不需要。

继续执行。会在这个目录生成virtualenv。

```
/home/pi/.virtualenvs/mycroft/bin/python2.7
```

不过安装过程还是会用git去下载东西。



# 运行

```
./start-mycroft.sh debug
```

debug会在后台运行。有一个交互命令行给你输入。



# 配置信息

配置信息的位置在mycroft-core/mycroft/configuration/mycroft.conf。

Mycroft官方提供了一个Home Service，你可以不用。

需要设置一下：

```
[WeatherSkill] api_key = ""
```



stt用的是google的。



