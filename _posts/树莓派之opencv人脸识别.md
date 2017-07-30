---
title: 树莓派之opencv人脸识别
date: 2017-07-28 19:42:15
tags:

	- 树莓派

	- opencv

---

我尝试了安装opencv，但是从各种情况来看，似乎是需要一些GUI库才行，我的Raspbian是lite版本，没有图形界面的。所以暂时不去管opencv的。

看看simplecv是否可用。

`sudo pip install https://github.com/sightmachine/SimpleCV/zipball/develop`。安装。

但是在树莓派上下载非常慢，这个下载下来大概是50M。我在电脑上下载下来，然后把压缩包放到树莓派上。解压。

```
sudo python ./setup.py build
sudo python ./setup.py install
```

运行看看，报错。提示没有scipy的库，用pip安装。

```
sudo pip install scipy
```

安装这个比较慢，最后还失败了。仔细看失败的原因。要做下面这些事情。

```
sudo apt-get install liblapack-dev libblas-dev  
sudo pip install nose  
sudo pip install atlas  
sudo pip install --upgrade scipy  
还是出错
sudo apt-get install gfortran  
sudo pip install --upgrade scipy  
现在这一步变得特别慢。先等着。成功了。
```

现在运行simplecv打印这个：`Cannot load OpenCV library which is required by SimpleCV`。那就是说还是要先安装opencv。暂时不在树莓派上折腾这个了。











