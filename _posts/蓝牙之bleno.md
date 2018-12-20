---
title: 蓝牙之bleno
date: 2018-12-19 15:48:35
tags:
	- 蓝牙
typora-root-url:../
---



bleno是nodejs下面的一个ble的库。

https://github.com/noble/bleno

github上的readme就有详细的使用说明。

这里例子在树莓派上运行正常。

https://github.com/teddyxiong53/nodejs_code/tree/master/bleno/01

这个可以进行收发。

https://github.com/teddyxiong53/nodejs_code/tree/master/bleno/02

我在02的基础上，自己定义了一个service。里面定义了一个characteristic。

可读可写可通知。

```
new bleno.Characteristic({
                        value : null, //这个只能是null，不是null，运行就会提示只能只读。
                        uuid : '34cd',
```





参考资料

1、bleno, 实现 BLE ( 蓝牙低能源) 外设的node.js 模块

https://www.helplib.com/GitHub/article_103947

2、Bluetooth Low Energy Peripherals with JavaScript

http://shawnhymel.com/703/bluetooth-low-energy-peripherals-with-javascript/

3、api documentation for bleno (v0.4.2)

https://npmdoc.github.io/node-npmdoc-bleno/build/apidoc.html

4、官方例子

https://github.com/noble/bleno/tree/master/examples