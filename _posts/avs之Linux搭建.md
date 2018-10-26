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
make -j4
sudo make install
```

编译安装curl

```
cd ~/sdk-folder/third-party
wget http://curl.haxx.se/download/curl-7.54.0.tar.bz2
tar -xvjf curl-7.54.0.tar.bz2
cd curl-7.54.0
./configure --with-nghttp2=/usr/local --with-ssl
make -j4
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



# 解决问题

我直接手动修改log级别为DEBUG9。出现了下面的警告。

```
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/sdk-build/SampleApp/src$ ./SampleApp ../../../AlexaClientSDKConfig.json 
2018-10-09 07:51:40.403 [  1] I sdkVersion: 1.7.1
configFile ../../../AlexaClientSDKConfig.json
2018-10-09 07:51:40.441 [  1] W Logger:debugLogLevelSpecifiedWhenDebugLogsCompiledOut:level=DEBUG9:

WARNING: By default DEBUG logs are compiled out of RELEASE builds.
Rebuild with the cmake parameter -DCMAKE_BUILD_TYPE=DEBUG to enable debug logs.
```

修改编译命令如下：

```
cd ${AVS_HOME}/sdk-folder/sdk-build && cmake ${AVS_HOME}/sdk-folder/sdk-source/avs-device-sdk -DSENSORY_KEY_WORD_DETECTOR=OFF -DGSTREAMER_MEDIA_PLAYER=ON -DPORTAUDIO=ON -DPORTAUDIO_LIB_PATH=${AVS_HOME}/sdk-folder/third-party/portaudio/lib/.libs/libportaudio.a -DPORTAUDIO_INCLUDE_DIR=${AVS_HOME}/sdk-folder/third-party/portaudio/include -DCMAKE_BUILD_TYPE=DEBUG && make -j4
```

编译运行，打印就很详细了。

看到这个错误。

```
2018-10-09 07:57:28.365 [  1] E Settings:initializeFailed:reason=SettingNotFoundinConfigFile
2018-10-09 07:57:28.365 [  1] E Settings:createFailed:reason=Initialization error.
2018-10-09 07:57:28.366 [  1] E DefaultClient:initializeFailed:reason=unableToCreateSettingsObject
2018-10-09 07:57:28.366 [  1] 5 DefaultClient:DirectiveSequencerShutdown
```

找到问题所在了，就是locale这个参数没有设置值，给en-US就好了。

现在可以跑起来了。现在把打印看一遍。

不改配置，单独编译，命令是：

```
cd ${AVS_HOME}/sdk-folder/sdk-build && make -j4
```

参数里，可以带上log基本参数。

我当前的json配置。

