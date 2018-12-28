---
title: nodejs之protobuf
date: 2018-12-28 17:57:17
tags:
	- nodejs

---



在安装的node_modules目录下，有个readme，里面有详细说明。

网上很多的文章，都不对了。太老了。

写一个awesome.proto。

```
package awesomepackage;
syntax = "proto3";
message AwesomeMessage {
    string awesome_field = 1;
}
```







