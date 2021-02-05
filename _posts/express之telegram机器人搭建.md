---
title: express之telegram机器人搭建
date: 2021-02-05 14:36:11
tags:
	- telegram

---

--

看telegram里有很多的机器人，又在github上看到有python写的telegram，那么自然就想到express也可以做。看看具体怎么实现。

telegram提供了bot api。

有一个对应的npm包，叫telegram-bot-client。

写一个client.js

```
var TelegramClient = require('telegram-bot-client')
var client = new TelegramClient('xxx')//写入你的telegram bot token
module.exports = client;
```

app.js

```
var app = express()
var client = require('./client')
client.setWebhook('xxx')//你的webhook url
app.post('/', (req, res, next) {
	client.sendMessage(req.body.message.chat.id, 'hello I am robot')
	.promise()
	.then(
		()=> res.json({ok:true})
	).catch(next)
})
```

就这么简单。



参考资料

1、Building a Telegram Bot using express.js

https://blog.frederikring.com/articles/telegram-bot-express-js/