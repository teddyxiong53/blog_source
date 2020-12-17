---
title: autojs一个基本例子
date: 2020-12-15 17:25:30
tags:
- autojs
---

1

定位组件是autojs的最常见的操作，这很类似前端的定位dom元素。

在任何点击之前都需要找到对应的组件，

这不同于点击某像素位置，点击组件更能适配不同分辨率的手机。

在auto.js中通过各种条件选取到的控件称为[UiSelector](https://link.zhihu.com/?target=https%3A//hyb1996.github.io/AutoJs-Docs/%23/widgetsBasedAutomation%3Fid%3Duiselector)。

那么筛选条件是如何确定呢？

打开Auto.js应用的悬浮窗，在喵铺主页，点击Auto.js**悬浮窗**后选择出现的**蓝色按钮**，

点击**布局范围分析**后选择领喵币按钮**查看控件信息**，你就能看到如图2所示的信息。

现在这些按钮，都不是文本的了。

```
auto.waitFor()
var appName = "手机淘宝";
launchApp(appName);
sleep(3000);
//寻找领喵币按钮并点击
var lingmiaobi = text("领喵币").findOnce();
if (lingmiaobi) {
    lingmiaobi.click();
    sleep(1000);
}
else {
    toast("未检查到领喵币按钮");
    //中止脚本
    exit();
}
```

上面这个就是打开app，找到里面的按钮，然后点击。

然后这里面就一些按钮叫“去浏览”，也是自动点击。

```
//开始执行任务
execTask();
function execTask() {
    while(true) {
        var target =  text("去进店").findOnce() || text("去浏览").findOnce();
        if (target == null) {
            toast("任务完成");
            break;
        }
        target.click();
        sleep(3000);
        //浏览网页20s
        viewWeb(20);
        back();
        sleep(1000);
    }
}
```

相信现在你看这段代码能看懂了，viewWeb是一会儿我们要写的函数，

目的是模拟浏览网页20s的操作，

虽说淘宝要求15s就行了，但是可能部分手机加载耗时比较多，所以多写了5s。

当判断任务栏有"去进店"、"去浏览"的组件时，点击跳转至浏览广告，浏览完毕后，返回至任务栏页面，循环执行该操作直到找不到"去进店"、"去浏览"的组件结束（任务完成后按钮文字会变成"已完成"）。

```
function viewWeb(time) {
    gesture(1000, [300, 600], [300, 300]);
    var cnt = 1;
    while(true) {
        var finish = desc("任务完成").exists() || textStartsWith("已获得").exists();
        if (finish || cnt > time) {
            break;
        }
        sleep(1000);
        cnt += 1;
    }
    //模拟返回键，返回到任务栏页面
    back();
}
```

我可以参考上面的，写领取淘金币的。



autojs的悬浮按钮，布局分析，布局范围分析，选中目标组件，可以生成代码。

这就非常有用了。这个功能真的很强大了。

但是对图片生成代码，会失败，看网上说是只能生成简单代码。



搜索按钮，一般可以text、desc、id。

但是手机淘宝里，这些都是空。

那么就只能用坐标的方式了。

500,500 这个坐标，是在这个图片内部。

可以点击过来。

```
setScreenMetrics(1080, 2400);
click(500, 500)
```

然后就是分析淘金币的界面。

进来后，有几个按钮，

逛店铺：这个的逻辑是跟领喵币类似，都是逛10s，然后可以领10个淘金币。

先就实现这一个。

这个也只能靠坐标了。

（100,140）这个点可以。

进去后的界面逻辑跟上面一样，之前是“逛10秒+10 ”，逛完后，就变成“已完成”。

“逛10秒+10 ”这个文本在desc里可以看到。

调用不能进行click操作。

打印这对象。可卡因看到`clickable: false; `。

```
boundsInParent: Rect(0, 0 - 170, 77); boundsInScreen: Rect(781, 412 - 951, 489); packageName: com.taobao.taobao; className: android.view.View; text: null; contentDescription: 逛10秒+10; viewId: null; checkable: false; checked: false; focusable: false; focused: false; selected: false; clickable: false; longClickable: false; enabled: true; password: false; scrollable: false; [ACTION_SELECT, ACTION_CLEAR_SELECTION, ACTION_ACCESSIBILITY_FOCUS, ACTION_NEXT_AT_MOVEMENT_GRANULARITY, ACTION_PREVIOUS_AT_MOVEMENT_GRANULARITY, ACTION_SET_SELECTION]
```

这个应该怎么处理呢？

那么只能转变一下，先找到“逛10秒”的按钮，然后得到它的坐标。点击坐标。

```
TypeError: Cannot find function boundsInScreen in object
```

还真没有。boundsInParent可以找到。

没有boundsInScreen还比较难处理。

# 网上找的一段代码

```
auto.waitFor()
var packageName = currentPackage()
if(packageName != 'com.taobao.taobao') {
    launchApp("手机淘宝");
    toast("打开手机淘宝中");
    waitForPackage('com.taobao.taobao')
}

function run() {
    className('android.widget.LinearLayout').desc('捉猫猫').findOne().click()
    className('android.view.View').clickable(true).depth(18).indexInParent(5).findOne().click()
    sleep(2000)
    if (text("签到").exists()) {
        text("签到").findOne().click();
        sleep(1600);
        toast("签到成功")
    }

    toast("开始进行 去进店 任务！")
    goShop()

    toast("开始进行 去浏览 任务！")
    goBrowse()

}

function goShop() {
    let x = device.width / 2, y = device.height / 5;
    while (text("去进店").exists()) {

        text("去进店").findOne().click()
        sleep(2000)
        var task = className('android.view.View').desc('任务完成').exists()
        while(!task) {
            swipe(x, 4*y, x, y,1000);
            sleep(3000)
            task = className('android.view.View').desc('任务完成').exists()
            if (task) toast('任务完成');
        }
        back()
        sleep(2000)

    }
}

function goBrowse() {
    while (text("去浏览").exists()) {
        //判断是否有去浏览
        text("去浏览").findOne().click();
        sleep(20000)
        back()
        sleep(2000)
    }
}

run()
```



参考资料

1、Auto.js快速入门实战教程

https://zhuanlan.zhihu.com/p/90065914

2、

https://www.autojs.org/topic/232/%E5%A4%A7%E4%BD%AC%E4%BB%AC%E8%A7%A3%E9%87%8A%E4%B8%80%E4%B8%8B%E7%82%B9%E5%87%BB%E7%94%9F%E6%88%90%E4%BB%A3%E7%A0%81-%E4%BD%86%E6%98%AF%E5%A4%B1%E8%B4%A5%E6%98%AF%E4%BB%80%E4%B9%88%E5%8E%9F%E5%9B%A0-%E8%B0%A2%E8%B0%A2