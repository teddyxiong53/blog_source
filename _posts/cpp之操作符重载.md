---
title: cpp之操作符重载
date: 2018-11-22 17:23:19
tags:
	- cpp

---



看看一个简单的等于和不等于的重载。

```
bool DeviceInfo::operator==(const DeviceInfo& rhs) {
    if (getClientId() != rhs.getClientId()) {
        return false;
    }
    if (getProductId() != rhs.getProductId()) {
        return false;
    }
    if (getDeviceSerialNumber() != rhs.getDeviceSerialNumber()) {
        return false;
    }

    return true;
}

bool DeviceInfo::operator!=(const DeviceInfo& rhs) {
    return !(*this == rhs);
}
```

有这么几点是我之前没有认识到的。

1、不等于是对等于的调用。只是把结果取反一下而已。

2、要用对象来调用，所以this是一个指针，要进行指针取值操作。



