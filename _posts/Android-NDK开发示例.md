---
title: Android NDK开发示例
date: 2017-02-17 19:12:36
tags:
	- Android 
	- NDK
---
本文描述的开发环境是：windows7 + Android Studio。
使用ndk，我们可以用C或者C++来开发代码，然后跟Java代码一起链接。
NDK的N表示Native，本地的意思。
NDK存在的意义是什么？
1、基于SDK写的代码，生成的apk文件，很容易被反编译了，不够安全。
2、已经有很多现成的模块是有C或者C++写的。
3、C和C++的效率比Java高。

NDK的语言基础是Java的JNI特性。JNI是Java Native Interface的缩写。
# 1. ndk的安装
ndk的安装，你可以打开SDK目录下的`SDK Manager.exe`来安装ndk-bundle。
然后就在Android Studio的`File--Project Structure--SDK Location--Android NDK location`来指定ndk bundle的路径。
这样环境就准备好了。

# 2. 建立基本工程
建立默认的工程就好了，带一个基本界面的那种，免去自己定义界面的麻烦。
默认的Java文件是MainActivity.java。在同一个目录下新建一个JniTest.java的文件。
内容如下：
```
package com.teddyxiong53.www.ndkhello;
public class JniTest {
    static {
        System.loadLibrary("hello");
    }
    public static native String stringFromC() ;
    public static native String intFromC(int i, int j) ;

}
```

然后点开Android Studio左下角的Terminal工具界面。
我的工程目录是：`D:\work\android\NdkHello`。要注意实际路径的修改。
输入下面的命令：
```
cd D:\work\android\NdkHello\app\src\main
javah -d jni -classpath D:\work\android_sdk\platforms\android-23\android.jar;..\..\build\intermediates\classes\debug     com.teddyxiong53.www.ndkhello.JniTest
```
然后在main目录下回得到一个jni的目录。里面就一个`com_teddyxiong53_www_ndkhello_JniTest.h`的头文件。这个是自动生成的。
现在你在jni目录下新建一个c文件，就叫hello.c。
把头文件里2个函数名拷贝到hello.c里。函数原型没有带形参，我们改一下，加上形参，然后加上实现。最后文件如下：
```
#include <jni.h>
JNIEXPORT jstring JNICALL Java_com_teddyxiong53_www_ndkhello_JniTest_stringFromC
  (JNIEnv * env, jclass clazz)
{
    return (*env)->NewStringUTF(env, "String from c code ");
}
JNIEXPORT jstring JNICALL Java_com_teddyxiong53_www_ndkhello_JniTest_intFromC
  (JNIEnv * env, jclass clazz, jint i, jint j)
{
    return i+j;
}
```
然后打开`app/build.bundle`文件，在defaultConfig 项里加上ndk项。
```
defaultConfig {
        applicationId "com.teddyxiong53.www.ndkhello"
        minSdkVersion 19
        targetSdkVersion 23
        versionCode 1
        versionName "1.0"
        ndk {
            moduleName "hello"
            ldLibs "log"
            abiFilters "armeabi", "armeabi-v7a", "x86"
        }
    }
```
最后在MainActivity.Java里，通过一个TextView来呈现ndk函数的结果。
```
public class MainActivity extends AppCompatActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        TextView tv = (TextView)findViewById(R.id.tv);
        tv.setText(JniTest.stringFromC() + JniTest.intFromC(1,2));
    }
}
```
现在运行结果有问题，暂时不查，后续再看吧。




