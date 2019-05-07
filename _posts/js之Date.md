---
title: js之Date
date: 2019-05-07 10:25:25
tags:
	- js
---



Date基于unix时间戳，是从1970年开始的毫秒数。



在node里，对Date加点后，按两下tab键进行补全。看到这些提示。

```
Date.__defineGetter__
Date.__defineSetter__
Date.__lookupGetter__
Date.__lookupSetter__
Date.__proto__
Date.hasOwnProperty
Date.isPrototypeOf
Date.propertyIsEnumerable
Date.toLocaleString
Date.valueOf
Date.apply
Date.arguments
Date.bind
Date.call
Date.caller
Date.constructor
Date.toString
Date.UTC
	Date.UTC(year,month,day,hours,minutes,seconds,ms)
	举例：
	> Date.UTC(2000,1,1,1,1,1,1)
	949366861001
	
Date.length
	值固定为7 ，表示构造函数可以接收的参数的个数。
Date.name
	就是字符串'Date'
Date.now
	返回1970年以来的毫秒数。
Date.parse
	var unixTimeZero = Date.parse('01 Jan 1970 00:00:00 GMT');
	返回的是毫秒数。
Date.prototype
```

定义一个Date实例。进行补全。得到这些：

```
d.__defineGetter__
d.__defineSetter__
d.__lookupGetter__
d.__lookupSetter__
d.__proto__
d.hasOwnProperty
d.isPrototypeOf
d.propertyIsEnumerable
d.constructor
d.getDate
	是本月的几号。
d.getDay
	是周几。
d.getFullYear
	2019这种格式。
d.getHours
	10点就是10 。
d.getMilliseconds
	338这样。
d.getMinutes
	24这样。
d.getMonth
	5月份是输出4 。
d.getSeconds
	
d.getTime
	毫秒数。
d.getTimezoneOffset
	返回的是格林威治时间跟本地时间的分钟差。北京时间是-480，表示格林威治时间比北京时间慢480分钟。
d.getUTCDate
	
d.getUTCDay
d.getUTCFullYear
d.getUTCHours
d.getUTCMilliseconds
d.getUTCMinutes
d.getUTCMonth
d.getUTCSeconds
	这些，跟不带UTC的好像没有差别。
d.getYear
	2019年是输出119 。
d.setDate
	
d.setFullYear
d.setHours
d.setMilliseconds
d.setMinutes
d.setMonth
d.setSeconds
d.setTime
d.setUTCDate
d.setUTCFullYear
d.setUTCHours
d.setUTCMilliseconds
d.setUTCMinutes
d.setUTCMonth
d.setUTCSeconds
d.setYear
d.toDateString
	'Tue May 07 2019'
d.toGMTString
	'Tue, 07 May 2019 02:24:24 GMT'
d.toISOString
	'2019-05-07T02:24:24.338Z'
d.toJSON
	'2019-05-07T02:24:24.338Z'
d.toLocaleDateString
	'2019-5-7'
d.toLocaleString
	'2019-5-7 10:24:24'
d.toLocaleTimeString
	'10:24:24'
d.toString
d.toTimeString
	'10:24:24 GMT+0800 (GMT+08:00)'
d.toUTCString
d.valueOf
```



参考资料

1、

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Date