---
title: amlogic之usbboot操作
date: 2021-06-07 10:37:11
tags:
	- amlogic

---

--

usbboot是一种模式，不依赖flash里的内容，通过usb进行调试。

对于调试flash内容损坏导致系统无法情况的情况，非常有用。

我现在是看一个multi boot的问题。boot损坏导致系统无法启动。

具体是这么操作：

1、首先准备好update.exe工具。从参考资料1里最下面下载。

2、用usb连接板子，按住usb_boot_sw按钮再上电，系统就进入到usbboot模式了。板端的串口要介绍，输出都是从串口输出的。

3、然后执行下面的操作：

```
update.exe cwr  .\u-boot.bin.usb.bl2  0xfffc0000
update.exe write .\usbbl2runpara_ddrinit.bin 0xfffcc000
update.exe run 0xfffc0000
update.exe write .\u-boot.bin.usb.bl2 0xfffc0000
update.exe write .\u-boot.bin.usb.tpl 0x200c000
update.exe write  .\usbbl2runpara_runfipimg.bin 0xfffcc000


update.exe run 0xfffc0000
sleep.exe 3
update.exe  bulkcmd "nand init"
```

最后这个`update.exe  bulkcmd "nand init"`是必须执行的。

update的命令格式是这样：

```
update.exe bulkcmd "xxx"
```

可以这样查看帮助信息：

```
update.exe bulkcmd "help"
```

可以看到的帮助信息有：

```
BULKcmd[help]
?       - alias for 'help'
aml_bcb - aml_bcb
aml_sysrecovery- Burning with amlogic format package from partition sysrecovery
amlmmc  - AMLMMC sub system
amlnf   - aml mtd nand sub-system
autoscr - run script from memory
avb     - avb
base    - print or set address offset
bcb     - bcb
boot_cooling- cpu temp-system
booti   - boot arm64 Linux Image image from memory
bootm   - boot application image from memory
bootp   - boot image via network using BOOTP/TFTP protocol
cbusreg - cbus register read/write
chpart  - change active partition
clkmsr  - Amlogic measure clock
cmp     - memory compare
cp      - memory copy
crc32   - checksum calculation
dcache  - enable or disable data cache
defenv_reserv- reserve some specified envs after defaulting env
dhcp    - boot image via network using DHCP/TFTP protocol
echo    - echo args to console
efuse   - efuse commands
efuse_obj- eFUSE object program commands
efuse_user- efuse user space read write ops
emmc    - EMMC sub system
env     - environment handling commands
ethloop - ethloop       - loopback test using ethernet test package

exit    - exit script
false   - do nothing, unsuccessfully
fastboot- use USB Fastboot protocol
fatinfo - print information about filesystem
fatload - load binary file from a dos filesystem
fatls   - list files in a directory (default /)
fatsize - determine a file's size
fdt     - flattened device tree utility commands
forceupdate- forceupdate
get_avb_mode- get_avb_mode
get_bootloaderversion- print bootloader version
get_rebootmode- get reboot mode
get_slot_state- get_slot_state a suc_stete
get_system_as_root_mode- get_system_as_root_mode
get_valid_slot- get_valid_slot
gpio    - query and control gpio pins
gpt     - GUID Partition Table
guid    - GUID - generate Globally Unique Identifier based on random UUID
help    - print command description/usage
i2c     - I2C sub-system
icache  - enable or disable instruction cache
imgread - Read the image from internal flash with actual size
itest   - return true/false on integer compare
jtagoff - disable jtag
jtagon  - enable jtag
keyman  - Unify key ops interfaces based dts cfg
keyunify- key unify sub-system
loop    - infinite loop on address range
macreg  - ethernet mac register read/write/dump
md      - memory display
mm      - memory modify (auto-incrementing address)
mmc     - MMC sub system
mmcinfo - display MMC info
mtdparts- define flash/nand partitions
mw      - memory write (fill)
mwm     - mw mask function
nand    - NAND sub-system
nboot   - boot from NAND device
nm      - memory modify (constant address)
open_scp_log- print SCP messgage
phyreg  - ethernet phy register read/write/dump
ping    - send ICMP ECHO_REQUEST to network host
printenv- print environment variables
query   - SoC query commands
rarpboot- boot image via network using RARP/TFTP protocol
readMetadata- readMetadata
read_temp- cpu temp-system
reboot  - set reboot mode and reboot system
reset   - Perform RESET of the CPU
ringmsr - Amlogic measure ring
rpmb_state- RPMB sub-system
rsvmem  - reserve memory
run     - run commands in an environment variable
saradc  - saradc sub-system
saradc_12bit- saradc sub-system
saveenv - save environment variables to persistent storage
sdc_burn- Burning with amlogic format package in sdmmc 
sdc_update- Burning a partition with image file in sdmmc card
set_active_slot- set_active_slot
set_trim_base- cpu temp-system
set_usb_boot- set usb boot mode
setenv  - set environment variables
showvar - print local hushshell variables
sleep   - delay execution for some time
store   - STORE sub-system
systemoff- system off 
tee_log_level- update tee log level
temp_triming- cpu temp-system
test    - minimal test like /bin/sh
tftpboot- boot image via network using TFTP protocol
true    - do nothing, successfully
ubi     - ubi commands
ubifsload- load file from an UBIFS filesystem
ubifsls - list files in a directory
ubifsmount- mount UBIFS volume
ubifsumount- unmount UBIFS volume
unpackimg- un pack logo image into pictures
update  - Enter v2 usbburning mode
usb     - USB sub-system
usb_burn- Burning with amlogic format package in usb 
usb_update- Burning a partition with image file in usb host
usbboot - boot from USB device
uuid    - UUID - generate random Universally Unique Identifier
version - print monitor, compiler and linker version
vpp     - vpp sub-system
watchdog- enable or disable watchdog
write_trim- cpu temp-system
write_version- cpu temp-system
```



update的子命令有这些：

```
partition
	往一个分区写入一个镜像。
	update.exe partition bootloader u-boot.bin.usb.bl2
mwrite
mread
	从flash的2M处读取内容并存储到本地的boot.dump文件。
	update.exe mread store boot normal 0x20000 boot.dump
	从ddr读取内容
	update.exe mread mem 0x108000 normal mem.dump
	
tplcmd
bulkcmd
	这个最重要，就是执行uboot的命令。
write/cwr
	
run
read
wreg
rreg
password
chipinfo
chipid
bl2_boot
```



操作实例

```
# 把flash 2M处的内容读取出来。
update.exe mread store bootloader normal 0x200000 ./compare_bad.bin
# 把bl2分区完全擦除
update.exe  bulkcmd "store erase partition bootloader 0 0"
# 重新写入bl2分区镜像。
update.exe  partition bootloader u-boot.bin.usb.bl2
# 依次擦除所有的bl2备份。
update.exe  bulkcmd "amlnf bl2_erase 0"
update.exe  bulkcmd "amlnf bl2_erase 1"
update.exe  bulkcmd "amlnf bl2_erase 2"
update.exe  bulkcmd "amlnf bl2_erase 3"
update.exe  bulkcmd "amlnf bl2_erase 4"
update.exe  bulkcmd "amlnf bl2_erase 5"
update.exe  bulkcmd "amlnf bl2_erase 6"
```



参考资料

1、Update命令

https://wiki-china.amlogic.com/Amlogic_Tools/Update%e5%91%bd%e4%bb%a4