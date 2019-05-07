---
title: js之Array
date: 2018-12-22 14:37:17
tags:
	- js
---



在node里，输入Array，加点，然后tab补全看提示。

得到这些：

```
Array.__defineGetter__
Array.__defineSetter__
Array.__lookupGetter__
Array.__lookupSetter__
Array.__proto__
Array.hasOwnProperty
Array.isPrototypeOf
Array.propertyIsEnumerable
Array.toLocaleString
Array.valueOf
Array.apply
Array.arguments
Array.bind
Array.call
Array.caller
Array.constructor
Array.toString
Array.from
	从一个字符串或者其他可迭代对象得到一个数组。
	var arr = Array.from("abc")
Array.isArray
	
Array.length
	表示构造函数可以接收的参数格式，是1 。
Array.name
	就是这个类的名字。
Array.of
	用参数来产生一个数组。
	Array.of(7)//得到数组[7]
	Array.of(1,2)//得到数组[1，2]
Array.prototype
```

然后定义一个Array实例，对这个实例tab补全，得到这些：

测试的arr是这样定义的：

```
> var arr = ['a', 'b', 'c']
```



```
arr.__defineGetter__
arr.__defineSetter__
arr.__lookupGetter__
arr.__lookupSetter__
arr.__proto__
arr.hasOwnProperty
arr.isPrototypeOf
arr.propertyIsEnumerable
arr.valueOf
arr.concat
	连接多个数组。
arr.constructor
arr.copyWithin
	数组内部浅拷贝，会改变数组内容。
arr.entries
	返回数组的iterator对象。可以用这个来遍历数组。
	> var it= arr.entries()
    undefined
    > it
    Object [Array Iterator] {}
    > it.next()
    { value: [ 0, 'a' ], done: false }
arr.every
	参数：一个函数。
	看看数组里的内容是否符合这个函数的条件。
	> arr.every(x => typeof x === 'string')
	true
arr.fill
	用指定值填充数组。
	> arr.fill(0)
	[ 0, 0, 0 ]
arr.filter
	> arr.filter(x => typeof x === 'string')
	[ 'a', 'b', 'c' ]
arr.find
	返回第一个满足调节的元素。
	> arr.find(x => typeof x === 'string')
	'a'
arr.findIndex
	跟上面类似，只是返回的是索引值。
	> arr.findIndex(x => typeof x === 'string')
	0
arr.forEach
	参数是一个函数。
	对数组的每个元素都执行一下函数。
	> arr.forEach(x=> console.log(x))
    a
    b
    c
arr.includes
	看数组里是否包含某个元素。
	> arr.includes('a')
	true
arr.indexOf
	> arr.indexOf('a')
	0
arr.join
	> arr2 = [1, 2, 3]
    [ 1, 2, 3 ]
    > arr.join(arr2)
    'a1,2,3b1,2,3c'
    这个拼接挺奇怪的。在a和b之间插入1,2，3.
    
arr.keys
	> var it = arr.keys()
    undefined
    > it.next()
    { value: 0, done: false }
    > it.next()
    { value: 1, done: false }
    > it.next()
    { value: 2, done: false }
    > it.next()
    { value: undefined, done: true }
arr.lastIndexOf
arr.map
	理解为映射，参数是一个函数，相当于映射函数。
	> arr.map(x => x+1)
	[ 'a1', 'b1', 'c1' ]
arr.pop
	> arr = ['a', 'b', 'c']
    [ 'a', 'b', 'c' ]
    > arr.pop()
    'c'
    > arr
    [ 'a', 'b' ]
arr.push
	> arr.push('c')
    3
    > arr
    [ 'a', 'b', 'c' ]
arr.reduce
	把数组元素进行累加。一般时候给数字的进行累加。
	> arr.reduce(x => x+1)
    'a11'
    > arr
    [ 'a', 'b', 'c' ]
arr.reduceRight
arr.reverse
	> arr.reverse()
	[ 'c', 'b', 'a' ]
arr.shift
	向左移位。
	> arr.shift()
    'a'
    > arr
    [ 'b', 'c' ]
arr.slice
	从索引位置开始切片。
	> arr.slice(1)
	[ 'b', 'c' ]
	> arr.slice(1,2)
	[ 'b' ]
arr.some
	至少有一个是符合条件的。
	> arr.some(x=> typeof x === 'string')
	true
arr.sort
	> arr.sort()
	[ 'a', 'b', 'c' ]
	指定比较规则：
	> arr.sort((a,b) => a < b)
	[ 'c', 'b', 'a' ]
arr.splice
	插入元素。
	参数1：位置。
	参数2：删除元素个数。
	参数3：插入元素。
	> arr.splice(1,0,'d')
    []
    > arr
    [ 'a', 'd', 'b', 'c' ]
arr.toLocaleString
arr.toString
arr.unshift
	向右移位，把最前面的位置腾出来。
	> arr.unshift('e')
    5
    > arr
    [ 'e', 'a', 'd', 'b', 'c' ]
arr.values
arr.length
	数组的长度。
```





参考资料

1、JavaScript Array 对象

http://www.runoob.com/jsref/jsref-obj-array.html

2、常用操作

https://developer.mozilla.org/zh-CN/docs/Web/JavaScript/Reference/Global_Objects/Array