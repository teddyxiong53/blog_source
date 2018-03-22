---
title: Linux驱动之iio目录
date: 2018-03-22 21:23:49
tags:
	- Linux驱动

---



iio是Industrial IO，工业io。

下面放的一些工业是常用的基于i2c、spi的设备的驱动。很有实用价值。

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

iio被提取为一个子系统。

相关接口也有一套公共的。

```
struct iio_dev {
  struct device dev;
  struct cdev chrdev;
  ...
}
```



先看温度、湿度、光、模拟量、重力感应、加速计、磁力计。

# 温度

看tmp006的。这个是TI的一款新品。

基于I2C 。

