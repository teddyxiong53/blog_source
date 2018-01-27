---
title: xposed框架了解
date: 2018-01-21 18:18:59
tags:
	- xposed

---



先用起来再说。不想root手机，安装了VAXposed框架。

VAXposed相当于一个沙盒。你可以把你手机里的其他应用在这里复制一份，最简单就是当一个多开器来用。也是简单方便的。

使用效果有：

1、里面的QQ和微信不能马上收到消息。

2、不能运行vpn工具。

3、不能运行YouTube这种要求谷歌服务的程序。



现在有了感性的认识了。那么再看看xposed的原理。



# 原理

xposed框架的核心思想在于将java层普通函数注册成本地JNI方法，用这种方式变相地实现hook机制。

那么就有这么三个问题：

1、dalvik虚拟机在执行java层代码的时候，是怎么识别JNI方法的？

2、怎样才能将java层普通方法注册成JNI方法？

3、xposed具体做了什么？

先看第一个。

先看看一个类的加载过程：当一个类第一次被使用到的时候，这个类的字节码会被加载到内存，并且只加载一次。这个被加载的字节码的入口维持着一个该类所有方法描述符的list。这些方法描述符包含的信息有：

```
1、方法代码放在哪里。
2、方法的参数有哪些。
3、方法的属性，例如public这些。
```

方法描述符实际上对于C语言的一个结构体。

```
struct Method {
  ClassObject *clazz;
  u4 accessFlags;//这个就是表示了public这些属性的flag
}
```

一个类在执行之前先被load到内存，之后要进行字节码校验，然后查找并load含有main的类。

在这个调用链里，有个dvmCallMethodV的函数，里面有这样的代码：

```
if(dvmIsNativeMethod(method)) {//native也是在accessFlags里标记的。
  
}
```

就这样判断了是否native方法。

然后看第二个疑问。

要看xposed的代码。代码是C++写的。

```
SET_METHOD_FLAG(method, ACC_NATIVE);
```

（说实话，这里我没太看懂，先放着）

看第三个疑问：xposed做了些什么事情？

