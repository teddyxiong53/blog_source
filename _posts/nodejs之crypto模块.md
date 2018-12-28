---
title: nodejs之crypto模块
date: 2018-12-28 11:55:17
tags:
	- nodejs
---



```
const crypto = require("crypto");
function sha256(value) {
    let shasum = crypto.createHash("sha256");
    shasum.update(value);
    return shasum.digest('hex');
}
console.log(sha256("12"));
console.log(sha256("34"));
```

