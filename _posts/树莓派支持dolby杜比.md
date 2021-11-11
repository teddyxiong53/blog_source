---
title: 音频之ac3音频格式
date: 2021-11-11 14:31:43
tags:
	- 音频

---

--

x600扩展板，用来给树莓派增加dolby支持。

```
 - 真正高清无损 完美音质 从树莓派HDMI信号里的声音解码分离
 - 支持模拟音频2.1声道输出
 - 支持数字音频5.1声道光纤和同轴输出
 - 彻底解决树莓派主板自带声卡音质差的问题
 - 可通过RCA莲花座或3.5mm 标准耳机插孔外接音响设备
 - 可实现音频同步分离输出，有PASS、2 0CH、5.1CH三种音频模式可选择
 - 支持杜比数码AC-3、DTS、LPCM等多种数字音频格式输出
 - 支持HDMI 输出（视频和音频信号与HDMI输入端完全相同)
```

修改config.txt

```
hdmi_force_hotplug=1       设定 HDMI 热拔插功能为开启状态
hdmi_group                            选择显示输出设备为 DMT 类型 (电脑显示器) 或 CEA 类型 (电视机)
hdmi_mode                            选择显示分辨率
```

hdmi_group=2           
(选择 "1" 为电视机, 选择 "2" 为电脑显示器)



如何用树莓派4b 实现DVD功能？

比如播放内存卡的hdr视频，就输出hdr信号，播放dolby vision视频就输出dolby vision信号。 只播放内存卡里面的，不考虑DVD光驱。



参考资料

1、	X600 扩展板

http://www.suptronics.com/Xseries/x600_cn.html