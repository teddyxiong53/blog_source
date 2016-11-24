---
title: xx-net工作分析
date: 2016-10-30 23:16:52
tags:
	- xx-net
---
使用GoAgent翻墙，GoGotest需要经常搜索新的Google IP进行替换才能使用，而xx-net的出现就是解决这个问题。
xx-net是集成了GoAgent和GoGotest的封包软件，能够根据当前网络状况搜索最新的Google IP，并且替换到GoAgent里。

文件调用流程分析。
XX-Net-master的文件目录如下所示。
```
code/ -- 源代码目录
data/ -- 程序用到的数据
README.md -- xx-net的说明介绍文档
start* 
start.bat -- 这个里面就一句话，调用了start.vbs。
start.vbs -- 这个就是xx-net的入口脚本。
SwitchyOmega/ -- chrome浏览器的插件，不用管。
```
code目录情况。
```
download.md
gae_proxy/ 
launcher/ -- 入口代码
LICENSE.txt 
python27/ -- python运行环境
update_version.txt
version.txt
x_tunnel/
xx_net.sh* 
```
那我们就从start.vbs脚本开始看。
这是一个VBScript脚本，语法没学过，不过脚本语言都差不多。
注意下面这句就是了，最后会调用到这个python脚本`launcher\start.py`。在`XX-Net-master\code\default\launcher`目录下。
```
strArgs = strExecutable & " " & quo & strCurrentPath & "\code\" & strVersion & "\launcher\start.py" & quo
```
`start.py`就是真正的入口了。
从实际效果看，执行start.vbs后，就会打开系统默认浏览器，然后在系统托盘那里生成一个X图标。
运行的log文件保存在`./data/launcher/launcher.log`里，每次运行都会清空之前的内容。
读log文件可以帮助我们梳理程序的流程。
下面摘录log里重要的部分。
```
Oct 31 21:41:56.838 - [INFO] use build-in openssl lib
Oct 31 21:41:56.841 - [INFO] start XX-Net 3.2.6
Oct 31 21:41:56.841 - [DEBUG] start confirm_xxnet_exit
Oct 31 21:41:57.871 - [DEBUG] good, xxnet:8087 cleared! -- 这个是检查端口的占用清空
Oct 31 21:41:58.885 - [DEBUG] good, xxnet:8085 clear!
Oct 31 21:41:58.885 - [DEBUG] finished confirm_xxnet_exit
Oct 31 21:42:00.668 - [INFO] module gae_proxy started  --启动gae 代理
Oct 31 21:42:00.668 - [INFO] start gae_proxy time cost:1782 ms
Oct 31 21:42:00.954 - [INFO] module x_tunnel started --启动x_tunnel模块
Oct 31 21:42:00.954 - [INFO] start x_tunnel time cost:286 ms
Oct 31 21:42:00.954 - [INFO] begin to start web control
Oct 31 21:42:00.958 - [INFO] launcher web control started. --启动浏览器
....中间略过部分信息
Oct 31 21:42:10.134 - [INFO] download https://raw.githubusercontent.com/XX-net/XX-Net/master/code/default/update_version.txt to D:\XX-Net-master\data\downloads\version.txt, retry:0
Oct 31 21:42:10.868 - [INFO] update to stable version 3.2.7
Oct 31 21:42:10.868 - [INFO] download  --这部分进行了版本检查，发现有新版本，就下载了新的版本。
```
最后程序的主循环在这里：
```
if config.get(["modules", "launcher", "show_systray"], 1):
        sys_tray.serve_forever()
else:
        while True:
            time.sleep(100)
```
`sys_tray`可以处理你在托盘图标上的鼠标事件，例如设置各种信息。




