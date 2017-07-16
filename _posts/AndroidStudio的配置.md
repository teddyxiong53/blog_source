---
title: Android Studio的配置
date: 2017-07-13 00:01:39
tags:

	- Android Studio

---

现在要用Android Studio开发Android Things，版本需要更新，依赖的Android SDK也需要更新到7.0版本以上。网络已经翻墙。所以就可以用简单原始的方式进行。

# 1. 更新Android Studio

我的当前版本是2.1.1，检查看到最新版本是2.3.3。是否必须升级？

作为一个安装包达到将近2个G的软件，居然不能增量升级，不太想升级。网上看是有增量升级的方法，但是太麻烦。

后面仔细看了下，是带Android SDK的版本大概2G，IDE本身是450M左右。我有单独下载Android的SDK的。

更新版本后，编译会出现`java.lang.UnsupportedClassVersionError: com/android/build/gradle/AppPlugin : Unsupported major.minor version 52.0`。网上查了下，说是Android Studio2.2以上版本强制要求JDK8.0以上。下载更新JDK。

Java7和Java8可以共存。安装Java8之后，把环境变量的JAVA_HOME改到java8的目录就好了。

但是实际上看，还是不行。我把Java7的卸载掉，重启电脑。然后看，提示java7找不到了。说明刚刚还是再找Java7的。修改指定的jdk。File然后Other settings然后Default Project structure。选择使用内置的jdk。



# 2. 更新Android SDK版本

看到Android Things至少要Android7.0才行。

在Android Studio里，点击Tools，然后Android，然后SDK Manager，然后是打开StandAlone SDK Manager。我后续的操作都统一从Android Studio里开始做。

从这里可以看到，Android 7.0对应API 24，Android 6.0对应API 23。

把代理地址配置一下，下载速度有600KB左右，还可以接受。

我把Android 6/7/8的更新都下载安装了。



# 3. 工程错误的自动修正

我导入Android Things的sample工程，有提示错误，你点击错误，它就会自动给你去下载缺失的东西进行修正。多亏了可以翻墙，不然这些事情真的挺麻烦的。



