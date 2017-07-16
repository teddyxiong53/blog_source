---
title: AndroidThings之SDK分析
date: 2017-07-16 17:37:03
tags:

	- AndroidThings

---

本文基于Google官网信息整理。

包的基本结构如下：

```
things/
	AndroidThings：这个就是版本号信息。
	bluetooth/
		BluetoothProfile
		BluetoothProfileManager.ServiceListner
		BluetoothProfileManager
	pio/
		Gpio
		GpioCallback
		I2cBusDriver
		I2cDevice
		I2sDevice
		PeripheralManagerService
		PioDriveManager
		Pwm
		PwmDriver
		SpiBusDriver
		SpiDevice
		UartDevice
		UartDeviceCallback
		UartDeviceDriver
	userdriver/
		AudioInputDriver
		AudioOutputDriver
		GpsDriver
		InputDriver
		InputDriverBuilder
		UserDriverManager
		UserSensor
		UserSensorDriver
		UserSensorReading
		
```

