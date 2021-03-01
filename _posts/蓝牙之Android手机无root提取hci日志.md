---
title: 蓝牙之Android手机无root提取hci日志
date: 2021-02-23 13:58:30
tags:
- 蓝牙
---

--

需要提取安卓手机里的hci日志。但是root又很麻烦。想到这个是一个常见的需求。谷歌不可能要求大家都去root手机。

确实是有办法在不root的前提下，提取手机里的hci日志的。

具体做法如下：

1、下载最新的adb。

```
wget https://dl.google.com/android/repository/platform-tools-latest-linux.zip
```

解压。然后把当前目录添加到PATH环境变量里。

需要尽量新的版本的adb。至少我在1.0.31版本上是不能正常使用的。

2、保证手机已经打开了开发者模式，并勾选了hci日志生成选项。

3、执行adb bugreport xx命令。xx是生成的压缩文件的名字，随便写。这个命令会在当前目录生成一个zip压缩文件。生成需要一点时间。

```
/data/user_de/0/com.android.shell/files/bugreports/bugreport-2021-02-23-13-56-29.zip: 1 file pulled, 0 skipped. 13.2 MB/s (4375397 bytes in 0.316s)
```

4、解压生成的xx.zip文件。

里面有这些文件

```
Archive:  xx.zip
  inflating: version.txt             
  inflating: FS/data/log/bt/btsnoop_hci.log  
  inflating: FS/data/log/bt/btsnoop_hci.log.last  
  inflating: bugreport-2021-02-23-13-56-29.txt  
  inflating: main_entry.txt          
  inflating: dumpstate_log.txt  
```

btsnoop_hci.log 这个就是的。

用wireshark打开就可以看了。



参考资料

1、[Linux] Update adb & fastboot to the latest version

https://androideputies.com/2016/12/11/linux-update-adb-fastboot-to-the-latest-version/