---
title: vscode之在windows下开发Linux程序配置
date: 2018-12-26 15:36:36
tags:
	- vscode

---



一直没有找一个满意的c/c++开发IDE，现在用了vscode，非常满意。

如果开发C语言，可以进行自动补全，那肯定是一件很爽的事情。



打开C语言项目目录，如果有头文件找不到，vscode就会弹出提示，要你去看一个教程，进行配置。



includePath在哪里定义？

在当前目录的.vscode下面的c_cpp_properties.json里。

一旦出错，就会自动生成。

我的当前生成是这样的。

```
{
    "configurations": [
        {
            "name": "Win32",
            "includePath": [
                "${workspaceFolder}/**"
            ],
            "defines": [
                "_DEBUG",
                "UNICODE",
                "_UNICODE"
            ],
            "windowsSdkVersion": "10.0.17134.0",
            "compilerPath": "C:/Program Files (x86)/Microsoft Visual Studio/2017/Community/VC/Tools/MSVC/14.14.26428/bin/Hostx64/x64/cl.exe",
            "cStandard": "c11",
            "cppStandard": "c++17",
            "intelliSenseMode": "msvc-x64"
        }
    ],
    "version": 4
}
```

你也可以自己触发生成，方法是：

```
>cpp edit configuration
```

是打开命令pallet，输入上面的，是模糊匹配出来的。

或者在提示找不到的头文件上悬停鼠标，会出现一个绿色的小气球，你点击气球，也会创建这个文件。



vscode会根据你的系统类型，默认到你的os的相关路径下去找的。



我觉得最好的方法，还是靠包含cygwin下面的头文件，用绝对路径的方式。

如果cygwin下面没有，就用apt-cyg安装。

```
            "includePath": [
                "${workspaceFolder}/**",
                "${workspaceFolder}/src",
                "D:\\cygwin\\usr\\include"

            ],
```

可以了。



# 配置gdb

我把配置上传到github。弄清楚了就很简单。



配置上传在这里。

https://github.com/teddyxiong53/vscode_conf/tree/master/windows_cygwin

参考资料

1、Configuring includePath for better IntelliSense results

https://github.com/Microsoft/vscode-cpptools/blob/master/Documentation/Getting%20started%20with%20IntelliSense%20configuration.md

2、

https://blog.csdn.net/lidong_12664196/article/details/68928136





