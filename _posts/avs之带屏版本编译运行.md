---
title: avs之带屏版本编译运行
date: 2018-11-03 16:42:19
tags:
	- avs

---



1、检查ca_settings.cnf和generate.sh里的内容，根据需求调整，当前只供测试用。

2、运行generate.sh脚本。

```
hlxiong@hlxiong-VirtualBox:~/work2/avs-screen/linux-screen/AlexaClientSDK/tools/Gui/certificates$ ./generate.sh 
Generating a 2048 bit RSA private key
...................................................................+++
...............................+++
writing new private key to 'ca.key'
-----
Generating a 2048 bit RSA private key
...........................................................................................................................................................................................................................+++
..............+++
writing new private key to 'client.key'
-----
Generating a 2048 bit RSA private key
..............+++
..............................+++
writing new private key to 'server.key'
-----
Signature ok
subject=/CN=MMSDK_Client_Cert/C=US/ST=WA/L=Seattle/O=Amazon
Getting CA Private Key
Signature ok
subject=/CN=localhost/C=US/ST=WA/L=Seattle/O=Amazon
Getting CA Private Key
```

提示要输入密码，我直接回车，没有看到报错，应该是可以为空密码的。

然后需要在系统里设备把这些key设置为always trust的。

```
hlxiong@hlxiong-VirtualBox:~/work2/avs-screen/linux-screen/AlexaClientSDK/tools/Gui/certificates$ tree -h
.
├── [1.4K]  ca.cert
├── [1.7K]  ca.key
├── [ 765]  ca_settings.cnf
├── [  17]  ca.srl
├── [ 277]  cert_settings.cnf
├── [1.3K]  client.cert
├── [2.7K]  client.chain
├── [ 985]  client.csr
├── [1.7K]  client.key
├── [3.6K]  client.p12
├── [1.2K]  generate.sh
├── [1.3K]  server.cert
├── [2.7K]  server.chain
├── [ 972]  server.csr
└── [1.7K]  server.key
```

我们需要把ca.cert的内容拷贝到系统目录下去。

```
sudo cp ca.cert /usr/local/share/ca-certificates
```

当前我的系统这个目录下还没有文件。

然后更新一下。

```
sudo update-ca-certificates
```

```
hlxiong@hlxiong-VirtualBox:~/work2/avs-screen/linux-screen/AlexaClientSDK/tools/Gui/certificates$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
0 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```

看这个打印，并没有起任何作用。

算了，看文档，可以不使用这个安全措施。

```
use DISABLE_WEBSOCKET_SSL option during the build and use '?insecure=1' when opening GUI
```

需要安装npm。

```
sudo apt-get install npm
```

执行下面的命令的时候，在npm install的时候，卡住不懂，我执行run build的，会出错，说webpack找不到。

```
cd AlexaClientSDK/GUI/js
npm install
npm run build
```

先安装webpack。

```
sudo npm install webpack -g
```

这个可以看到进度条的变化。

也不行，还是按步骤来。

卡住，先等半个小时再看吧。

看到打印说，不用用代理好像。先把代理关闭。



我这边编译avs很顺利。

问题就是nodejs的环境弄不好。

这2者的关系是什么？

我觉得我的nodejs安装有问题，可能跟我的代理有关系。

关闭所有代理。就好了。停止polipo。unset http_proxy等。

```
npm config set https-proxy 
```

然后再试。就可以了。还要注意换成淘宝的源。

websocketpp是做什么的？



现在看看带屏版本有哪些不一样的地方。



对比，

版本号升级到1.8.1，发布于2018年7月9日。

```
ACL：interface类，增加析构函数。之前可能因为这个导致了内存泄露。
ADSL：对MessageInterpreter进行了改写。
AMFL：对FocusManager里的变量改成函数。
ApplicationUtilities：DefaultClient进行了完善。
Authorization：新的去掉了这个目录。
```

