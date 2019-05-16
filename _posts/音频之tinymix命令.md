---
title: 音频之tinymix命令
date: 2019-05-16 14:42:11
tags:
	- 音频

---



看rk3308里的例子。有用到tinymix这个工具。研究一下。

```
tinymix controls
	查看有哪些可以控制的内容。当前在rk3308上，看到有80项。
```

前面几项是这样：

```
/dev # tinymix controls
Number of controls: 80
ctl     type    num     name
0       INT     1       ADC MIC Group 0 Left Volume
1       INT     1       ADC MIC Group 0 Right Volume
```

```
tinymix get 0 //0表示id。表示获取id为0的配置项的内容。
```

```
/dev # tinymix get 0
0 (range 0->3)
```

这个是volume值，范围是0到3 。

对应的还有tinymix set id value。这样来修改设置。

总之，作用就是读取设置，修改设置。



tinymix是精简的alsa utils之一。

还有：

```
tinycap
	录音
tinyplay
	播放
```



参考资料

1、

https://blog.csdn.net/johnny_nass_hu/article/details/53537942