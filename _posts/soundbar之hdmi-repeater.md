---
title: soundbar之hdmi-repeater
date: 2021-10-21 10:38:33
tags:
	- soundbar

---

--

IT66321 是一款 HDMI2.0 2 IN 至 1 OUT 开关，支持高达 6Gbps/通道的最大信号速率。

它符合最新的 HDMI2.0b 规范并向下兼容 HDMI1.4 和 DVI 规范。 

IT66321 具有 6Gbps/通道能力，可支持超高分辨率内容流，例如4Kx2K@50/60Hz 视频格式



IT66321 还内置 HDCP1.4/2.2 硬件引擎，

可用于禁用输出端口的 HDCP 加密或将 HDCP2.2 转换为 HDCP1.4 以用于封闭系统应用。

每个IT66321芯片都预编程了唯一的HDCP密钥，符合HDCP 1.4/2.2标准，以提供高清内容的安全传输。 IT66321 的用户无需购买任何 HDCP 密钥或 ROM。

IT66321 还提供了完整的消费电子控制 (CEC) 功能解决方案。 

HDMI 规范的这一可选 CEC 功能允许用户通过 HDMI 网络控制两个或多个启用 CEC 的设备。

借助 IT66321 嵌入式 CEC PHY，用户可以使用高级软件 API 轻松实现所有必要的远程控制命令。

CEC 总线相关协议由 CEC PHY 处理，从而消除了 MCU 的额外负载



对于 HTiB、SOUNDBAR 音箱和 AVR 的系统设计人员而言，

提高家庭影院的用户体验就意味着不断克服各种实施挑战。

最新版 HDMI 标准中又增添了新特性，如*音频回传通道*（ARC）、3D 显示格式以及对*消费电子控制*（CEC）协议的改进。

为了帮助设计人员应对此类挑战，ADI 公司推出了集成这些新特性的 *HDMI收发器产品*。



以 [ADV7623](http://www.analog.com/cn/products/adv7623.html), 为例，

这款 HDMI 收发器集成了 4:1 HDMI 输入*多路复用器*（mux）、HDMI 接收器、*屏幕显示*（OSD）引擎和 HDMI 发射器。

就个体而言，上述每种功能应该都需要彼此独立的 IC 及五花八门的固件，

但一个收发器就可以将全部功能组合到一个综合解决方案中，

节省了板载面积、降低了固件复杂程度、缩减了物料成本，为家庭影院系统设计人员带来了极大方便。

![ HDMI 收发器功能框图](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/hdmi-fig-01.jpg)



# SOUNDBAR 音箱

随着超薄大屏幕平板电视的日益普及，

新兴的 *SOUNDBAR* 音箱成为一种补充性的影音系统。

这种音响系统结构紧凑、安装方便，

音质远远高于电视扬声器。

大部分 HTiB 和 SOUNDBAR音箱都与大屏幕 HDTV 配套使用，

因此其音频和视频连接主要采用 HDMI 接口。

SOUNDBAR 音箱一般都拥有多个 HDMI输入端用于各种信号源，

拥有一个 HDMI 输出端用于连接电视，同时内置音频处理系统和扬声器。

图 3 所示为典型的SOUNDBAR 音箱系统。

![Figure 3](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/hdmi-fig-03.jpg)



高级 SOUNDBAR 音箱装有多个扬声器和放大器，

**具备环绕声解码能力，**

其电子和声学设计特性可以产生环绕声效果，

而无需在后面安置单独的扬声器。

中高端 SOUNDBAR 音箱系统包含 DVD 或蓝光播放机，从而形成与 HTiB 相似的系统架构。





作为 HDMI 规范中的新特性，

音频回传通道（ARC）让 HTiB得以处理来自下游器件的音频。

如果要在没有 ARC 的情况下收听电视音频，

你需要一条单独电缆（S/PDIF 光纤或同轴电缆）将电视或调谐器的音频送回至 HTiB。

有了 ARC，HDMI 电缆就可以将 2 通道 S/PDIF 或多通道音频从电视回传到 HTiB，

无需使用额外的音频电缆。

HDMI 收发器在 HDMI 输出端口提供一个 ARC 接收器。

在电视、机顶盒或其他下游 HDMI 接收器件使用调谐器接收新媒体内容的情况下，ARC 就显得意义重大。

用户如果不想再听性能一般的电视机扬声器声音，

可以轻松采用高保真的HTiB 系统输出。

回传的音频数据通过 HDMI 电缆从电视传递至 HTiB（方向与传统的视频数据路径相反），不用担心对 HTiB的视频输出在电缆上是否处于有效状态。

# 音频插入和提取

HDMI 收发器在 HTiB 内的另一用途是提取 HDMI 音频，

并用数字信号处理（DSP）芯片进行处理。

这样，音频可重新插入HDMI 流送往电视。

由于很多电视无法处理多通道音频格式，

而 DSP 芯片可以**将音频下采样为立体声**，

然后将音频重新插入 HDMI 链路中送往电视。

或者，**输入音频可由 HTiB 源的新数据流完全取代并嵌入HDMI 信号中送往电视**。

这种情况下，只用音频插入特性即可。

一个此类应用的例子是将 iPod®接入 HtiB，将其音频与独立的视频流混合在一起。

在家庭影院配置中，HTiB系统可用作HDMI中继器，接受HDMI输入然后作为 HDMI 输出发送。

例如，蓝光播放器可用作输入HTiB 的源器件。要利用远高于电视扬声器的 HTiB 音质，就必须在 HTiB 内从 HDMI 信号中提取音频。最理想的情况是，音响发烧友一定希望HTiB能输出完全8通道I2S音频，不过HDMI链路也能提供 2 通道 I2S 或 S/PDIF.视频继续传送至电视或显示器，完成系统路径。只有 HDMI/HDCP（*高带宽数字内容保护*）中继器或收发器型器件才能处理这种音频提取。



![Figure 4](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/hdmi-fig-04.jpg)



# IT66121FN

IT66121除了各种视频输出格式支持，

同时还支持8个通道的I 2 S数字音频，

高达192kHz的采样率和高达24位的样本大小。

IT66121还支持S / PDIF输入高达192kHz的采样率。

由IT提供HDMI规格V1.3支持新的高比特率音频（HBR）66121中两个接口：

四个I 2 S输入端口或S / PDIF输入端口。

HBR的两个接口可能的最高帧速率支持高达768kHz 支持TTL

IT66121默认情况下，

带有集成HDCP ROM的预编程HDCP密钥，确保安全的数字内容传输的。

用户不必担心HDCP密钥的采购和维护。

IT66121消费电子控制（CEC）功能，还提供了一个完整的解决方案。

这个可选的CEC功能的HDMI规范允许用户来控制两个或更多个通过HDMI网络的CEC功能的设备。

随着嵌入式CEC PHY IT66121，用户可以使用高层次软件API轻松地执行所有必要的远程控制命令。CEC总线相关协议是由CEC PHY，从而消除了额外的负荷的MCU处理..

IT66121FN是联阳科技(ITE)推出的一款低功率单通道HDMI传输器，该芯片符合HDMI 1.3a, HDCP 1.2以及DVI1.0等标准，IT66121为数字电视提供了有效的解决方案，如DVD播放器、A/V接收器、机顶盒等。





# 参考资料

1、

https://www.ite.com.tw/en/product/view?mid=100

2、

https://blog.csdn.net/weixin_30629653/article/details/96084736

3、

https://zhuanlan.zhihu.com/p/217414084