---
title: Linux之proc信息为0
date: 2018-03-12 21:40:29
tags:
	- Linux

---



cat /proc/iomem，普通用户，并不是报没有权限的错误，而是全给0 。

```
pi@raspberrypi:/proc$ cat iomem
00000000-00000000 : System RAM
  00000000-00000000 : Kernel code
  00000000-00000000 : Kernel data
00000000-00000000 : dwc_otg
00000000-00000000 : /soc/dma@7e007000
00000000-00000000 : /soc/vchiq
00000000-00000000 : /soc/mailbox@7e00b880
00000000-00000000 : /soc/watchdog@7e100000
00000000-00000000 : /soc/cprman@7e101000
00000000-00000000 : /soc/gpio@7e200000
00000000-00000000 : /soc/serial@7e201000
  00000000-00000000 : /soc/serial@7e201000
00000000-00000000 : /soc/mmc@7e202000
00000000-00000000 : /soc/spi@7e204000
00000000-00000000 : /soc/thermal@7e212000
00000000-00000000 : /soc/aux@0x7e215000
00000000-00000000 : /soc/serial@7e215040
00000000-00000000 : /soc/mmc@7e300000
00000000-00000000 : /soc/i2c@7e804000
00000000-00000000 : dwc_otg
```



要sudo权限才能看信息。

```
pi@raspberrypi:/proc$ sudo cat iomem
00000000-3b3fffff : System RAM
  00008000-00afffff : Kernel code
  00c00000-00d417b3 : Kernel data
3f006000-3f006fff : dwc_otg
3f007000-3f007eff : /soc/dma@7e007000
3f00b840-3f00b84e : /soc/vchiq
3f00b880-3f00b8bf : /soc/mailbox@7e00b880
3f100000-3f100027 : /soc/watchdog@7e100000
3f101000-3f102fff : /soc/cprman@7e101000
3f200000-3f2000b3 : /soc/gpio@7e200000
3f201000-3f201fff : /soc/serial@7e201000
  3f201000-3f201fff : /soc/serial@7e201000
3f202000-3f2020ff : /soc/mmc@7e202000
3f204000-3f204fff : /soc/spi@7e204000
3f212000-3f212007 : /soc/thermal@7e212000
3f215000-3f215007 : /soc/aux@0x7e215000
3f215040-3f21507f : /soc/serial@7e215040
3f300000-3f3000ff : /soc/mmc@7e300000
3f804000-3f804fff : /soc/i2c@7e804000
3f980000-3f98ffff : dwc_otg
```



要注意这个很坑的特性。

