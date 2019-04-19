---
title: css之@media
date: 2019-04-19 14:52:25
tags:
	- css

---

1

语法：

```
@media mediatype and | not | only (media feature)
{
    css-code;
}
```

也可以针对不同的媒体使用不同的css文件。

```
<link rel="stylesheet" media="mediatype and | not| only(media feature)" href="xx.css">
```



首先要看meta。

```
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
```



屏幕尺寸小于960px的写法。

```
@media screen and (max-device-width:960px) {
    body {
        background: red;
    }
}
```



参考资料

1、CSS3 @media 用法总结

https://www.jianshu.com/p/b8f375b52a61