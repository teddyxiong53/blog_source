---
title: vue之vue-cnode代码分析
date: 2019-08-21 17:17:03
tags:
	- vue
---

1

代码在这里：

https://github.com/lzxb/vue-cnode

看main.js里。

```
import 'normalize.css'
	这个是进行一些基础的css设置。
	这个项目在这里。
	https://github.com/necolas/normalize.css/
	
```



cnode的api是这样的：

```
路径前缀为：
https://cnodejs.org/api/v1

主题
获取所有
get /api/v1/topics
获取指定主题
get /api/v1/topic/5433abed12

主题收藏
post /api/v1/topic_collect/collect
	参数：
		accessToken
		topic_id
	返回值：
		{"success": true}
取消收藏
post /api/v1/topic_collect/de_collect
获取用户收藏的所有主题
get /api/v1/topic_collect/xx


用户
获取用户信息
get /api/v1/user/xx
验证accessToken的正确性
post /api/v1/xxxxxxxx

消息通知
获取未读消息数
get /api/v1/message/count
获取所有消息
get /api/v1/messages
把所有的消息标记为已读
post /api/v1/message/mark_all
把单个消息标记为已读
post /api/v1/message/mark_one/xxxxxx
```



参考资料

1、

https://cnodejs.org/api