---
title: Android gradle分析
date: 2017-07-13 21:52:56
tags:

	- Android
	- gradle

---

下载了一个Android的示例程序，build -- Clean Project。提示`Could not resolve com.android.tools.build:gradle:2.3.0.`。之前也碰到过类似问题，解决过，但是忘了。现在把这个梳理一下。



# 1. 什么是gradle

1、gradle是一个基于ant和maven概念的自动化构建工具，类似于Linux下的make。

2、使用了一种基于Groovy的特定领域语言来编写，而不是xml。

3、目前只支持Java等，后续会增加对其他语言的支持。

ant、maven、gradle是Java世界里的3大构建工具。

gradle采用和ant类似的策略，以task做为构建的 最小单位，task之间存在依赖关系。例如要完成单元测试C，你需要先完成编译产品源码A和编译单元测试源代码B。

所以任务链就是A-B-C。

当你执行gradle C的时候，它会帮你自动完成A和B。

在gradle中，每一个待编译的工程都叫一个project。每一个project在构建的时候都包含一系列的task。



# 2. 一个简单的gradle脚本文件分析

这个文件是来自于Android Things的simpleio的例子。

1、第一行的apply plugin代表的作用是什么？

这个表示是一个app。对于一个lib的话，第一行应该是`apply plugin:'com.android.library'`。

```
apply plugin: 'com.android.application'

android {
    compileSdkVersion 25
    buildToolsVersion '25.0.2'

    defaultConfig {
        applicationId "com.example.androidthings.simplepio"
        minSdkVersion 24
        targetSdkVersion 25
        versionCode 1
        versionName "1.0"
    }
    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android.txt'), 'proguard-rules.pro'
        }
    }
}

dependencies {
    provided 'com.google.android.things:androidthings:0.4-devpreview'
}
```

# 3. jcenter是什么

看build.gradle文件，里面有一个jcenter。这个是什么？有什么作用？

1、jcenter是一个代码库。很多人把自己的 aar文件打包上传到jcenter的服务器上。这样其他人就可以用。jcenter的提供商是Bintrary，这家公司提供了很多的类似服务jcenter是针对Java的。

2、如果我想把我的库分享给其他人，那么我们先用github账号登陆到Bintrary网站。地址是`https://bintrary.com`。

3、jcenter是目前应用最广的第三方gradle仓库。





gradle构建过程分为3个阶段：

```
1、初始化阶段。
2、配置阶段。
3、执行阶段。

```



参考资料

1、打通Android Gradle编译过程的任督二脉

https://cloud.tencent.com/developer/article/1032349