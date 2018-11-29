---
title: esp8266之SmartConfig
date: 2018-11-29 14:57:28
tags:
	- esp8266
typora-root-url: ..\
---



搜索一下esp8266目录下的SmartConfig，

```
Administrator@doss MINGW64 /d/work/study/esp8266/2.4.2
$ grep -nwr "beginSmartConfig" .
./libraries/ESP8266WiFi/keywords.txt:108:beginSmartConfig       KEYWORD2
./libraries/ESP8266WiFi/src/ESP8266WiFiSTA.cpp:664:bool ESP8266WiFiSTAClass::beginSmartConfig() {
./libraries/ESP8266WiFi/src/ESP8266WiFiSTA.h:104:        bool beginSmartConfig();

```



需要手机app来配和。

app的代码在这里。

https://github.com/EspressifApp/EsptouchForAndroid

现在安装一个Android studio环境来生成apk。

Android Studio下载大概1个G。

发现有现成的apk文件，直接安装看看。

用Arduino的IDE 写一个smart_config.ino文件。内容如下：

```
#include <ESP8266WiFi.h>;

void setup() {
  Serial.begin(115200);
  delay(10);

  // 必须采用 AP 与 Station 兼容模式
  WiFi.mode(WIFI_AP_STA);
  delay(500);


 // 等待配网
  WiFi.beginSmartConfig();

 // 收到配网信息后ESP8266将自动连接，WiFi.status 状态就会返回：已连接
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
    // 完成连接，退出配网等待。
    Serial.println(WiFi.smartConfigDone());
  }

  Serial.println("");
  Serial.println("WiFi connected");  
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

int value = 0;

void loop() {
}
```

但是配网不成功。





参考资料

1、

https://www.jianshu.com/p/db9dffa96470

