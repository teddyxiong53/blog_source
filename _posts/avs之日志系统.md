---
title: avs之日志系统
date: 2018-09-25 10:58:17
tags:
	- 智能音箱

---



avs的日志系统写得很好，可以学习一下，移植到我自己的其他项目上去用。

层次关系是这样的：

1、每个cpp文件里，包含头文件。

```
#include <AVSCommon/Utils/Logger/Logger.h>
```

2、cpp文件里定义一个TAG。

```
static const std::string TAG("FocusManager");
```

3、cpp文件里定义LX宏。

```
#define LX(event) alexaClientSDK::avsCommon::utils::logger::LogEntry(TAG, event)
```

4、在调用的地方这样用：

```
ACSDK_ERROR(LX("createChannelFailed").d("reason", "channelNameExists").d("config", config.toString()));
```

展开后是：



日志级别是：

```
DEBUG9到DEBUG0，INFO, WARN, ERROR, CRITICAL, NONE, UNKNOWN
```



我采用移植到我的系统里的方式来学习。

1、先写Level.h。主要定义了枚举类Level。和一个<<的重载。

2、写LogEntry.h。这个还包含了一个简单的头文件LogEntryStream.h。LogEntryStream.h又包含了LogEntryBuffer.h文件。

3、写Logger.h。

总的来说，是借助了较复杂的宏拼接展开的技巧来实现的。







