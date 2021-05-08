---
title: 通知之pushplus
date: 2021-05-03 08:50:11
tags:
	- 通知

---

--

之前用了很长时间的server酱来做通知，但是后来server酱就限制了使用数量，每天只能发5条。就切换到pushplus上了。

pushplus功能也更强大。值得研究一下。

pushplus的QQ群号：**28619686**

pushplus集成了微信、短信、邮件等实时信息的推送。

你只需要调用简单的api，就可以快速完成消息的推送。

之前是这个网站，已经废弃了。

http://pushplus.hxtrip.com/

现在是这个网站了。

http://pushplus.plus/

但是2个网站其实都还能登陆。

get方式发送：

```
http://www.pushplus.plus/send?token=xxx&title=yyy&content=zzz&template=html
```

post方式发送

```
http://www.pushplus.plus/send
content-type:application/json

{
	"token":"xxx",
	"title":"yyy",
	"content":"zzz",
	"template":"html",
	"channel":"wechat",
	"webhook":"webhook编码"
}
```

template有这些可选值：

```
html
text
json
markdown
cloudMonitor:这个是阿里云的报警定制模板。
```

channel可以是：

```
wechat:这个是公众号，就是默认的。
webhook: 可以是企业微信机器人，钉钉机器人，飞书机器人。
cp:企业微信应用。
sms：短信，未开放。
mail；邮件，未开放。
```



参考资料

1、官网



