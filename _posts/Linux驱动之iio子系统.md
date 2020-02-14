---
title: Linux驱动之iio子系统
date: 2018-03-22 21:23:49
tags:
	- Linux驱动
typora-root-url: ..\
---



iio是Industrial IO，工业io。

下面放的一些工业是常用的基于i2c、spi的设备的驱动。很有实用价值。

iio子系统是指那些在分类的时候，**处于hwmon和input子系统之间的设备。**

iio到目前还一直是在drivers/staging目录下，没有被并入主线版本。

现在的4.11版本里看，是已经是主线版本了。

在某些情况下，iio和hwmon、Input之间的相当大的重叠。

我们先看看有哪些设备的驱动。文件总共300多个。

```
├── accel：加速计。
├── adc：模拟量采集。
├── amplifiers：增益放大器。
├── buffer：
├── chemical
├── common：各种Sensor。
├── counter：
├── dac：数模转换器。
├── frequency
├── gyro：重力感应。
├── health：
├── humidity：湿度。
├── imu
├── light：光传感器。
├── magnetometer：磁力计。
├── multiplexer：
├── orientation
├── potentiometer
├── potentiostat
├── pressure
├── proximity
├── temperature
└── trigger
```



相关接口也有一套公共的。

```
struct iio_dev {
  struct device dev;
  struct cdev chrdev;
  ...
}
```



这个子系统的框架图是这样的：

![Linux内核之iio子系统-图1](/images/Linux内核之iio子系统-图1.png)



硬件ringbuffer的支持。

现在很多的传感器自身就带了ringbuffer，极大地减轻了CPU的负担。

这个枚举就定义了所有的类型。

```
enum iio_chan_type {
	IIO_VOLTAGE,
	IIO_CURRENT,
	IIO_POWER,
	IIO_ACCEL,
	IIO_ANGL_VEL,
	IIO_MAGN,
	IIO_LIGHT,
	IIO_INTENSITY,
	IIO_PROXIMITY,
	IIO_TEMP,
	IIO_INCLI,
	IIO_ROT,
	IIO_ANGL,
	IIO_TIMESTAMP,
	IIO_CAPACITANCE,
	IIO_ALTVOLTAGE,
	IIO_CCT,
	IIO_PRESSURE,
	IIO_HUMIDITYRELATIVE,
	IIO_ACTIVITY,
	IIO_STEPS,
	IIO_ENERGY,
	IIO_DISTANCE,
	IIO_VELOCITY,
	IIO_CONCENTRATION,
	IIO_RESISTANCE,
};
```

定义了对应的设备类型和总线类型：

```
struct bus_type iio_bus_type = {
	.name = "iio",
};
struct device_type iio_device_type = {
	.name = "iio_device",
	.release = iio_dev_release,
};
```



# iio的 使用

直接读取sys下的文件，这样会触发一次采集行为。

```
/sys/devices/platform/ff1e0000.saradc/iio:device0 # cat in_voltage0_raw
388
```



# adc_keys

这个是在input目录下，但是看到包含了iio的头文件。



```
 adc-keys1 {
     compatible = "adc-keys";
     io-channels = <&saradc 1>;
     io-channel-names = "buttons";
     poll-interval = <100>;
     keyup-threshold-microvolt = <1800000>;
     status = "disabled";

     esc-key {
         linux,code = <KEY_MICMUTE>;
         label = "micmute";
         press-threshold-microvolt = <1130000>;
     };

     home-key {
         linux,code = <KEY_MODE>;
         label = "mode";
         press-threshold-microvolt = <901000>;
     };

     menu-key {
         linux,code = <KEY_PLAY>;
         label = "play";
         press-threshold-microvolt = <624000>;
     };

     vol-down-key {
         linux,code = <KEY_VOLUMEDOWN>;
         label = "volume down";
         press-threshold-microvolt = <300000>;
     };

     vol-up-key {
         linux,code = <KEY_VOLUMEUP>;
         label = "volume up";
         press-threshold-microvolt = <18000>;
     };
 };
```



# 参考资料

1、linux iio子系统

https://blog.csdn.net/tsy20100200/article/details/47101661

2、

https://tinylab.org/lwn-465358/

3、linux IIO子系统使用说明

https://blog.csdn.net/xjq163/article/details/80790613