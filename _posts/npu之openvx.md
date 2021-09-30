---
title: npu之openvx
date: 2021-09-07 19:57:33
tags:
	- npu

---

--

OpenVX 是个开放、免版税的，

用于跨平台计算机**视觉应用加速**的标准。

OpenVX 实现了计算机视觉处理中**性能和能耗**方面的优化，

特别是嵌入式和**实时应用**案例中起到重要作用，

例如面部、身体和动作跟踪，智能视频监控，高级驾驶协助系统（ADAS），物体和场景重建，增强现实，视觉检测，机器人学等等。

除了 OpenVX 规范，Khronos 还开发了一整套一致性测试和采用者计划，

让标准执行者可以测试他们的执行，**如果通过一致性测试即可使用 OpenVX 标识**。

树莓派目前已经支持 Khronos OpenVX 1.3 API 了。下面来介绍一下如何在树莓派4B上安装开源 OpenVX 1.3 库。

https://github.com/KhronosGroup/OpenVX-sample-impl

这个仓库是openvx的一个实现的例子。但是不能算是参考实现。

https://github.com/kiritigowda/openvx-samples.git

这个是测试用的。

这个是教程。

https://github.com/rgiduthuri/openvx_tutorial

我给自己一个任务：用openvx的接口来实现音频的yesno语音识别的概念。



https://www.khronos.org/assets/uploads/developers/library/2017-openvx-12-overview/Khronos-OpenVX-Webinar_Sep2017.pdf



参考资料

1、

https://shumeipai.nxez.com/2020/07/11/openvx-api-for-raspberry-pi.html

2、

https://dfc.pub/yi-gou-ji-suan/ru-he-cheng-wei-yi-ming-yi-gou-bing-xing-ji-suan-gong-cheng-shi/