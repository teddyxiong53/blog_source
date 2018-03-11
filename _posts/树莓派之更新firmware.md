---
title: 树莓派之更新firmware
date: 2018-03-09 22:49:19
tags:
	- 树莓派

---



网上说用rpi-update这个工具。

```
pi@raspberrypi:/lib/modules$ which rpi-update
/usr/bin/rpi-update
```

在这里。是个脚本。我们先看看内容是做了些什么。

先看看执行的内容：

```
pi@raspberrypi:~$ sudo bash -x /usr/bin/rpi-update
+ set -o nounset
+ set -o errexit
+ REPO_URI=https://github.com/Hexxeh/rpi-firmware
+ UPDATE_SELF=1
+ UPDATE_URI=https://raw.githubusercontent.com/Hexxeh/rpi-update/master/rpi-update
+ [[ unset == \u\n\s\e\t ]]
+ [[ unset != \u\n\s\e\t ]]
+ [[ unset != \u\n\s\e\t ]]
+ [[ unset == \u\n\s\e\t ]]
+ NOOBS_CHECK=1
+ BRANCH=master
+ ROOT_PATH=/
+ BOOT_PATH=/boot
+ WORK_PATH=//root
+ SKIP_KERNEL=0
+ SKIP_SDK=0
+ SKIP_REPODELETE=0
+ SKIP_BACKUP=0
+ SKIP_DOWNLOAD=0
+ SKIP_WARNING=0
+ WANT_SYMVERS=0
+ PRUNE_MODULES=0
+ RPI_UPDATE_UNSUPPORTED=0
+ JUST_CHECK=0
+ FW_REPO=https://github.com/Hexxeh/rpi-firmware.git
+ FW_REPOLOCAL=//root/.rpi-firmware
+ FW_PATH=/boot
+ FW_MODPATH=//lib/modules
+ FW_REV=
+ FW_REVFILE=/boot/.firmware_revision
+ '[' 0 -ne 0 ']'
+ [[ 0 -ne 0 ]]
+ echo ' *** Raspberry Pi firmware updater by Hexxeh, enhanced by AndrewS and Dom'
 *** Raspberry Pi firmware updater by Hexxeh, enhanced by AndrewS and Dom
+ [[ ! -d //root ]]
+ [[ 1 -ne 0 ]]
+ update_self
+ echo ' *** Performing self-update'
 *** Performing self-update
+ _tempFileName=/usr/bin/rpi-update.tmp
+ curl -Ls --output /usr/bin/rpi-update.tmp https://raw.githubusercontent.com/Hexxeh/rpi-update/master/rpi-update
++ stat -c %a /usr/bin/rpi-update
+ OCTAL_MODE=755
+ chmod 755 /usr/bin/rpi-update.tmp
+ cat
+ echo ' *** Relaunching after update'
 *** Relaunching after update
+ exec /bin/bash //root/.updateScript.sh
 *** Raspberry Pi firmware updater by Hexxeh, enhanced by AndrewS and Dom
```

直接更新吧。

```
pi@raspberrypi:~$ sudo bash  /usr/bin/rpi-update
 *** Raspberry Pi firmware updater by Hexxeh, enhanced by AndrewS and Dom
 *** Performing self-update
 *** Relaunching after update
 *** Raspberry Pi firmware updater by Hexxeh, enhanced by AndrewS and Dom
#############################################################
WARNING: This update bumps to rpi-4.14.y linux tree
Be aware there could be compatibility issues with some drivers
Discussion here:
https://www.raspberrypi.org/forums/viewtopic.php?f=29&t=197689
##############################################################
Would you like to proceed? (y/N)
 *** Downloading specific firmware revision (this will take a few minutes)
  % Total    % Received % Xferd  Average Speed   Time    Time     Time  Current
                                 Dload  Upload   Total   Spent    Left  Speed
100   168    0   168    0     0     76      0 --:--:--  0:00:02 --:--:--    76
100 55.3M  100 55.3M    0     0  27515      0  0:35:10  0:35:10 --:--:-- 42879
 *** Updating firmware
 *** Updating kernel modules


 *** depmod 4.14.24-v7+
 *** depmod 4.14.24+
 *** Updating VideoCore libraries
 *** Using HardFP libraries
 *** Updating SDK
 *** Running ldconfig
 *** Storing current firmware revision
 *** Deleting downloaded files
 *** Syncing changes to disk
 *** If no errors appeared, your firmware was successfully updated to bdb826a8db75ba36d754bd71fb64d3905d3bd026
 *** A reboot is needed to activate the new firmware
```



#更新头文件

现在kernel的版本是

```
pi@raspberrypi:~$ uname -r
4.14.24-v7+
```

我还没有安装对应版本linux-headers。所以编译的驱动程序没法跑的。

查询一下有没有官方的对应的发布包。

```
pi@raspberrypi:~$ dpkg-query -s linux-headers-$(uname -r)
dpkg-query: package 'linux-headers-4.14.24-v7+' is not installed and no information is available
Use dpkg --info (= dpkg-deb --info) to examine archive files,
and dpkg --contents (= dpkg-deb --contents) to list their contents.
```

没有。

那就只能自己编译kernel来得到了。

从这里下载压缩包。

https://github.com/raspberrypi/linux/tree/rpi-4.14.y

我先跟4.4.y的对比一下，看看改了什么。

```
1、从压缩包大小上，大了30M。4.4的是161M，现在是190M。
2、对比了一下，不少的文件改动还挺大的，以后慢慢看。
```

把zcat /proc/config.gz > ~/.config

然后把这个.config拷贝到rpi-4.14.y目录里。

make headers_install 。这个不对，这个是给编译应用的头文件。

我还是需要先make modules。

然后再编译一个我自己的模块，然后用insmod试一下，现在正常了。







