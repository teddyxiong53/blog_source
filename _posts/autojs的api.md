---
title: autojs的api
date: 2020-12-15 15:42:30
tags:
- 脚本
---

1

# 全局函数

```
currentPackage()
	返回最近一个应用的包名。可以认为是当前正在运行的应用的包名。
currentActivity()
waitForPackage(package[,period=200])
	等待目标应用被打开。period是轮询间隔，默认200ms。
	例如，等待微信被打开。
	waitForPackage("com.tecent.mm")
	一直阻塞。
waitForActivity(activity[, period = 200])
	类似上面。
sleep(n)
	睡眠毫秒。
log(msg)
	在控制台打印。vscode可以看到，手机日志里也可以看到。
toast(msg)
	手机上显示toast。
toastLog(msg)
	上面2个函数的结合体。
setClip(text)
	设置剪贴板内容。
getClip()
	获取剪贴板内容。
exit()
	立刻停止脚本运行。
random(min, max)
	产生随机数。
random()
	返回0到1之间的浮点随机数。
requiresApi(api)
	需要安卓sdk api版本达到才能运行。
	Android 7.0： 24
requiresAutojsVersion(version)
	要求autojs的版本。
	version参数可以是整数表示版本号，例如requiresAutojsVersion(250)；也可以是字符串格式表示的版本，例如"3.0.0 Beta", “3.1.0 Alpha4”, "3.2.0"等。
	
runtime.requestPermissions(permissions)
	尽管安卓有很多权限，但必须写入Manifest才能动态申请，为了防止权限的滥用，目前Auto.js只能额外申请两个权限：
    access_fine_location GPS权限
    record_audio 录音权限
    
runtime.loadJar(path)
	加载目标jar文件，加载成功后将可以使用该Jar文件的类。
	
runtime.loadDex(path)
	加载目标dex文件，加载成功后将可以使用该dex文件的类。
context
	全局变量。一个android.content.Context对象。
	注意该对象为ApplicationContext，因此不能用于界面、对话框等的创建。
```

# app相关函数



```
launch(packageName)
	打开应用。
	例如：打开微信。
	launch("com.tencent.mm")
launchApp(appName)
	通过名字打开微信。
	如果不存在，返回false。
	launchApp("手机淘宝")
	如果名字对应多个app，只打开第一个。
launchPackage(packageName)
	跟launch(packageName)一样。
getPackageName(appName)
	根据名字拿到包名。
	例如：getPackageName("手机淘宝")
	
getAppName(packageName)
	根据包名拿到应用名字。
	
========上面的，可以加app前缀，也可以不加。
app.versionCode
	如果在Auto.js中运行则为Auto.js的版本号；在打包的软件中则为打包软件的版本号。
	
app.openAppSetting(packageName)
	打开应用的设置页面。可能不存在，则返回false。
app.viewFile(path)
	打开文件，如果这种文件找不到合适的应用来打开，则抛出ActivityNotException
	
app.editFile(path)
	编辑文件。
app.uninstall(packageName)
	卸载应用。
app.openUrl(url)
	用默认浏览器打开url。
	
app.startActivity(name)
	启动Auto.js的特定界面。该函数在Auto.js内运行则会打开Auto.js内的界面，在打包应用中运行则会打开打包应用的相应界面。
	例如：
	app.startActivity("console");
```





例子：

```
//启动APP
if (currentPackage() != "com.chaoxing.mobile") {
    toast("即将打开超星！");
    //直接打开学习通
    app.launchApp("学习通");
} else {
    toast("已经在学习通中，即将开始进行下一步操作！");
};
```



## intent相关

```
app.intent(options)
	options是一个对象。
	可以包括的有：
	action: 
	type: 意图对应的mime type
	data：意图的数据。
	...
	
```

例如，打开查看图片，是这样：

```
var i = app.intent({
	action: "VIEW",
	type: "image/png",
	data: "file:///sdcard/1.png"
})
context.startActivity(i)
```

需要注意的是，除非应用专门暴露Activity出来，

否则在没有root权限的情况下使用intent是无法跳转到特定Activity、应用的特定界面的。

例如我们能通过Intent跳转到QQ的分享界面，

是因为QQ对外暴露了分享的Activity；

而在没有root权限的情况下，我们无法通过intent跳转到QQ的设置界面，

因为QQ并没有暴露这个Activity。

```
app.startActivity(options)
	
app.sendBroadcast(options)

app.startService(options)

app.sendBroadcast(name)
app.intentToShell(options)

app.parseUri(uri)

app.getUriForFile(path)

```



# 基于坐标的模拟

使用坐标进行点击、滑动的函数。这些函数有的需要安卓7.0以上，有的需要root权限。

要获取要点击的位置的坐标，可以在开发者选项中开启"指针位置"。

基于坐标的脚本通常会有分辨率的问题，这时可以通过setScreenMetrics()函数来进行自动坐标放缩。

这个函数会影响本章节的所有点击、长按、滑动等函数。

通过设定脚本设计时的分辨率，使得脚本在其他分辨率下自动放缩坐标。

控件和坐标也可以相互结合。

一些控件是无法点击的(clickable为false), 无法通过.click()函数来点击，这时如果安卓版本在7.0以上或者有root权限，就可以通过以下方式来点击：



# 用户界面: UI

ui模块提供了编写用户界面的支持。

带有ui的脚本的的最前面必须使用"ui";指定ui模式，否则脚本将不会以ui模式运行。正确示范:

```
"ui";

//脚本的其他代码
```



# 代码片段



https://easydoc.xyz/doc/25791054/uw2FUUiw/AiGMZYiu

这个是系列教程

https://www.jianshu.com/u/21d627ffdcf2



## 运行原理

rhino犀牛引擎赋予了java执行js的能力，

而auto.js在rhino的基础上实现了访问安卓底层功能的大部分接口，

而且集成了opencv这个强大的图像处理库，

再加上手机系统自带的webview可以搭载完整的web应用，

webview又可以**通过JSBridge与底层java通信**。

至此，前端技术体系实现安卓脚本或其他应用的方案变得非常容易。





参考资料

1、

https://easydoc.xyz/doc/25791054/uw2FUUiw/Af2UuRxd