---
title: 微信之openid和unionid理解
date: 2019-04-24 15:51:25
tags:
	- 小程序

---



一个openid，对于一个公众号的空间内，是唯一的。

代表了关注这个公众号的一个用户。

unionid，对于一个微信开放平台下的应用，同一个用户的unionid是唯一的。

就像超市里的会员卡。

每个接入到微信的应用（包括公众号、app）就相当于一个独立的商场。

用户使用这些应用就像是逛商场。

商场为会员卡来唯一识别每一个顾客。

会员卡只能在对应的商场才能用。

这样比较安全，比你用身份证去逛超市要安全。

这个会员卡，就相当于openid。

而像万达这样的大集团。他们有不同的商场，他们的商场之间的会员卡是可以通用的。

那么他们的会员卡号，就要保证所有商场都唯一。这个就是unionid了。

获得了开发平台认证的，才有unionid。

一个unionid，可以绑定10个app、10个网站、10个公众号。

```
  // 获取 WX Context (微信调用上下文)，包括 OPENID、APPID、及 UNIONID（需满足 UNIONID 获取条件）
  const wxContext = cloud.getWXContext()
```



openid是28位的。

unionid是29位的。



第三方获取openid的两种方式：

1、静默授权。用户无感知。

2、用户同意授权。



可以这样理解：

```
openid = hash(uid + app_id)
```

你无法从openid反推uid。uid就是用户的身份证（微信id）。是腾讯的命根子，它不会给你的。

而且，对于用户来说，也不安全。





参考资料

1、给产品经理讲技术：微信的openid和unionid

https://www.25xt.com/html5css3/11968.html

2、关于微信openid没人提及过的几个问题

https://segmentfault.com/q/1010000002403358

3、微信开发中 openID 与 unionID 的区别

https://juejin.im/post/5c7c6cec51882577f37076d6