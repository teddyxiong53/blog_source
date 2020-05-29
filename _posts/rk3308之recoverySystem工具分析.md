---
title: rk3308之recoverySystem工具分析
date: 2020-05-29 10:09:08
tags:
	- rk3308

---

1

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

带2个参数的方式。

会先把升级包里的recovery部分的数据直接写入到/dev/block/by-name/recovery分区。

相当于最先是对recovery进行升级。

这个是在重启之前做的事。

从头文件的注释看，这个是Android里弄出来的代码。



```
#define  UPDATE_IMG             "update.img"
#define  DEV_RECOVERY_NODE      "/dev/block/by-name/recovery"
```



fastoryDataReset

```

```



参考资料

1、Bootloader - Main system - Recovery的三角关系

https://www.cnblogs.com/LittleRedPoint/p/3935301.html