---
title: 渗透所需windows知识
date: 2018-12-30 21:41:38
tags:
	- windows

---



windows系统目录一直不太了解。

现在看看。

syswow64和system32是什么关系。

system32目录包含：

1、windows系统文件。包括dll文件。exe文件。

有时候第三方软件也会安装到这里。

system32下面放的是64位的。

当你需要手动防止dll文件的时候，你必须搞清楚这些目录之间的关系。

wow是windows  32 on windows 64的缩写。

 允许windows在64位的机器上运行32位的程序。

所以这名字起得比较别扭，名字里有32的，是64位的。

名字里有64的，是32位的。



windows系统，的确有让程序员难以掌控的感觉。



```
C:\ProgramData\Microsoft\Wlansvc\Profiles\Interfaces
	这个目录下面放的是wifi相关配置信息。xml写的。
	从这个目录下进行分析，可以得出连接过的wifi的密码情况。
```



windows7 的windows目录

```

```



# 常用管理工具

```
msconfig
	管理启动项的。
sysdm.cpl
	这个是打开计算机属性那个窗口。
	在c:\windows\system32目录下。
	后面的cpl是control panel的缩写。
	可以修改计算机名字。
perfmon.msc
	这个的打开性能监视器。
regedit
	打开注册表。是一个分层数据库。托管了所有的windows系统配置。
hdwwiz.cpl
	设备管理器。hardware wizard control panel。
	devmgmt这个也是一样的。
taskmgr
	打开任务管理器。
gpedit.msc
	本地组策略编辑。
mstsc
	远程桌面。
shutdown -s -t 60
	60秒后
control
	这个就是打开控制面板的。
systeminfo
	查看系统信息。例如上电时间。
	可以看到安装时间，卡机时间点，
	安装的补丁情况。
	网卡情况。
tasklist
	应该是taskadmin 的子命令。
```

# 基础命令

## dir

要在基本的cmd里运行，很多选项才有用。powershell里有些不能正常工作。

```
dir /? 查看帮助
dir /s 递归查看所有子目录。
dir /a 查看所有的文件。
dir /ah 只查看隐藏文件。
dir /w 用紧凑方式显示。
dir /p 分页方式显示，效果类似less。

```

```
echo 1 >1.txt 这样来创建文件吧。
md xx  创建目录。
rd xx  删除目录。
copy src dst
move src dst
del *.c  删除所有c文件。
	不能删除文件夹。
deltree 递归删除目录。
format 相当于fdisk，别用。
ren 重命名
type 相当于cat，把内容打印处理。

```

## 查找命令

```
dir /s | findstr txt 这样可以找出所有的txt文件。
```





https://www.jb51.net/article/39902.htm

# net 命令

这个命令其实很强大，可以做很多事情。

> net /help

这样查看net的帮助信息。

可以看到子命令有：

```
accounts 
computer 
config 
continue 
file 
group 
help 
helpmsg 
localgroup 
pause 
session 
share 
start 
statistics 
stop 
time 
use 
user 
view                   
```

查看子命令的帮助信息：

> net xx /help



## accounts

net accounts命令更新用户的账号数据库。对所有的账号修改密码和登陆要求。

不带参数的时候，是显示当前的密码、登陆限制、域信息这些设置。

例如这样：

```
强制用户在时间到期之后多久必须注销?:     从不
密码最短使用期限(天):                    0
密码最长使用期限(天):                    42
密码长度最小值:                          0
保持的密码历史记录长度:                  None
锁定阈值:                                从不
锁定持续时间(分):                        30
锁定观测窗口(分):                        30
计算机角色:                              WORKSTATION
命令成功完成。
```

net accounts命令要正常工作，需要满足2个条件：

1、密码和登陆要求只有在用户账号已经建立后才能生效。

2、Net Logon Service必须在domain里所有的服务器上运行（如果这个服务器参与了verify的话）。这个服务器在windows启动的时候自动启动。

可以跟的参数：

