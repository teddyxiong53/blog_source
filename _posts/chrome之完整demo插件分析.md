---
title: chrome之完整demo插件分析
date: 2019-01-21 14:37:12
tags:
	- chrome
---





参考的是这个demo：

https://github.com/sxei/chrome-plugin-demo

演示的功能有：

```
background操作
	1、打开background
		这样打开的。background.html文件还是有的。
		window.open(chrome.extension.getURL('background.html'))
		在background.html里有2个超链接，演示了跨域调用和获取popup标题。
			跨域调用就是访问了baidu.com，用jQuery的异步get方法。
	2、调用background里的js方法。
		var bg = chrome.extension.getBackgroundPage();
		是一个window对象。
		这样来获取到background对象。
		调用里面的自己写的函数：bg.testBackground();
	3、获取background页面的title。
		var bg = chrome.extension.getBackgroundPage();
		bg.document.title
	4、设置background页面的title。
		bg.document.title = title;
窗口演示操作
	1、打开新的窗口。
		chrome.windows.create({state: 'maximized'});
	2、执行简单窗口动画。
		chrome.windows.getCurrent
		chrome.windows.update
	3、当前窗口最大化。
		chrome.windows.getCurrent({}, (currentWindow) => {
		// state: 可选 'minimized', 'maximized' and 'fullscreen'
		chrome.windows.update(currentWindow.id, {state: 'maximized'});
		});
	4、当前窗口最小化。
	5、关闭当前窗口。
		chrome.windows.remove(currentWindow.id);
标签操作演示
	1、新标签打开百度。
		chrome.tabs.create({url: 'https://www.baidu.com'});
	2、当前标签打开新网页。
		getCurrentTabId(tabId => {
		chrome.tabs.update(tabId, {url: 'http://www.so.com'});
		});
	3、获取当前标签id。
		chrome.tabs.query({active: true, currentWindow: true}, function(tabs){})
	4、切到第一个标签。
		chrome.tabs.highlight({tabs: 0});
popup和content-scripts通信
	1、短连接发送。
		chrome.tabs.sendMessage
	2、长连接发送
		var port = chrome.tabs.connect(tabId, {name: 'test-connect'});
		port.postMessage
		port.onMessage.addListener
		在content-scripts.js也这样写。
dom交互演示
	1、修改页面背景色
		chrome.tabs.executeScript(tabId, {code: code});
	2、修改字体。
		通过sendMessage。
		chrome.tabs.sendMessage(tabId, message, function(response)
国际化
	需要一个_locale目录，下面的定义各种message字段，另外用chrome.i18n.getMessage("helloWorld")
其他
	1、显示徽章。
	chrome.browserAction.setBadgeText({text: 'New'});
	chrome.browserAction.setBadgeBackgroundColor({color: [255, 0, 0, 255]});
	2、隐藏徽章。
	chrome.browserAction.setBadgeText({text: ''});
	chrome.browserAction.setBadgeBackgroundColor({color: [0, 0, 0, 0]});
	3、显示桌面通知。
		chrome.notifications.create
	4、检测网页视频。
```

```
地址栏功能
输入go，就会触发demo的命令行。
在manifest里配置。
"omnibox": { "keyword" : "go" },
你输入美女，会自动帮你联想一些东西。
```

```
选项界面

```

```
devtools
可以在F12出来的界面里加一个标签，可以做一些操作。
```



```
popup.html 
popup.js
background.html
background.js
```



文件关系：

```
入口就是popup.html文件，这个里面的超链接的引用都是写在popup.js里的js函数。

```



参考资料

1、

