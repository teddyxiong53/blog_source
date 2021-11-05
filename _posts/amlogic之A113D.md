---
title: amlogic之A113D
date: 2021-11-04 16:53:25
tags:
	- amlogic

---

--

A113D的寄存器分布

ARM cortex-M3 CPU in Always-On (AO) domain
io_aobus_base
这个ao就是Always On的意思。而不是我之前以为的audio output的意思。
挂在这个总线上的，有一个i2c，和红外发射。就这2个。

寄存器都集中在F980 0000以后的。
其实寄存器用不了多少地址空间。
因为都是人写的，人写的，就必然是有限的。

audio path分析
A113D集成
3个TDM输入/输出接口、
1个SPDIF输入/输出接口、
1个PDM接口多达 8 个通道，
3 个 TODDR (FIFO) 用于将输入数据传输到 DDR，
3 个 FRDDR (FIFO)用于将数据从 DDR 传输到输出，
1 个 TDM LB 和环回用于 AEC，
1 个硬件重采样用于时钟同步、
1 个用于语音唤醒的电源检测和 
1 个时钟锁定器检测两个时钟的差异。 

当前aplay -l，看到是这样，这个格局是怎么形成的？

```
/sys/kernel/debug/aml_reg # aplay -l
**** List of PLAYBACK Hardware Devices ****
card 0: AMLAUGESOUND [AML-AUGESOUND], device 0: TDM-A-dummy multicodec-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 1: TDM-B-dummy-alsaPORT-i2sCapture dummy-1 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 2: TDM-C-tas5782m multicodec-2 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 4: SPDIF-A-dummy dummy-4 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Loopback [Loopback], device 0: Loopback PCM [Loopback PCM]
```

就一个声卡，card 0，auge。

自身有0/1/2/4 这4个。为什么没有3？3是pdm的。对应录音的。

0为什么对应tdma？

这个就是在设备树里写的顺序了。

现在arecord -l看到的是这样：

这个没有2，但是多了3和5 。

```
/sys/kernel/debug/aml_reg # arecord -l
**** List of CAPTURE Hardware Devices ****
card 0: AMLAUGESOUND [AML-AUGESOUND], device 0: TDM-A-dummy multicodec-0 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 1: TDM-B-dummy-alsaPORT-i2sCapture dummy-1 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 3: PDM-dummy dummy-3 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 4: SPDIF-A-dummy dummy-4 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 0: AMLAUGESOUND [AML-AUGESOUND], device 5: LOOPBACK-A-dummy-alsaPORT-loopback dummy-5 []
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Loopback [Loopback], device 0: Loopback PCM [Loopback PCM]
```



设备树里有些东西，是给uboot用的，kernel完全不用的。

例如分区信息。

```
	partitions: partitions{
		parts = <11>;
		part-0 = <&logo>;
		part-1 = <&recovery>;
		part-2 = <&rsv>;
		part-3 = <&tee>;
		part-4 = <&crypt>;
		part-5 = <&misc>;
		part-6 = <&instaboot>;
		part-7 = <&boot>;
		part-8 = <&system>;
		part-9 = <&cache>;
		part-10 = <&data>;

		logo:logo{
			pname = "logo";
			size = <0x0 0x2000000>;
			mask = <1>;
		};
```



参考资料

1、芯片手册