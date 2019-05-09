---
title: 微信之用nodejs做公众号后台
date: 2019-05-09 11:18:11
tags:
	- nodejs
	- 微信
---

1

按照《nodejs微信公众号开发——1》这个系列教程来。

下载对应的github的代码：

https://github.com/Panfen/wemovie

登陆自己的公众号（我的是一个订阅号），生成测试号，把appid和appsecret记录下来。

填写到config.js里。

然后启动localtunnel服务。

把得到url填写到测试号的配置里。

然后扫描测试号的二维码进行关注。微信提示“该公众号提供的服务出现故障 请稍后再试”。

我要看一下代码先。

看到node app.js这里，有错误：

```
hlxiong@hlxiong-VirtualBox ~/work/test/wechat/wemovie-master $ node app.js       
Listening 8080...

  Error: get menu failed!
      at /home/hlxiong/work/test/wechat/wemovie-master/wechat/wechat.js:244:12
      at tryCatcher (/home/hlxiong/work/test/wechat/wemovie-master/node_modules/bluebird/js/release/util.js:16:23)
      at Promise._settlePromiseFromHandler (/home/hlxiong/work/test/wechat/wemovie-master/node_modules/bluebird/js/release/promise.js:512:31)
      at Promise._settlePromise (/home/hlxiong/work/test/wechat/wemovie-master/node_modules/bluebird/js/release/promise.js:569:18)
      at Promise._settlePromise0 (/home/hlxiong/work/test/wechat/wemovie-master/node_modules/bluebird/js/release/promise.js:614:10)
      at Promise._settlePromises (/home/hlxiong/work/test/wechat/wemovie-master/node_modules/bluebird/js/release/promise.js:694:18)
      at Promise._fulfill (/home/hlxiong/work/test/wechat/wemovie-master/node_modules/bluebird/js/release/promise.js:638:18)
```

看到在config目录下，有一个wechat.txt文件。

里面有accessToken。这个从哪里来呢？

我们在浏览器访问一下这个地址。里面的appid和appsecret替换一下。

```
https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=APPID&secret=APPSECRET
```

可以得到返回的json字符串。我们复制替换原来的wechat.txt里的内容。

但是我看到wechat.txt里的内容会被修改的。所以其实不需要手动来做。

现在仍然是一样的错误。

我加上打印，当我在微信里发一个消息给公众号的时候，打印了这些：

```
{ request:
   { method: 'POST',
     url:
      '/?signature=f0a9ee690053162456a4cf66d68853f57bd2cfda&timestamp=1557383427&nonce=1882778831&openid=oK7Cx5_61yrpcWw9KN2kytKGDBZ8',
     header:
      { 'x-real-ip': '203.205.219.181',
        'x-forwarded-for': '203.205.219.181',
        host: 'moody-goose-97.localtunnel.me',
        'x-forwarded-proto': 'https',
        'x-nginx-proxy': 'true',
        connection: 'close',
        'content-length': '280',
        'user-agent': 'Mozilla/4.0',
        accept: '*/*',
        pragma: 'no-cache',
        'content-type': 'text/xml' } },
  response: { status: 404, message: 'Not Found', header: {} },
  app: { subdomainOffset: 2, proxy: false, env: 'development' },
  originalUrl:
   '/?signature=f0a9ee690053162456a4cf66d68853f57bd2cfda&timestamp=1557383427&nonce=1882778831&openid=oK7Cx5_61yrpcWw9KN2kytKGDBZ8',
  req: '<original node req>',
  res: '<original node res>',
  socket: '<original node socket>' }
```



参考资料

1、

https://github.com/node-webot/wechat

2、Node.js + Express 认证微信公众号

https://juejin.im/post/5b403977e51d45191d79ba5a

3、 nodejs微信公众号开发——1.接入微信公众号

https://segmentfault.com/a/1190000008979327