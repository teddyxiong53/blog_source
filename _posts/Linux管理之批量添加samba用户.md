---
title: Linux管理之批量添加samba用户
date: 2017-07-25 23:29:13
tags:

	- Linux管理

---

基于服务器来做开发，需要把服务器的空间映射到windows下来进行一些操作。

几十个用户，所以选择批量添加的方式。

批量添加的一个问题在于，添加时需要两次输入密码，必须把这个行为自动化了。可以用expect工具来做。

借用前面的username.txt。

```
#!/bin/sh

cat username.txt | while read line
do 
	expect -c "
	spawn smbpasswd -a $line
	expect {
	\"New SMB password:\" {set timeout 300; send \"123456\r\";}
	\"Retype new SMB password:\" {send \"123456\r\"; exp_continue;}
	}
	expect eof"
done

```

