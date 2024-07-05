---
title: openharmony（1）
date: 2024-06-08 15:10:09
tags:
      - 鸿蒙

---



# 先尝试在树莓派3b上跑起来



https://hazhuzhu.com/embedded/notes-of-porting-openharmony-on-raspberrypi-4b.html

# 下载代码编译

https://blog.csdn.net/u010018991/article/details/109100925

```
cd ~/harmony
repo init -u https://gitee.com/openharmony/manifest.git -b master --no-repo-verify
repo sync -j16
```

有488个仓库。

