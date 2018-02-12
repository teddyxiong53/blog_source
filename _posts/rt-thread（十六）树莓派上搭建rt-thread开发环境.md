---
title: rt-thread（十六）树莓派上搭建rt-thread开发环境
date: 2018-02-07 09:59:44
tags:
	- rt-thread

---



春节期间还是想继续研究rt-thread。之前都是在台式机上结合虚拟机来做的。

回家就得再笔记本上做。笔记本的性能太差，跑虚拟机很卡。所以打算把我的树莓派上搭建一个rt-thread的开发环境。这样后续有外出需求时，也可以比较方便地继续研究。

整个过程跟《rt-thread（一）Ubuntu下用qemu仿真》类似。不过也有几点要注意的。

1、安装arm-none-gcc工具链。虽然树莓派上的默认gcc就是针对arm的。但是还是需要安装一下，不然会出现newlib的头文件找不到。

2、安装scons。用apt-get来安装。pip安装会有些东西没有。

3、把我的当前开发目录直接拷贝到树莓派上。

4、编译运行都可以。

树莓派的编译速度也是非常慢的。

春节期间，主要以阅读代码为主，调试只是为了验证疑问。

5、搭建git环境。在笔记本上把我的博客都同步下来。这样博客就可以继续写了。





# 回家之后的情况

1、发现没有带串口线，也没有带网线。

现在没法连接到树莓派上。

2、现在蹭到了一个网，是tplink的，没法破解admin密码。但是有连接WiFi的密码。

3、我现在希望把U盘里的ext4分区挂载到Windows下，修改里面WiFi连接的部分。然后用nmap扫描的方式发现树莓派的ip地址。

http://www.fs-driver.org/download.html

下载这个软件。可以识别ext分区。

不行。我现在只好把笔记本切到kali Linux下去做了。

4、我在kali Linux下，可以自动挂载U盘下的分区。修改/etc/network/interfaces文件。

然后选择连接到我笔记本上插着的小米WiFi上。这样是可以的。但是无线的不稳定。

我又在家里发现了网线。所以这个就不再折腾了。

5、把笔记本的有线的ip固定为192.168.0.1，我之前的树莓派就一直是配置的自动获取ip。现在就是不知道树莓派到底被分配了哪个ip。只好把192.168.0这个网段扫描一遍，不想下载软件。我是用手机共享网络来上网的。所以找了一个bat脚本来扫描。内容如下：

```
@echo off
color F0
rem 设置窗口背景色为白色，文字颜色为黑色
title 批处理扫网段(By TaoGe)
rem 设置窗口标题
echo.
echo 输入你要扫描的IP段，直接按回车则为192.168.16：
set /p IpDuan=
rem 将用户输入赋值给IpDuan变量
if "%IpDuan%"=="" (set IpDuan=192.168.16)
rem 判断IpDuan变量是否赋值，如果为空，则赋值为192.168.16
echo 输入你要扫描的IP起始位，直接按回车则为1：
set /p QiShi=
rem 将用户输入赋值给QiShi变量
if "%QiShi%"=="" (set QiShi=1)
rem 判断QiShi变量是否赋值，如果为空，则赋值为1
echo 输入你要扫描的IP结束位，直接按回车则为255：
set /p JieShu=
rem 将用户输入赋值给JieShu变量
if "%JieShu%"=="" (set JieShu=255)
rem 判断JieShu变量是否赋值，如果为空，则赋值为255
echo 起始IP：%IpDuan%.%QiShi%  
rem 显示起始IP
echo 结束IP：%IpDuan%.%JieShu%  
rem 显示结束IP
echo ======================================================= >>Ping-%IpDuan%.txt
rem 记录分割线
echo 开始时间：%date%%time% >>Ping-%IpDuan%.txt
rem 记录开始时间
echo 起始IP：%IpDuan%.%QiShi% >>Ping-%IpDuan%.txt  
rem 记录起始IP
echo 结束IP：%IpDuan%.%JieShu% >>Ping-%IpDuan%.txt 
rem 记录结束IP
echo 正在扫描，请等待...
echo 提前结束请直接关闭窗口
@for /l %%n in (%QiShi%,1,%JieShu%) do @ping -w 600 -n 1 %IpDuan%.%%n|find  /i "ttl" >>Ping-%IpDuan%.txt
rem 开始执行
echo 结束时间：%date% %time%  >>Ping-%IpDuan%.txt
rem 记录结束时间
echo ======================================================= >>Ping-%IpDuan%.txt
rem 记录分割线
echo 扫描完毕,按任意键退出...&pause>nul
```

最后发现被分配了192.168.0.109的ip。用ssh连接过去。正常。



