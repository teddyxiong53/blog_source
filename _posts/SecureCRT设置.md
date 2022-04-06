---
title: SecureCRT设置
date: 2018-01-24 09:11:53
tags:
	- SecureCRT

---



# 设置终端色彩

我习惯石青色的背景色。

Emulation选择VT100，勾选ANSI Color和use color scheme。

ansi color不选的话，make menuconfig就会混乱。

# 设置log格式

```
d:\securecrt_log\[%S]-%M-%D-[%h-%m-%s].log
在on each line上，设置
[%h:%m:%s:%t]
```

# 直接发送文件

可以直接把文件拖放到securecrt的窗口里进行发送。

是使用zmodem等进行的。

安装zmodem文件：

```
apt-get install lrzsz
```

# 自动化脚本



参考资料

1、利用SecureCrt实现自动化脚本

https://www.pianshen.com/article/766445705/