---
title: Linux之selinux
date: 2018-09-20 11:52:04
tags:
	- Linux

---

--

什么是selinux？



selinux的se是Security Enhanced的意思。

主要价值是提供了一个灵活可配置的MAC机制。

构成：

1、内核里se模块。代码在linux-stable\security\selinux

CONFIG_SECURITY_SELINUX。

2、用户态工具。

selinux是NSA和selinux社区共同工作的结果。



# 简介

SELinux，全称Security-Enhanced Linux，是一个Linux安全子系统，

它提供了强化的访问控制机制，

可以限制进程的权限，

防止未经授权的访问和操作。

嵌入式Linux系统通常需要考虑安全性，特别是在IoT设备和其他敏感环境中。

下面是一些与嵌入式Linux和SELinux相关的常见问题：

1. SELinux是什么以及它在嵌入式Linux中的作用是什么？
   - SELinux是Linux内核的一个安全模块，用于强化操作系统的安全性。它在嵌入式Linux中的作用是提供了一种基于策略的访问控制，允许您定义哪些进程可以访问系统资源和如何访问这些资源。

2. 在嵌入式Linux中启用SELinux需要注意哪些事项？
   - 在嵌入式系统中启用SELinux需要**编译内核时启用SELinux支持，并生成一个适当的策略文件**。您还需要确保嵌入式应用程序能够与SELinux策略兼容，否则可能会出现权限问题。

3. 如何创建和管理SELinux策略文件？
   - **SELinux策略文件是规定哪些进程可以执行哪些操作的规则集合**。您可以使用工具如`semanage`、`audit2allow`和`sepolgen`来管理策略文件。创建策略文件需要了解您的应用程序的需求，以确保它们能够在SELinux启用的环境中正常运行。

4. SELinux如何帮助保护嵌入式系统的安全？
   - SELinux可以限制进程的权限，**即使一个进程被攻破，攻击者也会受到限制。**它还可以减少潜在漏洞的危害，提高系统的整体安全性。

5. SELinux如何与其他嵌入式安全措施（例如加密和固件签名）协同工作？
   - SELinux是一种安全策略，可以与其他嵌入式安全措施协同工作。例如，您可以使用SELinux来限制哪些进程可以访问加密密钥或重要的固件组件。这种综合使用有助于提高整体系统安全性。

# selinux的发展历史

SELinux（Security-Enhanced Linux）的发展历史可以追溯到20世纪90年代末和21世纪初。以下是SELinux的主要发展历史里程碑：

1. **1996年 - NSA的Flask项目启动：** NSA（美国国家安全局）开始了一个名为Flask的项目，旨在研究和开发强化的操作系统安全模型，以提高Linux系统的安全性。

2. **2000年 - NSA发布SE Linux：** NSA发布了SE Linux，一个Linux内核模块，它引入了一种基于Mandatory Access Control（MAC）的安全机制，允许对系统资源的访问进行强化控制。这是SELinux的雏形。

3. **2003年 - SELinux被合并到Linux内核：** SELinux代码被合并到Linux内核的2.6版本，这意味着它变成了Linux内核的一部分，而不再需要单独下载和编译。

4. **2004年 - 发布SELinux参考策略：** NSA发布了SELinux的参考策略，这些策略文件定义了如何配置SELinux以增加系统的安全性。这些策略成为了SELinux的基础。

5. **2005年 - Fedora引入SELinux：** Fedora Linux发布了首个将SELinux启用的发行版。它成为了SELinux广泛采用的一个里程碑。

6. **2008年 - 发布SELinux 2.0：** SELinux 2.0版本带来了改进和增强，以提高配置和管理SELinux策略的可用性。

7. **2010年 - Android引入SELinux：** Google的Android操作系统开始引入SELinux，加强了移动设备的安全性。

8. **2015年 - RHEL默认启用SELinux：** Red Hat Enterprise Linux（RHEL）在其7.0版本中默认启用SELinux，强化了服务器端系统的安全性。

9. **2021年 - 最新发展：** 我的知识截止日期是2021年，所以我无法提供关于SELinux的最新发展。不过，SELinux在各种Linux发行版中持续演进，以满足不断增长的安全需求。

SELinux的发展历史显示了其作为一个强大的安全增强工具的演进，并在各种领域，从服务器到移动设备，都得到了广泛采用。它在加强Linux系统安全性方面发挥了重要作用。

# 内核打开selinux的方法





SELinux 主要由美国国家安全局开发。2.6 及以上版本的 Linux 内核都已经集成了 SELinux 模块。

SELinux 的结构及配置非常复杂，而且有大量概念性的东西，要学精难度较大。很多 Linux 系统管理员嫌麻烦都把 SELinux 关闭了。

**如果可以熟练掌握 SELinux 并正确运用，我觉得整个系统基本上可以到达"坚不可摧"的地步了（请永远记住没有绝对的安全）。**



# 参考资料

1、SELINUX工作原理

https://www.cnblogs.com/gailuo/p/5041034.html

2、一文彻底明白linux中的selinux到底是什么

https://blog.csdn.net/weixin_42350212/article/details/81189717