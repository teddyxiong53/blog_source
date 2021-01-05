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





命名规律

weui1.0开始命名有一点的规律。

之前都是只有下划线。

现在是这样的形式。

```
weui-aaa__bbb-bbb_ccc-ccc
```

单横杠为连字符。

双下划线是连接block和element。

单下划线连接modify。



weui测试环境。

https://github.com/Tencent/weui

把这个仓库clone到本地。

```
npm install
npm start
```

这样是在电脑上运行测试例子。你可以修改查看效果。

修改导致网页自动重新加载。马上就可以看到效果。

是靠gulp来做到的。

weui的代码是用less写的。然后编译成css发布。

![image-20210104160315170](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210104160315170.png)

读less代码才能理顺思路。

还兼容了黑暗模式和白天模式。



参考资料

1、WeUI for 小程序--使用教程

https://blog.csdn.net/chq1988/article/details/73549027

2、WeUI库说明

https://www.vxzsk.com/50.html

3、

https://www.bookstack.cn/read/WeUIwiki/2.md

https://github.com/Tencent/weui/wiki

