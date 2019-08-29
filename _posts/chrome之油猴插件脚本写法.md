---
title: chrome之油猴插件脚本写法
date: 2019-08-28 14:36:03
tags:
	- chrome
---

1

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



参考资料

1、油猴脚本开发入门(TamperMonkey)

https://www.jianshu.com/p/2408cdb487c0

2、官网资料

<https://www.tampermonkey.net/documentation.php?version=4.8.41&ext=dhdg>