---
title: nodejs之mocha
date: 2019-05-09 11:42:11
tags:
	- nodejs
---



写一个app.js，里面代码：

```
var assert = require('assert');
describe('Array', function() {
  describe('#indexOf()', function() {
    it('should return -1 when the value is not present', function() {
      assert.equal([1, 2, 3].indexOf(4), -1);
    });
  });
});
```

运行：

```
./node_modules/mocha/bin/mocha app.js
```

注意，不是用node来运行，而是用mocha来运行。



新建目录结构如下：

```
├── hello.js
├── node_modules
├── package.json
├── package-lock.json
└── test
		hello-test.js
```

hello.js内容：

```
module.exports = function(...rest) {
    var sum = 0
    for(var v of rest) {
        sum += v
    }
    return sum
}
```

hello-test.js内容：

```
const assert = require("assert")
const sum = require("../hello")

describe("#hello.js", ()=> {
    describe("#sum()", ()=> {
        it("sum() should return 0", function() {
            assert.strictEqual(sum(),0)
        })
        it("sum(1) should return 1", function() {
            assert.strictEqual(sum(1),1)
        })
    })
})

```

执行：

```
./node_modules/.bin/mocha test/hello-test.js
```

输出：

```


  #hello.js
    #sum()
      ✓ sum() should return 0
      ✓ sum(1) should return 1


  2 passing (6ms)
```





参考资料

1、

https://mochajs.org/

2、

https://www.liaoxuefeng.com/wiki/1022910821149312/1101756368943712