```
 {
    "cblAuthDelegate":{
        // Path to CBLAuthDelegate's database file. e.g. /home/ubuntu/Build/cblAuthDelegate.db
        // Note: The directory specified must be valid.
        // The database file (cblAuthDelegate.db) will be created by SampleApp, do not create it yourself.
        // The database file should only be used for CBLAuthDelegate (don't use it for other components of SDK)
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/cblAuthDelegate.db"
    },
    "deviceInfo":{
        // Unique device serial number. e.g. 123456
        "deviceSerialNumber":"123456",
        // The Client ID of the Product from developer.amazon.com
        "clientId":"amzn1.application-oa2-client.35febb1698874deca2ae0e7ac1d813d6",
        // Product ID from developer.amazon.com
        "productId":"teddy_echo"
    },
    "capabilitiesDelegate":{
        // The endpoint to connect in order to send device capabilities.
        // This will only be used in DEBUG builds.
        // e.g. "endpoint": "https://api.amazonalexa.com"
        // Override the message to be sent out to the Capabilities API.
        // This will only be used in DEBUG builds.
        // e.g. "overridenCapabilitiesPublishMessageBody": {
        //          "envelopeVersion":"20160207",
        //          "capabilities":[
        //              {
        //                "type":"AlexaInterface",
        //                "interface":"Alerts",
        //                "version":"1.1"
        //              }
        //          ]
        //      }
    },
    "miscDatabase":{
        // Path to misc database file. e.g. /home/ubuntu/Build/miscDatabase.db
        // Note: The directory specified must be valid.
        // The database file (miscDatabase.db) will be created by SampleApp, do not create it yourself.
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/miscDatabase.db"
    },
    "alertsCapabilityAgent":{
        // Path to Alerts database file. e.g. /home/ubuntu/Build/alerts.db
        // Note: The directory specified must be valid.
        // The database file (alerts.db) will be created by SampleApp, do not create it yourself.
        // The database file should only be used for alerts (don't use it for other components of SDK)
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/alerts.db"
    },
    "settings":{
        // Path to Settings database file. e.g. /home/ubuntu/Build/settings.db
        // Note: The directory specified must be valid.
        // The database file (settings.db) will be created by SampleApp, do not create it yourself.
        // The database file should only be used for settings (don't use it for other components of SDK)
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/settings.db",
        "defaultAVSClientSettings":{
            // Default language for Alexa.
            // See https://developer.amazon.com/docs/alexa-voice-service/settings.html#settingsupdated for valid values.
            "locale":"en-US"
        }
    },
    "bluetooth" : {
        // Path to Bluetooth database file. e.g. /home/ubuntu/Build/bluetooth.db
        // Note: The directory specified must be valid.
        // The database file (bluetooth.db) will be created by SampleApp, do not create it yourself.
        // The database file should only be used for bluetooth (don't use it for other components of SDK)
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/bluetooth.db"
    },
    "certifiedSender":{
        // Path to Certified Sender database file. e.g. /home/ubuntu/Build/certifiedsender.db
        // Note: The directory specified must be valid.
        // The database file (certifiedsender.db) will be created by SampleApp, do not create it yourself.
        // The database file should only be used for certifiedSender (don't use it for other components of SDK)
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/certifiedsender.db"
    },
    "notifications":{ 
        // Path to Notifications database file. e.g. /home/ubuntu/Build/notifications.db
        // Note: The directory specified must be valid.
        // The database file (notifications.db) will be created by SampleApp, do not create it yourself.
        // The database file should only be used for notifications (don't use it for other components of SDK)
        "databaseFilePath":"/home/hlxiong/work/avs/sdk-folder/application-necessities/notifications.db"
    },
    "sampleApp":{
        // To specify if the SampleApp supports display cards.
        "displayCardsSupported":false
        // The firmware version of the device to send in SoftwareInfo event.
        // Note: The firmware version should be a positive 32-bit integer in the range [1-2147483647].
        // e.g. "firmwareVersion": 123
        // The default endpoint to connect to.
        // See https://developer.amazon.com/docs/alexa-voice-service/api-overview.html#endpoints for regions and values
        // e.g. "endpoint": "https://avs-alexa-na.amazon.com"

        // Example of specifying suggested latency in seconds when openning PortAudio stream. By default,
        // when this paramater isn't specified, SampleApp calls Pa_OpenDefaultStream to use the default value.
        // See http://portaudio.com/docs/v19-doxydocs/structPaStreamParameters.html for further explanation
        // on this parameter.
        //"portAudio":{
        //    "suggestedLatency": 0.150
        //}
    }

    // Example of specifying output format and the audioSink for the gstreamer-based MediaPlayer bundled with the SDK.
    // Many platforms will automatically set the output format correctly, but in some cases where the hardware requires
    // a specific format and the software stack is not automatically setting it correctly, these parameters can be used
    // to manually specify the output format.  Supported rate/format/channels values are documented in detail here:
    // https://gstreamer.freedesktop.org/documentation/design/mediatype-audio-raw.html
    //
    // By default the "autoaudiosink" element is used in the pipeline.  This element automatically selects the best sink
    // to use based on the configuration in the system.  But sometimes the wrong sink is selected and that prevented sound
    // from being played.  A new configuration is added where the audio sink can be specified for their system.
    // "gstreamerMediaPlayer":{
    //     "outputConversion":{
    //         "rate":16000,
    //         "format":"S16LE",
    //         "channels":1
    //     },
    //     "audioSink":"autoaudiosink"
    // },

    // Example of specifying a default log level for all ModuleLoggers.  If not specified, ModuleLoggers get
    // their log level from the sink logger.
    //"logging":{
    //     "logLevel":"DEBUG9"
    //},

    // Example of overriding a specific ModuleLogger's log level whether it was specified by the default value
    // provided by the logging.logLevel value (as in the above example) or the log level of the sink logger.
    //"acl":{
    //    "logLevel":"DEBUG9"
    //}
 }


// Notes for logging
// The log levels are supported to debug when SampleApp is not working as expected.
// There are 14 levels of logging with DEBUG9 providing the highest level of logging and CRITICAL providing
// the lowest level of logging i.e. if DEBUG9 is specified while running the SampleApp, all the logs at DEBUG9 and
// below are displayed, whereas if CRITICAL is specified, only logs of CRITICAL are displayed.
// The 14 levels are:
// DEBUG9, DEBUG8, DEBUG7, DEBUG6, DEBUG5, DEBUG4, DEBUG3, DEBUG2, DEBUG1, DEBUG0, INFO, WARN, ERROR, CRITICAL.

// To selectively see the logging for a particular module, you can specify logging level in this json file.
// Some examples are:
// To only see logs of level INFO and below for ACL and MediaPlayer modules,
// -  grep for ACSDK_LOG_MODULE in source folder. Find the log module for ACL and MediaPlayer.
// -  Put the following in json:

// "acl":{
//  "logLevel":"INFO"
// },
// "mediaPlayer":{
//  "logLevel":"INFO"
// }

// To enable DEBUG, build with cmake option -DCMAKE_BUILD_TYPE=DEBUG. By default it is built with RELEASE build.
// And run the SampleApp similar to the following command.
// e.g. ./SampleApp /home/ubuntu/.../AlexaClientSDKConfig.json /home/ubuntu/KittAiModels/ DEBUG9"

```



