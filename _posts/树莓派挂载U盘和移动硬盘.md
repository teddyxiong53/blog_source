---
title: 树莓派挂载U盘和移动硬盘
date: 2016-11-18 22:40:14
tags:
	- 树莓派
---
树莓派的SD卡不够大，所以就希望可以把U盘和移动硬盘挂上去用。
树莓派在外接U盘时，不会自动挂载，需要手动用mount命令来挂载。
我们先插入一个U盘，这个U盘是16G的，格式化为fat32格式。只有一个分区。插入到树莓派上，看`/dev`下面的设备，有
```
pi@raspberrypi:~ $ ls /dev/sd
sda   sda1  
```
我们进行挂载，U盘是懒人听书的，所以命名为lrts：
```
sudo mkdir /mnt/lrts
sudo mount -o uid=pi,gid=pi /dev/sda1 /mnt/lrts
```
我们把uid和gid指定为pi，不然挂载上去后，就是属于root用户的，不方便使用。
不用的话，就可以用命令吧U盘卸载。
```
sudo umount /mnt/lrts
```
现在再插入一个U盘，这个U盘有2个分区。新插入的第二个U盘被分配为sdb。我们把分区都挂载上来看看。
```
pi@raspberrypi:~ $ ls /dev/sd
sda   sda1  sdb   sdb1  sdb2  

pi@raspberrypi:/mnt $ sudo mkdir teddy0
pi@raspberrypi:/mnt $ sudo mkdir teddy1
pi@raspberrypi:/mnt $ sudo mount -o uid=pi,gid=pi /dev/sdb1 /mnt/teddy0
pi@raspberrypi:/mnt $ sudo mount -o uid=pi,gid=pi /dev/sdb2 /mnt/teddy1
pi@raspberrypi:/mnt $ ls
lrts  teddy0  teddy1
pi@raspberrypi:/mnt $ cd teddy0
pi@raspberrypi:/mnt/teddy0 $ ls
pi@raspberrypi:/mnt/teddy0 $ cd ..
pi@raspberrypi:/mnt $ cd teddy1
pi@raspberrypi:/mnt/teddy1 $ ls
EFI  install  live
pi@raspberrypi:/mnt/teddy1 $ 
```
现在把2个U盘都拔掉，因为usb口这里比较拥挤了。把移动硬盘插入看看。
因为只有移动硬盘，所以移动硬盘被命名为sda了。也只有一个分区。可以正常访问。电源驱动能力还够。
```
pi@raspberrypi:/mnt/ydyp $ ls
Autorun.inf       D          E            
BaiduYunDownload  diskimg    F            
Bookmark.html     Downloads  FeigeDownload
```







