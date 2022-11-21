---
title: pastebin研究
date: 2022-11-04 19:48:32
tags:
	- 网络

---

--

看flask的一些项目的时候，看到有人实现pastebin这样一个形态。

之前没有了解过这个东西。

现在了解一下。

1.为什么需要 pastebin ？
一开始，pastebin 主要用来分享代码，程序员写完代码后想给别人看，直接把代码粘贴至 pastebin，然后把 url 发给其他人，其他人点开链接就可以直接看到代码，代码的缩进格式会保持不变，代码评审人员看起来会比较舒服。实际上，任何纯属文本数据都可以通过 pastebin 来共享，比如以下应用场景：

用做一个在线的纯文本文档。

突破限制，发一些长推文。比如 twitter 限制只能发 140 个字符的推文，这样我们将长推文写在 pastebin 上，然后在 twitter 上发 url 即可。

上传源代码用于代码评审和合作。

重新发表一些被主流网站删除的文章。

垃圾邮件/网站的促销活动，因为内容是一个链接，可以绕过反垃圾、反广告系统。

分享一些黑色的网站，宣传一些隐私的活动或其他敏感信息，因为生成的 url 是不可猜测的。



# flask实现pastebin



# 参考资料

1、

这篇文章不错。

https://blog.csdn.net/somenzz/article/details/115107134

2、

https://github.com/donnemartin/system-design-primer/blob/master/README-zh-Hans.md