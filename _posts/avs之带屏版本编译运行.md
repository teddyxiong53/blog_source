---
title: avs之带屏版本编译运行
date: 2018-11-03 16:42:19
tags:
	- avs

---



1、检查ca_settings.cnf和generate.sh里的内容，根据需求调整，当前只供测试用。

2、运行generate.sh脚本。

```
hlxiong@hlxiong-VirtualBox:~/work2/avs-screen/linux-screen/AlexaClientSDK/tools/Gui/certificates$ ./generate.sh 
Generating a 2048 bit RSA private key
...................................................................+++
...............................+++
writing new private key to 'ca.key'
-----
Generating a 2048 bit RSA private key
...........................................................................................................................................................................................................................+++
..............+++
writing new private key to 'client.key'
-----
Generating a 2048 bit RSA private key
..............+++
..............................+++
writing new private key to 'server.key'
-----
Signature ok
subject=/CN=MMSDK_Client_Cert/C=US/ST=WA/L=Seattle/O=Amazon
Getting CA Private Key
Signature ok
subject=/CN=localhost/C=US/ST=WA/L=Seattle/O=Amazon
Getting CA Private Key
```

提示要输入密码，我直接回车，没有看到报错，应该是可以为空密码的。

然后需要在系统里设备把这些key设置为always trust的。

```
hlxiong@hlxiong-VirtualBox:~/work2/avs-screen/linux-screen/AlexaClientSDK/tools/Gui/certificates$ tree -h
.
├── [1.4K]  ca.cert
├── [1.7K]  ca.key
├── [ 765]  ca_settings.cnf
├── [  17]  ca.srl
├── [ 277]  cert_settings.cnf
├── [1.3K]  client.cert
├── [2.7K]  client.chain
├── [ 985]  client.csr
├── [1.7K]  client.key
├── [3.6K]  client.p12
├── [1.2K]  generate.sh
├── [1.3K]  server.cert
├── [2.7K]  server.chain
├── [ 972]  server.csr
└── [1.7K]  server.key
```

我们需要把ca.cert的内容拷贝到系统目录下去。

```
sudo cp ca.cert /usr/local/share/ca-certificates
```

当前我的系统这个目录下还没有文件。

然后更新一下。

```
sudo update-ca-certificates
```

```
hlxiong@hlxiong-VirtualBox:~/work2/avs-screen/linux-screen/AlexaClientSDK/tools/Gui/certificates$ sudo update-ca-certificates
Updating certificates in /etc/ssl/certs...
0 added, 0 removed; done.
Running hooks in /etc/ca-certificates/update.d...
done.
```

看这个打印，并没有起任何作用。

算了，看文档，可以不使用这个安全措施。

```
use DISABLE_WEBSOCKET_SSL option during the build and use '?insecure=1' when opening GUI
```

需要安装npm。

```
sudo apt-get install npm
```

执行下面的命令的时候，在npm install的时候，卡住不懂，我执行run build的，会出错，说webpack找不到。

```
cd AlexaClientSDK/GUI/js
npm install
npm run build
```

先安装webpack。

```
sudo npm install webpack -g
```

这个可以看到进度条的变化。

也不行，还是按步骤来。

卡住，先等半个小时再看吧。

看到打印说，不用用代理好像。先把代理关闭。



我这边编译avs很顺利。

问题就是nodejs的环境弄不好。

这2者的关系是什么？

我觉得我的nodejs安装有问题，可能跟我的代理有关系。

关闭所有代理。就好了。停止polipo。unset http_proxy等。

```
npm config set https-proxy 
```

然后再试。就可以了。还要注意换成淘宝的源。

websocketpp是做什么的？



现在看看带屏版本有哪些不一样的地方。



对比，

版本号升级到1.8.1，发布于2018年7月9日。

```
ACL：interface类，增加析构函数。之前可能因为这个导致了内存泄露。
ADSL：对MessageInterpreter进行了改写。
AMFL：对FocusManager里的变量改成函数。
ApplicationUtilities：DefaultClient进行了完善。
Authorization：新的去掉了这个目录。
```



关键还是看懂websocketpp如何起作用的。

