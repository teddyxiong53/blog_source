---
title: rk3308之recoverySystem工具分析
date: 2020-05-29 10:09:08
tags:
	- rk3308

---



代码在external/recoverySystem目录下。

基本逻辑：

```
1、不带参数。
	recoverySystem
	作用是执行恢复出厂操作。
	
2、带1个参数。
	recoverySystem ota
	recoverySystem update
		这2个命令作用一样，都是执行升级。
	recoverySystem factory
	recovertySystem reset
		这2个命令作用一样，都是恢复出厂设置。
3、带2个参数。
	recoverySystem ota /data/xx.img
	recoverySystem upate /data/xx.img
```

**带2个参数的方式。**

**会先把升级包里的recovery部分的数据直接写入到/dev/block/by-name/recovery分区。**

**相当于最先是对recovery进行升级。**

这个是在重启之前做的事。

从头文件的注释看，这个是Android里弄出来的代码。



```
#define  UPDATE_IMG             "update.img"
#define  DEV_RECOVERY_NODE      "/dev/block/by-name/recovery"
```



# fastoryDataReset

```
主要是2个步骤：
1、组装一个bootloader_message。
2、把这个message写入到misc分区。然后执行reboot。
```

message的内容是：

```
command: boot-recovery
recovery: recovery --wipe-data
systemFlag: false
```

写入misc分区的步骤：

```
1、fopen("/dev/block/by-name/misc", "wb")
2、fseek(fp, 16*1024, SEEK_SET);//偏移到16K的位置。
3、fwrite(msg, sizeof(*msg), 1, fp);
4、reboot(RB_AUTOBOOT);
```



在uboot里，

```
./common/android_bootloader.c:175:      if (!strcmp("boot-recovery", bcb.command))
```



# rebootUpdate

函数逻辑：

```
1、如果有path参数
	往misc分区里写入下面的message
	command: boot-recovery
	recovery: recovery --update_package=/xx/yy/update.img
	systemFlag: false
	然后就reboot了。
2、否则依次查找下面的位置是否合法。
	#define SD_UPDATE_FILE "/mnt/sdcard/update.img"
    #define USB_UPDATE_FILE "/mnt/udisk/update.img"
    #define DATA_UPDATE_FILE "/userdata/update.img"
```



# WriteFwData

这个就是带2个参数的模式。这个会先单独把recovery从升级包里提取出来，提前进行写入操作。

这个就是对于需要升级recovery的场景。很少使用。



参考资料

1、Bootloader - Main system - Recovery的三角关系

https://www.cnblogs.com/LittleRedPoint/p/3935301.html