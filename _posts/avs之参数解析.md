---
title: avs之参数解析
date: 2018-11-21 11:17:19
tags:
	- avs
---





ConfigurationNode

全局只读配置对象。

树形结构键值对。

getRoot函数。

工具函数有：

getInt

getString。

这些工具函数都是对内部函数getValue的封装。

重载了[]操作符。

静态成员变量。

```
    static rapidjson::Document m_document;
    static ConfigurationNode m_root;
```



使用就是这样：

```
auto config = alexaClientSDK::avsCommon::utils::configuration::ConfigurationNode::getRoot();
```

```
config['xx']['yy']
```



