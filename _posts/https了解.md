---
title: https了解
date: 2018-07-30 22:33:00
tags:
	- 网络

---



https在日常工作生活中经常看到，但是却没有仔细去了解过。

现在配置nginx，就碰到https的配置了。所以务必要进行学习了。



什么是https证书？

我们可以快速过一下http的发展过程。

1、最早的http，是没有加密的。所以黑客通过抓包，就可以轻易获取你的通信内容。

2、然后就出现了对称加密。对称，就是加密和解密的秘钥是一样的。这个还是不安全，因为一旦黑客也拿到了秘钥，你的信息还是会很容易被获取到。

3、然后就出现了非对称加密。非对称，就是加密和解密的秘钥是不同两把。加密的，是公钥，是公开的，每个人都可以拿到。解密的私钥，只有网站服务端有。

4、但是，非对称加密，还是有漏洞的，黑客可以做一个钓鱼网站。来骗取你的重要信息。

5、怎么解决这个问题？所以就出现了证书这个东西。就类似营业执照一样。特点就是难以伪造。伪造一个公司容易，伪造一个政府就很难了。

具体怎么操作？

先是由国家权威机构生成一个“国家权威非对称加密”。其中公钥部分以根证书的形式，颁发给每一个互联网用户。

这样就保证了每个人都可以解密来自国家权威机构的加密信息。

然后，网站负责人向国家提交各种材料，申请一个SSL证书。这个证书要国家用那个根证书对应的私钥来生成。

有很多机构都可以颁发根证书。上面提的国家只是一个例子。



A公司的张三要到B公司去拜访，但是B公司没有人认识A。怎么办呢？A公司给张三开了一张介绍信，信中说：兹有张三先生前往贵公司办理业务，请给予接洽。然后在信上改上A公司的公章。

B公司的前台李四小姐，看到介绍信上有A公司的公章，而A和B公司业务往来比较多，李小姐就相信张先生不是歹人。

在上面的描述里，A公司就是CA证书。

假如跟B公司有业务往来的公司很多，每个公司的公章都不同，那么前台就得学会认识各种不同的公章，这个就很麻烦。所以，有人从这里发现了商机，开了一家C公司。专门开展“代理公章”业务。

这样，A公司的张三去B公司，就要带两张介绍信：

介绍信1、含有C公司的公章和A公司的公章，并且特别注明，C公司信任A公司。

介绍信2、只有A公司的公章。

这样，前台只需要记住C公司的公章就好了。认公章的事情，就让C公司来专门完成这个烦人的事情。



http不安全的根源是http是明文传输的。

你在谷歌搜索了一个关键词（假如谷歌使用的是http），在中间的任何一个节点上都可以抓取到你搜索的内容，你的隐私毫无保障。



# 从零开始搭建https网站

证书跟域名一样，也需要购买，而且价格不便宜。

我们用免费的letsencrypt。

```
git clone https://github.com/letsencrypt/letsencrypt
```

我们使用letsencrypt来生成https所需要的整数。

作为一个免费的解决方案，letsencrypt只提供域名认证证书。

所以，我们只需要证明域名是自己所有即可。

最简单的方式是用letsencrypt的webroot验证方式。

告诉letsencrypt你的nginx的WebRoot和你的域名。

letsencrypt会在WebRoot的.well-known文件夹下放一个特别的文件。

然后使用域名去访问这个文件，如果可以访问到，当然能够证明域名是你的。



# 有哪些CA机构

世界上较早的数字认证中心是美国的verisign公司。

还有加拿大的entrust公司。

中国的安全认证体系分为金融CA和非金融CA 。

金融CA，由中国人民银行管理。

非金融CA，由中国电信负责。

中国CA又可以分为行业性CA和区域性CA。



阿里云提供了CA证书申请的渠道。

https://www.aliyun.com/product/cas?spm=5176.8142029.388261.284.42016d3eKFx8od

一个CA证书，一年需要1700元，比域名还贵。



不过，有个好消息，为了推广https。电子前哨站基金会提供了免费的CA证书。

https://letsencrypt.org/





# 自签名证书的生成和安装

有时候，我们在内部系统传输数据要用ssl协议，但是我们又不想花钱去申请CA。

这个时候，我们就可以用自签名CA。

首先要说明的是，自签名CA是不安全的。





# 申请免费证书

certbot就是一个命令行工具，用来帮我们从let's encrypt这个网站申请免费的https证书。

```
certbot-auto certonly --manual \
-d *.only4u.tech \
-d only4u.tech --agree-tos \
--manual-public-ip-logging-ok --preferred-challenges \
dns-01 --server https://acme-v02.api.letsencrypt.org/directory
```



# 参考资料

1、Nginx配置ssl证书(中间证书)

https://blog.csdn.net/gudufeiyang/article/details/58603402

2、什么是HTTPS？为什么要购买证书？

https://blog.csdn.net/fangqun663775/article/details/55189107

3、CA证书扫盲，https讲解

https://www.cnblogs.com/handsomeBoys/p/6556336.html

4、使用CA自签名证书搭建HTTPS网站

https://blog.csdn.net/shion0305/article/details/73776449

5、CA证书

https://blog.csdn.net/yangyuge1987/article/details/79209473

6、openssl ca(签署和自建CA)

https://www.cnblogs.com/f-ck-need-u/p/7115871.html

7、从零开始搭建一个HTTPS网站

https://blog.csdn.net/rickiyeat/article/details/53783605