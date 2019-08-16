---
title: nodejs之lodash
date: 2019-03-04 16:42:03
tags:
	- nodejs
---



看nodejs的底层库，看到很多都用到了lodash这个库。

这个库是做什么的呢？

lodash是一个js的原生库。

不需要引入其他依赖。

设计目的是：提高开发者效率，提高原生方法的性能。

lodash用一个下划线来表示，就像jquery用$来表示一样。这样用起来非常简洁。

可以在浏览器里使用，也可以在nodejs里使用。

有多年开发经验的工程师，往往都有自己的一套工具库，称为utils、helpers等等。

这套库一方面是自己技术的积累，另一方面也是对某些技术的扩展，领先于技术规范的制定和实现。



lodash通过降低array、number、object、string这些的使用难度，从而让JavaScript变得简单易用。

lodash的模块化方法，非常适用于：

```
1、遍历array、object、string。
2、对值进行检测和操作。
3、创建符合功能的函数。
```



api分析

```
Array相关
	填充数据、查找元素、数组分片……
Collection相关
	
Date相关
Function相关
Language相关
Math相关
Number相关
Object相关
Seq相关
String相关
Util相关
Properties相关
Methods相关

lodash/fp
	提供了更加接近函数式编程的开发方法。
	
```





不过到了ES6之后，很多东西语言本身已经带了。



引入lodash的方法

前端：

```
<script src="https://cdn.jsdelivr.net/npm/lodash@4.17.10/lodash.min.js"></script>
```

nodejs：

```
var _ = require("lodash")
```



##N次循环

```
基础版本
for(var i=0; i<5; i++) {
    
}
使用Array的方法
Array.apply(null, Array(5)).forEach(function() {
    
})
使用lodash
_.times(5, function() {
    
})
```

我觉得这一条倒不能看出很大的优势。



```
数组相关
1、chunk
	对数组进行切分。
	var arr = [1,2,3,4]
	_.chunk(arr, 2)//得到的是[[1,2],[3,4]
	以2为单位进行切分。
2、compact
	去除无效值。空值、0，NaN。
	_.compact(['1','2', ' ', 0])
	得到的是['1','2']
3、uniq
	数组去重。
	_.uniq([1,1,2])
	得到的是[1,2]
4、filter和reject。
	过滤。参数是一个匿名函数。
	这个2个效果是相反的。
	_.filter([1,2], x => x=1)
	得到的是[1]
	_.reject([1,2], x => x=1)
	得到的是[2]
5、map
	数组遍历。
	_.map([1,2], x => x+1)
	得到的是[2,3]
6、merge 
	参数合并。
7、assignIn。
	类似参数对象合并。
	
8、concat。
	数组连接。
9、keys。
	取出对象的所有key值组成新的数组。

	
参考资料
https://www.jianshu.com/p/a64a6aa4cd95


lodash常用/最频繁使用的方法
https://blog.csdn.net/Embrace924/article/details/80757854
```

```
var arr = [1]
var other = _.concat(arr, 2, [3], [[4]])
console.log(other)
输出：
[ 1, 2, 3, [ 4 ] ]
```



可以被ES6语法取代的lodash功能有下面这些。

```
> [1,2,3].map(n=>n*2)
[ 2, 4, 6 ]
> [1,2,3].reduce((total,n)=>total+n)
6
> [1,2,3].filter(n=> n<=2)
[ 1, 2 ]
```

```
> const [head,...tail] = [1,2,3]
undefined
> head
1
> tail
[ 2, 3 ]
```



assign、extend、merge都是进行对象的合并的，区别何在？

先看看基本的使用。

从左往右进行合并。同名的就覆盖。

```
> _.assign({}, {a:1},{b:2})
{ a: 1, b: 2 }
```

assign会忽略原型链上的属性。

```
function Foo() {
    this.a = 1;
}
Foo.prototype.b = 2;//这个是会被忽略的。
var ret = _.assign({c:3}, new Foo())
console.log(ret)
```

结果：

```
{ c: 3, a: 1 }
```

在lodash 3.x版本的时候，extend是assign的别名。

在4.x版本的时候，extend是assignIn的别名。区别就是会把原型链上的属性也合并进来了。



merge跟assign也类似。

merge就是在某个属性为简单对象时，会进行属性合并，而不是覆盖。



after函数

