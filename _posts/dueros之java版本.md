---
title: dueros之java版本
date: 2018-05-19 19:04:46
tags:
	- dueros
typora-root-url: ..\
---



java版本代码都有，然后我还可以正常编译在手机上测试运行。

所以是目前最适合的学习材料。



1、下载代码。

https://github.com/dueros/dcs-sdk-java

2、用Android studio打开工程。

修改里面的client id为你自己申请的值。

```
public class DcsSampleOAuthActivity extends Activity implements View.OnClickListener {
    // 需要开发者自己申请client_id
    // client_id，就是oauth的client_id
    private static final String CLIENT_ID = "";//这里修改。
```

3、然后编译出apk文件，发送到手机端安装。

4、打开App，填入你的百度账号和密码，进行授权，然后进进入到主界面了。

![](/images/dueros之java版本-主界面.png)

点击说话，就是唤醒了设备，然后你可以说一些话。

也可以直接用“小度小度”来语言唤醒。

主界面是DcsSampleMainActivity。

```
    private void startMainActivity() {
        Intent intent = new Intent(DcsSampleOAuthActivity.this, DcsSampleMainActivity.class);
        startActivity(intent);
        finish();
    }
```



类层次结构

```
androidapp
	DcsSampleApplication.java
	DcsSampleMainActivity.java
	DcsSampleOauthActivity.java
	DcsSampleScreenHtmlActivity.java
androidsystemimpl
	alert
		AlertsFileDataStoreImpl.java
	audioinput
		AudioVoiceInputImpl.java
		AudioVoiceInputThread.java
	playbackcontroller
		IPlaybackControllerImpl.java
	player
		AudioStoreThread.java
		AudioStreamStoreImpl.java
		AudioTrackPlayerImpl.java
		IAudioStreamStore.java
		MediaPlayerImpl.java
		MediaPlayerPreferenceUtil.java
	wakeup
		WakeUpDecodeThread.java
		WakeUpImpl.java
		WakeUpNative.java
	webview
		BaseWebView.java
	AudioRecordThread.java
	HandleImpl.java
	PlatformFactoryImpl.java
	
api
	IConnectionStatusListener.java
devicemodule
	
framework
http
oauth
systeminterface
util
	CommonUtil.java
	
wakeup
```

理解系统，重要的是devicemodule和framework这2个目录。

devicemodule下面，是8个模块，就叫八大金刚吧。



保存闹钟是alarms.json文件。



文件

```
/DCS
	LogAll.txt
	Speaker
	Alert
		alarms.json
```

我们看看LogAll.txt文件的内容。



alarms.json里的内容。

```
[{"token":"eyJib3RfaWQiOiJhaS5kdWVyb3MuYm90LmFsYXJtIiwicmVzdWx0X3Rva2VuIjoiMzVhMDRkYzNkMDUyZjVjMWI3N2FmYmQ2ZDAxYjEyMzgiLCJib3RfdG9rZW4iOiI1MTI4NzgwNWRhMzc5In0=","type":"ALARM","scheduledTime":"2018-05-19T11:19:07+0000"}]
```



从HeartBeat类看起。

这个是进行定时跟服务器通信的。

```
private final HttpRequestInterface httpRequest;//用来发起http请求的接口。
关键函数是这里。
private void startPing() {
        httpRequest.cancelRequest(HttpConfig.HTTP_PING_TAG);
        httpRequest.doGetPingAsync//这里。
       
具体实现是在OkHttpRequestImpl里。
DcsHttpManager.get()//这里得到一个builder。
                .url(HttpConfig.getPingUrl())
                .headers(HttpConfig.getDCSHeaders())
                .tag(HttpConfig.HTTP_PING_TAG)
                .build()
                .execute(dcsCallback);//关键是这个函数。这里还是只放入到一个队列，具体发送行为看不到。
```

安卓平台是用Handler来处理的。