```
/forcelogoff:10   
/minpwlen:10
/maxpwage:10
/minpwage:10
/uniquepw:8
/domain
```

## computer

可以跟2个参数：

```
/add
/del
```

用来从一个domain里添加或者删除计算机。

这个命令只有在windows NT 服务器上才有用。



## config

有2个子命令，都是查看性质的。

```
server  查看本机作为server相关情况。
workstation 查看本机作为workstation的相关情况。
```

## continue

这个表示继续某个服务，后面带一个参数，就是服务的名字。

没有什么用。



## file

查看或者关闭文件fd。

## group

这个只有domain controller才能做的。没什么用。

## localgroup

不带参数，表示查看本地用户组有哪些。

```
/add
/del
```

## session



```
/list
/delete
```

## share

这个很重要。是进行网络挂载用的。

当从远程计算机浏览本地计算机时，将不显示以字符 $ 结尾的共享资源名。

创建一个共享：

```
net share DataShare=c:/test_share /remark:"this is a share test"
```

删除这个共享：

```
net share DataShare /delete
```



## statistics

统计。

```
net statistics workstation
net statistics server 作为server，所有网络数据情况。
```

## time

## use

## user

这个管理用户的。

## view



```
%temp%
	这个是临时文件目录。
	等于：
	C:\Users\Administrator\AppData\Local\Temp
	清除临时文件，就清空这个目录就好了。
	
```

这样就可以查看当前工作组下面的所有机器。

```
net view /domain:WorkGroup
```



知道对方的计算机名字，怎么得到ip地址？

```
有两种方法：
1、ping hostname 就可以得到ip。
2、nbtstat.exe -a hostname
```



# 操作步骤

windows查看当前登陆的用户有哪些

> net user

开机时长是多久

> systeminfo

进程有哪些。

> tasklist



#windows命令行参数语法

cmd 命令里的 短横线 斜杠有什么区别？

dos的命令，是斜杠来带参数，而windows也从unix那边弄了一些命令行工具过来。这些工具就是用短横线做参数开头的。



Windows 用反斜杠（“\”）的历史来自 DOS，而 DOS 的另一个传统是用斜杠（“/”）表示命令行参数，比如：

> cd %SystemDrive%
> dir /s /b shell32.dll

用斜杠表示命令行参数是兼容性原因。

这个问题最初起源自 IBM。

IBM 在最初加入 DOS 开发时贡献了大批工具，它们都是用斜杠处理命令行参数的。

而这个传统源自于 DEC/IBM，比如当年的 VMS 就是用斜杠处理命令行参数，它的目录分隔符是美元符（“$”）。顺便说一句，这个传统也被部分地继承进了 DOS 和 Windows 体系，日文版的 Windows 就把反斜杠在屏幕上显示为“¥”，虽然实际上还是反斜杠。

如今的 Windows 内核在处理路径时确实可以同时支持斜杠和反斜杠。

很多时候我们看到用斜杠时出错，是因为应用程序层面的原因。

比如 cmd.exe 就不支持用斜杠表示路径，而PowerShell.exe 支持，也正因为这个原因，PowerShell 开始转而使用减号作为命令行参数的起始符。





这篇文章消化一下

https://my.oschina.net/u/2308739/blog/546956?p={{currentPage+1}}



参考资料

作为程序的参数，多数程序对于 - 和 / 的处理是一样的，都是引导参数。有些程序必须是 - 不能用 /，反之亦然。

https://zhidao.baidu.com/question/448002470.html?qbl=relate_question_0

Windows 的路径中表示文件层级为什么会用反斜杠 ‘\’，而 UNIX 系统都用斜杠 ‘/’？

https://www.zhihu.com/question/19970412

SYSTEM32 下DLL文件的简单说明

https://blog.csdn.net/Delete123/article/details/2287264?utm_source=blogxgwz4

Windows学习总结（17）——Windows 15个重要运行命令

https://blog.csdn.net/u012562943/article/details/78312396