在被调用N次后执行。

```
> var done = _.after(2, function() {console.log("call 2 times ok")})
undefined
> done()
undefined
> done()
call 2 times ok
undefined
```

ary函数

每个最多接收N个参数。

```
> _.map(['1','2','3'], _.ary(parseInt, 1))
[ 1, 2, 3 ]
```

before函数

跟after函数是一对。

表示最多调用多少次。后面的调用，就跟最后一次调用行为相同 。

在前端，用来限制一个按钮最多被按多少次。

下面这个例子，只打印了2次，后面的就不再打印了。

```
> var ret = _.before(3, function() {console.log("xx")})
undefined
> ret()
xx
undefined
> ret()
xx
undefined
> ret()
undefined
```

at函数

从指定位置取出元素，返回一个数组。

```
> var obj = {a:1, b:2, cc:{c0:3, c1:4}}
undefined
> obj
{ a: 1, b: 2, cc: { c0: 3, c1: 4 } }
> _.at(obj, 'cc.c0')
[ 3 ]
```



有接近300个函数。

```
> const _ = require("lodash")
undefined
> _
{ [Function: lodash]
  templateSettings:
   { escape: /<%-([\s\S]+?)%>/g,
     evaluate: /<%([\s\S]+?)%>/g,
     interpolate: /<%=([\s\S]+?)%>/g,
     variable: '',
     imports: { _: [Circular] } },
  after: [Function: after],
  ary: [Function: ary],
  assign: [Function],
  assignIn: [Function],
  assignInWith: [Function],
  assignWith: [Function],
  at: [Function],
  before: [Function: before],
  bind: { [Function] placeholder: [Circular] },
  bindAll: [Function],
  bindKey: { [Function] placeholder: [Circular] },
  castArray: [Function: castArray],
  chain: [Function: chain],
  chunk: [Function: chunk],
  compact: [Function: compact],
  concat: [Function: concat],
  cond: [Function: cond],
  conforms: [Function: conforms],
  constant: [Function: constant],
  countBy: [Function],
  create: [Function: create],
  curry: { [Function: curry] placeholder: [Circular] },
  curryRight: { [Function: curryRight] placeholder: [Circular] },
  debounce: [Function: debounce],
  defaults: [Function],
  defaultsDeep: [Function],
  defer: [Function],
  delay: [Function],
  difference: [Function],
  differenceBy: [Function],
  differenceWith: [Function],
  drop: [Function: drop],
  dropRight: [Function: dropRight],
  dropRightWhile: [Function: dropRightWhile],
  dropWhile: [Function: dropWhile],
  fill: [Function: fill],
  filter: [Function: filter],
  flatMap: [Function: flatMap],
  flatMapDeep: [Function: flatMapDeep],
  flatMapDepth: [Function: flatMapDepth],
  flatten: [Function: flatten],
  flattenDeep: [Function: flattenDeep],
  flattenDepth: [Function: flattenDepth],
  flip: [Function: flip],
  flow: [Function],
  flowRight: [Function],
  fromPairs: [Function: fromPairs],
  functions: [Function: functions],
  functionsIn: [Function: functionsIn],
  groupBy: [Function],
  initial: [Function: initial],
  intersection: [Function],
  intersectionBy: [Function],
  intersectionWith: [Function],
  invert: [Function],
  invertBy: [Function],
  invokeMap: [Function],
  iteratee: [Function: iteratee],
  keyBy: [Function],
  keys: [Function: keys],
  keysIn: [Function: keysIn],
  map: [Function: map],
  mapKeys: [Function: mapKeys],
  mapValues: [Function: mapValues],
  matches: [Function: matches],
  matchesProperty: [Function: matchesProperty],
  memoize: { [Function: memoize] Cache: [Function: MapCache] },
  merge: [Function],
  mergeWith: [Function],
  method: [Function],
  methodOf: [Function],
  mixin: [Function: mixin],
  negate: [Function: negate],
  nthArg: [Function: nthArg],
  omit: [Function],
  omitBy: [Function: omitBy],
  once: [Function: once],
  orderBy: [Function: orderBy],
  over: [Function],
  overArgs: [Function],
  overEvery: [Function],
  overSome: [Function],
  partial: { [Function] placeholder: [Circular] },
  partialRight: { [Function] placeholder: [Circular] },
  partition: [Function],
  pick: [Function],
  pickBy: [Function: pickBy],
  property: [Function: property],
  propertyOf: [Function: propertyOf],
  pull: [Function],
  pullAll: [Function: pullAll],
  pullAllBy: [Function: pullAllBy],
  pullAllWith: [Function: pullAllWith],
  pullAt: [Function],
  range: [Function],
  rangeRight: [Function],
  rearg: [Function],
  reject: [Function: reject],
  remove: [Function: remove],
  rest: [Function: rest],
  reverse: [Function: reverse],
  sampleSize: [Function: sampleSize],
  set: [Function: set],
  setWith: [Function: setWith],
  shuffle: [Function: shuffle],
  slice: [Function: slice],
  sortBy: [Function],
  sortedUniq: [Function: sortedUniq],
  sortedUniqBy: [Function: sortedUniqBy],
  split: [Function: split],
  spread: [Function: spread],
  tail: [Function: tail],
  take: [Function: take],
  takeRight: [Function: takeRight],
  takeRightWhile: [Function: takeRightWhile],
  takeWhile: [Function: takeWhile],
  tap: [Function: tap],
  throttle: [Function: throttle],
  thru: [Function: thru],
  toArray: [Function: toArray],
  toPairs: [Function],
  toPairsIn: [Function],
  toPath: [Function: toPath],
  toPlainObject: [Function: toPlainObject],
  transform: [Function: transform],
  unary: [Function: unary],
  union: [Function],
  unionBy: [Function],
  unionWith: [Function],
  uniq: [Function: uniq],
  uniqBy: [Function: uniqBy],
  uniqWith: [Function: uniqWith],
  unset: [Function: unset],
  unzip: [Function: unzip],
  unzipWith: [Function: unzipWith],
  update: [Function: update],
  updateWith: [Function: updateWith],
  values: [Function: values],
  valuesIn: [Function: valuesIn],
  without: [Function],
  words: [Function: words],
  wrap: [Function: wrap],
  xor: [Function],
  xorBy: [Function],
  xorWith: [Function],
  zip: [Function],
  zipObject: [Function: zipObject],
  zipObjectDeep: [Function: zipObjectDeep],
  zipWith: [Function],
  entries: [Function],
  entriesIn: [Function],
  extend: [Function],
  extendWith: [Function],
  add: [Function],
  attempt: [Function],
  camelCase: [Function],
  capitalize: [Function: capitalize],
  ceil: [Function],
  clamp: [Function: clamp],
  clone: [Function: clone],
  cloneDeep: [Function: cloneDeep],
  cloneDeepWith: [Function: cloneDeepWith],
  cloneWith: [Function: cloneWith],
  conformsTo: [Function: conformsTo],
  deburr: [Function: deburr],
  defaultTo: [Function: defaultTo],
  divide: [Function],
  endsWith: [Function: endsWith],
  eq: [Function: eq],
  escape: [Function: escape],
  escapeRegExp: [Function: escapeRegExp],
  every: [Function: every],
  find: [Function],
  findIndex: [Function: findIndex],
  findKey: [Function: findKey],
  findLast: [Function],
  findLastIndex: [Function: findLastIndex],
  findLastKey: [Function: findLastKey],
  floor: [Function],
  forEach: [Function: forEach],
  forEachRight: [Function: forEachRight],
  forIn: [Function: forIn],
  forInRight: [Function: forInRight],
  forOwn: [Function: forOwn],
  forOwnRight: [Function: forOwnRight],
  get: [Function: get],
  gt: [Function],
  gte: [Function],
  has: [Function: has],
  hasIn: [Function: hasIn],
  head: [Function: head],
  identity: [Function: identity],
  includes: [Function: includes],
  indexOf: [Function: indexOf],
  inRange: [Function: inRange],
  invoke: [Function],
  isArguments: [Function: baseIsArguments],
  isArray: [Function: isArray],
  isArrayBuffer: [Function],
  isArrayLike: [Function: isArrayLike],
  isArrayLikeObject: [Function: isArrayLikeObject],
  isBoolean: [Function: isBoolean],
  isBuffer: [Function: isBuffer],
  isDate: [Function],
  isElement: [Function: isElement],
  isEmpty: [Function: isEmpty],
  isEqual: [Function: isEqual],
  isEqualWith: [Function: isEqualWith],
  isError: [Function: isError],
  isFinite: [Function: isFinite],
  isFunction: [Function: isFunction],
  isInteger: [Function: isInteger],
  isLength: [Function: isLength],
  isMap: [Function],
  isMatch: [Function: isMatch],
  isMatchWith: [Function: isMatchWith],
  isNaN: [Function: isNaN],
  isNative: [Function: isNative],
  isNil: [Function: isNil],
  isNull: [Function: isNull],
  isNumber: [Function: isNumber],
  isObject: [Function: isObject],
  isObjectLike: [Function: isObjectLike],
  isPlainObject: [Function: isPlainObject],
  isRegExp: [Function],
  isSafeInteger: [Function: isSafeInteger],
  isSet: [Function],
  isString: [Function: isString],
  isSymbol: [Function: isSymbol],
  isTypedArray: [Function],
  isUndefined: [Function: isUndefined],
  isWeakMap: [Function: isWeakMap],
  isWeakSet: [Function: isWeakSet],
  join: [Function: join],
  kebabCase: [Function],
  last: [Function: last],
  lastIndexOf: [Function: lastIndexOf],
  lowerCase: [Function],
  lowerFirst: [Function],
  lt: [Function],
  lte: [Function],
  max: [Function: max],
  maxBy: [Function: maxBy],
  mean: [Function: mean],
  meanBy: [Function: meanBy],
  min: [Function: min],
  minBy: [Function: minBy],
  stubArray: [Function: stubArray],
  stubFalse: [Function: stubFalse],
  stubObject: [Function: stubObject],
  stubString: [Function: stubString],
  stubTrue: [Function: stubTrue],
  multiply: [Function],
  nth: [Function: nth],
  noConflict: [Function: noConflict],
  noop: [Function: noop],
  now: [Function],
  pad: [Function: pad],
  padEnd: [Function: padEnd],
  padStart: [Function: padStart],
  parseInt: [Function: parseInt],
  random: [Function: random],
  reduce: [Function: reduce],
  reduceRight: [Function: reduceRight],
  repeat: [Function: repeat],
  replace: [Function: replace],
  result: [Function: result],
  round: [Function],
  runInContext: [Function: runInContext],
  sample: [Function: sample],
  size: [Function: size],
  snakeCase: [Function],
  some: [Function: some],
  sortedIndex: [Function: sortedIndex],
  sortedIndexBy: [Function: sortedIndexBy],
  sortedIndexOf: [Function: sortedIndexOf],
  sortedLastIndex: [Function: sortedLastIndex],
  sortedLastIndexBy: [Function: sortedLastIndexBy],
  sortedLastIndexOf: [Function: sortedLastIndexOf],
  startCase: [Function],
  startsWith: [Function: startsWith],
  subtract: [Function],
  sum: [Function: sum],
  sumBy: [Function: sumBy],
  template: [Function: template],
  times: [Function: times],
  toFinite: [Function: toFinite],
  toInteger: [Function: toInteger],
  toLength: [Function: toLength],
  toLower: [Function: toLower],
  toNumber: [Function: toNumber],
  toSafeInteger: [Function: toSafeInteger],
  toString: [Function: toString],
  toUpper: [Function: toUpper],
  trim: [Function: trim],
  trimEnd: [Function: trimEnd],
  trimStart: [Function: trimStart],
  truncate: [Function: truncate],
  unescape: [Function: unescape],
  uniqueId: [Function: uniqueId],
  upperCase: [Function],
  upperFirst: [Function],
  each: [Function: forEach],
  eachRight: [Function: forEachRight],
  first: [Function: head],
  VERSION: '4.17.11',
  _: [Circular] }
```



参考资料

1、lodash入门

https://www.jianshu.com/p/d46abfa4ddc9

2、

https://www.zhihu.com/topic/20029773/hot

3、可以使用ES6取代的10个Lodash特性

https://www.w3cplus.com/javascript/lodash-features-replace-es6.html

4、

https://www.lodashjs.com/

5、Lodash学习笔记

https://www.cnblogs.com/webbest/p/8268115.html

6、学习lodash——这一篇就够用

https://blog.csdn.net/qq_35414779/article/details/79077618

7、Lodash 中 assign，extend 和 merge 的区别

https://scarletsky.github.io/2016/04/02/assign-vs-extend-vs-merge-in-lodash/

