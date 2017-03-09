---
title: 自定义一套C语言的带级别控制的log宏
date: 2017-03-02 22:01:59
tags:
	- C语言
---
以简单使用为原则，就定义4个宏：LOGE、LOGD、LOGI、LOGW。
分别表示：Error、Debug、Info、Warning。
保证在gcc可以正常使用。

打印中带上行号和函数名。文件名就不带了。
涉及的语法是GNU C的可变参数宏的定义。
实现如下：
```
#include <stdio.h>
#define LOGE(fmt, arg...) 	\
{\
	printf("[E][%s:%d]",__func__, __LINE__);\
	printf(fmt,##arg);\
}
#define LOGD(fmt, arg...) 	\
{\
	printf("[D][%s:%d]",__func__, __LINE__);\
	printf(fmt,##arg);\
}
#define LOGI(fmt, arg...) 	\
{\
	printf("[I][%s:%d]",__func__, __LINE__);\
	printf(fmt,##arg);\
}
#define LOGW(fmt, arg...) 	\
{\
	printf("[W][%s:%d]",__func__, __LINE__);\
	printf(fmt,##arg);\
}
int main()
{
    	LOGE("%d:%s\n", 111, "hhh"); 
	LOGD("%d:%s\n", 111, "hhh"); 
	LOGW("%d:%s\n", 111, "hhh"); 
	LOGI("%d:%s\n", 111, "hhh"); 
}

```

