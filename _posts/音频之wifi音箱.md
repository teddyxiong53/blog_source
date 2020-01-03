---
title: 音频之wifi音箱
date: 2019-12-25 15:17:51
tags:
	- 音频

---

1

```
基于MT7688AN开发，开发板：独尊科技DM06/芒果Widora_NEO（16+128）。

支持功能：
1）Airplay音频推送；
2）DLNA功能（DMR、DMS）；
3）文件共享Samba；
4）wifi中继。

Target: ramips
Subtarget: mt7628
architecture: mipsel_24kc
Bootloader: U-Boot
CPU: MediaTek MT7628
CPU Cores: 1
CPU MHz: 580
Flash MB: 8
RAM MB: 64

可以在这么小的资源的情况实现功能。
```

从github上下载代码。

使用git clone的方式来下载，因为还有些子目录需要git来获取的。下载后大概400M。

ReadMe(GuideLine)文件，按照这个说明，进行编译。

```
1)change local feeds dir
./patchfirst.sh

2)
./scripts/feeds update -a

3)patch packages
./patchfirst.sh

4)
./scripts/feeds install -a

5)
rm -rf .config
make menuconfig
* Select the options as below:
    * Target System: `Ralink RT288x/RT3xxx`
    * Subtarget: `MT7688 based boards`
    * Target Profile: `dm06 iot board` or `widora-neo board`
* Save and exit

6)
make V=99
```

编译比较耗时。

大概3个小时左右。

生成的最终镜像大概11M。uImage只有1M多一点。rootfs 10M左右。

到rootfs下面du查看一下，是78M。压缩比很高啊。

应该还删除了很多文档性质的东西。



gstreamer需要的插件：

```
├── gst-plugin-scanner
├── libgstalsa.so
├── libgstasf.so
├── libgstaudioconvert.so
├── libgstaudioparsers.so
├── libgstaudioresample.so
├── libgstautodetect.so
├── libgstcoreelements.so
├── libgstfaad.so
├── libgstflac.so
├── libgsticydemux.so
├── libgstid3demux.so
├── libgstisomp4.so
├── libgstivorbisdec.so
├── libgstmad.so
├── libgstmms.so
├── libgstogg.so
├── libgstplayback.so
├── libgstsouphttpsrc.so
├── libgsttypefindfunctions.so
├── libgstvolume.so
├── libgstwavparse.so
└── libgstwma.so
```



参考资料

1、开源wifi音箱

https://blog.csdn.net/gq213/article/details/51820459

2、DuZun DM06

https://openwrt.org/toh/hwdata/duzun/duzun_dm06

3、

http://www.link-card.com.cn/products.asp?id=10