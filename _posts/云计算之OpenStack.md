---
title: 云计算之OpenStack
date: 2018-07-13 21:16:00
tags:
	- 云计算

---



我们从这几个问题出发：

1、什么是OpenStack。

2、OpenStack可以做什么。

3、helloworld。



OpenStack是一套软件。总共的代码超过2000万行。超过585加企业，解决4万人在支持这个项目。

包括7大核心组件：

1、compute。计算。代号为Nova。最核心的。

2、Object Storage。对象存储。代号为Swift。

3、Identity。身份认证。代号为Keystone。

4、Dashboard。仪表盘。代号为Horizon。

5、Block Storage。块存储。代号为Cinder。

6、Network。网络。代号为Quantum。

7、Image Service。镜像服务。代号为Glance。



为什么要选择云计算的方案？

1、可以有效解决硬件单点故障问题。

2、可以按照实际需要增加硬件资源。

3、解决国内南北互通问题。

4、按需增加带宽。

5、成本更低。



# 云计算分类

私有云，一般就是企业内部搭建的，供内部使用的。

公有云。阿里云。AWS这些都是。



OpenStack每6个月更新一次。基本跟Ubuntu同步。



OpenStack所有项目都是基于Python开发，并且都是标准的Python项目



OpenStack可以成为云计算时代的linux。

Mirantis是一家做OpenStack方案的公司。



# 参考资料

1、一分钟快速入门openstack

https://www.cnblogs.com/likehua/p/3605651.html

2、告诉你一个真实的OpenStack

http://www.360doc.com/content/16/1124/16/37466175_609195077.shtml

3、OpenStack从入门到放弃

https://www.cnblogs.com/pythonxiaohu/p/5861409.html

4、What Is OpenStack | OpenStack Tutorial For Beginners | OpenStack Training | Edureka

https://www.youtube.com/watch?v=Kfj5XiNdJN0

5、devstack部署openstack环境

https://www.cnblogs.com/Allvirus/p/7783962.html

6、某大型企业私有云建设思路解析

http://cloud.51cto.com/art/201606/512215.htm

7、基于openstack安装部署私有云详细图文教程

https://www.jb51.net/article/104511.htm

8、到底选openstack还是vmware?

https://www.zhihu.com/question/24376873

9、OpenStack主力公司Mirantis公开承认前者的衰败，转投K8阵营

https://www.sohu.com/a/191483034_575815