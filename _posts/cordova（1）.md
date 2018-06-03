---
title: cordova（1）
date: 2018-06-03 12:09:21
tags:
	- cordova

---



在看一个Android里合入jQuery的例子的时候，运行程序出错了，看到用到的底层是cordova，所以现在先看看cordova的使用。

#简介

1、cordova是一个开源的移动开发框架。

2、开发者可以用html、css、js来做跨平台的开发。

3、还可以调用到设备的硬件功能，例如传感器，相机。

4、简单来说，就是cordova提供了js跟原生的交互通道。



# 安装

1、因为是cordova是用node.js来进行安装的。所以需要先安装node.js。我已经安装好了。

2、用npm来进行安装。

```
npm install -g cordova
```

3、需要jdk1.8的。我也已经安装了的。

4、验证。输入下面的命令，看看能否运行。我这个是正常的。

```
C:\Users\Administrator
λ cordova requirements
? May Cordova anonymously report usage statistics to improve the tool over time? Yes

Thanks for opting into telemetry to help us improve cordova.
```



# helloworld项目

1、到目录下创建工程。

```
D:\work\cordova
λ cordova create hello_cordova com.teddyxiong53 HelloCordova
```

```
D:\work\cordova\hello_cordova  (com.teddyxiong53@1.0.0)
λ ls -lh
total 5.0K
-rw-r--r-- 1 Administrator 197121 985 Jun  3 12:18 config.xml
drwxr-xr-x 1 Administrator 197121   0 Jun  3 12:18 hooks/
-rw-r--r-- 1 Administrator 197121 367 Jun  3 12:18 package.json
drwxr-xr-x 1 Administrator 197121   0 Jun  3 12:18 platforms/
drwxr-xr-x 1 Administrator 197121   0 Jun  3 12:18 plugins/
drwxr-xr-x 1 Administrator 197121   0 Jun  3 12:18 res/
drwxr-xr-x 1 Administrator 197121   0 Jun  3 12:18 www/
```

2、添加安卓平台。

```
D:\work\cordova\hello_cordova  (com.teddyxiong53@1.0.0)
λ cordova platform add android –save
Using cordova-fetch for cordova-android@~7.0.0
Adding android project...
Creating Cordova project for the Android platform:
        Path: platforms\android
        Package: com.teddyxiong53
        Name: HelloCordova
        Activity: MainActivity
        Android target: android-26
Subproject Path: CordovaLib
Subproject Path: app
Android project created with cordova-android@7.0.0
Android Studio project detected
Android Studio project detected
Discovered plugin "cordova-plugin-whitelist" in config.xml. Adding it to the project
Installing "cordova-plugin-whitelist" for android

               This plugin is only applicable for versions of cordova-android greater than 4.0. If you have a previous platform version, you do *not* need this plugin since the whitelist will be built in.

Adding cordova-plugin-whitelist to package.json
Saved plugin info for "cordova-plugin-whitelist" to config.xml
--save flag or autosave detected
Saving android@~7.0.0 into config.xml file ...
Using cordova-fetch for –save
```

3、编译。

```
D:\work\cordova\hello_cordova  (com.teddyxiong53@1.0.0)
λ cordova build
Android Studio project detected
```

4、导入到Android Studio。

打开AS，把工程导入进入。



# 参考资料

1、android混合开发：cordova的安装使用

https://blog.csdn.net/q649381130/article/details/70158255