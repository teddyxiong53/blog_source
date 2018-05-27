---
title: Android之SharedPreferences
date: 2018-05-27 17:58:43
tags:
	-Android

---



SharedPreferences在android中主要以xml文件的方式保存较小的键值对。

可以保存的数值类型有：

```
 - String
 - Float
 - Boolean
 - Int
 - Long
 - StringSet  Set集合，泛型为String
```

SharedPreferences以xml的形式保存在 data/data/包名/shared_prefs 这个目录下。

一个例子。

```
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <string name="name">nick</string>
    <int name="age" value="18" />
    <float name="high" value="1.8" />
    <boolean name="isBoy" value="true" />
    <long name="ID" value="123456789999999" />
    <set name="setString">
        <string>1</string>
        <string>2</string>
        <string>3</string>
        <string>4</string>
    </set>
</map>
```



# 参考资料

1、SharedPreferences的用法及指南

https://blog.csdn.net/IT_XF/article/details/54356993