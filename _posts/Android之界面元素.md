---
title: Android之界面元素
date: 2017-12-30 13:51:12
tags:
	- Android

---



Android界面元素关系。不求全面，但求简单易用。

```
1、文本类。
	1）TextView。
	2）EditView。
2、图片类。
	1）ImageView。
3、框架类。
	1）ListView。
	2）GridView。
4、按钮类。
	1）Button。还有单选、多选的，不细看。
5、弹窗类。
	1）ProgressBar。进度条。
	2）AlertDialog。弹窗。
6）导航类。
	1）ActionBar。
```
创建一个Android工程xhl_view_simple。
把上面的元素都包含进来。
主界面用一个GridView。
Android界面的class之间的关系。
View：最基础的类。代表一块白色矩形区域。

View的主要xml属性说明：
```
1、颜色类。
	1）alpha。透明度。
	2）background。背景色。
2、事件类。
	1）clickable。是否可以单击。
	2）focusable。是否可以得到焦点。
	3）longClickable。是否可以长按。
	4）onClick。单击事件响应。
	
3、id。
	1）id。控件的id。
	
4、尺寸类。
	1）minHeight。
	2）minWidth。
	
5、其他。
	1）keepScreenOn。控件显示的时候，保持屏幕常亮。
```
对于容器类的，还要多几个需要注意的：
```
1、尺寸。
	1）layout_height。
	2）layout_width。都给match_parent就好。或者wrap_content。
```
# 选择一个主界面布局方式

选择GridLayout的布局方式。GridLayout是从Android4.0开始加入的。

GridLayout的布局效果，可以通过LinearLayout嵌套来达到类似效果。也可以用RelativeLayout来达到类似效果。但是不如GridLayout方便和效果好。

有些嵌套四五层的其他布局，可以一层的GridLayout就解决。

布局为16宫格的。Grid为一个正方形。在最底下，有一个跨两列的，有一个跨两行的。先这么设置。

把界面写出来先。

# 写主界面的xml文件

工具：用AS。网络带翻墙。配置AS的代理。

1、新建一个空的Android工程。名字叫xhl_simple_view。

2、在res下新建layout目录，新建main.xml文件。

3、添加14个按钮，依次命名为btn1到btn14，其中12和13号大小不同，占据两个格子，一竖一横。

4、新建java文件MainActivity.java。修改AndroidManifest.xml文件。运行看效果。ok。

下一步，我们要在btn1改名字为“文件控件类”，添加事件处理，点击就进入到相关的界面进行处理。btn的变量名就不改了。

# 文本控件演示界面设计

就TextView和EditText这两种基本的。两种的属性基本一样，就是EditText多了编辑相关属性。

TextView的xml属性有60来个。

在一般的简单App开发中，需要关注文本的哪些特点呢？

1、设置字体及大小。

2、对邮件、网址添加链接功能。

3、设置文字背景图片和颜色。

# 文本控件演示界面开发

1、在Layout里增加一个text_demo.xml文件。增加对应的java文件TextDemoActivity。

2、这个界面用什么布局？我应该逐步把Android的其他类型的布局都添加进来。这个我们就用最简单的LinearLayout吧。

我们会显示几个不同的文本，就按居中的方式，依次往下排。挨着顶部往下排。

3、我们先把text_demo界面简单写一个。

4、现在要在MainActivity.java里，加入btn1的事件响应代码。要在事件处理里，进行Activity的切换了。   

加上这个代码就可以了：

```
Intent intent = new Intent(MainActivity.this, TextDemoActivity.class);
                startActivity(intent);
```

接下来



