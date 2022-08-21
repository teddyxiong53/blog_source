---
title: yodaos之jsruntime在buildroot-qemu里运行
date: 2022-08-21 20:32:08
tags:
	- yodaos

---

--

对我比较有价值的，就是jsruntime。

鉴于官方提供的仓库没法直接使用。

我决定在qemu里弄一个测试环境。这样测试起来也比较方便。

就用qemu x86_64的。

就在package下面弄一个rokid的目录。

看jsruntime依赖了这些东西：

```
DEPENDS:=+libstdcpp +android-system-core +shadow-node \
	   +opus +speech +vol_ctrl +wpa_ctrl +ota_unpack \
	   +lumenlight +libffmpeg-audio-dec +librplayer +input-event \
	   +aliyunloglite +flora +httpsession +httpdns +property
```

一个个看

```
android-system-core
	对应这个目录。
	$(ROKID_DIR)/3rd/android_lib/system/core
	
```



跟buildroot同一级目录，弄一个buildroot-yodart目录。



参考资料

