---
title: 一份符合LICENSE要求的开源软件清单
date: 2022-08-11 15:59:08
tags:
	- 开源

---

--

现在要对代码进行license合规审查。

找到一份sonos的代码清单，先过一遍，了解一下。

```
Abseil c++库
	谷歌的。Apache2协议。
ALAC
	apple的解码库。
	协议应该是苹果的，但是跟GPL2应该差不多。
alsa-lib
	LGPL 2
alsa-utils
	GPL 2
Anacapa Web Server
	协议自定义的。看有apache的。
logback-android
	Eclipse Public License v1.0
	
AppAuth-Android
	Apache协议。
ARM CMSIS
	Apache-2.0
ARM NE10
	arm的neon库。
	BSD协议。
Atheros HAL
	atheros wireless driver的抽象层。
	来自freebsd，那应该是bsd license的。
Alexa Client SDK
	就是avs的，Apache协议。
BL2
	arm的BL2，bootloader的一部分。
	TrustZone与OP-TEE
BlueZ
	GPL2协议
Bonjour
	mDNSResponder project
	apache协议。
BoringSSL
	BoringSSL is a fork of OpenSSL
	OpenSSL License
	Original SSLeay License
	这个协议就比较复杂了。

```



参考资料

1、

https://www.sonos.com/documents/gpl/13.3/SonosOpenSourceAttributions.pdf