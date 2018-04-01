---
title: Linux驱动之iio子系统
date: 2018-03-22 21:23:49
tags:
	- Linux驱动
typora-root-url: ..\
---



iio是Industrial IO，工业io。

下面放的一些工业是常用的基于i2c、spi的设备的驱动。很有实用价值。

iio子系统是指那些在分类的时候，处于hwmon和input子系统之间的设备。



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



# 参考资料

1、linux iio子系统

https://blog.csdn.net/tsy20100200/article/details/47101661



