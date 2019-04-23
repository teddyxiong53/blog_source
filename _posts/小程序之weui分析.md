---
title: 小程序之weui分析
date: 2019-04-23 09:39:25
tags:
	- 小程序

---



网站在这里：https://weui.io/

依次有：

```
1、表单
	Button
	Input
	List
	Slider
	Uploader
2、基础组件
	Article
	Badge
	Flex
	Footer
	Gallery
	Grid
	Icons
	Loadmore
	Panel
	Preview
	Progress
3、操作反馈
	Actionsheet
	Dialog
	Msg
	Picker
	Toast
4、导航相关
	Navbar
	Tabbar
5、搜索相关
	SearchBar
6、层级规范
	4层，从下到上依次是：
	Content
	Navigation
	Mask
	Popout
```



使用：

1、把weui.wxss文件拷贝到工程的根目录。

2、在app.wxss里加入：

```
@import ‘weui.wxss’;
```

然后就可以使用了。



参考资料

1、WeUI for 小程序--使用教程

https://blog.csdn.net/chq1988/article/details/73549027