---
title: node-red研究
date: 2020-04-27 21:22:22
tags:		
	- nodejs

---

1



https://www.bilibili.com/video/BV1s7411p7dj



现在对express掌握了。在寻找各种express应用的时候，发现node-red就是基于express的。

那么正好，我可以把node-red深入学习一下。

官网：https://nodered.org/



Node-RED是一种编程工具，用于以新颖有趣的方式将硬件设备、API和在线服务连接在一起。

它提供了一个基于浏览器的编辑器，

使您可以轻松地使用设计器中的各种节点将流连接在一起，

只需单击即可将其部署到其运行，

简洁高效的完成一个服务的部署。



轻量级运行时基于Node.js构建，

充分利用了其事件驱动的非阻塞模型。

这使得它非常适合在低成本的硬件（如Raspberry Pi）上的网络边缘以及云中运行。



在Node-RED中创建的流使用JSON存储，可以轻松导入和导出以与他人共享。



node-red技术在搭建具备网络与图形化功能的上位机、编程入门方面有很强的先天优势，

也可以拿来做物联网资源的扩展，或与树莓派搭配做网关功能。



node-red也是属于低代码平台的一种。



Node-Red是IBM公司开发的一个可视化的编程工具。

它允许程序员通过组合各部件来编写应用程序。

这些部件可以是

硬件设备(如：Arduino板子)、

Web API(如：WebSocket in和WebSocket out)、

功能函数(如：range)

或者在线服务(如：email)。 

Node-Red提供基于网页的编程环境。

通过拖拽已定义node到工作区并用线连接node创建数据流来实现编程。

程序员通过点击‘Deploy’按钮实现一键保存并执行。

程序以JSON字符串的格式保存，方便用户分享、修改。 

Node-Red基于Node.js，它的执行模型和Node.js一样，也是事件驱动非阻塞的。

理论上，**Node.js的所有模块都可以被封装成Node-Red的一个或几个node。**



# 使用场景

https://nodered.top/ha/caiyun/

应该是给非专业人士用的吧。



几年前就从树莓派，arduino 等创客教程中看到了Node-RED。

只知道它是IBM 公司的一个开源项目-基于数据流(dataflow)的可视化编程工具。

网上的许多文章和例子大都是树莓PI，arduino的node-RED/ IoT 例子，

这给我造成 Node-RED 是个小玩意的印象。

并没有太多地留意和深入地学习。

直到最近，发现许多大公司的产品都支持Node-RED，

比如西门子公司的IoT2000，

研华公司的WISE PaaS 网关，

美国OPTO Groov EPIC等设备中都安装了Node-RED，

表明它在工业物联网和控制中已经广泛应用了。

Node-RED 和Docker，MQTT，InFluxDB 等术语同时出现在许多网络文章中。

Node-RED 并不只是业余爱好者的编程工具。

它俨然成为工业物联网，设备和云端数据流控制的有力工具，

在工业物联网，边缘计算和云端都具有专业的应用场景。 



使用Node-RED 可以不编写任何程序，使用Web 浏览器界面进行可视化编写数据流控制程序。

提高了物联网终端设备的编程效率。

而厂家的工作就是要为客户编写各种Node 和flow 库。



同样地，Node-RED 也可以部署在云端，

或者边缘设备上，

实现云端应用的可始化编程。

下面是一个典型的应用架构。

Node-RED 主要用于物联网数据的格式转换和预处理。

并将数据存储到实时数据库influxDB 中，最后Grafana 可视化显示。



Node-RED 的强大之处在于众多公司和个人已经开发了大量的Node-RED库，在Node-RED 网站上可以找到大量的节点（目前可以看到有3124 个节点）。





# 安装运行

安装

```
npm i -g node-red
```

运行

