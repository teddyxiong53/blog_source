---
title: Android系统之Android.mk文件分析
date: 2020-06-23 17:56:49
tags:
	- Android

---

1

Android.mk的一个小型的Makefile文件。

会被编译系统解析多次。所以，应该尽量精简里面的变量。

该文件运行你把代码分成不同的modules。每一个module可以是静态库、动态库。

你可以在一个Android.mk里定义多个module，也可以用同一份代码生成不同的modules。

编译系统会帮你处理大部分的工作。

我直接从aosp里找一个简单的包来看看就好了。

从external目录下，zlib为例。

![img](../images/random_name/1892430-81ede115f8650d46.webp)



Android.mk一般用来编译生成可执行文件，静态库，动态库，jar包，apk文件。

我们在external目录下新建一个simple_test目录，下面新建Android.mk文件。内容如下：

```
LOCAL_PATH := $(call my-dir)
# 清空除了LOCAL_PATH之外的所有环境变量
include $(CLEAR_VARS)
# 指定目标文件名
LOCAL_MODULE := test
# 指定源文件
LOCAL_SRC_FILES := test.c
# 指定输出目录
LOCAL_MODULE_PATH := $(LOCAL_PATH)/bin
# 指定编译格式
include $(BUILD_EXECUTABLE)
```

然后写一个test.c。里面就打印一行。

在simple_test目录下，执行mm。会进行编译，比较慢，居然要1分钟才能编译完。

引用其他的库。

```
# 引用系统静态库
LOCAL_STATIC_LIBRARIES += libxx
# 引用系统动态库
LOCAL_SHARED_LIBRARIES += libxx
# 引用第三方动态库，假设库文件放在当前路径下的lib目录下。
LOCAL_LDFLAGS := -L$(LOCAL_PATH)/lib -lxx
# 引用第三方静态库
LOCAL_LDFLAGS := $(LOCAL_PATH)/lib/libxx.a
```



# 管理多个源代码文件

有两种方法：

1、一个个写出来。

2、通配。

通配的话，编译系统提供了一个函数。

```
LOCAL_C_ALL_FILES := $(call all-c-files-under)
LOCAL_SRC_FILES := $(LOCAL_C_ALL_FILES)
```

# 生成多个目标文件

除了LOCAL_PATH变量不变，剩余的部分，复制粘贴一份到下面。改一下目标名字。就可以了。





# 使用系统的日志打印

```
#include <stdio.h>
#define LOG_TAG "test"
#include <utils/Log.h>

int main()
{
    printf("hello android\n");
    ALOGD("test log");
    return 0;
}
```

直接编译，会报错，因为这个需要链接liglog.so。

加上这句就好了。

```
LOCAL_SHARED_LIBRARIES += liblog
```

# LOCAL_MODULE_TAGS

在zlib的Android.mk文件里。

```
LOCAL_MODULE_TAGS := optional
```

这一句的意义是什么？

LOCAL_MODULE_TAGS ：=user \ eng \ tests \ optional

user:指该模块只在user版本下才编译

eng:指该模块只在eng版本下才编译

tests:指该模块只在tests版本下才编译

optional:指该模块在所有版本下都编译



加编译选项

```
LOCAL_CFLAGS += -O3 -DUSE_MMAP
```



参考资料

1、Android .mk语法

这个实际上是从ndk的说明文档里翻译的。

https://www.jianshu.com/p/bee78310e420

2、5. Android.mk 的基本语法

https://www.jianshu.com/p/9aab51f4cd6f