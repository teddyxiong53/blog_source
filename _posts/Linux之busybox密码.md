---
title: Linux之busybox密码
date: 2018-07-25 10:10:28
tags:
	- Linux

---



shadow采用DES加密方式，破解方式为暴力破解，可以采用字典攻击：



能够改成SHA256的吗？

要用到SHA256或者SHA512的密码加密，glic版本需大于2.7。

密文格式：

```
$id$salt$encrypted
```

id表示加密方式：

1：md5

2：blowfish

5：sha256

6：sha512

我的电脑上的是sha512的。

```
hlxiong:$6$mVGZZSS/$h0NBgyePsyfIqFihAEvXwbllDPlBzWdI.qH4vkOYVvTKgpzvg/6fqRP.66.xcmYDWv3C.2EENZcVoH7OxDjq61:17662:0:99999:7:::
vboxadd:!:17662::::::
sshd:*:17662:0:99999:7:::
git:$6$cBmnuYnh$MyT6fFx0bqy9/Hlym/fOWYITUZ8zzTWwlFSZ0FSWjN8OFbkPmjF4I3x8twaqh23j6OD42d.kTSUMO2LZyrfUQ0:17662:0:99999:7:::
```



# 参考资料

1、linux口令相关（passwd/shadow）及破解方式

https://blog.csdn.net/qc20042/article/details/5638645

2、关于Linux系统中的密码加密流程及原理 

http://blog.sina.com.cn/s/blog_4d1f40c00101cvd8.html

3、如何在 Linux 中产生、加密或解密随机密码

https://linux.cn/article-5486-1.html

