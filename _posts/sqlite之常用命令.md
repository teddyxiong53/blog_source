---
title: sqlite之常用命令
date: 2018-02-06 15:33:56
tags:
	- sqlite

---



sqlite数据库小巧方便，是很不错的嵌入式数据库。大量地在手机、机顶盒等设备里使用。

1、输入sqlite3，进入到sqlite的命令行里。

2、sqlite的命令都是以点号开头的。

3、

.open packages.dbsqlite

.databases 查看当前的数据库。

```
sqlite> .databases
seq  name             file
---  ---------------  ----------------------------------------------------------
0    main             Z:\work\rt-thread\rt-thread\bsp\qemu-vexpress-a9\packages\
```

.tables 查看表。

```
sqlite> .tables
packagefile
```

查看表里的内容。

```
sqlite> select * from packagefile;
partition-1.0.1/.gitignore|partition-1.0.1.zip|97a40190cf692d26a40878c675a54049
partition-1.0.1/LICENSE|partition-1.0.1.zip|fc178bcd425090939a8b634d1d6a9594
partition-1.0.1/README.md|partition-1.0.1.zip|15ab31b21f2a6aa58ff70f328acdec4e
partition-1.0.1/SConscript|partition-1.0.1.zip|58ff6f5882bde0d3a7efecd73b8bf5c1
partition-1.0.1/partition.c|partition-1.0.1.zip|104ed3303230f073ae95d6d74afc5843
partition-1.0.1/partition.h|partition-1.0.1.zip|d3f6d672839a74498f9267f2a5d74181
iperf-1.0.0/.gitignore|iperf-1.0.0.zip|97a40190cf692d26a40878c675a54049
iperf-1.0.0/LICENSE|iperf-1.0.0.zip|86d3f3a95c324c9479bd8986968f4327
iperf-1.0.0/README.md|iperf-1.0.0.zip|2a039ed47ec9d4ee485dbc488cfc73c9
iperf-1.0.0/SConscript|iperf-1.0.0.zip|1347f8b891714f0e29a554ed8b2e6d56
iperf-1.0.0/iperf.c|iperf-1.0.0.zip|6042db7efca2015f5f6db273fa7c8335
hello-1.0.0/.gitignore|hello-1.0.0.zip|97a40190cf692d26a40878c675a54049
hello-1.0.0/LICENSE|hello-1.0.0.zip|fc178bcd425090939a8b634d1d6a9594
hello-1.0.0/README.md|hello-1.0.0.zip|c2fca9b093b74af94f85ee41ff898352
hello-1.0.0/SConscript|hello-1.0.0.zip|03efbc258f97886ce38ec6b9f8823b5c
hello-1.0.0/hello.c|hello-1.0.0.zip|2bba3479923b75e22a6ac8b50b1db229
```

执行sql脚本，生成数据库。

```
sqlite3.exe -init schema.sql flaskr.sqlite3
```

