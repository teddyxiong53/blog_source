---
title: amlogic之anti-rollback
date: 2022-10-25 13:52:33
tags:
	- amlogic

---

--

Anti-[Rollback](https://so.csdn.net/so/search?q=Rollback&spm=1001.2101.3001.7020)-“防回滚”是为了防止有人恶意刷入旧版本固件，

并利用旧版本固件中已知的漏洞来实现不法操作。



防回滚是一种保护机制。

具体做法是：如果检测到设备被降级到较低的版本（或者不合法的构建版本），那么就阻止设备启动。

目的是避免黑客通过把设备降低到有漏洞的老版本来进行root破解等操作。

这个功能必须要有Secure Boot V3的支持。

对于amlogic芯片，有一个OTP的bit可以设置是否使能防回滚功能。

FEAT_ENABLE_ANTI_ROLLBACK



测试方法

```
cd bootloader\uboot-repo\fip\a5\generate-device-keys
```

版本信息是这里配置的

```
bootloader\uboot-repo\bl33\v2019\board\amlogic\a5_av400\fw_arb.cfg
```

内容是这样：

```
# Configure Firmware Anti-rollback Versions
device_scs_vers=0x0
device_tee_vers=0x0
device_ree_vers=0x0

```

在uboot的头文件里，要加上这个配置。

```
#define CONFIG_AML_SIGNED_UBOOT 1
//这个默认是没有使能的。
```

要验证的话，我们就先把device_scs_vers=0x01生成一个uboot镜像。

然后device_scs_vers=0x0再生成一个镜像（相当于得到一个低版本镜像）



# otp写入工具及方法



# 参考资料

1、

https://confluence.amlogic.com/display/SW/Firmware+Anti-Rollback

2、

https://confluence.amlogic.com/display/SW/S905Y4+NSTV+CAS+Spec?preview=%2F231115345%2F231115347%2F%E6%B0%B8%E6%96%B0%E8%A7%86%E5%8D%9A%E5%AE%89%E5%85%A8%E8%8A%AF%E7%89%87%E9%9C%80%E6%B1%82%E5%8F%8A%E7%94%9F%E4%BA%A7%E8%A7%84%E8%8C%83V4.pdf

3、

