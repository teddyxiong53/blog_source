---
title: Android（一）界面元素
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

#EditTextDemo加入

接下来我在btn2上，加入进入EditTextDemo的代码。

这样看来，我的Demo的组织不是非常合理，不过，每个Button进入的东西简单一致就好。一个Button相当于一个知识点。当前是14个Button，如果有可能超过14条，我就把最后一个Button表示其他的意思，进去是一个List，然后这个就可以无限扩展。就这么安排。

EditText常用的：

1、hint。就是你框里面的提示文字。

2、selectAllOnFocus。焦点切到上面时，把里面的内容都选中。

3、inputType。常用的有：numberPassword（只接受数字密码）、number（只接受数字输入）、date（只接受日期输入）、phone（只接受电话号码）。

这个界面就用TableLayout来布局。

我们就构造一个注册界面，这种界面最适合TableLayout和EditText了。

开始动手：

1、新建一个新的xml文件：edittext_demo.xml。

界面内容：

```
用户名：
密码：
生日：
电话：
邮箱：
注册按钮（按下后，给一个toast提示“注册成功”）
```

生成toast的方法：

```
Toast toast = Toast.makeText(EditTextDemoActivity.this, "注册成功", Toast.LENGTH_LONG);
                toast.show();
```

# 按钮演示

到目前，我们只用了最基本的带文字的普通按钮。

1、Switch。比较好看。类似显示中的开关。Toggle的话，是按下后，字符会变化。不好看。不用。

2、单选。RadioButton。重要属性有：checked（设置默认选中的那个为true）、text。男、女是两个Radio。属于同一个RadioGroup。

3、多选。还是有用的。

其实，这个是可以加入到上面的注册界面上的。但是出于简单化的考虑，还是单独放一个界面。

这个界面用哪种Layout呢？这个还是用TableLayout。



# ImageView

这个就ImageView这一个类。

演示程序，就做一个简单的图片浏览器。可以显示一张图片。

重要的属性：

1、src。指定图片的名字。

具体操作：

1、增加image_demo.xml文件。

2、增加mageDemoActivity.java文件。

其实很简单，但是我的不知道为什么图片一直显示不出来。我先放着。



# ListView

这个是一个很常用的组件。例如一般文件管理器里，显示所有的文件的时候，就是一个ListView。

主要的属性：

1、entries。就是List条目的内容写什么。可以指定到values目录下的arrays.xml文件里。

指定数组元素内容的方式是最简单的，但是不够灵活。不能对ListView的外观进行改变。

如果想要改变的话，怎么做呢？

就要通过Adapter来做。对ListView调用setAdapter来做。

另外，还有其他Android帮我们做好的一些东西，例如直接继承ListActivity。做法有好几种。

我们现在只做基于数组元素的。

操作步骤：

1、新建list_demo.xml文件。

2、在values目录下新建arrays.xml文件。

内容如下：

```
<?xml version="1.0" encoding="utf-8" ?>
<resources>
    <string-array name="habits">
        <item>读书</item>
        <item>打球</item>
        <item>旅行</item>
    </string-array>
</resources>
```

4、新建ListDemoActivity.java。

# 进度条

进度条，我就看普通的水平进度条和环形进度条。

ProgressBarDemo设计：

1、设计一个Button，点击开始，然后让两个进度条在2秒内走完。

2、暂时不在弹窗里做，就在普通的Activity里做。

搞定。

# 弹窗

弹窗有基本的确定取消弹窗，还有进度条弹窗。

我就涉及一个Button，一点击，就弹出一个弹窗。

搞定。



暂时先到这。

