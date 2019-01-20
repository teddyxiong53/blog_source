---
title: 《chrome扩展及应用开发》读书笔记
date: 2019-01-19 20:41:51
tags:
	- chrome

---



书的地址在这：http://www.ituring.com.cn/book/miniarticle/60134

github在这里：

https://github.com/sneezry/chrome_extensions_and_apps_programming

# my_clock

**这个是演示最简单的应用。**

这个是第一个应用。

新建一个my_clock目录。

新建manifest.json文件。

这个只写了popup.html。没有写选项的文件。

我放在这里了。

https://github.com/teddyxiong53/chrome_plugin/tree/master/study/my_clock

# cannot_touch

**这个是演示操作当前界面元素。**

本来要实现的效果是你鼠标靠近谷歌的搜索按钮的时候，这个按钮的位置就会自动躲开。

可以没有图标，没有html文件，就一个manifest.json和一个js文件，也可以构成一个插件。

https://github.com/teddyxiong53/chrome_plugin/tree/master/study/cannot_touch

我在当前的谷歌网站上，是无法实验通过的。

因为现在的谷歌页面改了。

不管先。

这个的目的是测试操作用户正在浏览的界面。



#what_is_my_ip

**这个是演示跨域。**

简单说，就是访问其他的网站的内容。

跨域的概念：

跨域是指js通过XMLHTTPRequest请求数据时，调用js的页面所在的域和被请求页面的域不一致。

什么是域？协议+主机+端口号。这个就是一个域。

```
http://xx.com:8080
```

这就是一个域。

对于网站来说，浏览器处于安全的考虑，是不允许跨域的。

但是如果不允许插件跨域，那么插件的功能就受到很大的限制。

所以谷歌允许chrome扩展不受限于跨域。

需要在manifest.json里加上声明。

如果我们想要设计一款获取维基百科的数据并显示在其他网页中的扩展，就要在manifest里这样声明。

```
{
  "permissions": [
        "*://*.wikipedia.org/*"
    ]
}
```

我们可以利用如下的代码发起异步请求。

```
function httpRequest(url, callback) {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url, true);
    xhr.onreadystatechange = function() {
        if(xhr.readyState == 4) {
            callback(xhl.responseText);
        }
    }
    xhr.send();
}
```

这个我用httpbin的来替代。可以运行成功。

碰到一点问题，调试得到经验：

1、修改后，什么都不用做，直接点击插件就可以看到生效的。

2、在popup弹出的界面上右键，选择审查，可以看到对应的console，可以加log进行调试。

# website_status

**这个是演示常驻后台的用法。**

调试后台的方法。这个需要在chrome://extensions里，点击背景页，才可以看到对应的console。

我采用proxy switch的方法，并不能看出效果来。console里在打印错误。



# weather

**这个是演示带选项页面的用法。**

就是在manifest里加一个“options_page”的选项就好了。

把对应的html写了就行。

当前的写法不行了，因为这个网站现在需要认证了。



# 右键菜单



# 操作你的浏览器

## 书签

chrome为开发者提供了添加、分类和排序等方法来操作书签。

同时也提供了读取书签的方法。

要在扩展中操作书签，需要在manifest里添加书签权限。

```
"permissions": [
  "bookmarsk"
]
```

书签对象有8个属性：

```
id
parentId
index
url
title
dateAdded
dateGroupModified
children
```

书签对象包括文件夹和书签。就像文件对象包括文件夹和文件一样。

只有id和title是必须的。

id是自动分配的。

**创建一个书签的方法：**

```
chrome.bookmarks.create({
  parentId:"1",
  index:0,
  title:"google",
  url:"http://www.google.com"
}, function(bookmark) {
  console.log(bookmark);
});
```

注意上面的parentId，写的是1, 0对应的是根节点的id。

根节点下面不允许创建书签和书签分组的。

根节点下面有3个默认的书签分组：

```
书签栏
其他书签
移动设备书签
```

如果不指定parentId，默认是加入到其他书签里。