```
export AVS_HOME=~/work/avs
cmake -DENABLE_WEBSOCKET_SERVER=ON \
-DWEBSOCKETPP_INCLUDE_DIR=/home/hlxiong/work2/avs-screen/linux-screen/websocketpp-0.8.1 \
-DOPENSSL_ROOT_DIR=/usr/bin/openssl \
-DGSTREAMER_MEDIA_PLAYER=ON \
-DCMAKE_BUILD_TYPE=DEBUG \
-DPORTAUDIO=ON \
-DPORTAUDIO_LIB_PATH=${AVS_HOME}/sdk-folder/third-party/portaudio/lib/.libs/libportaudio.a  \
-DPORTAUDIO_INCLUDE_DIR=${AVS_HOME}/sdk-folder/third-party/portaudio/include \
-DDISABLE_WEBSOCKET_SSL=ON \
../AlexaClientSDK
```



关键还是看懂websocketpp如何起作用的。

```
#ifdef ENABLE_WEBSOCKET_SERVER//这个使能了。
    std::string websocketInterface;
    sampleAppConfig.getString(WEBSOCKET_INTERFACE_KEY, &websocketInterface, DEFAULT_WEBSOCKET_INTERFACE);

    int websocketPortNumber;
    sampleAppConfig.getInt(WEBSOCKET_PORT_KEY, &websocketPortNumber, DEFAULT_WEBSOCKET_PORT);

    /*
     * Create the websocket server that handles communications with websocket clients
     */
    m_webSocketServer = std::make_shared<WebSocketServer>(websocketInterface, websocketPortNumber);

#ifdef ENABLE_WEBSOCKET_SSL//这个没使能。
    std::string sslCaFile;
    sampleAppConfig.getString(WEBSOCKET_CERTIFICATE_AUTHORITY, &sslCaFile);

    std::string sslCertificateFile;
    sampleAppConfig.getString(WEBSOCKET_CERTIFICATE, &sslCertificateFile);

    std::string sslPrivateKeyFile;
    sampleAppConfig.getString(WEBSOCKET_PRIVATE_KEY, &sslPrivateKeyFile);

    m_webSocketServer->setCertificateFile(sslCaFile, sslCertificateFile, sslPrivateKeyFile);
#endif
```

分析一下WebSocketServer这个类。

WebSocketConfig

看看运行打印。

```
2018-11-05 01:45:42.689 [  1] 9 WebSocket:AccessLog::create_connection
2018-11-05 01:45:42.689 [  1] 9 WebSocket:AccessLog::asio con transport constructor
2018-11-05 01:45:42.689 [  1] 9 WebSocket:AccessLog::connection constructor
2018-11-05 01:45:42.689 [  1] 9 WebSocket:AccessLog::transport::asio::init
2018-11-05 01:45:42.689 [  1] 9 WebSocket:AccessLog::asio::async_accept
2018-11-05 01:45:42.689 [  1] I WebSocketServer:Listening for websocket connections:interface=127.0.0.1,port=8933
```

我用浏览器访问127.0.0.1:8933，得到的是空白界面。但是avs的打印有输出。

```
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::GET / HTTP/1.1
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en;q=0.5
Cache-Control: max-age=0
Connection: keep-alive
Host: 127.0.0.1:8933
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0


2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::process handshake request
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::HTTP REQUEST
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::connection write_http_response
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::Raw Handshake response:
HTTP/1.1 426 Upgrade Required
Server: WebSocket++/0.8.1


2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::handle_write_http_response
2018-11-05 01:58:50.935 [  1] E WebSocket:ErrorLog::Handshake ended with HTTP error: 426
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::connection terminate
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::WebSocket Connection 127.0.0.1:43188 v0 "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:60.0) Gecko/20100101 Firefox/60.0" / 426 websocketpp:28 Upgrade required
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::asio connection async_shutdown
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::asio con handle_async_shutdown
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::connection handle_terminate
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::open handshake timer cancelled
2018-11-05 01:58:50.935 [  1] 9 WebSocket:AccessLog::asio socket shutdown timer cancelled
2018-11-05 01:58:57.398 [  2] 5 CBLAuthDelegate:requestRefresh
2018-11-05 01:58:57.398 [  2] E HttpPost:doPostFailed:reason=curl_easy_performFailed,result=7,error=Couldn't connect to server
2018-11-05 01:58:57.398 [  2] 5 CBLAuthDelegate:receiveTokenResponse:code=0
```

