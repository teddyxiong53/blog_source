---
title: dlna之upmpdcli分析
date: 2020-04-28 16:16:08
tags:
	- dlna

---

1

因为gmrender有问题，打算找一个其他的dlna renderer来辅助验证一下。

然后就找到了upmpdcli这个，是以mpd为backend的，这个刚好是符合我的需求啊。

buildroot里自带了，编译跑起来看看。

可以看到设备，但是播放没有声音。

/etc/init.d/S99upmpdcli stop

然后手动执行：

```
upmpdcli -c /etc/upmpdcli.conf -f doss -m 1
```

连上，播放。

```

:3:src/ohradio.cxx:88::OHRadio: python2 not found, no radio service will be 
	这个没所谓。
:3:libupnpp/upnpavutils.cxx:91::parseProtoInfEntry: bad format: [http-get:*:audio/mpeg:DLNA.ORG_OP=01:*]
	
created:2:src/upmpd.cxx:158::checkContentFormat: resource has no protocolinfo
:2:src/avtransport.cxx:393::set(Next)AVTransportURI: unsupported format: uri http://fs.android2.kugou.com/b8f762e0d373893b1494ee00b07cd1f2/5ea7f114/G175/M02/0B/19/7w0DAF2KNWWAQIzvADo1gWSDkYA642.mp3
```

看这意思，是mp3格式不支持？

这个必须解决。

MP3是主流格式，不支持那怎么行？

但是不对啊，不是用mpd做后端的吗？解码这些不是mpd来完成吗？



手机上用BubbleUPnP是正常的。

音乐文件是我的笔记本上搭建的一个http服务器。

用QQ音乐也是正常的。

用酷狗是会报上面的错误的。

是酷狗音乐有什么特别的加密之类的吗？

也不是吧，我用gmrender是可以正常播放的。







参考资料

1、官网

这个对相关知识讲得非常全面。很好。

https://www.lesbonscomptes.com/upmpdcli/upmpdcli-manual.html