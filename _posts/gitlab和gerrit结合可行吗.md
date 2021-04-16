---
title: gitlab和gerrit结合可行吗
date: 2021-03-24 10:51:41
tags:
	- 项目

---

--

开发风格
gitlab的特点是一个人维系一个分支。
gerrit的特点是一个团队维系一个分支。（这里的分支对应一个业务需求）

权限管理
gitlab提供了比较多的选择，可以根据需要创建project，每个团队可以根据自己的需求管理自己的代码，方式更加的灵活。

gerrit比较单一，而且权限配置比较复杂，往往都是要联系管理员做出修改，每个团队很难做到对代码的个性化管理。

代码评审
gitlab是以merge request作为一次review，merge request中可能包含多个 commit，如果review不通过也不需要发起另一次merge request。

**gerrit是以commit作为一次review，由于changeId的存在，可以对一次commit反复的进行review。**
如果task划分的粒度够细的话，并不会影响各个团队的review习惯。

团队协作
**gitlab可以选择公开代码，团队间可以看到互相的代码，有利于团队的协作。**
**gerrit由于权限控制问题，只能在权限范围内公开代码。**

信息共享
gitlab 可以提供issues，wiki等功能方便开发者与使用者之间的沟通，并且gitlab可以无缝的与一些项目管理工具集成，比如:jira。
gerrit 这个方面比较欠缺。
gitlab每个项目都有自己的wiki，很方便查看。

# 有关gitlab+gerrit+jenkins集成

现在比较流行的CI系统，

gitlab提供代码查看功能，

gerrit保存真正得代码，

jenkins通过plugin发布 gerrit上的代码。

这样做没有体现出gitlab的特点，而且由于gerrit的权限问题，很多代码无法放在gitlab上，gitlab沦为代码查看工具，很多功能形同虚设。

有关docker：
考虑到公司将使用docker技术，对于dockerfile存放等问题，gitlab比gerrit支持的更好（因为权限，文件查看的问题）。

有关CI：
jenkins提供了plugin，可以通过从gitlab上拉取代码直接部署（已测试成功，CA采用sshkey）。

总结
**gerrit作为谷歌管理安卓项目的版本管理工具还是有其优点的，**

**多部门之间的权限隔离，强制review的机制都是其优点，**

反观gitlab作为github的开源版，遵循了一套开源的流程，比较符合大多数人得习惯。

所以，通过比较，推荐使用gitlab作为版本管理工具，并且不与gerrit做集成。






参考资料

1、GitLab 与 Gerrit对比

https://blog.csdn.net/bjstyle/article/details/79107086