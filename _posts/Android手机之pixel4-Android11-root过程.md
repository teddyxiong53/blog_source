---
title: Android手机之pixel4-Android11-root过程
date: 2020-12-28 10:52:30
tags:
- 手机
---

1

## 总结

这个是我做后面的步骤，碰到的问题。

1、fastboot一定要下载最新的版本。

我因为电脑上很久之前安装了fastboot，就没有重新安装最新版本。

结果碰到了几个问题

```
1、fastboot不支持flashing命令。
	这个我用安装的华为手机助手里的fastboot来做了。
2、fastboot flash boot magisk.img
	这个命令会失败。
	因为当前手机的系统是AB系统的。而我的fastboot因为版本太老，根本不知道ab系统的是什么。
	所以会去找boot分区，结果找不到，报了失败（而我没有留意到这个失败信息，导致我很困惑为什么烧写了分区没有起作用）。
	这个也是用华为的fastboot就可以了。
```



## 解锁bootloader

先点击build号码7次，打开开发者选项。

然后搜索oem解锁。允许解锁。这个比国内手机操作简单。

## 进入bootloader模式	

然后用数据线把手机连接到电脑。

如果识别到手机，执行：

```
adb reboot bootloader
```

等手机重启到bootloader模式后，执行：

```
fastboot flashing unlock
```

注意fastboot要新一些的，老的没有flashing这个子命令。

执行命令后，手机这边界面有变化。

需要你按一下音量减（因为从文字看，当前显示是不要unlock，按一下之后，就切换到可以unlock），然后按一下电源键（相当于确认）。

然后会黑屏一下，然后就可以看到已经是解锁状态了。

然后我们重启手机，执行这个命令重启。

```
fastboot reboot
```

## 下载magisk manager

https://github.com/topjohnwu/Magisk/releases/download/manager-v8.0.2/MagiskManager-v8.0.2.apk

下载这个apk文件。

## 提取boot.img文件

到这里下载

https://developers.google.com/android/ota

我手机当前版本是RP1A.200720.009

![image-20201228111042794](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201228111042794.png)

下载这个ota包。1.6G。

解压压缩包，从里面得到payload.bin文件。

![image-20201228111935488](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201228111935488.png)

我们需要从里面解压出boot.img文件。

payload.bin不能直接解压，需要借助工具。

payload.bin里面有3个重要的东西：

system.img、boot.img、vendor.img。

root的方式，可以分为两类：使用twrp和不使用twrp。

现在大多使用不用trwp的方式。

因为很多手机找不到可用的twrp包。

**Payload Dumper Tool**

这个工具的下载地址：

https://www.mediafire.com/file/pslxh616isribx6/payload_dumper.zip/file

是用python写的脚本。

安装一下依赖。

```
pip install -r requirements.txt
```

把payload.bin拷贝到当前目录下，执行命令：

```
python payload_dumper.py payload.bin
```

![image-20201228112531190](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201228112531190.png)

在output目录下生成这些文件。

![image-20201228112545934](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201228112545934.png)

我们就得到了boot.img文件。

## 把magisk打包到boot.img里，并写入

把boot.img发送到手机上的/sdcard/Download目录下。

```
adb push boot.img /sdcard/Download
```

Android11的，需要使用最新的调试版本（金丝雀版本）的magisk app。

从这里下载就好了。

https://www.droidwin.com/fix-magisk-patched-boot-img-issues-android-11/

安装到手机

```
adb install app-debug.apk
```

然后手机上打开magisk软件，点击安装，选择打包补丁。

会把boot.img自动打包进magisk的文件。

得到一个magisk_patched_xx.img这样的文件。

我们把这个文件拉取到电脑上。

```
adb pull magisk_pathed.img ./
```

然后让手机进入到fastboot模式

```
adb reboot bootloader
```

在fastboot模式下，执行

```
fastboot flash boot magisk_patched.img
```

这个就是把打包后的boot镜像，写入到boot分区。

然后重启手机

```
fastboot reboot
```

就可以看到root已经完成了。









参考资料

1、

https://www.droidwin.com/unlock-bootloader-google-pixel-devices/

2、

https://www.droidwin.com/root-pixel-4-4a-11/

3、How to Extract payload.bin and get stock boot image file

https://www.droidwin.com/extract-payload-bin-stock-boot-image/