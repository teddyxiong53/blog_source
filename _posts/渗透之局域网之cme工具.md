---
title: 渗透之局域网之cme工具
date: 2020-09-28 11:42:30
tags:
	- 渗透

---

1

CrackMapExec是一个后渗透工具。简称CME。它的slogo是是渗透网络的瑞士军刀。

用来自动测试一个Active Directory网络的安全性。

CME使用了Impacket库和PowerSploit Toolkit。

用来处理网络协议和执行一些后渗透操作。

尽管主要是被设计用来做防御用途的。

CME也可以被蓝队使用来进行攻击。

```
#~ python3 -m pip install pipx
#~ pipx ensurepath
#~ pipx install crackmapexec
```

探测目标smb

```
cme smb 172.16.2.3
```

得到的信息如下：

```
SMB         172.16.2.3      445    LOCALHOST        [*] Windows 6.1 (name:LOCALHOST) (domain:) (signing:False) (SMBv1:True)
```

可以暴力破解对应的密码。

```
cme smb 172.16.2.3 -u ./user.txt -p ./password.txt
```



# smb协议

## 枚举网络内的所有smb服务器

```
cme smb 172.16.2.0/23
```

这样还可以得到机器的os信息。

但是并不准确，例如扫描到我的Linux笔记本，看到的却是windows系统。



## 枚举空session

```
cme smb 172.16.2.241 -u '' -p ''
cme smb 172.16.2.241 -u '' -p '' --pass-pol
```

## 枚举匿名登陆

```
cme smb 172.16.2.241 -u 'a' -p ''
```

就是随便给一个用户，密码留空，就可以检测对方是否允许匿名登陆。

## 枚举share

```
cme smb 172.16.2.241 -u 'hlxiong' -p '123' --shares
```





参考资料

1、

https://mpgn.gitbook.io/crackmapexec/smb-protocol/enumeration/untitled