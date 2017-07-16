---
title: Android之AVD
date: 2017-07-16 12:24:15
tags:

	- Android

---

Android的是基于qemu的。

# 1. 创建AVD

新建一个Pixel的AVD，选择这个是因为我比较习惯1080P的屏幕尺寸。

AndroidStudio会使用默认的镜像来创建这个AVD，你可以可以自己从这个地址去下载对应的镜像。

http://dl.google.com/android/repository/sys-img/google_apis/x86_x64-23_r21.zip

目前就使用默认的。

到对应的目录下可以看到3个文件。

```
$ ls -l
total 1
drwxr-xr-x 1 Administrator 197121   0 七月 16 12:25 metrics/
drwxr-xr-x 1 Administrator 197121   0 七月 16 12:34 Pixel_API_23.avd/
-rw-r--r-- 1 Administrator 197121 129 七月 16 12:35 Pixel_API_23.ini
```

Pixel_API_23.avd目录下是sdcard.img、userdata.img文件。还有一个config.ini文件。

# 2. AVD中SD卡的文件管理

在AS的Tools> Android Device Monitor 界面里。

我尝试放入一个文件到SD卡目录。结果打印了这个。

```
[2017-07-16 13:14:40] Failed to push the item(s).
[2017-07-16 13:14:40] null
```



# 3. logcat里狂打印AudioFlinger错误

进入到设置界面里的Google，这个应该是要监听Google now的“ok Google”导致的。关闭这个功能就好了。