```
static class MainThreadExecutor implements Executor {
            private final Handler handler = new Handler(Looper.getMainLooper());

            @Override
            public void execute(Runnable r) {
                handler.post(r);
            }
        }
```



然后从WakeUp类开始看。

类层次是：

```
IWakeUp 在systeminterface包。
	WakeUp  在wakeup包。这个类的作用是什么？相当于对接口的一个简单包装。
		WakeUpImpl 在androidsystemimpl\wakeup。
		WakeUpNative 这个是跟cpp文件打交道的。
		WakeUpDecodeThread extends Thread
```

在main Activity里。

```
// init唤醒
        wakeUp = new WakeUp(platformFactory.getWakeUp(),
                platformFactory.getAudioRecord());
        wakeUp.addWakeUpListener(wakeUpListener);
        // 开始录音，监听是否说了唤醒词
        wakeUp.startWakeUp();
```



```
public class WakeUpNative {

    // 加载动态库.so文件
    static {
        System.loadLibrary("wakeup");
        // 唤醒词解码so库
        System.loadLibrary("bdEASRAndroid");
    }
```



```
    // 唤醒词
    private static final String WAKEUP_WORD = "小度小度";
    // 唤醒词声学模型模型文件
    private static final String WAKEUP_FILENAME = "libbdEasrS1MergeNormal.so";
```



然后是平台工厂里的getAudioRecord。这个就涉及到录音了。

是audio input设备。

相关类有：

```
IAudioRecord
	就2个接口，startRecord、stopRecord。
AudioRecordThread

```



靠的是Android的这3个类来实现录音的。

```
import android.media.AudioFormat;
import android.media.AudioRecord;
import android.media.MediaRecorder;
```

录音：

```
		audioRecord.startRecording();
        byte[] buffer = new byte[bufferSize];
        while (isStartRecord) {
            int readBytes = audioRecord.read(buffer, 0, bufferSize);
            if (readBytes > 0) {
                linkedBlockingDeque.add(buffer);
            }
        }	
```

audio input和audio Record是什么关系？

audio input是audio  Record的后端。是输入到dcs的意思。



IPlatformFactory是一个聚合了系统的各个模块的工厂类。

总的来说，输入是3个类：

```
wakeup
audio record
audio input
```

输出是3个类：

```
media player
audio track player
alert player
```

我们先看MediaPlayer的。

```
IMediaPlayer
	方法较多。
	主要是play、stop、pause 、resume。
	有一个PlayState的枚举。状态有8种。
	然后内部有一个监听类。监听了这8种状态。
	然后实现了一个默认的监听类。
MediaPlayerImpl

```

播放器的底层是安卓的。

```
import android.media.MediaPlayer;
```

先看闹钟的，这个比较简单。

```
IAlertsDataStore
	2个方法：readFromDisk和writeToDisk
AlertsFileDataStoreImpl
Alert
AlertScheduler
AlertHandler
	里面就2个方法startAlert和stopAlert。
	
```

```
.
├── AlertHandler.java
├── AlertScheduler.java
├── AlertsDeviceModule.java  这个相当于总的入口。
├── ApiConstants.java
└── message
    ├── Alert.java
    ├── AlertPayload.java
    ├── AlertsStatePayload.java
    ├── DeleteAlertPayload.java
    └── SetAlertPayload.java
```

分为两种：

```
public enum AlertType {
        ALARM,
        TIMER
    }
```

```
// 闹铃开始是播放的音频文件
    private static final String ALARM_NAME = "assets://alarm.mp3";
```

```
AlertsDeviceModule类
	继承了BaseDeviceModule
	实现了AlertHandler接口。
	在构造的时候，会从文件里读取之前的闹钟。
		如果当前时间距离闹钟响已经超过30分钟了。就丢弃。
		丢弃是要把消息上报到服务端的。
		每一个闹钟有一个token来唯一标识。
		
```

闹钟对应的播放器。

