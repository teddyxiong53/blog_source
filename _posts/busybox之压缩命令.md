---
title: busybox之压缩命令
date: 2018-08-06 15:36:38
tags:
	- busybox

---



需要定期把板端的文件压缩上传。



bzip

压缩比较慢。

```
 bzip2 -z f1.txt f2.txt
```

这样，会直接把原文件删掉的。

-k 保留原文件



busybox里的tar不能用来压缩。



xz





```
tar -zcvf - pma|openssl des3 -salt -k password | dd of=pma.des3
```



最后的方法：

```
加密过程：
bzip2 -k dcssdk.log 
openssl des3 -salt -k 1234 -in dcssdk.log.bz2 -out dcssdk.log.des3
解密过程：
openssl des3 -d -k 1234 -in dcssdk.log.des3 -out dcssdk.log.bz2
bzip2 -k -d dcssdk.log.bz2
```



# 参考资料

http://man.linuxde.net/bzip2

在Linux下打包tar文件时添加密码的方法

https://www.aliyun.com/jiaocheng/174859.html