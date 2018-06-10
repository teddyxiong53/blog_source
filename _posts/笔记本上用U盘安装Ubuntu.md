---
title: 笔记本上用U盘安装Ubuntu
date: 2018-06-06 21:31:57
tags:
	- Ubuntu

---



我的笔记本上本来是安装了kali和win7双系统的。现在打算把kali换成Ubuntu。

选择U盘安装的方式。

1、用ultraiso工具，把Ubuntu 16.04 32位的iso文件，写入到U盘里。

2、笔记本开机。选择从U盘启动。然后进入到Ubuntu的安装引导界面了。一路下一步就好了。

注意连接到网络。

选择分区的时候，要把之前的kali的删掉，重新格式化。

我的笔记本总共250G。分了100G给Ubuntu，其余的都给windows。

安装过程下载东西太慢，skip掉。



# 软件安装

1、更新阿里源。

2、安装openssh。后面的操作就远程去做。把笔记本当成服务器来访问。



# 各类环境

## dueros环境

1、

```
sudo apt-get install python-dateutil \
gstreamer1.0 \
gstreamer1.0-plugins-good \
gstreamer1.0-plugins-ugly \
python-gi \
python-gst-1.0 \
gir1.2-gstreamer-1.0 
```

```
sudo apt-get install python-dev libatlas-base-dev
sudo pip install tornado  
sudo pip install hyper 
sudo apt-get install python-dateutil
sudo apt-get install python-pyaudio
```



```
teddy@teddy-ThinkPad-SL410:~$ aplay -l
**** PLAYBACK 硬體裝置清單 ****
card 0: Intel [HDA Intel], device 0: ALC269 Analog [ALC269 Analog]
  子设备: 1/1
  子设备 #0: subdevice #0
card 1: HDMI [HDA ATI HDMI], device 3: HDMI 0 [HDMI 0]
  子设备: 1/1
  子设备 #0: subdevice #0
```

```
teddy@teddy-ThinkPad-SL410:~$ arecord -l
**** CAPTURE 硬體裝置清單 ****
card 0: Intel [HDA Intel], device 0: ALC269 Analog [ALC269 Analog]
  子设备: 1/1
  子设备 #0: subdevice #0
```



# 参考资料

1、在win7系统中用U盘安装Ubuntu16.04

https://blog.csdn.net/qq_20444875/article/details/78887768