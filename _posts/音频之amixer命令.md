---
title: 音频之amixer命令
date: 2019-05-16 15:15:11
tags:
	- 音频

---



命令的基本格式：

```
amixer [options] [cmd]
```

选项：

```
-c, --card N
	指定声卡
-D, --device N
	选择设备，默认是default设备。
-d, --debug
	debug模式。
-n, --nocheck
	不要进行range检查。
-v, --version
	版本。
-q, --quiet
	不要打印。
-i, --inactive
	把不活跃的也显示出来。
-a, --abstract L
	选择抽象级别。none或者basic
-s, --stdin
	从stdin连续得到输入命令。
-R, --raw-volume
	使用raw value。默认就是的。
-M, --mapped-volume
	使用映射过的volume值。
	
```

命令：

```
scontrols
	显示所有的mixer简单控制项。
scontents
	显示mixer contents
sset id value
	作用类似tinymix set id value
sget id
controls
contents
cget id value
	c表示one control。
cget id
```



参考资料

1、