现在仍然是有错误。授权不成功。看网上有个说是productid给的不对。但是我的是对的。

```
2018-10-09 08:21:30.712 [  2] 5 HttpPost:doPostSucceeded:code=400
2018-10-09 08:21:30.712 [  2] 5 CBLAuthDelegate:receiveTokenResponse:code=400
2018-10-09 08:21:30.712 [  2] 5 CBLAuthDelegate:mapHTTPStatusToError:code=400,error=INVALID_REQUEST
2018-10-09 08:21:30.713 [  2] 5 CBLAuthDelegate:errorInLwaResponseBody:error=authorization_pending,errorCode=AUTHORIZATION_PENDING
2018-10-09 08:21:30.713 [  2] 5 CBLAuthDelegate:setAuthError:authError=AUTHORIZATION_PENDING
2018-10-09 08:21:30.713 [  2] 0 CBLAuthDelegate:receiveTokenResponseFailed:result=AUTHORIZATION_PENDING
```

我知道了。每次运行都需要把命令行上打印出来的这种代码在网站上提交一下。

```
https://amazon.com/us/code' and enter the code: AKL66X
```

接下来可以在树莓派上来做了。

另外，还有一个limited的问题。

这个是因为要在secure profile哪里，选择other platform，把client id填入，然后点击generate，生成一个新的client id，把新生成的，写到json配置里，然后启动就好了。

如果之前出错了的。那么就把cbl那个db文件删掉就好了。





#参考资料

1、

https://github.com/alexa/avs-device-sdk/wiki/Ubuntu-Linux-Quick-Start-Guide

2、Linux平台:Alexa语音服务快速入门指南

https://blog.csdn.net/z2066411585/article/details/78573368

3、

https://github.com/alexa/avs-device-sdk/issues/705