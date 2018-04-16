---
title: arduino（二）
date: 2018-04-16 11:49:16
tags:
	- arduino

---



我觉得需要梳理一下arduino程序的编译过程，因为它进行了一个封装。

怎么才能看到这个编译过程呢？习惯了Makefile那一套机制，觉得windows下这种不透明让人觉得难受。

arduino IDE 的代码在这里：

https://github.com/arduino/Arduino/

处理过程如下：

1、我们写的文件是一个.ino文件，用的是C语言语法。所以IDE首先要做的，就是把这个ino文件转换成C或者C++文件。

2、然后调用gcc进行编译。得到elf文件，再转成bin文件。

在这个目录下，有一个boards.txt和一个platform.txt文件。

C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0

在platform.txt里，有这些内容，说明了什么？

工具链这些在这里配置。

```
build.lwip_lib=-llwip_gcc
build.lwip_flags=-DLWIP_OPEN_SRC

compiler.path={runtime.tools.xtensa-lx106-elf-gcc.path}/bin/
compiler.sdk.path={runtime.platform.path}/tools/sdk
```



C:\Users\Administrator\AppData\Local\Arduino15

这个目录下有个preference.txt的文件。

另外在D:\Program Files (x86)\Arduino\lib这个目录下，也有一个preference.txt文件。

后面这个相当于是系统默认的，前面那个相当于用户修改的。同名参数会覆盖。

注意看这个。系统里我没有搜索到stdout.txt和stderr.txt这2个文件。

```
console.error.file=stderr.txt
console.length=500
console.lines=4
console.output.file=stdout.txt
```

为了看到编译和上传过程，我们依次点击：文件，首选项，显示详细输出，勾选编译和上传。

我们再对WiFiScan进行编译看看。