```
teddy@thinkpad:~/work/test/websocket-test$ node-red
2 Feb 11:41:56 - [info] 

Welcome to Node-RED
===================

2 Feb 11:41:56 - [info] Node-RED version: v1.2.7
2 Feb 11:41:56 - [info] Node.js  version: v10.22.0
2 Feb 11:41:56 - [info] Linux 4.15.0-128-generic x64 LE
2 Feb 11:41:57 - [info] Loading palette nodes
2 Feb 11:42:05 - [info] Settings file  : /home/teddy/.node-red/settings.js
2 Feb 11:42:05 - [info] Context store  : 'default' [module=memory]
2 Feb 11:42:05 - [info] User directory : /home/teddy/.node-red
2 Feb 11:42:05 - [warn] Projects disabled : editorTheme.projects.enabled=false
2 Feb 11:42:05 - [info] Flows file     : /home/teddy/.node-red/flows_thinkpad.json
2 Feb 11:42:05 - [info] Creating new flow file
2 Feb 11:42:05 - [warn] 

---------------------------------------------------------------------
Your flow credentials file is encrypted using a system-generated key.

If the system-generated key is lost for any reason, your credentials
file will not be recoverable, you will have to delete it and re-enter
your credentials.

You should set your own key using the 'credentialSecret' option in
your settings file. Node-RED will then re-encrypt your credentials
file using your chosen key the next time you deploy a change.
---------------------------------------------------------------------

2 Feb 11:42:06 - [info] Starting flows
2 Feb 11:42:06 - [info] Started flows
2 Feb 11:42:06 - [info] Server now running at http://127.0.0.1:1880/

```

从上面可以得到的信息：

1、配置文件在~/.node-red/settings.js里。

2、默认上下文是存放在内存里，应该是可以配置存到磁盘里的。

3、运行在1880端口上。



![](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/20180619173259554)



数据流的编辑界面由四部分组成。

最左边是已定义的各种node的列表，我们称之为控件区；

中间是一个工作区，

用户可以拖放node到工作区来创建node的实例，

Node-Red为每个node实例赋予了唯一的ID，

通过双击node实例来编辑单个实例，

通过连接node的in和out创建数据流，

node实例会记录out口连线的信息，每条线会记录目标node实例的信息；

最右边是debug node的输出区及node的帮助信息显示区。

右上角有‘Deploy’（或者“部署”）按钮，用来把编写的程序保存到本地并执行。 



数据流的执行：

通过读取用户编辑的数据流信息，

可以知道node的类型及可编辑部分的值，

据此来创建node的可执行实例；

通过读取编辑时连线的信息，

可以得到可执行实例间的数据关系，

实例间的数据发送和接受是利用Node.js的event模块实现的。 



注意：

在Node-Red的根目录下，

可以通过执行‘node red.js’运行Node-RED。

Node-Red编辑完成的数据流默认保存在`flows_XX.json`，

可以通过执行`‘node red.js flows_.json’，`

在不启动浏览器的情况下执行已经编辑完成的程序，

这个在实际部署的时候非常有用。

# HelloWorld

启动node-red以后，

在浏览器中，

将控件区内的输入节点“inject”与输出节点“debug”，

使用鼠标左键拖入工作区内。 

感觉有点画电路原理图的意思。

又有点gstreamer里pipe控件的意思。

双击控件，可以修改控件的信息，包括类型。

例如，我们上面放进来的是inject节点，默认是时间戳类型，我们可以修改为文字类型。

![image-20210202131127815](https://gitee.com/teddyxiong53/playopenwrt_pic/raw/master/image-20210202131127815.png)

切换到调试窗口。点击inject控件的触发按钮，就可卡因看到这里打印了我们给控件填写的hello world被打印出来了。







# 基本概念

Node-RED本身只包含了一些核心的基本节点，但还有大量来自于Node-RED项目和广大社区的其他节点可以使用。

你可以在[Node-RED代码库](http://flows.nodered.org/)或[npm仓库](https://www.npmjs.com/browse/keyword/node-red)中寻找所需要的节点。



# 参考资料

1、Node-RED:1 - 简介

<https://www.jianshu.com/p/be1c98280c71>

2、使用nodered操作数据库

<https://www.ctolib.com/topics-141718.html>

3、ibm官网教程

https://developer.ibm.com/zh/components/node-red/tutorials/

4、node-red的入门教程集合

https://bbs.iobroker.cn/t/topic/1165

5、中文文档

https://nodered.top/

6、

https://nodered.17coding.net

7、yummy说电子的node-red系列文章

挺不错的。

https://blog.csdn.net/geek_monkey/category_7744078.html

8、Node-RED 的工业应用场景

https://blog.csdn.net/yaojiawan/article/details/88626832