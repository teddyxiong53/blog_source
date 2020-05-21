---
title: bat脚本经验
date: 2018-08-03 09:10:28
tags:
	- Windows

---



偶尔会需要用bat写一些Windows下用的脚本。都是很简单的。我不打算花时间去专门学习。

所以把用到的东西总结下来。



打印是echo。

变量是用两个百分号包含起来。

定义变量是set a=“”

**注释：rem和双冒号都可以。**

不区分大小写。

```
@echo off  关闭echo命令本身的回显。一般都要加上这一行。
echo %date%  不区分大小写
echo %DATE%
pause
```

关键词：

pause

exit

这2个最常用的。

转义字符是^ 。而不是类Unix里的反斜杠。

```
rem "check daemon existence"
echo ps ^> /data/ps_info.log > cmd.txt 
echo exit >> cmd.txt

adb shell < cmd.txt
```



根据日期和时间生成目录名。

```
@echo off
set YYYYmmdd=%date:~0,4%%date:~5,2%%date:~8,2%
set hhmiss=%time:~0,2%%time:~3,2%%time:~6,2%
set "dirname=doss_%YYYYmmdd%_%hhmiss%"
echo %dirname%
pause
```

这个有点问题，对于小时数小于10的，不能正确处理。

```
@echo off
set YYYYmmdd=%date:~0,4%%date:~5,2%%date:~8,2%
if "%time:~0,2%" lss "10" (set hh=0%time:~1,1%) else (set hh=%time:~0,2%)
set mi=%time:~3,2%
set ss=%time:~6,2%

set "dirname=doss_%YYYYmmdd%_%hh%%mi%%ss%"
echo %dirname%

if not exist %dirname% (
	md %dirname%
	
) else (
	echo %dirname% exist
)
```



条件判断怎么做？

很奇葩，是用小括号来做范围框定。

```
set /p a= 请输入内容：

if "%a%"=="1" (
    echo 1111111111111111111111111111
    pause
)else (
    if "%a%"=="2" (
        echo 222222222222222222222222
        pause
    )else (
        if "%a%"=="3" (
            echo 3333333333333333333333
            pause
        )else (
            if "%a%"=="4" (
                echo 444444444444444444444444444444444444
                pause
            )
        )
    )
    echo 没有多余的选择，按任意键盘退出
    pause
    exit
)
```



for循环。

```
在cmd窗口中：for %I in (command1) do command2 
在批处理文件中：for %%I in (command1) do command2
```





# 杀掉多个同名进程

有两种方式：

1、

```
wmic process where name='nginx.exe' call terminate
```

2、

```
taskkill /f /t /im nginx.exe
```



# 查看退出码

```
echo %ERRORLEVEL%
```

相当于`echo $?`



# sleep

bat居然都没有现成的sleep可以调用。

我看了一圈，最简单的方式是用vbs来做。

新建一个sleep.vbs文件。里面内容。以ms为单位的。

```
WScript.sleep 1000
```

然后在bat脚本里调用。

```
Wscript sleep.vbs
```



# 定义函数



#环境变量

```
cmd的环境变量操作：
set 查看当前的环境变量。
set A=1 设置环境变量。
set A 查看某个环境变量。
这个在powershell下面是不行的。
```



# 带菜单的写法

下面这个是典型例子。可以用。

```
@echo off 
chcp 65001
color 0a

:menu_choose
echo "================================"
echo "bat工具"
echo "1. 菜单1"
echo "2. 菜单2"
echo "3. 菜单3"
echo "输入q再回车退出"
echo "================================"

set /p num=你的选择是：

if "%num%" == "1" goto menu_1
if "%num%" == "2" goto menu_2
if "%num%" == "3" goto menu_3
if "%num%" == "q" exit

echo "你的选择不正确"
goto menu_choose

:menu_1
echo "菜单1"
goto menu_choose

:menu_2
echo "菜单2"
goto menu_choose


:menu_3
echo "菜单3"
goto menu_choose
```





现在有一个需求，就是批量格式化SD卡，然后拷贝一些文件进去。

这个可以分解为：

1、格式化磁盘。

dos下面的命令有：diskpart。这个是交互式的命令。能不能直接执行呢？

可以，后面可以跟一个脚本。

```
diskpart [/s <script>] [/?]
```

脚本的内容，就是把后面的输入的内容一行行写到脚本里就好了。



# 参考资料

1、

https://blog.csdn.net/qq_16559905/article/details/78575147

2、DOS命令格式化磁盘方法

https://jingyan.baidu.com/article/e9fb46e140a04a7521f766d4.html

3、windows下如何实现类似awk获取文件字段值功能

https://jingyan.baidu.com/article/0320e2c10ca7c31b87507bce.html