create方法成功后，会自动调用后面的回调函数。

传递给回调的参数是书签对象。

create函数只接受8个属性里面的4个。其他4个不支持。

如果不指定index，默认是加到parent的最后面。

创建书签分组，就是create传递的属性里，不包含url，chrome就认为是书签分组。

**调整书签的位置。**

通过move方法可以调整书签的位置。

这种调整是可以跨越父节点的。

例如下面的代码，就把id为16的书签移动到了id为17的父节点的第5的位置。

```
chrome.bookmarks.move('16',{
  parentId:'7',
  index:4
}, function(bookmark) {
  console.log(bookmark);
});
```

**更新书签。**

用update方法来做。可以更改title和url。

```
chrome.bookmarks.update("16", {
  title:"gmail",
  url:"https://mail.google.com"
}, function(bookmark) {
  console.log(bookmark);
});
```

**移除书签。**

通过remove和removeTree可以删除书签。

remove可以删除书签和空的书签分组。

removeTree则可以删除包含书签的书签分组。

```
chrome.bookmarks.remove("16", function() {
  console.log("boorkmark 16 has been removed");
});
chrome.bookmarks.removeTree("6", function() {
  console.log("bookmark group 6 has been removed");
});
```

**获取书签内容。**

用getTree方法可以获取完整的书签树。

如果书签树的结构过于复杂，那么getTree的效率就会很低。

```
chrome.bookmarks.getTree(function(bookmarkArray) {
  console.log(bookmarkArray);
});
```

这个函数返回的是一个数组，数组里只有一个元素，就是书签树的根节点。

用getChildren可以获取指定节点的子节点。但只限于当前层，不会遍历子目录的。

下面的代码获取了根节点的所有子节点。

```
chrome.bookmarks.getChildren("0", function(bookmarkArray) {
  console.log(bookmarkArray);
});
```

getSubTree，跟getChildren不同，它会遍历子目录里的内容。

下面的代码跟getTree等价。

```
chrome.bookmarks.getSubTree("0", function(bookmarkArray) {
  console.log(bookmarkArray);
});
```

get方法可以获取指定节点的属性。可以同时获取多个，把id用数组传递下去就好了。

```
chrome.bookmarks.get(['16','17'], function(bookmarkArray) {
  console.log(bookmarkArray);
});
```

getRecent方法，则获取最近条件的N个书签。

```
chrome.bookmarks.getRecent(5, function(bookmarkArray) {
  console.log(bookmarkArray);
});
```

search方法。可以搜索匹配指定字符串的书签对象，匹配的位置包括title和url。

```
chrome.bookmarks.search("google", function(bookmarkArray) {
  console.log(bookmarkArray);
});
```

**书签相关的事件。**

chrome提供了多个事件来监控书签操作行为。

```
onCreated：传递给回调的是bookmark对象。
onRemoved：传递了id和removeInfo。
onChanged：传递了id和changeInfo。
onMoved：传递了id和moveInfo。
onChildrenReorded：记录书签目录下更改子节点顺序的行为。传递了id和reorderInfo。注意是reorder（排序）
```

```
chrome.bookmarks.onCreated.addListener(function(bookmark) {
  console.log(bookmark);
});
```

## cookies

cookies是浏览器记录在本地的用户数据。

例如用户登录信息。

要管理cookies，就需要在manifest里声明cookies权限。同时还有声明cookies所在的域。

```
"permissions": [
  "cookies",
  "*://*.google.com"
]
```

如果你要管理所有的cookies，则这样声明。但是尽量不要这么做。用户会觉得不安全。

```
"permission":[
  "cookies",
  "<all_urls>"
]
```

Cookie对象包括这些属性：

```
name
value
domain
hostOnly
path
secure
httpOnly
session
expirationDate
storeId
```

**读取cookies。**

有2个方法：get和getAll。

get方法可以指定name、url、storeId。storeId可以不传递。

```
chrome.cookies.get({
  url:"https://github.com",
  name:"dotcom_user"
}, function(cookie) {
  console.log(cookie.value);
})
```

