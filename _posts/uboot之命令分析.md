---
title: uboot之命令分析
date: 2018-04-07 10:30:10
tags:
	- uboot

---



现在把uboot里的所有命令分析一下。

在mini2440的uboot里。这个uboot有点老。但是也简单。

所有命令都在这里了。

```
MINI2440 # help
?       - alias for 'help'
autoscr - run script from memory
base    - print or set address offset
bdinfo  - print Board Info structure
boot    - boot default, i.e., run 'bootcmd'
bootd   - boot default, i.e., run 'bootcmd'
bootm   - boot application image from memory
bootp   - boot image via network using BootP/TFTP protocol
chpart  - change active partition
cmp     - memory compare
coninfo - print console devices and information
cp      - memory copy
crc32   - checksum calculation
date    - get/set/reset date & time
dhcp    - invoke DHCP client to obtain IP/boot params
dynenv  - dynamically placed (NAND) environment
dynpart - dynamically calculate partition table based on BBT
echo    - echo args to console
erase   - erase FLASH memory
ext2load- load binary file from a Ext2 filesystem
ext2ls  - list files in a directory (default /)
fatinfo - print information about filesystem
fatload - load binary file from a dos filesystem
fatls   - list files in a directory (default /)
flinfo  - print FLASH memory information
flinit  - Initialize/probe NOR flash memory
fsinfo  - print information about filesystems
fsload  - load binary file from a filesystem image
go      - start application at address 'addr'
help    - print online help
icrc32  - checksum calculation
iloop   - infinite loop on address range
imd     - i2c memory display
iminfo  - print header information for application image
imls    - list all images found in flash
imm     - i2c memory modify (auto-incrementing)
imw     - memory write (fill)
imxtract- extract a part of a multi-image
in      - read data from an IO port
inm     - memory modify (constant address)
iprobe  - probe to discover valid I2C chip addresses
itest   - return true/false on integer compare
loadb   - load binary file over serial line (kermit mode)
loads   - load S-Record file over serial line
loady   - load binary file over serial line (ymodem mode)
loop    - infinite loop on address range
ls      - list files in a directory (default /)
md      - memory display
mm      - memory modify (auto-incrementing)
mmcinit - init mmc card
mtdparts- define flash/nand partitions
mtest   - simple RAM test
mw      - memory write (fill)
nand    - NAND sub-system
nboot   - boot from NAND device
nfs     - boot image via network using NFS protocol
nm      - memory modify (constant address)
out     - write datum to IO port
ping    - send ICMP ECHO_REQUEST to network host
printenv- print environment variables
protect - enable or disable FLASH write protection
rarpboot- boot image via network using RARP/TFTP protocol
reginfo - print register information
reset   - Perform RESET of the CPU
run     - run commands in an environment variable
s3c24xx - SoC  specific commands
saveenv - save environment variables to persistent storage
saves   - save S-Record file over serial line
setenv  - set environment variables
sleep   - delay execution for some time
tftpboot- boot image via network using TFTP protocol
usb     - USB sub-system
usbboot - boot from USB device
version - print monitor version
```

# autoscr

```
MINI2440 # help autoscr
autoscr [addr] - run script starting at addr - A valid autoscr header must be present
```

运行某个内存地址上的脚本文件。



# 参考资料

1、

https://blog.csdn.net/tangtang_yue/article/details/50634011