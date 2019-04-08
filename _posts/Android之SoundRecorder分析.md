---
title: Android之SoundRecorder分析
date: 2019-04-08 10:14:30
tags:
	- Android

---



SoundRecoder是一个录音软件。业务逻辑简单，界面也简单，适合分析学习。

涉及到的知识点：

```
1、PagerSlidingTabStrip用法。
	左右滑动切换tab。
2、ViewPager
3、Toolbar
4、资源xml文件分目录放。
5、OptionMenu的显示和事件响应。
6、FragmentPagerAdapter
	需要重写3个方法：getCount、getItem、getPageTitle。
7、Fragment写法。
8、FloatingActionButton
9、文件操作。
10、录音操作。
11、录音时保持屏幕常亮的方法。
12、数据库操作。
13、参数操作。

```



app的组成：

```
MainActivity
	包括2个Fragment。
	RecordFragment、FileFragment。
SettingsActivity
	在OptionMenu里打开。
	SettingsFragment，继承自PreferenceFragment。
```



参考资料

1、Android Fragment＋ViewPager 组合，一些你不可不知的注意事项

http://yifeng.studio/2016/12/23/android-fragment-and-viewpager-attentions/