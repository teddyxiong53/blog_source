---
title: B站研究之BiliExp脚本分析
date: 2020-12-15 11:46:30
tags:
- ubuntu
---

1

代码在这里：

https://github.com/happy888888/BiliExp

总体是一个运行然后退出的逻辑，需要借助cron这些工具来实现定时运行。

这样也挺好。

使用步骤：

1、把代码下载到Linux上。

2、修改config/config.json文件。把大部分都设置为false。我基本只使能了抽奖的。

3、重点的cookie数据设置。浏览器按F12，复制需要的3个东西。（拖动选择，然后按ctrl+C可以复制）

4、python3 BiliExp.py就可以了。这个脚本没有依赖太多东西，所以运行正常。不到一分钟运行完成。

![image-20201215115002020](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201215115002020.png)

5、完成后，会推送一条消息到你的微信，这个是靠Server酱的服务来做的。我之前有一个key，所以可以用。





银瓜子是什么？这个是看直播相关的，我从不看直播。所以不管。

所以银瓜子换硬币的，可以禁用掉。

这个比较适合部署到github actions来运行。



代码使用了python asyncio来做。



参考资料

1、

https://blog.csdn.net/z515878963/article/details/81184068