```
chrome.cookies.getAll({}, function(cookies) {
  console.log(cookies);
});
```

**设置cookies。**

```
chrome.cookies.set({
  "url": "http://github.com/test_cookie",
  "name": "test",
  "value": "foo",
  "secure": false,
  "httpOnly": false
}, function(cookie) {
  console.log(cookie);
});
```

**删除cookies。**

```
chrome.cookies.remove({
  url:"http://www.google.com",
  name: "_ga"
}, function(result) {
  console.log(result);
});
```

除非你很清楚自己在做什么，不要轻易去删除cookies，用户会很生气的。

**cookies相关事件。**

只有有个onChanged事件。监控设置和删除行为。

```
chrome.cookies.onChanged.addListener(function(changInfo) {
  console.log(changeInfo);
});
```

## 浏览器历史数据

这个我不感兴趣。先跳过。



## 管理插件

我们一般是通过chrome://extensions来进行插件的管理。

但是实际上也可以通过代码来做。

就是management接口。

要使用管理接口。需要在manifest里声明。

```
"permissions": [
  "management"
]
```

获取用户安装的插件。

有2个方法：get和getAll。

```
chrome.management.getAll(function(exInfoArray) {
  console.log(exInfoArray);
});
chrome.managerment.get(exId, function(exInfo) {
  console.log(exInfo);
});
```

exInfo对象的属性有：

```
id
name
shortName
description
version
mayDisable
enabled
disableReason
type：类型。可以取值为extension、hosted_app、packaged_app、legacy_packaged_app、theme。
appLaunchUrl
homepageUrl
updateUrl
offlineEnabled
optionUrl
icons: [
  {
    size
    url
  }
]
permissions
hostPermissions
installType：可能取值为：admin、development、normal、sideload、other。
```

## 标签

标签对象的属性：

```
id
index
windowId
openerTabId
highlighted
active
pinned
url
title
favIconUrl
status
incognito
width
height
sessionId
```

对应的是tabs相关方法。

manifest里申请权限：

```
"permissions:  [
  "tabs"
]
```

**获取标签信息**

```
get：获取指定id的的标签。
getCurrent：获取运行脚本所在的标签。
query：获取所有符合条件的标签。
```

```
chrome.tabs.get(tabId, function(tab) {
  console.log(tab);
});
chrome.tabs.getCurrent(function(tab) {
  console.log(tab);
});
```

query可以指定的条件有：

```
active
pinned
highlighted
currentWindow
lastFocusedWindow
status
title
url
windowId
windowType
index
```

例如下面的代码，获取了所有在窗口中活动的标签。

```
chrome.tabs.query({
  active:true
}, function(tabArray) {
  console.log(tabArray);
});
```

**创建标签**

```
chrome.tabs.create({
  windowId: wId,//wId表示创建标签所在的窗口的id，如果不指定，则在当前窗口打开。一般也不用指定。
  index:0,
  url:"http://www.google.com",
  active: true,
  pinned: false,
  openerTabId: tId
}, function(tab) {
  console.log(tab);
});
```

还可以通过duplicate方法来复制创建一个。

```
chrome.tabs.duplicat(tabId, function(tab) {
  console.log(tab);
});
```

更新标签。

```
chrome.tabs.update(tabId, {
  url: "http://www.google.com"
}, function(tab) {
  console.log(tab);
});
```

移动标签。

```
chrome.tabs.move(tabIds, {
  "windowId": wId,
  "index":0
}, function(tabs) {
  console.log(tabs);
});
```

重载标签。

```
chrome.tabs.reload(tabId, {
  bypassCache:true
}, function() {
  console.log("the tab has been reloaded");
});
```

移除标签。

```
chrome.tabs.remove(tabIds, function() {
  console.log("the tabs has been closed");
});
```

tabIds可以是一个数字，也可以是数字组成的数组。

获取当前标签页面的显示语言。

```
chrome.tabs.detectLanguage(tabId, function(lang) {
  console.log("the primary language of the tab is " + lang);
});
```

