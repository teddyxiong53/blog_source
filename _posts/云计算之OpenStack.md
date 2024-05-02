---
title: 云计算之OpenStack
date: 2018-07-13 21:16:00
tags:
	- 云计算

---

--

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

# 简介

OpenStack是一个开源的云计算平台，旨在提供可扩展性、灵活性和可定制性的基础设施即服务（IaaS）。它由一系列模块组成，每个模块负责不同的任务，包括计算、存储、网络和身份认证等方面。

这个项目最初由NASA和Rackspace合作发起，后来吸引了全球范围内的大量企业和开发者的参与，成为了目前最受欢迎的开源云计算平台之一。

OpenStack的主要组件包括：

1. Nova：负责计算资源的管理，包括虚拟机、容器和裸金属实例。
2. Swift：提供对象存储服务，适用于大规模的分布式存储需求。
3. Cinder：提供块存储服务，允许用户创建和管理持久性存储卷。
4. Neutron：负责网络服务，包括虚拟网络、子网和路由等。
5. Keystone：提供身份认证和授权服务，用于管理用户、角色和权限。
6. Glance：提供镜像服务，用于管理虚拟机和容器的镜像文件。
7. Horizon：提供Web界面，用于管理和监控OpenStack环境。

除了这些核心组件外，OpenStack还支持各种其他服务和插件，例如数据库服务（Trove）、消息队列服务（Zaqar）和负载均衡服务（Octavia）等。

总的来说，OpenStack为用户提供了一个构建和管理私有云、公有云和混合云的强大平台，具有高度的灵活性和可定制性，能够满足不同规模和需求的云计算环境。

# 发展历史

OpenStack的发展历史可以追溯到2010年，当时NASA和Rackspace合作推出了这个项目。以下是OpenStack的主要发展里程碑：

1. **2010年：项目启动**  
   - NASA和Rackspace发布了OpenStack计划，并将其作为开源项目发布，包括计算（Nova）和对象存储（Swift）两个组件。

2. **2011年：首个正式版本发布**  
   - OpenStack发布了首个正式版本，命名为Austin，其中包括Nova、Swift、Glance和Horizon等核心组件。

3. **2012年：扩展和社区增长**  
   - OpenStack社区快速增长，吸引了越来越多的贡献者和企业加入。Grizzly版本发布，引入了更多功能和改进。

4. **2013年：企业采用**  
   - OpenStack开始被企业广泛采用，成为构建私有云和公有云的首选平台。Havana版本发布，引入了更多的组件和功能，包括Neutron网络服务。

5. **2014年：Icehouse发布**  
   - OpenStack发布了Icehouse版本，继续增强平台的稳定性、性能和功能。该版本引入了更多企业级特性，并加强了安全性和可扩展性。

6. **2015年及以后：持续创新和成熟**  
   - OpenStack持续发布新版本，每个版本都引入了更多的功能和改进。社区规模持续扩大，吸引了越来越多的企业和个人参与。同时，各种部署工具和管理平台也不断涌现，为OpenStack的部署和管理提供了更多选择。

7. **2020年及以后：适应多云和边缘计算**  
   - 随着多云和边缘计算的兴起，OpenStack逐渐成为了构建混合云和边缘云的关键基础设施。社区持续推动项目的发展，以满足新兴的云计算需求和场景。

在过去的十多年里，OpenStack从一个起步阶段的项目发展成为了一项成熟而强大的开源云计算平台，为用户提供了丰富的功能和灵活的部署选项，成为了构建私有云、公有云和混合云的首选平台之一。

# OpenStack为什么没落了

虽然OpenStack在一段时间内被认为是云计算领域的未来，但它的发展道路并不一帆风顺，出现了一些挑战和限制，导致其在一定程度上失去了部分市场份额和影响力。以下是一些可能导致OpenStack没落的原因：

1. **复杂性和学习曲线高**：OpenStack作为一个庞大而复杂的平台，其部署、配置和管理相对复杂，需要高水平的技术技能和经验。这使得一些企业在采用OpenStack时面临着较高的学习曲线和部署成本。

2. **竞争对手的崛起**：随着公有云提供商（如AWS、Azure和Google Cloud）的崛起，以及容器技术（如Docker和Kubernetes）的普及，OpenStack面临着越来越激烈的竞争。这些竞争对手提供了更简单、更灵活和更易用的解决方案，吸引了更多用户和企业。

3. **社区和治理问题**：OpenStack作为一个开源项目，其发展依赖于社区的贡献和支持。然而，一些社区和治理问题可能影响了项目的发展和决策效率，使得一些贡献者和用户对项目的未来感到担忧。

4. **技术转变和趋势变化**：随着技术的发展和市场的变化，云计算领域出现了一些新的技术趋势，如容器化、微服务架构和边缘计算等。这些新技术和趋势对传统的IaaS平台提出了新的挑战，也改变了用户和企业的需求和偏好。

5. **营销和品牌影响力不足**：相比于一些大型公有云提供商，OpenStack的营销和品牌影响力相对较弱。这使得一些用户和企业更倾向于选择知名度更高、市场份额更大的云服务提供商，而非构建自己的OpenStack环境。

综合考虑这些因素，可以看出OpenStack在一定程度上失去了一些市场份额和影响力，但作为一个开源项目，它仍然在持续发展，并且在特定的场景和行业仍然具有一定的优势和价值。

# 个人部署OpenStack环境搭建

个人部署OpenStack环境需要一定的技术知识和经验，因为OpenStack是一个复杂的系统，涉及多个组件和服务的配置和集成。以下是一般步骤：

1. **硬件准备**：首先确定你拥有的硬件资源是否符合OpenStack的要求。至少需要一台物理服务器或虚拟机，具备足够的内存、CPU和存储资源来运行OpenStack各个组件。

2. **操作系统安装**：选择一种适合的Linux发行版作为OpenStack的操作系统基础。常见选择包括Ubuntu、CentOS等。安装操作系统，并进行基本的配置和网络设置。

3. **网络配置**：OpenStack需要一个网络环境来进行通信和管理。你可以选择使用物理网络或虚拟网络来构建OpenStack的网络基础设施。确保网络配置符合OpenStack的要求，并能够满足你的实际需求。

4. **安装OpenStack**：选择一种部署工具或方法来安装和配置OpenStack。目前常用的部署工具包括DevStack、Packstack、OpenStack-Ansible等。根据你的偏好和经验选择合适的工具，并按照其文档或指南进行安装和配置。

5. **配置组件**：一旦OpenStack安装完成，接下来需要对各个组件进行配置。这包括Nova、Neutron、Cinder等核心组件，以及Keystone等辅助组件。根据你的需求和环境进行相应的配置，包括网络设置、存储设置、认证设置等。

6. **测试和验证**：安装和配置完成后，进行测试和验证以确保OpenStack环境的正常运行。你可以创建虚拟机、网络、存储卷等资源，并进行基本的操作和管理来验证OpenStack的功能和性能。

7. **持续管理和维护**：一旦OpenStack环境运行起来，需要进行持续的管理和维护工作，包括监控系统状态、更新软件补丁、备份和恢复数据等。确保OpenStack环境的安全、稳定和高效运行。

需要注意的是，个人部署OpenStack环境需要一定的时间和精力，同时也需要具备一定的Linux系统管理和云计算知识。建议在开始之前先阅读OpenStack的文档和指南，以及相关的部署工具的文档，了解清楚整个过程和注意事项。

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