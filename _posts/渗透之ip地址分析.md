---
title: 渗透之ip地址分析
date: 2020-03-10 11:31:28
tags:
	- 渗透

---

1

获取到一个公网ip地址，可以从中分析出哪些有用的信息？

1、直接网上ip地址查询，可以搜索出一些信息。

2、whois 后面跟ip地址，可以查出更多的信息。

以139.155.29.206 这个地址为例。

网上查到的信息是。

```
您查询的IP:139.155.29.206
本站数据：四川省成都市 腾讯云
参考数据1：四川成都 tencent.com 电信/联通/移动
参考数据2：北京市海淀区 北龙中网(北京)科技有限公司
兼容IPv6地址：::8B9B:1DCE
映射IPv6地址：::FFFF:8B9B:1DCE
```

whois的信息更多更详细。整理如下：

```
1、属于139.155.0.0/16网段。
2、属于APNIC分配。分配时间是2010-11-03
```

```
person:         James Tian
address:        9F, FIYTA Building, Gaoxinnanyi Road,Southern
address:        District of Hi-tech Park, Shenzhen
country:        CN
phone:          +86-755-86013388-84952
e-mail:         harveyduan@tencent.com
nic-hdl:        JT1125-AP
mnt-by:         MAINT-CNNIC-AP
last-modified:  2016-10-31T07:10:47Z
source:         APNIC

person:         Jimmy Xiao
address:        9F, FIYTA Building, Gaoxinnanyi Road,Southern
address:        District of Hi-tech Park, Shenzhen
country:        CN
phone:          +86-755-86013388-80224
e-mail:         harveyduan@tencent.com
nic-hdl:        JX1747-AP
mnt-by:         MAINT-CNNIC-AP
last-modified:  2016-11-04T05:51:38Z
source:         APNIC
```



参考资料

1、

