---
title: 使用github来进行编译
date: 2020-11-24 14:09:30
tags:
	- github
---

1

GitHub Ac­tions 

Github Ac­tions 是 Mi­crosoft 收购 GitHub 后推出的 CI/CD 服务，

它提供了性能配置非常不错的虚拟服务器环境（E5 2vCPU/7G RAM），

基于它可以进行构建、测试、打包、部署项目。

对于公开仓库可免费无时间限制的使用，且单次使用时间长达 6 个小时，

这对于编译 Open­Wrt 来说是非常充足的。

不过 GitHub Ac­tions 有一定的使用门槛，首先要了解如何编写 workflow 文件。



下面用openwrt的自动编译来做。

首先你必须要熟悉整个 Open­Wrt 的编译过程，

这会让你非常容易的理解如何使用 GitHub Ac­tions 进行编译，即使你没有成功过。

因为实际上本地编译近 90% 失败的原因是因为网络问题导致的，

中国大陆特色，咱也不敢多说。

GitHub Ac­tions 服务器由 Mi­crosoft Azure 提供，拥有万兆带宽，可以使编译成功率大大提升。





参考资料

1、

https://p3terx.com/archives/build-openwrt-with-github-actions.html