```
IMediaPlayer mediaPlayer = deviceModuleHandler.getMultiChannelMediaPlayer()
                .addNewChannel(deviceModuleHandler.getPlatformFactory().createMediaPlayer(),
                        MediaChannel.ALERT.channelName,
                        MediaChannel.ALERT.priority);
对应的是PauseStrategyMultiChannelMediaPlayer。
暂停模式的播放控制策略
基于优先级进行比较，把优先级低的pause掉。

```

DcsFramework是一个核心类。

下面的这些对象都很重要。

```
	// 管理平台相关的对象
    private final IPlatformFactory platformFactory;
    // 管理deviceModules
    private final HashMap<String, BaseDeviceModule> dispatchDeviceModules;
    // 创建会话Id
    private final DialogRequestIdHandler dialogRequestIdHandler;
    // 基于通道活跃状态和优先级进行mediaPlayer调度
    private final BaseMultiChannelMediaPlayer multiChannelMediaPlayer;
    // 创建deviceModule工厂
    private DeviceModuleFactory deviceModuleFactory;
    // 和服务器端保持长连接、发送events和接收directives和维持心跳
    private DcsClient dcsClient;
    // 用于DeviceModules发送events
    private IMessageSender messageSender;
    // 服务器端返回response调度中心
    private DcsResponseDispatcher dcsResponseDispatcher;
```



devicemodule这个目录值得玩味。

```
teddy@teddy-ubuntu:~/work/dueros/dcs-sdk-java-master/app/src/main/java/com/baidu/duer/dcs/devicemodule$ tree -L 1
.
├── alerts
├── audioplayer
├── playbackcontroller
├── screen
├── speakcontroller
├── system
├── voiceinput
└── voiceoutput
```



```
IHandler
	就一个post方法。
HandlerImpl
```



静音和音量调节的关系。

```
    public void setVolume(float volume) {
        // 设置音量就不再静音了，比如：说了调衡音量等操作
        isMute = false;
        currentVolume = volume;
```



HttpConfig内容。

```
public class HttpConfig {
    // 请求https
    public static final String HTTP_PREFIX = "https://";
    // 请求host
    public static final String HOST = "dueros-h2.baidu.com";
    public static String endpoint = null;
    // 请求event事件
    public static final String EVENTS = "/dcs/v1/events";
    // 请求directives事件
    public static final String DIRECTIVES = "/dcs/v1/directives";
    // ping
    public static final String PING = "/dcs/v1/ping";
    // 请求event事件TAG
    public static final String HTTP_EVENT_TAG = "event";
    // 请求voice
    public static final String HTTP_VOICE_TAG = "voice";
    // 请求directives事件TAG
    public static final String HTTP_DIRECTIVES_TAG = "directives";
    // 请求ping的TAG
    public static final String HTTP_PING_TAG = "ping";
```



总体流程：

```
1、在MainActivity onCreate的时候，会initFramework。就是构造DcsFramework。
2、在这里会创建dcs client。里面会连接服务器。dcsClient.startConnect();
	就是发一个request请求。
	
```



打开日志文件的代码是这样。

```
    private void openAssignFolder(String path) {
        File file = new File(path);
        if (!file.exists()) {
            Toast.makeText(DcsSampleMainActivity.this,
                    getResources().getString(R.string.no_log),
                    Toast.LENGTH_SHORT)
                    .show();
            return;
        }
        Intent intent = new Intent(Intent.ACTION_VIEW);
        intent.addCategory(Intent.CATEGORY_DEFAULT);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
        intent.setDataAndType(Uri.fromFile(file), "text/plain");
        try {
            startActivity(Intent.createChooser(intent,
                    getResources().getString(R.string.open_file_title)));
        } catch (ActivityNotFoundException e) {
            e.printStackTrace();
        }
    }
```



我找一下，手机没有联网的时候，闹钟如何处理的？

