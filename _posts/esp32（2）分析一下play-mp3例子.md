---
title: esp32（2）分析一下play_mp3例子
date: 2018-12-04 19:44:08
tags:
	- esp32

---



上一篇文章，我们把play_mp3这个例子跑起来了。证明了板子是好的。我们的开发环境配置没有问题。

现在就分析一下这个例子。

esp-adf这个目录名字里，adf是Audio Development Framework。

下面有这些子目录。

```
components/
docs/
esp-idf/
examples/
LICENSE
project.mk
README.md
tools/
```

```
teddy@teddy-ThinkPad-SL410:~/work/esp32/esp-adf/components$ tree -L 1
.
├── adf_utils
├── audio_hal
├── audio_pipeline
├── audio_sal
├── audio_service
├── audio_stream
├── clouds
├── esp-adf-libs
├── esp_http_client
└── esp_peripherals
```

我们先看目录下的readme文件。

用esp32，你可以做的事情有：

1、播放音乐或者录音。

2、从网络播放音乐，从蓝牙播放音乐。从SD卡播放音乐。

3、集成微信和dlna。

4、网络收音机。

5、语音识别。



lyrat这个板子集成了：

1、语音唤醒。

2、按键唤醒。

3、音频播放器。

为智能音箱和智能家居设计。



另外还有一个esp-idf的概念。

idf是IoT Development Framework的意思。

idf是adf的基础。

官方文档在这里：

https://docs.espressif.com/projects/esp-adf/en/latest/index.html



建立source insight工程，看看这个工程。代码还不少，有4000多个。

Makefile里查询版本信息是这样：

```
teddy@teddy-ThinkPad-SL410:~/work/esp32/esp-adf$ git describe --always --tags --dirty
v1.0-beta1-62-g95b7fc3
```

靠的是调用esp-idf/make/project.mk文件。这个是主要的Makefile。

编译的输出目录是：~/work/esp32/esp-adf/examples/get-started/play_mp3/build$ 。

下面的东西挺多的。

```
teddy@teddy-ThinkPad-SL410:~/work/esp32/esp-adf/examples/get-started/play_mp3/build$ tree -L 1
.
├── adf_utils
├── app_trace
├── app_update
├── audio_hal
├── audio_pipeline
├── audio_sal
├── audio_service
├── audio_stream
├── aws_iot
├── bootloader
├── bootloader_support
├── bt
├── clouds
├── coap
├── console
├── cxx
├── driver
├── esp32
├── esp_adc_cal
├── esp-adf-libs
├── esp_http_client
├── esp_https_ota
├── esp_peripherals
├── esp-tls
├── esptool_py
├── ethernet
├── expat
├── fatfs
├── freertos
├── heap
├── idf_test
├── include
├── jsmn
├── json
├── libsodium
├── log
├── lwip
├── main
├── mbedtls
├── mdns
├── micro-ecc
├── newlib
├── nghttp
├── nvs_flash
├── openssl
├── partitions_singleapp.bin
├── partition_table
├── play_mp3.bin：500K
├── play_mp3.elf：2M
├── play_mp3.map
├── pthread
├── sdmmc
├── smartconfig_ack
├── soc
├── spiffs
├── spi_flash
├── tcpip_adapter
├── ulp
├── vfs
├── wear_levelling
├── wpa_supplicant
└── xtensa-debug-module
```

看play_mp3下面的readme。

播放一个7秒的mp3文件，这个文件被打包进bin文件了。

分析一下play_mp3_example.c文件。

入口是app_main。是基于freertos的。

menuconfig的内容就是在play_mp3目录下的sdkconfig文件。

生成的头文件是play_mp3/build/include/sdkconfig.h。



make flash是如何进行烧录的？



# 参考资料

1、官方文档

https://docs.espressif.com/projects/esp-adf/en/latest/index.html