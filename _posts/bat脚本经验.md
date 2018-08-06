---
title: bat脚本经验
date: 2018-08-03 09:10:28
tags:
	- Windows

---



偶尔会需要用bat写一些Windows下用的脚本。都是很简单的。我不打算花时间去专门学习。

所以把用到的东西总结下来。



打印是echo

变量是用两个百分号包含起来。

定义变量是set a=“”

注释：rem和双冒号都可以。

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



https://blog.csdn.net/qq_16559905/article/details/78575147

