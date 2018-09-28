---
title: avs之Linux搭建
date: 2018-09-28 14:22:35
tags:
	- 音箱

---



创建目录如下：

```
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder$ tree
.
├── application-necessities
├── sdk-build
├── sdk-source
└── third-party
```

安装基础工具：

```
 sudo apt-get install -y git gcc cmake openssl clang-format
```

安装音频相关库。

```
sudo apt-get install -y openssl libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev gstreamer1.0-plugins-good libgstreamer-plugins-good1.0-dev libgstreamer-plugins-bad1.0-dev gstreamer1.0-libav pulseaudio doxygen libsqlite3-dev repo libasound2-dev
```

这里开始报错。

```
E: 下载 http://mirrors.aliyun.com/ubuntu/pool/main/g/gcc-5/libobjc4_5.4.0-6ubuntu1~16.04.9_amd64.deb  404  Not Found [IP: 121.9.229.124 80] 失败

E: 下载 http://mirrors.aliyun.com/ubuntu/pool/main/g/gcc-5/libobjc-5-dev_5.4.0-6ubuntu1~16.04.9_amd64.deb  404  Not Found [IP: 121.9.229.124 80] 失败

E: 下载 http://mirrors.aliyun.com/ubuntu/pool/main/g/glib2.0/libglib2.0-dev_2.48.2-0ubuntu1_amd64.deb  404  Not Found [IP: 121.9.229.124 80] 失败

E: 有几个软件包无法下载，要不运行 apt-get update 或者加上 --fix-missing 的选项再试试？
```

执行一下apt-get update 再安装，就没有报错了。

安装其他工具。

```
sudo apt-get install -y g++ make binutils autoconf automake autotools-dev libtool pkg-config zlib1g-dev libcunit1-dev libssl-dev libxml2-dev libev-dev libevent-dev libjansson-dev libjemalloc-dev cython python3-dev python-setuptools  
```



编译安装nghttp2

```
cd ~/sdk-folder/third-party
git clone https://github.com/tatsuhiro-t/nghttp2.git
cd nghttp2
autoreconf -i
automake
autoconf
./configure
make
sudo make install
```

编译安装curl

```
cd ~/sdk-folder/third-party
wget http://curl.haxx.se/download/curl-7.54.0.tar.bz2
tar -xvjf curl-7.54.0.tar.bz2
cd curl-7.54.0
./configure --with-nghttp2=/usr/local --with-ssl
make
sudo make install
sudo ldconfig  
```

编译安装portaudio。

```
cd ~/sdk-folder/third-party
wget -c http://www.portaudio.com/archives/pa_stable_v190600_20161030.tgz && tar zxf pa_stable_v190600_20161030.tgz && cd portaudio && ./configure --without-jack && make  -j4
```

下载avs-sdk的代码。

```
cd ~/sdk-folder/sdk-source && git clone git://github.com/alexa/avs-device-sdk.git
```

编译avs-sdk。

```
cd /{HOME}/sdk-folder/sdk-build && cmake /{HOME}/sdk-folder/sdk-source/avs-device-sdk -DSENSORY_KEY_WORD_DETECTOR=OFF -DGSTREAMER_MEDIA_PLAYER=ON -DPORTAUDIO=ON -DPORTAUDIO_LIB_PATH=/{HOME}/sdk-folder/third-party/portaudio/lib/.libs/libportaudio.a -DPORTAUDIO_INCLUDE_DIR=/{HOME}/sdk-folder/third-party/portaudio/include && make
```

因为我的目录跟这个不一样。

替换如下：

```
export AVS_HOME=~/work/avs
```

```
cd ${AVS_HOME}/sdk-folder/sdk-build && cmake ${AVS_HOME}/sdk-folder/sdk-source/avs-device-sdk -DSENSORY_KEY_WORD_DETECTOR=OFF -DGSTREAMER_MEDIA_PLAYER=ON -DPORTAUDIO=ON -DPORTAUDIO_LIB_PATH=${AVS_HOME}/sdk-folder/third-party/portaudio/lib/.libs/libportaudio.a -DPORTAUDIO_INCLUDE_DIR=${AVS_HOME}/sdk-folder/third-party/portaudio/include && make -j4
```

编译通过了。

接下来修改配置文件。

```
~/sdk-folder/sdk-build/Integration/AlexaClientSDKConfig.json
```

主要就是指定一下db文件的路径。

改完后，要备份到外面的目录，因为这个目录下的文件，会被删掉。

运行。

```
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/sdk-build$ ./SampleApp/src/SampleApp ../AlexaClientSDKConfig.json 
2018-09-28 07:17:23.544 [  1] I sdkVersion: 1.7.1
configFile ../AlexaClientSDKConfig.json

2018-09-28 07:17:26.942 [  1] C SampleApplication:Failed to create default SDK client!
2018-09-28 07:17:26.942 [  1] C SampleApplication:Failed to initialize SampleApplication
################################################################
#       UNRECOVERABLE AUTHORIZATION ERROR: INVALID_VALUE       #
#       Entering limited interaction mode.                     #
################################################################

Failed to create to SampleApplication!
```

这个也是首先要一个授权，这里是授权失败了。

因为之前那个账号是很久之前弄的。所以现在我重新弄一个设备的client来注册。

参考这篇文章：https://github.com/alexa/avs-device-sdk/wiki/Create-Security-Profile。

做完了，才发现不需要。因为我之前把client id弄错了。clientid是很长的那个。

```
##################################
#       NOT YET AUTHORIZED       #
##################################

################################################################################################
#       To authorize, browse to: 'https://amazon.com/us/code' and enter the code: BSCS4N       #
################################################################################################
```

我登陆了网页，把code也输入了，提示成功了。

但是运行还是不行。

```
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/sdk-build$ ./SampleApp/src/SampleApp ../AlexaClientSDKConfig.json 
2018-09-28 07:47:05.134 [  1] I sdkVersion: 1.7.1
configFile ../AlexaClientSDKConfig.json
##################################
#       NOT YET AUTHORIZED       #
##################################

################################################################################################
#       To authorize, browse to: 'https://amazon.com/us/code' and enter the code: CCXX7J       #
################################################################################################

#################################################
#       Checking for authorization (1)...       #
#################################################

#################################################
#       Checking for authorization (2)...       #
#################################################

```

先放着，过段时间再看。



# 分析编译过程

看看传递进去的几个宏。

```
-DSENSORY_KEY_WORD_DETECTOR=OFF  这个表示不用关键字唤醒。
-DGSTREAMER_MEDIA_PLAYER=ON  使用gstreamer作为播放器。
-DPORTAUDIO=ON 
-DPORTAUDIO_LIB_PATH=${AVS_HOME}/sdk-folder/third-party/portaudio/lib/.libs/libportaudio.a 
-DPORTAUDIO_INCLUDE_DIR=${AVS_HOME}/sdk-folder/third-party/portaudio/include
```

到build目录下看看编译配置文件。



参考资料



https://github.com/alexa/avs-device-sdk/wiki/Ubuntu-Linux-Quick-Start-Guide



