---
title: Android系统（二）JNI系统分析
date: 2018-01-23 14:18:23
tags:
	- Android系统
---



JNI是Java Native Interface的缩写。表示java本地接口。

JNI是从java1.1版本开始引入的。用来支持java和其他语言（例如C语言）进行交互。

在Android系统中，JNI是java和C及C++连接的桥梁。让java可以调用C库。

在Android5.0的代码里，主要的JNI代码放在`frameworks/base/core/jni`目录下。这些代码被编译成libandroid_runtime.so文件。被放在`/system/lib`目录下。

要理解JNI，就要从java的本质说起。从本质上来说，java语言的运行完全依赖于脚本引擎对java代码进行解释和执行。脚本引擎就是JVM。

从本质上来看，Android是由linux系统加Dalvik虚拟机组成的。

Android用JNI封装了所有跟硬件相关的操作。

下面以MediaScanner为例进行分析。

调用关系是：

```
MediaScanner
	-- libmedia_jni.so
		-- libmedia.so
```

MediaScanner的作用是扫描媒体文件，得到歌曲时长等信息。并把这些信息放到媒体数据库里，给其他的应用来使用。



# 分析Native层

在现实应用中，java的native函数和JNI函数是一一对应的。在Android中，使用了JNINativeMethod的结构体来记录这种对应关系。

```
typedef struct {
    char *name;
    char *signature;
    void *fnPtr;
} JNINativeMethod;
```

需要注意是signature这个成员。它的值是这样的：

```
"()V"
"(II)V"
"(Ljava/lang/String;Ljava/lang/String;)V"
```

解释：

1、"()"里的字符表示参数。括号外面的表示返回值，V表示void。

```
"()V"对应的就是void func()
"(II)V"对应的是void func(int x, int y)
```

2、L表示java类。

下面看几个实际例子。

```
static JNINativeMethod gMethods[] = {
    {
        "processDirectory",
        "(Ljava/lang/String;Landroid/media/MediaScannerClent;)V",
        (void *)android_media_MediaScanner_processDirectory
    },
    //...
};
```

这个数组要注册：

```
int register_android_media_MediaScanner(JNIEnv *env)
{
    return AndroidRuntime::registerNativeMethods(env, kClassMediaScanner, gMethods, NELEM(gMethods));
}
```

`AndroidRuntime::registerNativeMethods`调用的是JNIHelp.cpp里的jniRegisterNativeMethods。

