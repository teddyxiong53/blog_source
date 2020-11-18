---
title: golang之perkeep
date: 2020-11-16 14:41:17
tags:
	- go语言

---

1

编译：

```
go run make.go
```

在windows下正常编译通过。

生成的二进制文件在：C:\Users\Administrator\go\bin

```
devcam.exe
genfileembed.exe
hello.exe
perkeepd.exe
pk-deploy.exe
pk-get.exe
pk-put.exe
pk.exe
publisher.exe
scancab.exe
scanningcabinet.exe
```

从pk.exe入手。

```
pk.exe env
```

会提示我需要

```
pk put init --newkey
```

这样就在生成了C:\Users\Administrator\AppData\Roaming\Perkeep\client-config.json文件。

```
{
  "servers": {
    "localhost": {
      "server": "http://localhost:3179",
      "auth": "localhost",
      "default": true
    }
  },
  "identity": "B2D4D65D1A77F1A6",
  "ignoredFiles": [
    ".DS_Store"
  ]
}
```



目前看起来并不直观，没有找到本地测试的方法。

逻辑略复杂。不适合作为当前的学习材料。

先暂停。



参考资料

1、官网

https://perkeep.org/cmd/