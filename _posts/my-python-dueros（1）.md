---
title: my_python_dueros（1）
date: 2018-10-27 15:21:25
tags:
	- dueros

---



现在自己把dueros的代码写一遍。Python版本的。

这个做一个记录。

代码提交到这个位置。

https://github.com/teddyxiong53/dueros/tree/master/my_python_dueros

先建立基本目录和文件。

```
Administrator@hostpc MINGW64 /d/work/git/dueros/my_python_dueros (master)
$ ls
app/  auth.py  enter_trigger_start.sh  sdk/  修改记录.md
```

先把授权的完成。这部分是独立的，而且内容不多。

为了方便理解，需要把tornado学习一下基本用法。

```
WORK_PATH="${PWD}"
export PYTHONPATH=${WORK_PATH}:${PYTHONPATH}
```

这个是必要的，不然是这样。

```
teddy@teddy-ThinkPad-SL410:~/work/dueros/python/my_python_dueros$ ./auth.sh 
Traceback (most recent call last):
  File "./app/auth.py", line 1, in <module>
    import sdk.auth as auth
ImportError: No module named sdk.auth
```

现在授权部分写完了。

有一点要注意的。

client id和client secret不能改成自己的。改了不行。访问网页会提示你redirect uri不对。

2018年10月27日17:14:08

先上传一个版本。

开始写主体部分。



先完成mic部分的。

在app目录下创建framework目录。

下面新建mic.py文件。新建player.py。新建`__init__.py`。

这个是一个包。

在App目录下新建一个app_config.py文件。

mic.py里面就一个Audio类。

是对pyaudio的包装。

内容很简单。

再写player.py文件。

也简单，是对gst的简单包装。

在app目录下新建utils目录。

里面写prompt_tone.py。这个用到了player.py。就是用来播放唤醒后咚的那一声。

enter_trigger_main.py，相当于一个聚合。

聚合了mic（输入）、dueros（处理）、player（输出）。

现在开始写dueros_core.py。在sdk目录下。先把基本框架弄出来。

DuerOS这个类，也是一个聚合类。

现在需要引入新的文件，alerts.py。

主要对外的接口就2个，set_alert和del_alert。



现在引入audio_player.py。这个在sdk目录下，跟app目录下的player.py是什么关系呢？

sdk下面的都是有namespace的，用来跟云端交互的。

sdk下新建speaker.py。这个是用来调节音量的。

目前方法都是空的。

新建speech_recognizer.py。

2018年10月28日13:39:24

再看system.py。

这个主要就是报告非活动时间的。

到这里，dueros_core.py里聚合的主要的其他类都写了。

现在我们回到dueros_core.py。









