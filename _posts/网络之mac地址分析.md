---
title: 网络之mac地址分析
date: 2017-11-04 11:08:18
tags:
	- 网络

---



mac地址一共6个字节，前面3个字节是OUI（组织唯一标识符）。后面3个字节是厂家分配。

前面3个字节的分配，用IEEE来负责。

在以太网传输协议里，是高字节先传输，但是在一个字节内部，是最低位先传输。

所以mac地址的第一个字节的bit0就是最先传输的。它被赋予了特殊的含义。

它表示了这个mac地址是单播地址还是组播地址。

第一个的bit1也有特别含义，表示这个地址是全球唯一，还是本地自己用着玩的。

mac地址也分为单播、组播、广播。广播是全0xff。



现在公司购买了一个mac地址段。

要要生成所有可用的mac地址。看看有没有像ip地址那样有保留地址。

但是MAC地址只需要在一个局域网内地址不重复即可。也就是说，拥有相同MAC地址的设备，分别在不同的网络里时，并不会影响它们正常运行的。





参考资料

1、官方保留的MAC地址

https://blog.csdn.net/weixin_33924312/article/details/89826126

2、MAC地址唯一，不能满足通信需求吗？为什么需要IP？

https://new.qq.com/omn/20181008/20181008A0LOUY.html?pc

3、Android P特性：MAC地址随机化

https://baijiahao.baidu.com/s?id=1594444965942761348&wfr=spider&for=pc

4、故障-因为MAC地址冲突造成的故障

https://www.cnblogs.com/evan-blog/p/9977171.html

5、给出一个MAC地址怎样区分出他是单播,组播还是广播地址？？

https://zhidao.baidu.com/question/311545349.html