```
D:\Program Files (x86)\Arduino\arduino-builder -dump-prefs -logger=machine -hardware D:\Program Files (x86)\Arduino\hardware -hardware C:\Users\Administrator\AppData\Local\Arduino15\packages -tools D:\Program Files (x86)\Arduino\tools-builder -tools D:\Program Files (x86)\Arduino\hardware\tools\avr -tools C:\Users\Administrator\AppData\Local\Arduino15\packages -built-in-libraries D:\Program Files (x86)\Arduino\libraries -libraries C:\Users\Administrator\Documents\Arduino\libraries -fqbn=esp8266:esp8266:d1_mini:CpuFrequency=80,UploadSpeed=921600,FlashSize=4M3M -ide-version=10803 -build-path C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671 -warnings=none -build-cache C:\Users\Administrator\AppData\Local\Temp\arduino_cache_817178 -prefs=build.warn_data_percentage=75 -prefs=runtime.tools.xtensa-lx106-elf-gcc.path=C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2 -prefs=runtime.tools.mkspiffs.path=C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\mkspiffs\0.1.2 -prefs=runtime.tools.esptool.path=C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\esptool\0.4.9 -verbose C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\examples\WiFiScan\WiFiScan.ino
D:\Program Files (x86)\Arduino\arduino-builder -compile -logger=machine -hardware D:\Program Files (x86)\Arduino\hardware -hardware C:\Users\Administrator\AppData\Local\Arduino15\packages -tools D:\Program Files (x86)\Arduino\tools-builder -tools D:\Program Files (x86)\Arduino\hardware\tools\avr -tools C:\Users\Administrator\AppData\Local\Arduino15\packages -built-in-libraries D:\Program Files (x86)\Arduino\libraries -libraries C:\Users\Administrator\Documents\Arduino\libraries -fqbn=esp8266:esp8266:d1_mini:CpuFrequency=80,UploadSpeed=921600,FlashSize=4M3M -ide-version=10803 -build-path C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671 -warnings=none -build-cache C:\Users\Administrator\AppData\Local\Temp\arduino_cache_817178 -prefs=build.warn_data_percentage=75 -prefs=runtime.tools.xtensa-lx106-elf-gcc.path=C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2 -prefs=runtime.tools.mkspiffs.path=C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\mkspiffs\0.1.2 -prefs=runtime.tools.esptool.path=C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\esptool\0.4.9 -verbose C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\examples\WiFiScan\WiFiScan.ino
Using board 'd1_mini' from platform in folder: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0
Using core 'esp8266' from platform in folder: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0
Detecting libraries used...
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-g++" -D__ets__ -DICACHE_FLASH -U__STRICT_ANSI__ "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/include" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/lwip/include" "-IC:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/core" -c -w -Os -g -mlongcalls -mtext-section-literals -fno-exceptions -fno-rtti -falign-functions=4 -std=c++11  -ffunction-sections -fdata-sections -w -x c++ -E -CC -DF_CPU=80000000L -DLWIP_OPEN_SRC   -DARDUINO=10803 -DARDUINO_ESP8266_WEMOS_D1MINI -DARDUINO_ARCH_ESP8266 -DARDUINO_BOARD="ESP8266_WEMOS_D1MINI"  -DESP8266 "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\cores\esp8266" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\variants\d1_mini" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\sketch\WiFiScan.ino.cpp" -o "nul"
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-g++" -D__ets__ -DICACHE_FLASH -U__STRICT_ANSI__ "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/include" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/lwip/include" "-IC:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/core" -c -w -Os -g -mlongcalls -mtext-section-literals -fno-exceptions -fno-rtti -falign-functions=4 -std=c++11  -ffunction-sections -fdata-sections -w -x c++ -E -CC -DF_CPU=80000000L -DLWIP_OPEN_SRC   -DARDUINO=10803 -DARDUINO_ESP8266_WEMOS_D1MINI -DARDUINO_ARCH_ESP8266 -DARDUINO_BOARD="ESP8266_WEMOS_D1MINI"  -DESP8266 "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\cores\esp8266" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\variants\d1_mini" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\sketch\WiFiScan.ino.cpp" -o "nul"
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\ESP8266WiFi.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\ESP8266WiFiAP.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\ESP8266WiFiGeneric.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\ESP8266WiFiMulti.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\ESP8266WiFiSTA.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\ESP8266WiFiScan.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\WiFiClient.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\WiFiClientSecure.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\WiFiServer.cpp
Using cached library dependencies for file: C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src\WiFiUdp.cpp
Generating function prototypes...
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-g++" -D__ets__ -DICACHE_FLASH -U__STRICT_ANSI__ "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/include" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/lwip/include" "-IC:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/core" -c -w -Os -g -mlongcalls -mtext-section-literals -fno-exceptions -fno-rtti -falign-functions=4 -std=c++11  -ffunction-sections -fdata-sections -w -x c++ -E -CC -DF_CPU=80000000L -DLWIP_OPEN_SRC   -DARDUINO=10803 -DARDUINO_ESP8266_WEMOS_D1MINI -DARDUINO_ARCH_ESP8266 -DARDUINO_BOARD="ESP8266_WEMOS_D1MINI"  -DESP8266 "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\cores\esp8266" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\variants\d1_mini" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\sketch\WiFiScan.ino.cpp" -o "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\preproc\ctags_target_for_gcc_minus_e.cpp"
"D:\Program Files (x86)\Arduino\tools-builder\ctags\5.8-arduino11/ctags" -u --language-force=c++ -f - --c++-kinds=svpf --fields=KSTtzns --line-directives "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\preproc\ctags_target_for_gcc_minus_e.cpp"
正在编译项目...
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-g++" -D__ets__ -DICACHE_FLASH -U__STRICT_ANSI__ "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/include" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/tools/sdk/lwip/include" "-IC:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/core" -c -w -Os -g -mlongcalls -mtext-section-literals -fno-exceptions -fno-rtti -falign-functions=4 -std=c++11 -MMD -ffunction-sections -fdata-sections -DF_CPU=80000000L -DLWIP_OPEN_SRC   -DARDUINO=10803 -DARDUINO_ESP8266_WEMOS_D1MINI -DARDUINO_ARCH_ESP8266 -DARDUINO_BOARD="ESP8266_WEMOS_D1MINI"  -DESP8266 "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\cores\esp8266" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\variants\d1_mini" "-IC:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi\src" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\sketch\WiFiScan.ino.cpp" -o "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\sketch\WiFiScan.ino.cpp.o"
Compiling libraries...
Compiling library "ESP8266WiFi"
使用已经编译的文件：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\libraries\ESP8266WiFi\ESP8266WiFi.cpp.o
使用已经编译的文件：
Compiling core...
使用已经编译的文件：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\cont.S.o
使用已经编译的文件：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\cont_util.c.o
使用已经编译的文件：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\core_esp8266_eboot_command.c.o
C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\spiffs\spiffs_nucleus.c.o
使用已经编译的文件：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\umm_malloc\umm_malloc.c.o
使用已经编译的文件：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\Esp.cpp.o
C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\spiffs_hal.cpp.o
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-ar" cru  "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/arduino.ar" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\core_esp8266_postmortem.c.o"
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-ar" cru  
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\xtensa-lx106-elf-gcc\1.20.0-26-gb404fb9-2/bin/xtensa-lx106-elf-ar" cru  "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/arduino.ar" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\core\core_esp8266_wiring_shift.c.o"
"C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/arduino.ar" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671\libraries\ESP8266WiFi\WiFiUdp.cpp.o" "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/arduino.ar" -lm -lgcc -lhal -lphy -lpp -lnet80211 -lwpa -lcrypto -lmain -lwps -laxtls -lsmartconfig -lmesh -lwpa2 -llwip_gcc -lstdc++ -Wl,--end-group  "-LC:\Users\Administrator\AppData\Local\Temp\arduino_build_683671"
"C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\tools\esptool\0.4.9/esptool.exe" -eo "C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0/bootloaders/eboot/eboot.elf" -bo "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/WiFiScan.ino.bin" -bm dio -bf 40 -bz 4M -bs .text -bp 4096 -ec -eo "C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671/WiFiScan.ino.elf" -bs .irom0.text -bs .text -bs .data -bs .rodata -bc -ec
使用 1.0  版本的库 ESP8266WiFi 在文件夹： C:\Users\Administrator\AppData\Local\Arduino15\packages\esp8266\hardware\esp8266\2.3.0\libraries\ESP8266WiFi 
项目使用了 226745 字节，占用了 (21%) 程序存储空间。最大为 1044464 字节。
全局变量使用了31952字节，(39%)的动态内存，余留49968字节局部变量。最大为81920字节。
```

