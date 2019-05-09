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



参考资料

1、

https://mochajs.org/