如果不指定tabId，则是获取当前的tab的语言。

获取标签可见部分的截图。

```
chrome.tabs.captureVisiableTab(windowId, {
  format: "jpeg",//还支持png。png的话，则会忽略quality参数。
  quality: 50
}, function(dataUrl) {
  window.open(dataUrl, "tabCapture");
});
```

注入js和css。

```
chrome.tabs.executeScript(tabId, {
  file: "js/ex.js",
  allFrames: true,
  runAt: "document_start"
}, function(resultArray) {
  console.log(resultArray);
});
```

也可以直接注入代码。

```
chrome.tabs.executeScript(tabId, {
  code: "document.body.style.backgroundColor='red'",
  allFrames: true,
  runAt: "document_start"
}, function(resultArray) {
  console.log(resultArray);
});
```

css的注入也类似上面的。

和其他标签通信。

```
chrome.tabs.sendMessage(tabId, message, function(response) {
  console.log(response);
});
```

标签相关事件。

因为标签的相关操作比较多，所以相应的事件也很多。

```
onCreated
onUpdated
onMoved
onActivated
onHighlighted
onDetached
onAttached
onRemoved
onReplaced
```



# 高级api

## 下载

声明权限。

```
"permissions": {
  "downloads"
}
```

创建下载。

```
chrome.downloads.download(options, callback);
```

options的属性：

```
url
filename
conflictAction：同名文件处理方式，可能为：uniquify（加后缀保证唯一），overwrite，prompt。
saveAs：是否弹出另存为窗口。
method: 请求方法是post还是get。
headers：自定义header数组。
body；post的数据。
```

下面我们就写一个保存当前页面的所有图片的插件。

manifest.json

```
{
  "manifest_version": 2,
  "name": "save all images",
  "version": "1.0",
  "description": "save all the images in current tab",
  "background": {
    "script": ["background.js"],
    "persistent": false
  },
  "permissions": [
    "activeTab",
    "contextMenus",
    "downloads"
  ]
}
```

编写background.js文件，用来：

1、创建邮件菜单。

2、用户点击菜单后，向当前标签页注入脚本。

3、进行下载。

```
chrome.runtime.onInstalled.addListener(function() {
  chrome.contextMenus.create({
    "id": "saveall",
    "type": "normal",
    "title": "保存所有图片"
  });
});
chrome.contextMenus.onClicked.addListener(function(info, tab) {
  if(info.menuItemId == "saveall") {
    chrome.tabs.executeScript(tab.id, {file: "main.js"}, function(results) {
      if(results && results[0] && results[0].length) {
        results[0].forEach(function(url) {
          chrome.downloads.download({
            url:url,
            conflictAction: "uniquify",
            saveAs: false
          });
        });
      }
    });
  }
});
```

最后编写注入脚本main.js。

```
[].map.call(document.getElementByTagName('img'), function(img) {
  return img.src;
});
```

## 网络请求

chrome提供了较为完整的方法，给扩展程序来分析、阻断和修改网络请求。

同时也提供了一系列的监听事件来监听各个阶段。

```
onBeforeRequest
onBeforeSendHeaders
onSendHeaders
onHeadersReceived

onResponseStarted
onCompleted
```

声明：

```
"permissions": [
  "webRequest",
  "webRequestBlocking",
  "*://*.google.com"
]
```

比较实用的做法有：阻断连接、更改headers、重定向。

阻断连接。

```
chrome.webRequest.onBeforeRequest.addListener(function(details) {
  return {cancel: true};
},
{
  urls: [
    "*://xx.com/*"
  ]
},
["blocking"]
);
```

更改headers

```
chrome.webRequest.onBeforeSendHeaders.addListener(
	function(details) {
      for(var i=0, headerLen=details.requestHeaders.length; i<HeaderLen; i++) {
        if(details.requestHeaders[i].name == "User-Agent") {
          details.requestHeaders.splice(i,1);
          break;
        }
        return {requestHeaders: details.requestHeaders};
      }
	},
	{
      urls: [
        "<all_urls>"
      ]
	},
	[
      "blocking",
      "requestHeaders"
	]
);
```