我现在设置一个闹钟，然后把手机网络关闭。1分钟后，闹钟还是响了。

那说明的确不是靠服务器发来的指令触发闹钟响的。

闹钟是借助于安卓的Handler。

还借助于

```
AlertScheduler extends Timer
```



```
public class Alert {
    private final String token;
    private final SetAlertPayload.AlertType type;
    // 触发时间，ISO 8601格式
    private final String scheduledTime;
```

从这里看，的确是依赖本机的定时器的。

但是dueros的linux版本，这些交互并没有看到对应的接口。

定闹钟的交互过程：

1、用户说定时1分钟。

2、服务器识别出来，下发指令给设备来定时吗？还是时间到了再给设备发指令提示呢？

从安卓版本来看，是在本地进行的定时。

```
    public void handleDirective(Directive directive) throws HandleDirectiveException {
        String directiveName = directive.getName();
        if (directiveName.equals(ApiConstants.Directives.SetAlert.NAME)) {
            // 设置一个闹铃／提醒的指令处理逻辑
            LogUtil.d(TAG, "alert-SetAlertPayload");
            SetAlertPayload payload = (SetAlertPayload) directive.payload;

            String alertToken = payload.getToken();
            String scheduledTime = payload.getScheduledTime();
            LogUtil.d(TAG, "alert-scheduledTime:" + scheduledTime);
```



那对于linux版本，也是要解析指令才行。

或者是dueros sdk里已经封装了实现了。因为这个是通用的性的，百度没有理由不进行实现啊。



# 自己编译

会提示需要mips的工具链。但是我用不上这个工具链。网上看到解释说要升级gradle版本。

那我就升级到gradle-3.4-rc-3-all.zip

修改app/gradle-wrapper/gradle-wrapper.properties文件。

当前是2.1.4的，替换。

然后执行build。需要重新下载。耐心等待。

但是这样问题仍然有。

打开git bash。进入到/d/android_sdk/ndk-bundle/toolchains。执行下面的语句。

```
 ln -sf aarch64-linux-android-4.9 mips64el-linux-android
 ln -sf aarch64-linux-android-4.9 mipsel-linux-android
```

的确就这样就可以了。

继续编译，还是报错。

```
* What went wrong:
A problem occurred configuring project ':app'.
> executing external native build for cmake D:\work\gome\dcs-sdk-java-master\app\CMakeLists.txt
```

查看详细错误：

```
CMake Error: Could not create named generator Android Gradle - Ninja
```

网上看了相同的错误，解决的办法是sdk manager -- 右下角勾选show details。然后cmake安装3.6的，而不是默认的3.10的。同时把3.10的勾选去掉，这样就会卸载3.10的。

再试一下。

```
CMake Error at D:/android_sdk/ndk-bundle/build/cmake/android.toolchain.cmake:174 (message):
  armeabi is no longer supported.  Use armeabi-v7a.
Call Stack (most recent call first):
  D:/android_sdk/cmake/3.6.4111459/share/cmake-3.6/Modules/CMakeDetermineSystem.cmake:98 (include)
  CMakeLists.txt


CMake Error: CMAKE_C_COMPILER not set, after EnableLanguage
CMake Error: CMAKE_CXX_COMPILER not set, after EnableLanguage
```

我直接修改app/build.gradle文件。去掉多余的架构。

```
ndk {
            // 平台
            abiFilters 'armeabi-v7a', 'arm64-v8a'
        }
```

再进行build。就成功了。

怎样进行在线调试呢？

edit Configuration。

但是module显示no module。这个怎么弄？

这个在线调试没有弄出来。但是可以安装apk到手机上用。

估计是这个的复杂结构导致无法在线调试？

我看其他的工程，不要设置默认就是可以调试的。



参考资料

1、

https://www.jianshu.com/p/16dde31679d3

2、epic 编译

这里找到了解决cmake错误的方法。

https://wufengxue.github.io/2019/02/25/epic.html