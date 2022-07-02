---
title: express之expressCart分析
date: 2021-02-02 16:00:11
tags:
	- express

---

--

expressCart是一个基于express的商城项目。

代码在这：

https://github.com/mrvautin/expressCart

下载代码，

```
npm i
npm run start
```

先到这个管理界面：

http://172.16.2.153:1111/admin

进行注册，然后登陆。

就可以进行商品信息的添加。

感觉不太好。添加商品，不成功，但是也没有明确给出提示，让我很蒙圈，也不知道哪里写得不对。

还是继续研究一下。毕竟基于express的开源商城项目，算这个比较正式一点。

仔细研究一下。

现在admin界面可以进去。

需要先设置用户信息。密码要复杂一点的。

然后用邮箱进行登陆。

这个登陆的管理员。

进行首页进行登陆。管理员是不能登陆的。

但是好像也没有看到注册。



参考资料

1、

https://github.com/mrvautin/expressCart/wiki
