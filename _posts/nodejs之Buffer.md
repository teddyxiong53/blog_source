---
title: nodejs之Buffer
date: 2018-12-28 13:40:17
tags:
	- nodejs
---



```
var str1 = "abc";
console.log(Buffer.isBuffer(str1));
```

字符串不是Buffer。

看d.ts里是这么写判断的。

```
isBuffer(obj: any): obj is Buffer;
```



一个测试代码：

```
class MyClass {
    constructor() {
        this._buffers = Array.prototype.slice.call(arguments).filter(function(a) {
            return Buffer.isBuffer(a);
        });
    }
    add(buf) {
        if(Buffer.isBuffer(buf)) {
            this._buffers.push(buf);
        } else {
            this._buffers.push(Buffer.alloc(buf.length, buf));
        }
    }
    clear() {
        return this._buffers = [];
    }
    size() {
        return this._buffers.reduce(function(prev, curr) {
            return prev + curr.length;
        }, 0);
    }

    slice(start, length) {
        var all_len = this.size() - start;
        if(typeof length == "undefined") {
            length = all_len;
        } else {
            ;
        }
        var buf_len = Math.min(length, all_len);
        var buf = Buffer.alloc(buf_len);

    }
}

var c1 = new MyClass(Buffer.alloc(5,'a'));
c1.add("bbbbb");
c1.add(Buffer.alloc(5,'c'));
console.log(c1._buffers);
console.log(c1.size());
console.log(c1._buffers.length);

```

输出：

```
[ <Buffer 61 61 61 61 61>,
  <Buffer 62 62 62 62 62>,
  <Buffer 63 63 63 63 63> ]
15
3
```