其实当前虽然有错误打印，但是基本是跑起来的。还需要改2个点就好了。

1、json文件里，把Display改为true。

2、亚马逊网站上，也要把Display的勾选上。

现在打开网页，点击网页最下面的原型按钮，就可以唤醒，查询天气，就可以看到界面渲染是效果了。





https://developer.amazon.com/zh/docs/alexa-voice-service/display-cards-overview.html



先看完这3个头文件。

```
#include "SampleApp/WebSocketServer.h"
#include "SampleApp/JsonGuiRenderer.h"
#include "SampleApp/JsonUIManager.h"
```

总的来说，就是在有变化的时候，发送json字符串到server。

网页就监听变化。

现在要看看js代码这边是如何进行渲染的。

index.html里就一行是有效的：

```
<script type="text/javascript" src="main.bundle.js"></script></body>
```

这个js脚本有1.2M。非常大。

这个代码没法看。太复杂。我对js不太熟悉。

我现在看看点击圆形按钮后的流程理一下。

应该是这里收到消息。

```
void JsonInputManager::onMessage
	    } else if (MESSAGE_TYPE_TAP_TO_TALK == messageType) {
        m_interactionManager->tap();
```

看看怎么把唤醒词加入进去。

```
        pathToInputFolder + "/common.res",
        {{pathToInputFolder + "/alexa.umdl", "ALEXA", KITT_AI_SENSITIVITY}},
        KITT_AI_AUDIO_GAIN,
```

目前这些资源是没有的。

这里有alexa.umdl文件。

https://github.com/Kitt-AI/snowboy/tree/master/resources/alexa/alexa-avs-sample-app

这里有common.res文件。

https://github.com/Kitt-AI/snowboy/tree/master/resources

这个运行命令要稍微改一下。需要加一个参数，指定资源的位置。

```
#if defined(KWD_KITTAI) || defined(KWD_SENSORY)

        if (argc < 3) {
            alexaClientSDK::sampleApp::ConsolePrinter::simplePrint(
                "USAGE: " + std::string(argv[0]) +
                " <path_to_AlexaClientSDKConfig.json> <path_to_inputs_folder> [log_level]");
            return EXIT_FAILURE;
        } else {
            pathToKWDInputFolder = std::string(argv[2]);
            if (4 == argc) {
                logLevel = std::string(argv[3]);
            }
        }
#else
```

最新版本的才能保存配置改了，只编译部分文件。否则配置改了，都是全部编译。

发现我加的错误，并没有编译进去。

是因为要加上这个配置。

```
export AVS_HOME=/home/hlxiong/work/avs
cd ${AVS_HOME}/sdk-folder/sdk-build \
&& cmake ${AVS_HOME}/sdk-folder/sdk-source/avs-device-sdk \
-DSENSORY_KEY_WORD_DETECTOR=OFF -DGSTREAMER_MEDIA_PLAYER=ON -DPORTAUDIO=ON \
-DPORTAUDIO_LIB_PATH=${AVS_HOME}/sdk-folder/third-party/portaudio/lib/.libs/libportaudio.a \
-DPORTAUDIO_INCLUDE_DIR=${AVS_HOME}/sdk-folder/third-party/portaudio/include \
-DCMAKE_BUILD_TYPE=DEBUG \   
-DKITTAI_KEY_WORD_DETECTOR=ON # 加上这个。
```

现在编译就会报错。

```
Creating the build directory for the AlexaClientSDK with build type: DEBUG
Creating AlexaClientSDK with keyword detector type: KittAi
CMake Error at build/cmake/KeywordDetector.cmake:70 (message):
  Must pass library path of Kitt.ai KeywordDetector!
Call Stack (most recent call first):
  build/BuildDefaults.cmake:22 (include)
  CMakeLists.txt:10 (include)
```

意思是要指定kittai的库的路径。

KITTAI_KEY_WORD_DETECTOR_LIB_PATH 这个要定义。

还需要加上include的路径。

```
apt-get install libatlas-base-dev
```

还是不行。算了。放弃snowboy的。这个反正也没有实用价值。

https://zhuanlan.zhihu.com/p/31189369

sensory的只能在树莓派上运行。



