---
title: Android Studio的配置
date: 2017-07-13 00:01:39
tags:

	- Android Studio

---

现在要用Android Studio开发Android Things，版本需要更新，依赖的Android SDK也需要更新到7.0版本以上。网络已经翻墙。所以就可以用简单原始的方式进行。

# 更新Android Studio

我的当前版本是2.1.1，检查看到最新版本是2.3.3。是否必须升级？

作为一个安装包达到将近2个G的软件，居然不能增量升级，不太想升级。网上看是有增量升级的方法，但是太麻烦。

后面仔细看了下，是带Android SDK的版本大概2G，IDE本身是450M左右。我有单独下载Android的SDK的。

更新版本后，编译会出现`java.lang.UnsupportedClassVersionError: com/android/build/gradle/AppPlugin : Unsupported major.minor version 52.0`。网上查了下，说是Android Studio2.2以上版本强制要求JDK8.0以上。下载更新JDK。

Java7和Java8可以共存。安装Java8之后，把环境变量的JAVA_HOME改到java8的目录就好了。

但是实际上看，还是不行。我把Java7的卸载掉，重启电脑。然后看，提示java7找不到了。说明刚刚还是再找Java7的。修改指定的jdk。File然后Other settings然后Default Project structure。选择使用内置的jdk。



#  更新Android SDK版本

看到Android Things至少要Android7.0才行。

在Android Studio里，点击Tools，然后Android，然后SDK Manager，然后是打开StandAlone SDK Manager。我后续的操作都统一从Android Studio里开始做。

从这里可以看到，Android 7.0对应API 24，Android 6.0对应API 23。

把代理地址配置一下，下载速度有600KB左右，还可以接受。

我把Android 6/7/8的更新都下载安装了。



# 工程错误的自动修正

我导入Android Things的sample工程，有提示错误，你点击错误，它就会自动给你去下载缺失的东西进行修正。多亏了可以翻墙，不然这些事情真的挺麻烦的。



# 引入jar库文件

1、切换到Project试图。在左上角的位置，默认是Android视图。

2、然后在Android Studio里，把jar文件粘贴到app/libs目录下。

3、在jar文件上右键，add as lib。这样才是ok。



# 增加assets目录

1、还是切换到Project试图。跟res在同一层目录下。所以是在app/src/main目录下。

2、然后在main目录上右键，新建folder，新建assets folder。就好了。



# 避免每次都下载gradle

https://blog.csdn.net/coder_e/article/details/62043159

参考上面这篇文章。

总的思路是把wrapper.properties里的gradle压缩包位置指定为本地的服务器的。

所以需要在本地搭建一个web server。

1、把windows的IIS打开。在控制面板，程序里。勾选后，不需要重启系统。

http://127.0.0.1/

我们可以用这个网址访问到IIS的页面，说明打开成功了。

用windows自带的，我们可以少费点心。可以保证基本稳定工作。

2、在C:\inetpub\wwwroot这个目录下（这个是IIS服务器的根目录）。

把gradle-3.3-all.zip文件拷贝到这里。

3、改wrapper.properties里面的内容：

```
distributionUrl=http://localhost/gradle-3.3-all.zip
```

4、然后把AS重启。



#sdk build tools版本问题

我用cordova生成的Android工程，用AS进行build操作。会提示错误。

```
Error:A problem occurred configuring project ':CordovaLib'. > Failed to find Build Tools revision 26.0.2
```



# 更新AS后，点击类不能跳转

重新建立项目就可以了。

