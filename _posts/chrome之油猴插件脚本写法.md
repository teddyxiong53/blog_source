---
title: chrome之油猴插件脚本写法
date: 2019-08-28 14:36:03
tags:
	- chrome
---

1

# 热门脚本

就看这个网站的脚本就好。比较好。

https://greasyfork.org/zh-CN/scripts

## AC-baidu:重定向优化百度搜狗谷歌必应搜索_favicon_双列

* 去掉百度、搜狗、谷歌搜索结果的重定向，回归为网站的原始网址

- 默认移除百度百家号的内容--应广大群众的需求
- 百度和谷歌搜索页面可以设置为单列、双列模式

效果是这样：

![image-20201211114753818](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211114753818.png)

在百度页面的右上角，增加了一个自定义按钮，可以进行设置。

![image-20201211114919680](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20201211114919680.png)

## 百度文库破解加强、全网VIP视频破解，免费在线看、抖音去水印下载、知乎使用增强、CSDN使用增强，等多功能脚本

1：百度文库文档免费下载、文档内容自由复制、广告过滤；

2：CSDN阅读加强：CSDN自动展开、去广告、净化剪贴板、免登陆等；

3：知乎使用增强：外链接直接跳出、内容自动展开、短视频下载等；

4：抖音去水印原视频下载，非调用第三方；

5：视频解析，支持大部分视频播放平台[支持优酷 | 腾讯 | 爱奇艺 | 哔哩哔哩等常用视频]；

6：全网音乐直接下载；

7：优惠券查询

## 本地 YouTube 下载器

https://greasyfork.org/zh-CN/scripts/369400-local-youtube-downloader

不需要透过第三方的服务就能下载 YouTube 视频。

此脚本只支援 Violentmonkey & Tampermonkey，请 Greasymonkey 的使用者注意一下。 

### 为什么不用 `youtube-dl`?

事实上 `youtube-dl` 确实比这个脚本可靠很多，因此如果你习惯的话继续使用 `youtube-dl` 是最好的选择。 然而，这个脚本的目的是为了让你能**简单**的一键下载 YouTube 影片，不用打开你的终端机去输入 `youtube-dl`。



# 编写方法

新建一个脚本，自动就有这个基本框架。

在里面进行修改。

```
// ==UserScript==
// @name         New Userscript
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  try to take over the world!
// @author       You
// @match        https://*/* //这里改一下。对任意网址都有效。
// @grant        none
// ==/UserScript==

(function() {
    'use strict';

    // Your code here...
    alert("hello");//我只增加了这一行。
})();
```

主要是靠jquery来操作页面元素。

头部可以添加的信息有：

```
@name
@namespace
@version
@author
@description
@homepage, @homepageURL, @website and @source
@icon, @iconURL and @defaulticon
@icon64 and @icon64URL
@updateURL
@downloadURL
@supportURL
@include
@match
@exclude
@require
@resource
@connect
@run-at
@grant
@noframes
@unwrap
@nocompat
```

重点是：

connect，这个是ajax请求对象网址。

require，这个是包含jquery等依赖的脚本。

grant：允许哪些函数。



应用编程接口函数有：

```
unsafeWindow
Subresource Integrity
GM_addStyle(css)
GM_deleteValue(name)
GM_listValues()
GM_addValueChangeListener(name, function(name, old_value, new_value, remote) {})
GM_removeValueChangeListener(listener_id)
GM_setValue(name, value)
GM_getValue(name, defaultValue)
GM_log(message)
GM_getResourceText(name)
GM_getResourceURL(name)
GM_registerMenuCommand(name, fn, accessKey)
GM_unregisterMenuCommand(menuCmdId)
GM_openInTab(url, options), GM_openInTab(url, loadInBackground)
GM_xmlhttpRequest(details)
GM_download(details), GM_download(url, name)
GM_getTab(callback)
GM_saveTab(tab)
GM_getTabs(callback)
GM_notification(details, ondone), GM_notification(text, title, image, onclick)
GM_setClipboard(data, info)
GM_info
<><![CDATA[your_text_here]]></>
```



实现百度云vip下载的原理是

```
1、获取原始链接地址。这个就可以绕过大小限制，不用非得用百度客户端了。
2、url里被注入了app_id，这个是百度自己的应用id。百度内部是没有对自己的应用限速的。
```

baiduwp.com，这个是搭建的一个专门针对百度云下载的网站。

作者有一个小葱计算的云平台。

我觉得这个网站有提供价值。



vip视频观看的原理又是什么？

搜索“万能vip视频解析接口”。

```
这个网站可以解析，
https://660e.com
腾讯视频上，战狼2的地址：
https://v.qq.com/x/cover/wi8e2p5kirdaf3j.html
```

通过抓包抓到的播放地址，是一个随机生成的地址。

所以，现在那些vip视频播放网站，都是靠的自己开通网站的vip权限，然后把取得的真实播放地址，转发给服务器上的的服务器。

通过挂广告联盟的广告来赚钱。还有就是给购物网站导流来赚钱。



参考资料

1、油猴脚本开发入门(TamperMonkey)

https://www.jianshu.com/p/2408cdb487c0

2、官网资料

<https://www.tampermonkey.net/documentation.php?version=4.8.41&ext=dhdg>

3、百度云限速破解(原理)

https://blog.csdn.net/hjlyffsina/article/details/94590899

4、使用Tampermonkey(油猴) 插件，重新实现了，百度搜索热点过滤功能

https://www.cnblogs.com/xuyaowen/p/TamperMonkey-Hot-Search-Killer.html

5、【教程、无技术含量】简单的油猴脚本编写教程

这个实现了微博视频下载的插件。简单但是实用。

https://www.52pojie.cn/thread-614101-1-1.html

6、这个网站很好。

https://www.wandhi.com/

7、万能vip视频解析接口

https://blog.csdn.net/cat1210/article/details/81254706

8、各大视频网站VIP解析 是什么原理

https://www.52pojie.cn/thread-576602-1-1.html