---
title: 签到之dailycheckin
date: 2021-05-03 10:32:11
tags:
	- 签到

---

--

代码在这里。

https://github.com/Sitoi/dailycheckin

python写的。

配置用json写的，总体操作性还比较好。

配置文件在config/config.json里。

现在看看什么值得买网站的签到。

这个的cookie比较长。

需要的格式是这样

```
"smzdm_cookie": "__jsluid_s=xxxxxx; __ckguid=xxxxxx; device_id=xxxxxx; homepage_sug=xxxxxx; r_sort_type=xxxxxx; _zdmA.vid=xxxxxx; sajssdk_2015_cross_new_user=xxxxxx; sensorsdata2015jssdkcross=xxxxxx; footer_floating_layer=xxxxxx; ad_date=xxxxxx; ad_json_feed=xxxxxx; zdm_qd=xxxxxx; sess=xxxxxx; user=xxxxxx; _zdmA.uid=xxxxxx; smzdm_id=xxxxxx; userId=xxxxxx; bannerCounter=xxxxxx; _zdmA.time=xxxxxx;"
```

我写一个脚本提取一下吧。一个个复制也是麻烦。

写了一下，发现提取的效果不太好。

直接复制，手动去掉一些看上去明显不需要而且导致json解析文件的部分。

直接可以签到成功。



