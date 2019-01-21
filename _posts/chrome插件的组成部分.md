---
title: chrome插件的组成部分
date: 2019-01-21 10:01:12
tags:
	- chrome

---



页面的组成部分

```
content-scripts
	向页面注入脚本。可以注入js和css。
background
	后台。常驻页面。
	插件里生命周期最长的，随着浏览器的打开而打开，关闭而关闭。
	全局的代码放这里。
	权限非常高：可以调用几乎所有的chrome api。可以跨域访问。
	所有可以通过chrome-extension://id/xx.html访问的页面都可以跨域。
	background，可以指定为html，也可以指定为js。如果是指定js，则会自动生成一个html文件。
event-pages
	为了应对background生命周期太长，所有代码写在里面会影响浏览器的性能。
	event-pages生命周期短一些。
	就是多了一个persistent的参数。
	在需要时加载，在空闲时关闭。
	不过一般来说，background也不会很耗性能。了解这个就好了。
popup
	这个就是点击插件图标弹出的小界面。
injected-script
	通过dom的方式向页面注入的一种js。
	为什么要把这种单独拉出来说呢？它跟content-scripts有什么区别呢？
	因为content-scripts有一个缺陷，就是不能访问页面里的js，虽然它可以访问dom。但是dom不能调用         content-scripts。
homepage_url
	放开发者的信息。
```



插件的8种展示形式

```
1、browser_action
	浏览器右上角增加一个图标。
2、page_action
	在地址栏的右侧。
	新版本的也挪到了跟browser_action一样的位置了。
3、右键菜单。
4、override
	覆盖掉特定页面。
	可以覆盖的页面有：历史记录、新标签页、书签。
5、devtools
6、options页面。
7、omnibox
8、桌面通知。
```



5种类型的js比较。

```
injected script
content script
popup js
background js
devtools js
```



参考资料

1、

https://www.cnblogs.com/liuxianan/p/chrome-plugin-develop.html