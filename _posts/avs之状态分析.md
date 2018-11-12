---
title: avs之状态分析
date: 2018-11-10 14:43:19
tags:
	- avs
---



dialog ux 聚合器是变化的分发者。变化的来源是哪里？

audio input注册称为dialog ux的观察者。

dialog ux靠notifyObserversOfState这个函数来通知观察自己的人。这个函数被自己的setState函数调用。

set state在什么时候会触发呢？

我看dialog ux自己也是一个观察者，观察了网络状态的变化，可谓是螳螂捕蝉黄雀在后。

网络变化的来源，就是来自于ping了。有变化就通知观察者。

dialog ux和audio input是相互观察。

dialog ux观察了audio input的状态变化。







