---
title: autojs实用脚本片段
date: 2020-12-16 16:22:30
tags:
- 自动化
---

1

# 日志保存位置

配置日志写入的文件。

```
console.setGlobalLogConfig({
    "file": "/sdcard/1.txt"
});
```

/sdcard这个路径是对的，可以写在文件系统里。

```
console.show()
```

这样还是可以很方便地观察总体的进度。比用toast要好。

# save on device

这样可以把脚本保存到设备上。



# 请求截屏权限

```
images.requestScreenCapture(false)
```

参数是表示是否是横屏。

这个函数只是申请截图权限，并不会真正执行截图，真正的截图函数是`captureScreen()`

该函数在截图脚本中只需执行一次，而无需每次调用`captureScreen()`都调用一次。

```
//请求截图
if(!requestScreenCapture()){
    toast("请求截图失败");
    exit();
}
//连续截图10张图片(间隔1秒)并保存到存储卡目录
for(var i = 0; i < 10; i++){
    captureScreen("/sdcard/screencapture" + i + ".png");
    sleep(1000);
}
```

# 抖音快手

模拟看视频，5秒，在此基础上，得到一个-4到4的一个随机数。
所以，最后就是1到9秒的。
看一半时间，进行关注和喜欢处理。
喜欢的概率是：1/15，1/29的概率关注。
喜欢是双击，所以是计算屏幕的中间，click然后sleep50ms，然后再click。
这样来模拟双击。
而关注，是text("关注").click

看了一个视频后，就是swipe来切换视频。
swipe是单数下滑，双数上划。
然后每6次也是下滑。

抖音的代码逻辑是一样的。

点击控件的中间位置。

```
let b = className("android.widget.TextView").text("" + columnName + "").findOnce().bounds();//推荐里面容易有广告
        click(b.centerX(), b.centerY());//进入到栏目
```

今日头条里返回，是这样来找返回按钮的：

```
let textViews = className("android.widget.ImageView").clickable(true).find();
        let b = textViews[0].bounds();
        click(b.centerX(), b.centerY());
```

因为在文章里，最左上角的返回图标，就是第一个图片。textViews[0]就是返回图标了。

点击返回。

而且这里的代码，比较明显可以看出来是autojs控件选中后生成的。



# 关于点击

点击事件我们是常用的**控件本身的click事件**是不用点击屏幕的，

比如id("btn_back").findOne().click();

然而对于控件没有点击事件的我们只能使用click()事件，

**这个事件是点击屏幕，所以当屏幕有遮挡这个点击事件将会失效，所以控制台console.show()要慎重使用。**

# 没有id等属性值的情况

很多控件没ID、text、desc无法直接查找，所以只能通过className遍历。

这样遍历风险极高，很多比较NB的App同一个UI上的className元素的数量不一致。

# 判断控件是否存在

查找控件存不存在使用exists ()。

一般情况下Autojs生成的代码是：

if (text("刷视频赚").exists()) {}，

不建议这样写，

有很多时候找不到或者是有多个文字一样的内容故：

let earnVideo= className("android.widget.TextView").text("刷视频赚").findOnce();这样写准确率更高。

# 健壮性

无论是find、findonce、findone后都需要判断一下是否是null。避免程序宕机。

# 打包图片资源

要使用网络资源，相对路径会有问题。



# loop

看有的代码里，有loop()这函数，但是我实际使用，提示这个接口已经过时，而且没有任何作用。

我自己写了一个死循环，这样是不行的。

因为js脚本都是单线程。死循环会导致事件无法响应。

如果要循环，可以起一个线程。

# findOne会阻塞

找不到会阻塞。

如果希望找不到就继续往下，应该使用findOnce函数。

findOne可以带一个时间参数。表示超时时间。

# 脚本最前面的"auto"

您也可以在脚本开头使用`"auto";`表示这个脚本需要无障碍服务，但是不推荐这种做法，因为这个标记必须在脚本的最开头(前面不能有注释或其他语句、空格等)，我们推荐使用`auto()`函数来确保无障碍服务已启用。



# 坐标得到负数

是浮动的，有可能得到负数。

一开始进来可以拿到合法的。保存起来。

layout层次分析。

total control直接控制手机进行直播。

给一个界面，让用户打开一下抖音，获取坐标数据保存。



参考资料

1、官网文档

https://hyb1996.github.io/AutoJs-Docs

2、AutoJs4.1.0开发心得

https://www.cnblogs.com/zy0412326/p/12581335.html