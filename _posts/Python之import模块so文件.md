---
title: Python之import模块so文件
date: 2018-10-27 13:05:04
tags:
	- Python

---



在看dueros的Python版本的时候，使用唤醒词版本的。

会出现这种错误。

```
teddy@teddy-ThinkPad-SL410:~/work/dueros/python/DuerOS-Python-Client-master$ ./wakeup_trigger_start.sh 
Traceback (most recent call last):
  File "./app/wakeup_trigger_main.py", line 21, in <module>
    from app.snowboy import snowboydecoder
  File "/home/teddy/work/dueros/python/DuerOS-Python-Client-master/app/snowboy/snowboydecoder.py", line 5, in <module>
    import snowboydetect
  File "/home/teddy/work/dueros/python/DuerOS-Python-Client-master/app/snowboy/snowboydetect.py", line 17, in <module>
    _snowboydetect = swig_import_helper()
  File "/home/teddy/work/dueros/python/DuerOS-Python-Client-master/app/snowboy/snowboydetect.py", line 16, in swig_import_helper
    return importlib.import_module('_snowboydetect')
  File "/usr/lib/python2.7/importlib/__init__.py", line 37, in import_module
    __import__(name)
ImportError: No module named _snowboydetect
```

看代码目录是这样的：

```
teddy@teddy-ThinkPad-SL410:~/work/dueros/python/DuerOS-Python-Client-master/app/snowboy$ ls -lh
总用量 3.3M
-rw-rw-r-- 1 teddy teddy  1.1K 3月   2  2018 demo2.py
-rw-rw-r-- 1 teddy teddy  1.1K 3月   2  2018 demo3.py
-rw-rw-r-- 1 teddy teddy   781 3月   2  2018 demo_arecord.py
-rw-rw-r-- 1 teddy teddy   757 3月   2  2018 demo.py
-rw-rw-r-- 1 teddy teddy  1.2K 3月   2  2018 demo_threaded.py
-rw-rw-r-- 1 teddy teddy     0 3月   2  2018 __init__.py
-rw-rw-r-- 1 teddy teddy   169 6月   6 23:21 __init__.pyc
-rw-rw-r-- 1 teddy teddy    15 3月   2  2018 requirements.txt
drwxrwxr-x 3 teddy teddy  4.0K 3月   2  2018 resources
-rw-rw-r-- 1 teddy teddy  6.5K 3月   2  2018 snowboydecoder_arecord.py
-rw-rw-r-- 1 teddy teddy  6.9K 3月   2  2018 snowboydecoder.py
-rw-rw-r-- 1 teddy teddy  7.4K 6月   6 23:21 snowboydecoder.pyc
-rw-rw-r-- 1 teddy teddy  4.8K 3月   2  2018 snowboydetect.py
-rw-rw-r-- 1 teddy teddy  7.5K 6月   6 23:21 snowboydetect.pyc
-rwxr-xr-x 1 teddy teddy 1009K 3月   2  2018 _snowboydetect.so
-rw-rw-r-- 1 teddy teddy  3.5K 3月   2  2018 snowboythreaded.py
-rw-rw-r-- 1 teddy teddy  2.3M 3月   2  2018 xiaoduxiaodu_all_10022017.umdl
```

那个_snowboydetect实际上是一个so文件。

看对应的Python代码是这么写的。

```
if _swig_python_version_info >= (2, 7, 0):
    def swig_import_helper():
        import importlib
        pkg = __name__.rpartition('.')[0]
        mname = '.'.join((pkg, '_snowboydetect')).lstrip('.')
        try:
            return importlib.import_module(mname)
        except ImportError:
            return importlib.import_module('_snowboydetect')
    _snowboydetect = swig_import_helper()
    del swig_import_helper
```

这里就涉及到一个东西：swig。

swig具体是什么呢？

swig主要是用来在python里使用C或者c++的库的。



# 参考资料

1、使用SWIG实现Python调用C/C++代码

http://cering.github.io/2015/12/08/%E4%BD%BF%E7%94%A8SWIG%E5%AE%9E%E7%8E%B0Python%E8%B0%83%E7%94%A8C-C-%E4%BB%A3%E7%A0%81/