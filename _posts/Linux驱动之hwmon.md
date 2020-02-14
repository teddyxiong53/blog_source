---
title: Linux驱动之hwmon
date: 2020-02-14 10:30:38
tags:
	 - Linux

---

1

什么是hwmon？

从名字看，是hardware monitor的意思，表示硬件监测。

主要代码在drivers/hwmon/hwmon.c里。

hwmon_device_register

比较典型的设备是CPU温度检测。

tsadc：ts表示temp Sensor。温度传感器。

rk的tsadc支持两种工作模式：

1、用户主动去读取。轮询模式

2、自动上报。类似中断模式。

在内核驱动代码里，有2个文件跟这个相关：

rockchip_tsadc.c

rockchip-hwmon.c



tsadc使用hwmon提供接口给用户空间。



先从设备树开始看。

设备树里配置的信息有：

```
tsadc: tsadc@ff1f0000 {
		compatible = "rockchip,rk3308-tsadc";
		reg = <0x0 0xff1f0000 0x0 0x100>;
		interrupts = <GIC_SPI 38 IRQ_TYPE_LEVEL_HIGH>;
		rockchip,grf = <&grf>;
		clocks = <&cru SCLK_TSADC>, <&cru PCLK_TSADC>;
		clock-names = "tsadc", "apb_pclk";
		assigned-clocks = <&cru SCLK_TSADC>;
		assigned-clock-rates = <50000>;
		resets = <&cru SRST_TSADC>;
		reset-names = "tsadc-apb";
		pinctrl-names = "init", "default", "sleep";
		pinctrl-0 = <&tsadc_otp_gpio>;
		pinctrl-1 = <&tsadc_otp_out>;
		pinctrl-2 = <&tsadc_otp_gpio>;
		#thermal-sensor-cells = <1>;
		rockchip,hw-tshut-temp = <120000>;
		status = "disabled";
	};
```

中断是高电平触发。时钟频率是50K。关机是温度是120度。

在/sys/class/hwmon下面。

以buildroot里的vexpress的为例。

下面有这些：

```
# cd hwmon/
# ls
hwmon0  hwmon1  hwmon2  hwmon3  hwmon4
```

0是amp表示电流。

```
# cat uevent 
OF_NAME=amp-vd10-s2
OF_FULLNAME=/dcc/amp-vd10-s2
OF_COMPATIBLE_0=arm,vexpress-amp
OF_COMPATIBLE_N=1
```

其他的是：

```
# cat hwmon2/name 
vexpress_power
# cat hwmon3/name 
vexpress_power
# cat hwmon4/name 
vexpress_temp
```



参考资料

1、[RK3288][Android6.0] TS-ADC驱动流程小结

https://blog.csdn.net/kris_fei/article/details/55045936