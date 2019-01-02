---
title: Windows之在VirtualBox安装macos
date: 2018-03-23 20:23:21
tags:
	- Windows

---



之前用VMware安装过，特别卡。

现在看看用VirtualBox安装怎么样。

参考这个来做。也是别人安装好的vmdk文件。

https://www.youtube.com/watch?v=6PEp7p4cnzg&t=77s



镜像下载地址在这：http://www.briteccomputers.co.uk/forum/showthread.php?tid=4516

创建虚拟机，名字就叫MacOS。磁盘选择解压的vmdk文件。

先执行这些命令：

```
cd "d:\Program Files\Oracle\VirtualBox\"
VBoxManage.exe modifyvm "MacOS" --cpuidset 00000001 000106e5 00100800 0098e3fd bfebfbff
VBoxManage setextradata "MacOS" "VBoxInternal/Devices/efi/0/Config/DmiSystemProduct" "iMac11,3"
VBoxManage setextradata "MacOS" "VBoxInternal/Devices/efi/0/Config/DmiSystemVersion" "1.0"
VBoxManage setextradata "MacOS" "VBoxInternal/Devices/efi/0/Config/DmiBoardProduct" "Iloveapple"
VBoxManage setextradata "MacOS" "VBoxInternal/Devices/smc/0/Config/DeviceKey" "ourhardworkbythesewordsguardedpleasedontsteal(c)AppleComputerInc"
VBoxManage setextradata "MacOS" "VBoxInternal/Devices/smc/0/Config/GetKeyFromRealSMC" 1 
```

然后启动虚拟机。

进入到苹果的设置界面。

设置好账号。

然后安装辅助工具。

通过双击pkg文件进行安装。

安装后，关闭虚拟机。输入下面的命令：

```
cd "d:\Program Files\Oracle\VirtualBox"
VBoxManage modifyvm "MacOS" --firmware efi
VBoxManage setextradata "MacOS" VBoxInternal2/EfiGraphicsResolution 1920x1080 
```

再启动 虚拟机。这样就可以切换到1080P的显示了。

