---
title: js之字符串函数
date: 2019-05-06 16:51:25
tags:
	- js
---





js的字符串函数有哪些？

大概有50个。

这个是在node的repl，定义一个var str = "aaa"，然后用tab 2次，提示出来的内容。

有用的函数：

```
charAt(index)
charCodeAt(index)
	这个是返回对应的Unicode值。
codePointAt
	好像作用跟charCodeAt差不多。
concat
	连接字符串。
endsWith
	看是否以某个字符串结尾。检查后缀时比较有用。
indexOf
	查找子字符串。
lastIndexOf
	最后一个匹配的子字符串。
length
	这个是属性，不是函数。
localeCompare
	相同返回0 。
match
	正则匹配。
repeat
	就是重复几次。
replace
	替换一部分字符串。可以用正则。
search
	返回的是子串的index位置。没找到返回-1 。
slice
	2个参数，start、end。表示截取一部分字符串。
split
	用指定的符号进行分割，得到一个数组。
startsWith
	跟endsWith类型。
substr
	这个第二个参数是长度，而不是索引值。
substring
	跟slice一样。
toLowerCase
	转小写。
toString
toUpperCase
trim
	去掉头尾空格。
	有4个衍生函数。
	trimStart、trimEnd。
	trimLeft、trimRight。
valueOf
	没有参数，效果跟toString差不多。
	
```



```
> str.match('hello')
[ 'hello', index: 0, input: 'hello你好', groups: undefined ]
> str.match('hello你好')
[ 'hello你好', index: 0, input: 'hello你好', groups: undefined ]
> str.match('hello你好1')
```

```
> var str1 = " hello world"
undefined
> str1.split(" ")
[ '', 'hello', 'world' ]
```



```
str.__defineGetter__
str.__defineSetter__
str.__lookupGetter__
str.__lookupSetter__
str.__proto__
str.hasOwnProperty
str.isPrototypeOf
str.propertyIsEnumerable
str.toLocaleString
str.anchor 浏览器里有用，返回一个超链接。
str.big 浏览器。废弃。
str.blink 
str.bold
str.charAt
str.charCodeAt
str.codePointAt
str.concat
str.constructor
str.endsWith
str.fixed
str.fontcolor
str.fontsize
str.includes
str.indexOf
str.italics
str.lastIndexOf
str.length
str.link
str.localeCompare
str.match
str.normalize
str.padEnd
str.padStart
str.repeat
str.replace
str.search
str.slice
str.small
str.split
str.startsWith
str.strike
str.sub
str.substr
str.substring
str.sup
str.toLocaleLowerCase
str.toLocaleUpperCase
str.toLowerCase
str.toString
str.toUpperCase
str.trim
str.trimEnd
str.trimLeft
str.trimRight
str.trimStart
str.valueOf
```





参考资料

1、