重定向，下面的代码把所有访问www.google.com.hk重定向到www.google.com。

```
chrome.webRequest.onBeforeRequest.addListener(
	function(details) {
      return {redirectUrl: details.url.replace("www.google.com.hk", "www.google.com")};
	},
	{
      urls: [
        "*://www.google.com.hk/*"
      ]
	},
	[
      "blocking"
	]
);
```

## 代理

声明：

```
"permissions": [
  "proxy"
]
```

可以通过

```
chrome.proxy.settings.set
```

这个方法来设置代理服务器。

这个方法需要2个参数：

```
1、代理设置对象。
2、回调函数。
```

代理设置对象包括：

```
1、mode属性。代理模式，可能为：direct（不代理），auto_detect、pac_script、fixed_servers、system。
2、rules属性。可选。
3、pacScript属性。可选。
```

举例：

```
var config = {
  mode: "fixed_servers",
  rules: {
    proxyForHttp: {
      scheme: "socks5",
      host: "1.2.3.4",
      port: 1080
    },
    proxyForHttps: {
      scheme: "sock5",
      host:"1.2.3.4",
      port:1080
    },
    proxyForFtp: {
      scheme: "http",
      host: "1.2.3.4",
      port:1080
    },
    bypassList: ["xx.com"]
  }
};
chrome.proxy.settings.set(
	{value: config},
	function() {
      console.log("set proxy ok");
	}
);
```

可以分析ProxySharp这个插件的代码来学习。

## 系统信息

chrome听了获取系统CPU、内存和 存储设备信息的接口。

声明：

```
"permissions": [
  "system.cpu",
  "system.memeory",
  "system.storage"
]
```

都有getInfo的方法。

```
chrome.system.cpu.getInfo(function(info) {
  console.log(info);
});
```



# chrome应用基础

## 扩展和应用的区别

chrome把平台上的程序分为扩展和应用。

这2个的文件结构是一样的。那么区别何在呢？

在早期的chrome里，这二者的区别非常模糊。

现在谷歌在把这二者区分开来。

总的来说：

1、扩展跟浏览器结合更加紧密。

2、应用则相当于把chrome看出一个开发环境。跟浏览器本身关系不大。

但是现在谷歌还是没有给出明确的定义。

应用范围两种：

1、hosted app。这个功能简单，像是一个高级是书签。只有一个图标和一个manifest.json。

2、packaged app。主要是这种。

应用一般会自动弹一个窗口出来的。

## 应用窗口

创建窗口。

```
chrome.app.window.create("blank.html", {
  id: "default"
});
```

窗口的默认大小是512x384像素。

标题栏高度一般是22像素。

你可以指定窗口的大小。

```
chrome.app.window.create("main.html", {
  id: "main",
  bounds: {
    width: 800,
    height:600
  },
  resizable: false
});
```

不显示标题栏。

```
chrome.app.window.create("blank.html", {
  id: "blank",
  frame: "none"
});
```

这样得到一个全白的窗口，你啥也干不了。不能关闭，不能最大化最小化。

我们可以把blank.html改一下。

```
<html>
    <head>
        <title>a more free style window</title>
        <style>
            body {
                margin: 0;
                padding: 0;
                border: #eee 1px solid;
            }
            #title_bar {
                -webkit-app-region: drag;<!-- 这一行是重点，现在可以拖拽了。 -->
                height: 22px;
                line-height: 22px;
                font-size: 16px;
                background-color: #eee;
                padding: 0 10px;
                box-sizing: border-box;
            }

        </style>
    </head>
    <body>
        <div id="title_bar">a more free style window</div>
    </body>
</html>
```

我们可以自己写最大化、最小化、关闭这3个按钮。

## 写一个计算机性能监视器



# 参考资料

1、Chrome插件（Extensions）开发攻略

https://www.cnblogs.com/guogangj/p/3235703.html#t9

