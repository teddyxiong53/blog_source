---
title: esp32（3）dueros运行
date: 2018-12-04 20:14:06
tags:
	- esp32

---



sdk里带了dueros的，看看怎么运行，先看看readme。

是连接到dueros3.0的。

1、需要先设置wifi名字和密码。

2、连接音箱到板子上。插到3.5mm插口上就好了。

3、修改dueros/main/duer_profile里，配置一下自己的百度账号信息。



唤醒词是“Hi lexin”。绿灯亮来指示唤醒状态。

也可以按一下rec键来唤醒。

进入dueros官网，配置一个新的设备，选择音箱，freertos，产品名字xhl_esp32 。

然后选择配置轻量级设备。

点击设备端开发，生成profile。会一次性生成20个。下载压缩包。

我们就选择第一个。19880000000001 

把这个文件里的内容复制出来，拷贝覆盖duer_profile的内容。

然后我们在dueros目录下，进行make menuconfig，配置wifi的信息。

是在Example Configuration下面。

然后先不要急着编译，因为dueros的bin文件比较大，所以我们需要先把分区扩大一下。

但是我看当我这个配置的已经是3M了。是够了的。

我先编译看看。

烧录。

```
serial.serialutil.SerialException: device reports readiness to read but returned no data (device disconnected or multiple access on port?)
/home/teddy/work/esp32/esp-adf/esp-idf/components/esptool_py/Makefile.projbuild:62: recipe for target 'flash' failed
make: *** [flash] Error 1
```

再试，又出现这个错误。

```
teddy@teddy-ThinkPad-SL410:~/work/esp32/esp-adf/examples/dueros$ make flash
Flashing binaries to serial port /dev/ttyUSB0 (app at offset 0x10000 )...
esptool.py v2.6-beta1
Serial port /dev/ttyUSB0
Connecting.......

A fatal error occurred: Invalid head of packet (0x01)
/home/teddy/work/esp32/esp-adf/esp-idf/components/esptool_py/Makefile.projbuild:62: recipe for target 'flash' failed
make: *** [flash] Error 2
```

把usb线重新拔插一下就好了。

运行打印：

