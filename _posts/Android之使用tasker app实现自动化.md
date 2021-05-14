---
title: Android之使用tasker app实现自动化
date: 2021-05-02 18:13:11
tags:
	- tasker

---

--

自动化任务，可以分为2个部分：

1、触发条件。

2、执行任务。

例如，检测到插入耳机，执行播放音乐操作。

这个就是一个自动化的场景。

触发条件是检测到插入耳机。

执行任务是播放音乐。

我们就以这个简单的场景来分析，看看在tasker里如何进行实现。

实验环境：

坚果pro2，刷的魔趣系统，root了。

tasker，需要付费。找破解版。我的qq收藏里有，是从tasker QQ群里找的。

不破解根本无法使用。

先创建一个任务，再创建一个场景，场景创建完的时候，会让你选择关联的任务的。

操作一遍就知道了。



知道了基本的操作逻辑。

我的主要目的就是tasker配合autojs来进行一些自动化脚本运行。

所以现在网上找一下相关的脚本。



#  Tasker定时任务（建议）步骤：

1. 新建任务(目的是启动蚂蚁森林脚本)，命名为【蚂蚁森林】。假设脚本路径为file:///storage/emulated/0/脚本/蚂蚁森林.js
2. 依次点击 添加(+)>系统>发送意图，来到操作修改界面
3. 其中，需要填写的选项如下：
   类别(Category)：`Default`
   Mime类型(MimeType)：`text/javascript`
   数据(Data)：`file:///storage/emulated/0/脚本/蚂蚁森林.js`
   包名(PackageName)：`org.autojs.autojs`
   类名(ClassName)：`org.autojs.autojs.external.open.RunIntentActivity`
   目标(Target)：`Activity`
4. 返回到任务界面，点击右上角应用(√)按钮生效。测试：长按【蚂蚁森林】任务，点击运行按钮，如果正常，将会开始收能量，测试成功
5. 在配置文件栏，新增定时任务。依次点击 添加(+)>时间，来到时间修改界面
6. 选择时间段，结束与开始时间相同
7. 返回到配置文件界面，选择【蚂蚁森林】任务，点击右上角应用(√)按钮生效





tasker 还是一个遇强则强的 APP ，

对于不想折腾的人，按照基本逻辑写任务或者在论坛和搜索引擎找任务就能给生活带来很多方便，

不需要学习如何去编程，如何去写复杂的算法和兼容。

对于像我一样喜欢折腾和探索的人，

 tasker 就和设计狮的 Illustrator ，程序猿的 IDE ，数学家的 Matlab 一样强大。



我在每次制作之前都会用「在 什么地方/什么时候/发生什么 时 干什么」的句式概括将要制作的 Tasker 任务，

比如这个实例就是「在收到包含验证码短信的时候复制并且自动填写验证码」。

根据这一句话，我们可以轻松按照几个步骤做好这个实例。



# 参考资料

1、安卓自动化神器Tasker基础入门教程

https://www.jianshu.com/p/3b91e56ca1aa

2、

https://github.com/joeyZhouYicheng/auto-punch

3、

https://gitee.com/handongke/autojs

4、

https://www.codetd.com/article/4716252

5、Tasker：Android 上的自动化标杆

https://sspai.com/post/45759

6、Tasker-安卓党的京东自动签到神器来了

https://post.smzdm.com/p/av7mllr4/