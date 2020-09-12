---
title: iflyos之evs自己实现js版本
date: 2020-09-10 14:29:17
tags:
	- js

---

1

默认版本，只能在树莓派上跑。

我简化一下，争取在笔记本上跑起来。

不要依赖c++部分的代码。

因为要用到ble，ble对node版本只支持到版本8的。用版本10的会编译失败。

所以用nvm切换到版本8的。

wifi的控制模块是这样：

```
module.exports = require('wpa_client').WpaClient
```

但是wpa_client是另外实现的。

```
./jsruntime/src/js/wpa_client.js
```

