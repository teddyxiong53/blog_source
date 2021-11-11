---
title: hdmi接口协议分析
date: 2021-11-09 14:25:43
tags:
	- hdmi

---

--

hdmi一般的连接：

```
机顶盒 --> TV/显示器
```

传输基于的是TMDS(Transition Minimized Differential Signaling)协议。

![hdmi_block](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20170612214716459)



HDMI cable由3组差分信号传输TMDS数据，1组差分信号传输clock。

此外，HDMI还有一个DDC的通道连接到sink的EDID。

CEC和HEAC都是HDMI的可选协议。

![hdmi_pin](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20170612215851100)

HDMI定义了五种类型的connector，上图是最常见的type A。

1-9是TMDS data传输用到的引脚，共有三组；
10-12是TMDS clock传输用到的引脚，共有一组，TMDS clock就是pixel clock；
13是CEC引脚，一种消费电子兼容的传输协议；
14是保留引脚；
15,16是DDC的引脚，DDC是基于I2C协议传输，故引脚为SCL和SDA；
17是接地；
18是+5V power；
19是HPD引脚，用于建立连接。



HDMI传输由三组TMDS通道和一组TMDS clock通道组成，TMDS clock的运行频率是video信号的pixel频率，在每个cycle，每个TMDS data通道发送10bit数据。



Audio数据以Audio Sample Packet或High Bitrate Audio Stream Packet的形式传输，

但是HDMI没有传输audio clock，

因此sink设备需要进行audio clock regeneration。



sink设备在ROM中存放EDID信息，

source在收到HPD后会通过DDC通道读取EDID得到显示设备的属性。

EDID包含两部分，前128字节符合EDID1.3数据结构，128字节的扩展EDID，符合CEA extension verison3。

CEA extension verison3如下图所示。


二、HDMI有什么特性？

1、可以传送无压缩的音频信号及高分辨率视频信号，数字信号，质量高。

2、提高高达5Gbps的数据传输带宽。

3、最高能支持1080P视频。

4、理论20m，实际一般为3m左右。

5、同时传输音频、视频、版权保护，在消费电子领域非常受欢迎。

6、HDMI是外部接口，对于视频的分辨率和色深的提升能力有限。

7、HDMI兼容性不好。

参考资料

1、

https://blog.csdn.net/flaoter/article/details/73252240

2、

https://blog.csdn.net/qq_37457748/article/details/97617285