从上面的打印，我们可以得出这些结论：

1、输出文件在这里：C:\Users\Administrator\AppData\Local\Temp\arduino_build_683671

这个目录下有这些内容：

```
arduino.ar
build.options.json
core/：核心文件的o文件和d文件。很多。
includes.cache
libraries/：编译的依赖的文件的o和d文件。
preproc/：预处理得到的文件。是靠ctags预处理的。
sketch/：这个目录下放的是ino生成的cpp文件。
WiFiScan.ino.bin：这是最后下载的文件，200K左右。
WiFiScan.ino.elf：这是链接到得到的文件。1M左右。
```



我们现在要找到arduino的main函数在哪里。

在这个目录下的main.cpp文件。

D:\Program Files (x86)\Arduino\hardware\arduino\avr\cores\arduino

里面内容是：

```
int main(void)
{
	init();

	initVariant();

#if defined(USBCON)
	USBDevice.attach();
#endif
	
	setup();
    
	for (;;) {
		loop();
		if (serialEventRun) serialEventRun();
	}
        
	return 0;
}
```



再看上传的过程。我烧录blink的示例程序。

```
esptool v0.4.9 - (c) 2014 Ch. Klippel <ck@atelier-klippel.de>
	setting board to nodemcu
	setting baudrate from 115200 to 921600
	setting port from COM1 to COM6
	setting address from 0x00000000 to 0x00000000
	espcomm_upload_file
	espcomm_upload_mem
	setting serial port timeouts to 1000 ms
opening bootloader
resetting board
trying to connect
	flush start
	setting serial port timeouts to 1 ms
	setting serial port timeouts to 1000 ms
	flush complete
	espcomm_send_command: sending command header
	espcomm_send_command: sending command payload
	read 0, requested 1
trying to connect
	flush start
	setting serial port timeouts to 1 ms
	setting serial port timeouts to 1000 ms
	flush complete
	espcomm_send_command: sending command header
	espcomm_send_command: sending command payload
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
	espcomm_send_command: receiving 2 bytes of data
Uploading 226368 bytes from C:\Users\Administrator\AppData\Local\Temp\arduino_build_605930/Blink.ino.bin to flash at 0x00000000
	erasing flash
	size: 037440 address: 000000
	first_sector_index: 0
	total_sector_count: 56
	head_sector_count: 16
	adjusted_sector_count: 40
	erase_size: 028000
	espcomm_send_command: sending command header
	espcomm_send_command: sending command payload
	setting serial port timeouts to 15000 ms
	setting serial port timeouts to 1000 ms
	espcomm_send_command: receiving 2 bytes of data
	writing flash
................................................................................ [ 36% ]
................................................................................ [ 72% ]
..............................................................                   [ 100% ]
starting app without reboot
	espcomm_send_command: sending command header
	espcomm_send_command: sending command payload
	espcomm_send_command: receiving 2 bytes of data
closing bootloader
	flush start
	setting serial port timeouts to 1 ms
	setting serial port timeouts to 1000 ms
	flush complete

```



bootloader是如何工作的？

我在esp8266的代码下面看到一个叫eBoot的东西。

bootloader如何烧录呢？还是已经固化了？

```
Bootloader is in ESP ROM,
```

内部是固化的，但是要自己弄应该也是可以的。我暂时不管这一块。







# 参考资料

1、Arduino IDE的编译执行过程解读

https://blog.csdn.net/u011000290/article/details/50850171

2、Build Process

https://github.com/arduino/Arduino/wiki/Build-Process

3、 ESP8266固件的编译（交叉编译工具链的建立）

https://blog.csdn.net/ydogg/article/details/72598581

4、Arduino代码机制-main.cpp

https://blog.csdn.net/qq_24027059/article/details/50689023

6、esp8266官方文档

https://arduino-esp8266.readthedocs.io/en/2.4.1/

7、RBOOT – A NEW BOOT LOADER FOR ESP8266

https://richard.burtons.org/2015/05/18/rboot-a-new-boot-loader-for-esp8266/

8、Wiring when burning the bootloader of esp8266 [closed]

https://arduino.stackexchange.com/questions/45717/wiring-when-burning-the-bootloader-of-esp8266