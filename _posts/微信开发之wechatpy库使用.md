---
title: 微信开发之wechatpy库使用
date: 2023-01-20 16:20:31
tags:
	- 微信

---



wechatpy是python开发的一个微信公众号后台框架。

https://github.com/wechatpy/wechatpy

现在打算用这个来把我的订阅号完善起来。

之前只有接收京东cookie更新的功能。现在不做这个了。所以要改变用途。

# 先把echo功能跑起来

就是为订阅号发什么，订阅号就回复什么。

参考这个来做。

https://github.com/wechatpy/wechatpy/blob/master/examples/echo/app.py

只是要注意，我的微信的域名，是通过前端的nginx反向代理后的，所以直接是

```
@app.route('/')
而不是
@app.route('/wechat')
```

我的没有使用加密方式。

运行起来，是可以正常进行echo回复的。

# 进一步开发

看了文档，没有什么特别的。

有点无趣，写的不怎样。

都是商用开发的内容。

我后面就根据需要直接对文字内容进行区分处理吧。



# 参考资料

