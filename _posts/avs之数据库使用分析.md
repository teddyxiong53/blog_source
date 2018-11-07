---
title: avs之数据库使用分析
date: 2018-11-06 14:18:27
tags:
	- avs

---



底层是sqlite3，看看是如何进行层层封装的。

SQLiteStatement

SQLiteDatabase

SQLiteMiscStorage

SQLiteUtils



SQLiteUtils这个是最底层的，直接封装了C语言函数。

操作的单位有2个，一个是db，一个是table。

对于db的操作有：

create、open、close、query。

对于table的操作有：

clear、drop。

里面的主要数据是sqlite3*指针类型。



然后是SQLiteStatement这个类。

SQLiteUtils也依赖了SQLiteStatement这个类。

主要数据结构是sqlite3_stmt。



misc这个数据库里，放的是发送的信息。

```
hlxiong@hlxiong-VirtualBox:~/work/avs/sdk-folder/application-necessities$ sqlite3 miscDatabase.db 
SQLite version 3.11.0 2016-02-15 17:29:24
Enter ".help" for usage hints.
sqlite> .table
capabilitiesDelegate_capabilitiesPublishMessage
sqlite> select * from capabilitiesDelegate_capabilitiesPublishMessage
   ...> ;
endpoint:https://api.amazonalexa.com,clientId:|amzn1.application-oa2-client.4d9a98169f91409987a4e163ff9b93b1
endpoint:https://api.amazonalexa.com,productId:|ubuntu_avs
endpoint:https://api.amazonalexa.com,deviceSerialNumber:|123456
endpoint:https://api.amazonalexa.com,envelopeVersion:|20160207
endpoint:https://api.amazonalexa.com,publishMsg:|{"envelopeVersion":"20160207","capabilities":[{"type":"AlexaInterface","interface":"System","version":"1.1"},{"type":"AlexaInterface","interface":"Alerts","version":"1.3"},{"type":"AlexaInterface","interface":"AudioActivityTracker","version":"1.0"},{"type":"AlexaInterface","interface":"AudioPlayer","version":"1.0"},{"type":"AlexaInterface","interface":"PlaybackController","version":"1.1"},{"type":"AlexaInterface","interface":"Settings","version":"1.0"},{"type":"AlexaInterface","interface":"Speaker","version":"1.0"},{"type":"AlexaInterface","interface":"SpeechRecognizer","version":"2.0"},{"type":"AlexaInterface","interface":"InteractionModel","version":"1.0"},{"type":"AlexaInterface","interface":"Notifications","version":"1.0"},{"type":"AlexaInterface","interface":"SpeechSynthesizer","version":"1.0"}]}
sqlite> 
```

