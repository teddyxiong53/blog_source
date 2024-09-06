---
title: filebrowser快速搭建文件服务器
date: 2024-09-06 13:50:17
tags:
	- server

---

--

需要把服务器的一个目录快速共享给其他人进行编辑。

到这里下载

https://github.com/filebrowser/filebrowser

添加一个用户：

```
./filebrowser users add teddy 123456
```

启动

```
nohup ./filebrowser -a 0.0.0.0  -p 2496 -r /home/teddy/work
```

