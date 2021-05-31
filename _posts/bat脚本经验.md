---
title: bat脚本经验
date: 2018-08-03 09:10:28
tags:
	- Windows

---



偶尔会需要用bat写一些Windows下用的脚本。都是很简单的。我不打算花时间去专门学习。

所以把用到的东西总结下来。

bat在运行过程中还可以修改，修改实时生效的。



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

# 学习方法

对于要了解id知识点。用xx /?就可以看到帮助信息。

# 注释

有两种，一种是rem。一种是双冒号。

二者的区别是：

rem注释掉的内容，是可以回显的。

双冒号的则不会回显。

双冒号是单冒号的一种特殊用法。

```
:xxx
	这种表示label
:后面跟一个特殊字符。
	这就构成一个非法的标号。
	解释器不识别，就变成了注释的效果了。
```

优先使用rem。

# 打印

就是echo。

打印一个空行：

```
echo.
	注意后面的.跟echo之间没有空格。
```

echo的其他用途。

对于需要用户回复的命令，可以用echo给一个答复。

```
echo y | del 1.txt
```

创建一个文件

```
echo ""> 1.txt
```

# 替换的默认的pause提示

pause默认的提示是按任意键继续。

我们要输出自己的怎么做？

```
echo 我的提示
pause > nul
```



# 条件判断

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



```
if "%1"=="/a" echo "第一个参数是a"
```

```
if /i "%1" equ "/a" echo "第一个参数是a"
```

判断文件的存在

```
if exist 1.bat echo "1.bat exists"
```

# 错误码



# 循环

for循环。

```
在cmd窗口中：for %I in (command1) do command2 
在批处理文件中：for %%I in (command1) do command2
```

这个可以比较复杂。

```
#对当前目录下，所有txt文件进行搜索包含abc。
find %%i in (*.txt) do find "abc" %%i
```

```
# 递归搜索当前目录及其子目录
find /r .\ %%i in (*.txt) do find "abc" %%i
```



# 获取命令执行的结果给变量

只能借助for循环来做了。自己替换一下就好了。

```
for /F %%i in ('find "network" wpa_supplicant.conf') do ( set result=%%i)
echo %result%
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

可以用timeout来做。下面这个表示sleep 1s的效果。只能是整数。

```
timeout.exe /t 1
```



# 定义函数

```
@echo off
SETLOCAL
CALL :Display 5 , 10
EXIT /B %ERRORLEVEL%
:Display
echo The value of parameter 1 is %~1
echo The value of parameter 2 is %~2
EXIT /B 0
```

嵌套调用

```
@echo off

call :total
EXIT /B %ERRORLEVEL%

:total
CALL :Display 5 , 10
call :Display 1,2
exit /b 0

:Display
echo The value of parameter 1 is %~1
echo The value of parameter 2 is %~2
exit /b 0
```



# 环境变量

```
cmd的环境变量操作：
set 查看当前的环境变量。
set A=1 设置环境变量。
set A 查看某个环境变量。
这个在powershell下面是不行的。
```

# start

启动外部程序。然后会等外部程序执行完，再继续往下走。

```
start calc.exe
```

# call

执行另外一个bat文件。有的应用用start调用出错，也可以改成用call调用。



# choice

等待用户做出选择。

不带任何参数，是给yes和no给用户选择。

# assoc和ftype

这2个命令作用有关联。

```
assoc 
	不带任何参数，则是列出系统当前的文件的关联情况。
	
```



# attrib

修改文件的属性，类似chmod。

# defined

查看是否定义过某个变量。一般用来检查环境变量是否设置了。

```
if defined JAVA_HOME goto findJavaFromJavaHome
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



# 修改标题

```
title "我的bat工具"
```

# 时间日期

查看当前日期

```
date /t
```

查看当前时间，只有hour和minute。

```
time /t
```

# find

```
find /c /n "123" 1.txt
```

# &和&&

& 表示顺序执行，即使前面的失败了。后面也仍然执行。

&&则前面的失败了，后面的不执行。

# ||

前面的成功了，后面的就不执行。

# 参数

```
依次用%0 %1到%9 来表示。
%0 表示程序本身的名字。
%* 表示从%1开始的所有参数。
```

对于参数的其他处理

波浪线有展开的意思。

```
%~1 这样表示把第一个参数的引号去掉（如果有的话）
%~f1 表示把参数展开成完整的文件路径（基于当前目录进行展开的，即使文件不存在）
%~d1 d表示驱动器。例如当前D盘，则得到D:
%~p1 p表示path。当前d:\work\test\bat
%~n1 把参数1扩展成文件名。去掉后缀名。
%~x1 得到后缀名。
%~s1 也是扩展成文件名。不知道跟f的区别是啥。
%~a1 获取文件的属性。类似rwx这样的一串。
%~t1 获取文件的修改时间。
%~z1 获取文件的大小。

上面的可以组合使用。
%~dp1 
%~nx1 
```

查看上面这些信息，可以用call /?来查看。



```
ver 查看系统版本
vol 查看当前磁盘的卷标
label c:system 把磁盘的卷标改成system
```

# 格式化磁盘

现在有一个需求，就是批量格式化SD卡，然后拷贝一些文件进去。

这个可以分解为：

1、格式化磁盘。

dos下面的命令有：diskpart。这个是交互式的命令。能不能直接执行呢？

可以，后面可以跟一个脚本。

```
diskpart [/s <script>] [/?]
```

脚本的内容，就是把后面的输入的内容一行行写到脚本里就好了。

# gradle.bat分析

这个是Android的编译脚本。不算太复杂。

可以学习一下。

如果不是调试模式，关闭echo。

```
@if "%DEBUG%" == "" @echo off
```

```
if "%OS%"=="Windows_NT" setlocal
```

开头和结尾，加上setlocal和endlocal。则本bat内部的修改，不会对外部产生影响。

```
set DIRNAME=%~dp0
```

获取当前路径。

```
if "%DIRNAME%" == "" set DIRNAME=.
```

确保路径不为空。

```
set CMD_LINE_ARGS=%*
```

拿到脚本的所有参数。



# 批处理脚本运行出现"The system cannot write to the specified device"错误

我的脚本在我的电脑上运行正常，发给生产用，就不正常，提示标题里的这个错误。

脚本里有中文提示。脚本用utf8编码的。

改成ANSI编码就好了。

脚本头部加上这个。另存为，编码选择为ANSI。

```
chcp 936
```

# 压缩和解压

makecab这个自带的命令可以压缩。这个不行，还挺麻烦。

expand命令可以解压。

用7zip就可以了。

安装7zip。然后把7z.exe和7z.dll拷贝到当前目录下，就可以随意使用了。

压缩

```
7z.exe a xx.zip xx
```



# 参考资料

1、

https://blog.csdn.net/qq_16559905/article/details/78575147

2、DOS命令格式化磁盘方法

https://jingyan.baidu.com/article/e9fb46e140a04a7521f766d4.html

3、windows下如何实现类似awk获取文件字段值功能

https://jingyan.baidu.com/article/0320e2c10ca7c31b87507bce.html

4、

https://juejin.im/post/6844903910856114190

5、BAT命令高级技巧

https://blog.csdn.net/mezheng/article/details/7961818

6、

https://blog.csdn.net/peng_cao/article/details/73999076

7、

这个网站讲解bat非常好。

https://www.tutorialspoint.com/batch_script/batch_script_functions_with_parameters.htm