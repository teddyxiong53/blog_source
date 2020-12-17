---
title: autojs实用脚本片段
date: 2020-12-16 16:22:30
tags:
- 自动化
---

1

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



参考资料

1、官网文档

https://hyb1996.github.io/AutoJs-Docs