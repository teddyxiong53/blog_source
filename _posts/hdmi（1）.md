---
title: hdmi（1）
date: 2022-10-13 13:46:33
tags:
	- hdmi

---

--

最近的工作涉及到较多的hdmi相关的概念。

在这篇文章统一进行学习梳理。



# SCDC

SCDC：State and Control Data Channel；

 VSDB：Vendor-Specific Data Block



参考资料

1、

https://blog.csdn.net/lxm920714/article/details/114119926

# RSEN

The [HDCP specification](https://www.digital-cp.com/sites/default/files/HDCP_Specification Rev1_3.pdf) explained the use of HPD (hot-plug detection) and RSEN (receiver sense): 

When HPD is high, the source reads EDID through I2C from the sink. 

Then when the RSEN goes high, the source turns on the TMDS signal in an appropriate format.



参考资料

1、

https://electronics.stackexchange.com/questions/375077/hdmi-receiver-sense-logic-and-tmds-capacitor-coupling

# 参考资料

1、HDMI设计3--HDMI 1.4/2.0 Transmitter Subsystem IP

https://blog.csdn.net/Archar_Saber/article/details/123018265

2、hdmi设计系列文章

https://blog.csdn.net/archar_saber/category_11616808.html