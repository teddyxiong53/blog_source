---
title: autojs（1）
date: 2023-05-05 13:22:11
tags:
	- autojs
---

--

# autojs替代品

autojs作者已经不更新了。转而做收费的autojs pro。而且不开源。

我只是偶尔轻度使用autojs。没有必要去付费。

当前有不少基于autojs的替代品。

## autoxjs

就是在autojs的基础上继续开发。

https://github.com/kkevsekk1/AutoX

## hamibot

这个也是基于autojs的。

还有配套的网站来远程管理。

# autox的资源



autox.js(autojs替代方案) 开发教程

https://blog.csdn.net/SUNbrightness/article/details/124229682

官网文档

http://doc.autoxjs.com

这个cli工具，生成autoxjs的工程目录。

https://github.com/kkevsekk1/webpack-autojs

# hamibot

这个因为有配套的网站，写代码调试都比较方便。

https://hamibot.com/

从这里直接写在线的脚本，执行就可以在手机上看到效果。

这里有一些脚本。

https://github.com/hamibot/awesome-hamibot

把这个下载到本地。

然后执行：

```
npm install
npm run build
```

把得到的dist/index.js上传到hamibot网站上。

然后加2个配置项，

```
const {
    _TOKEN,
    _SHOW_CONSOLE,
} = hamibot.env;
```

不加的话，会报错的。

然后执行，会有个warning，说pushplus报错。

这个肯定会报错。因为我们没有配置这个。

是因为这里要配置。src\config.json

```
[
    {
        "name": "_TOKEN",
        "type": "text",
        "label": "pushplus 的用户 Token",
        "help": "可以在 pushplus 的微信公众号中获取，不使用 pushplus 则留空"
    },
    {
        "label": "显示控制台(需要悬浮窗权限)",
        "type": "select",
        "name": "_SHOW_CONSOLE",
        "options": {
            "true": "是",
            "false": "否"
        }
    }
]
```

