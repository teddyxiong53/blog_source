---
title: setlocale使用分析
date: 2017-04-22 21:16:04
tags:
---
先看一个例子：
```
#include <stdio.h>
#include <locale.h>
#include <wchar.h>

int main()
{
    wchar_t str[]  ={ 25105, 29233 ,20320 ,0};
    setlocale(LC_ALL, "");
    printf("%ls\n", str);
    return 0;
}
```
这个例子的结果是打印出“我爱你”这3个汉字。

Linux里，用locale命令查看当前系统活动的locale信息：
```
teddy@teddy-ubuntu:~/test/c-test$ locale
LANG=zh_CN.UTF-8
LANGUAGE=zh_CN:zh
LC_CTYPE="zh_CN.UTF-8"
LC_NUMERIC="zh_CN.UTF-8"
LC_TIME="zh_CN.UTF-8"
LC_COLLATE="zh_CN.UTF-8"
LC_MONETARY="zh_CN.UTF-8"
LC_MESSAGES="zh_CN.UTF-8"
LC_PAPER="zh_CN.UTF-8"
LC_NAME="zh_CN.UTF-8"
LC_ADDRESS="zh_CN.UTF-8"
LC_TELEPHONE="zh_CN.UTF-8"
LC_MEASUREMENT="zh_CN.UTF-8"
LC_IDENTIFICATION="zh_CN.UTF-8"
LC_ALL=
```


