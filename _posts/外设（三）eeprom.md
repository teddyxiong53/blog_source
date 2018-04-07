---
title: 外设（三）eeprom
date: 2018-04-07 21:23:07
tags:
	- 外设

---



先看看AT24C02的芯片手册。



# 特点

1、标准电压操作。2.7V到5.5V。（那就是兼容3.3V和5V的电压了）。

2、工作在-40到125度。

3、尺寸从128字节到2K字节。AT24C01就是128字节。最后的后缀，就是在这个基础上相差倍数。

4、施密特触发。

5、400kHz兼容。

6、有写保护引脚。

7、有8字节页（01和02）和16字节页两种。

8、写页的一部分也是允许的。

9、100万次写。100年保存。

# 硬件封装

8个脚。

3个地址脚，

1个vcc，1个gnd。

1个sda，1个scl。

1个写保护。低电平时可以写。一般就直接接地了。



# 时序图

总线时序

写时序

读时序

# 设备寻址

高4位是1010 。eeprom都是这样的。相当于地址分类了。这个是i2c协议规定的。

一般把3根地址线也都接地。所以地址一般是0x50 。实际用的时候，会左移一位再用。

```
static struct i2c_board_info mini2440_i2c_devs[] __initdata = {
	{
		I2C_BOARD_INFO("24c08", 0x50),
		.platform_data = &at24c08,
	},
};
```



# 写操作

字节写。

页写。



# 通过sysfs来操作

```
/ # cd /sys/bus/i2c/devices/0-0050/
/sys/devices/platform/s3c2440-i2c.0/i2c-0/0-0050 # ls
driver     eeprom     modalias   name       power      subsystem  uevent
/sys/devices/platform/s3c2440-i2c.0/i2c-0/0-0050 # cat eeprom 
/sys/devices/platform/s3c2440-i2c.0/i2c-0/0-0050 # echo 123 > eeprom 
QEMU ee24c08_tx: write 0000=31
QEMU ee24c08_tx: write 0001=32
QEMU ee24c08_tx: write 0002=33
QEMU ee24c08_tx: write 0003=0a
/sys/devices/platform/s3c2440-i2c.0/i2c-0/0-0050 # cat eeprom 
123
123
```

我们就这样写入到eeprom里。然后读取出来。



# 参考资料

1、

https://baike.baidu.com/item/AT24C02/5665387?fr=aladdin