```\
ets Jun  8 2016 00:22:57

rst:0x1 (POWERON_RESET),boot:0x3f (SPI_FAST_FLASH_BOOT)
flash read err, 1000
ets_main.c 371 
ets Jun  8 2016 00:22:57

rst:0x10 (RTCWDT_RTC_RESET),boot:0x3f (SPI_FAST_FLASH_BOOT)
configsip: 0, SPIWP:0xee
clk_drv:0x00,q_drv:0x00,d_drv:0x00,cs0_drv:0x00,hd_drv:0x00,wp_drv:0x00
mode:DIO, clock div:1
load:0x3fff0018,len:4
load:0x3fff001c,len:5752
load:0x40078000,len:7892
load:0x40080000,len:5904
0x40080000: _WindowOverflow4 at /home/teddy/work/esp32/esp-adf/esp-idf/components/freertos/xtensa_vectors.S:1685

entry 0x4008031c
0x4008031c: _KernelExceptionVector at ??:?

I (29) boot: ESP-IDF v3.1.1-6-g2aa9a21 2nd stage bootloader
I (29) boot: compile time 20:31:42
I (31) boot: Enabling RNG early entropy source...
I (34) boot: SPI Speed      : 80MHz
I (38) boot: SPI Mode       : DIO
I (42) boot: SPI Flash Size : 4MB
I (46) boot: Partition Table:
I (50) boot: ## Label            Usage          Type ST Offset   Length
I (57) boot:  0 nvs              WiFi data        01 02 00009000 00006000
I (65) boot:  1 phy_init         RF data          01 01 0000f000 00001000
I (72) boot:  2 factory          factory app      00 00 00010000 00300000
I (80) boot: End of partition table
I (84) esp_image: segment 0: paddr=0x00010020 vaddr=0x3f400020 size=0x8f668 (587368) map
I (262) esp_image: segment 1: paddr=0x0009f690 vaddr=0x3ffb0000 size=0x00980 (  2432) load
I (263) esp_image: segment 2: paddr=0x000a0018 vaddr=0x400d0018 size=0x130dbc (1248700) map
0x400d0018: _flash_cache_start at ??:?

I (627) esp_image: segment 3: paddr=0x001d0ddc vaddr=0x3ffb0980 size=0x036cc ( 14028) load
I (632) esp_image: segment 4: paddr=0x001d44b0 vaddr=0x3ffb404c size=0x00000 (     0) load
I (634) esp_image: segment 5: paddr=0x001d44b8 vaddr=0x40080000 size=0x00400 (  1024) load
0x40080000: _WindowOverflow4 at /home/teddy/work/esp32/esp-adf/esp-idf/components/freertos/xtensa_vectors.S:1685

I (643) esp_image: segment 6: paddr=0x001d48c0 vaddr=0x40080400 size=0x17b90 ( 97168) load
I (684) esp_image: segment 7: paddr=0x001ec458 vaddr=0x400c0000 size=0x00000 (     0) load
I (684) esp_image: segment 8: paddr=0x001ec460 vaddr=0x50000000 size=0x00000 (     0) load
I (704) boot: Loaded app from partition at offset 0x10000
I (704) boot: Disabling RNG early entropy source...
I (705) spiram: SPI RAM mode: flash 80m sram 80m
I (710) spiram: PSRAM initialized, cache is in low/high (2-core) mode.
I (717) cpu_start: Pro cpu up.
I (721) cpu_start: Starting app cpu, entry point is 0x40081508
0x40081508: call_start_cpu1 at /home/teddy/work/esp32/esp-adf/esp-idf/components/esp32/cpu_start.c:231

I (0) cpu_start: App cpu up.
I (1190) spiram: SPI SRAM memory test OK
I (1191) heap_init: Initializing. RAM available for dynamic allocation:
I (1191) heap_init: At 3FFAE6E0 len 00001920 (6 KiB): DRAM
I (1197) heap_init: At 3FFBB6A0 len 00024960 (146 KiB): DRAM
I (1203) heap_init: At 3FFE0440 len 00003BC0 (14 KiB): D/IRAM
I (1210) heap_init: At 3FFE4350 len 0001BCB0 (111 KiB): D/IRAM
I (1216) heap_init: At 40097F90 len 00008070 (32 KiB): IRAM
I (1223) cpu_start: Pro cpu start user code
I (1227) spiram: Adding pool of 4096K of external SPI memory to heap allocator
I (1235) spiram: Reserving pool of 32K of internal memory for DMA/internal allocations
I (250) cpu_start: Starting scheduler on PRO CPU.
I (0) cpu_start: Starting scheduler on APP CPU.
I (346) DUEROS: ADF version is v1.0-beta1-62-g95b7fc3
W (346) ESP_PERIPH: Peripherals have been initialized already
I (347) gpio: GPIO[36]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:3 
I (356) gpio: GPIO[39]| InputEn: 1| OutputEn: 0| OpenDrain: 0| Pullup: 1| Pulldown: 0| Intr:3 
W (391) PERIPH_TOUCH: _touch_init
E (392) PERIPH_SDCARD: no sdcard detect
I (16240) DUEROS: PERIPH_NOTIFY_KEY_REC
I (23131) DUEROS: PERIPH_NOTIFY_KEY_REC
```

必须要插入SD卡才能继续跑。

然后我改了的profile没有放到板端，重新编译放进去。

可以语音唤醒。

```
W (70350) REC_ENG: ### spot keyword ###
I (70351) DUEROS: --- rec_engine_cb --- REC_EVENT_WAKEUP_START
I (70351) ESP_PERIPH: This peripheral has been added
W (71027) REC_ENG: State VAD silence_time >= vad_off_window
W (72208) REC_ENG: State VAD silence_time >= vad_off_window
W (73007) REC_ENG: State VAD silence_time >= vad_off_window
W (73840) REC_ENG: State VAD silence_time >= vad_off_window
W (74639) REC_ENG: State VAD silence_time >= vad_off_window
W (75439) REC_ENG: State VAD silence_time >= vad_off_window
W (76270) REC_ENG: State VAD silence_time >= vad_off_window
W (77070) REC_ENG: State VAD silence_time >= vad_off_window
W (77870) REC_ENG: State VAD silence_time >= vad_off_window
W (78670) REC_ENG: State VAD silence_time >= vad_off_window
W (79502) REC_ENG: State VAD silence_time >= vad_off_window
W (80302) REC_ENG: State VAD silence_time >= vad_off_window
I (80358) REC_ENG: Wakeup time is out
E (80370) REC_ENG: State FETCH_DATA, wakeup_time_out:1, vad_speech_on:0, vad_time_mode:0
W (80370) REC_ENG: State WAKEUP_END
I (80372) ESP_PERIPH: This peripheral has been added
I (80378) DUEROS: --- rec_engine_cb --- REC_EVENT_WAKEUP_END
I (80384) REC_ENG: state idle
```

可以交互，但是识别出来的概率比较低。





# 参考资料

1、

http://www.embed.cc/HTML/zixun/64787.html