---
title: 自己搭建ngrok服务
date: 2018-11-29 21:41:16
tags:
	- 网络

---



我终于还是决定在我的vps上搭建ngrok服务，来让我的局域网的树莓派可以从外网进行访问。

花生壳的那个6元的服务，其实也就是在国内搭建的ngrok服务。

花生壳的还有流量限制。

但是我没有域名，这是个问题，我得先找一个免费的二级域名。

我在freenom上申请了一个免费域名，teddyxiong53.ml。

需要在这个上面建立2个A记录。

ngrok.teddyxiong53.ml和*.ngrok.teddyxiong53.ml。

用来关联ngrok服务。

ngrok是基于go语言的。所以需要先安装golang。

```
apt-get install golang
```

在vps上，是以root身份登陆的。

在~/.bashrc最后加上这个。

```
export GOPATH=$HOME/go
PATH=$PATH:$HOME/.local/bin:$HOME/bin:$GOPATH/bin
```

然后

```
source ~/.bashrc
```

然后下载ngrok的源代码。

```
 mkdir -p ~/go/src/github.com/inconshreveable
 cd  ~/go/src/github.com/inconshreveable
 git clone https://github.com/inconshreveable/ngrok.git
 export GOPATH=~/go/src/github.com/inconshreveable/ngrok
```



接下来是需要我们生成自己的证书。

并且提供携带了该证书的ngrok客户端。

证书生成过程，需要一个基础域名。

我们前面定义的ngrok.teddyxiong53.ml就可以作为基础域名。

生成key文件。

```
root@debian:~/go/src/github.com/inconshreveable/ngrok# openssl genrsa -out rootCA.key 2048
Generating RSA private key, 2048 bit long modulus
.................................................................................................................................................................................................................+++
..............................+++
e is 65537 (0x10001)
```

生成perm文件。

```
openssl req -x509 -new -nodes -key rootCA.key -subj "/CN=ngrok.teddyxiong53.ml" -days 5000 -out rootCA.pem
```

生成device.key。

```
 openssl genrsa -out device.key 2048
```

生成device.csr。

```
openssl req -new -key device.key -subj "/CN=ngrok.teddyxiong53.ml" -out device.csr
```

签名。

```
root@debian:~/go/src/github.com/inconshreveable/ngrok# openssl x509 -req -in device.csr -CA rootCA.pem -CAkey rootCA.key -CAcreateserial -out device.crt -days 5000
Signature ok
subject=/CN=ngrok.teddyxiong53.ml
Getting CA Private Key
```

我们得到device和rootCA开头的，一共6个文件。

```
root@debian:~/go/src/github.com/inconshreveable/ngrok# ls
assets  contrib  CONTRIBUTORS  device.crt  device.csr  device.key  docs  LICENSE  Makefile  README.md  rootCA.key  rootCA.pem  rootCA.srl  src
```

在当前目录，执行下面的命令。

```
cp rootCA.pem assets/client/tls/ngrokroot.crt
cp device.crt assets/server/tls/snakeoil.crt
cp device.key assets/server/tls/snakeoil.key
```

然后我们编译ngrokd和ngrok。

```
make release-server
```

报错了。

```
import "context": import path doesn't contain a slash
```

网上查了下，说是需要更新go语言版本。

查看我当前的go的版本。

```
root@debian:~/go/src/github.com/inconshreveable/ngrok# go version
go version go1.3.3 linux/amd64
```

本来不想在vps上弄太多东西的。

现在需要下载golang的源代码，120M。

然后编译，需要安装gcc。

```
apt-get  install  build-essential
```

我接着看教程，还是有坑。

```
root@debian:~/down/go/src# ./all.bash 
Building Go cmd/dist using /usr/lib/go.
ERROR: Cannot find /usr/lib/go/bin/go.
Set $GOROOT_BOOTSTRAP to a working Go tree >= Go 1.4.
```

需要go的版本1.4以上。

还是采用github上clone下来，先保存一份，然后回退到1.4版本。

go从1.5版本开始实现自举，就是用go开发go。之前都是用C语言开发的。

```
git checkout go1.4
```

然后进入到src目录，执行：

```
./all.bash
```

vps做编译，性能不怎么够，慢慢等吧。

all.bash，是编译，并运行测试，测试对我们来说是多余的。

所以可以用执行make.bash来替代。

编译完，生成的东西，在bin目录下。

```
root@debian:~/down/github/go/bin# ./go version
go version go1.4 linux/amd64
```

现在我们需要把这个~/down/github/go目录，配置为默认的go环境。

在网上找到了更好的安装方法。

用第三方工具gvm来安装。

```
bash < <(curl -s -S -L https://raw.githubusercontent.com/moovweb/gvm/master/binscripts/gvm-installer)
```

```
gvm install go1.8.3
```

但是这个还是依赖go大于1.4版本。

我把目录这样放。

go放的是最新的代码，go1.4的是checkout到1.4后编译出来的。path是个空目录。

```
root@debian:~/.golang# ls
go  go1.4 path
```

然后在.bashrc里修改：

```
export GOROOT=$HOME/.golang/go
export GOPATH=$HOME/.golang/path
export GOROOT_BOOTSTRAP=$HOME/.golang/go1.4
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
```

然后进入go目录，执行编译。

```
root@debian:~/.golang/go/src# ./make.bash
```

但是报错了。

```
root@debian:~/.golang/go/src# ./make.bash
Building Go cmd/dist using /root/.golang/go1.4.
Building Go toolchain1 using /root/.golang/go1.4.
go build bootstrap/cmd/compile/internal/ssa: /root/.golang/go1.4/pkg/tool/linux_amd64/6g: signal: killed
go tool dist: FAILED: /root/.golang/go1.4/bin/go install -gcflags=-l -tags=math_big_pure_go compiler_bootstrap bootstrap/cmd/...: exit status 1
root@debian:~/.golang/go/src# 
```

网上找了下，是oom被杀了。dmesg查看。

```
[2138286.542443] Out of memory: Kill process 25286 (6g) score 723 or sacrifice child
[2138286.543360] Killed process 25286 (6g) total-vm:498236kB, anon-rss:409824kB, file-rss:0kB
root@debian:~/.golang/go/src# 
```

现在陷入死循环了。

我下载deb包来安装。这个需要依赖go的源文件。那还是回到老路上去了。

```
dpkg: dependency problems prevent configuration of golang-1.8-go:
 golang-1.8-go depends on golang-1.8-src (>= 1.8.5-1); however:
  Package golang-1.8-src is not installed.
```

我感觉这条路已经走不通了。

我发现被前面的文章误导了。

根本不需要编译。只需要把目录mv到/usr/local目录下就好了。

```
wget https://dl.google.com/go/go1.11.linux-amd64.tar.gz # 下载go语言
tar -zxvf go1.11.linux-amd64.tar.gz #解压tar包
mv go /usr/local/  #移动go语言
```

配置环境变量。我暂时放在.bashrc里，后面在改到/etc/profile里。

```
export GOROOT=/usr/local/go
export GOPATH=/usr/local/go/get_package #设置环境变量，Go语言的安装位置
export NGROK_DOMAIN=“ngrok.your.com” #设置环境变量，ngrok域名
export PATH=.:$GOROOT/bin:$PATH
```



现在编译ngrok。

```
make release-server
```

编译可以在树莓派上跑的client。

```
GOOS=linux GOARCH=arm make release-client
```

```
root@debian:~/go/src/github.com/inconshreveable/ngrok/bin/linux_arm# file ngrok 
ngrok: ELF 32-bit LSB executable, ARM, EABI5 version 1 (SYSV), statically linked, not stripped
```



在ngrok目录下，执行下面的命令启动。

```
./bin/ngrokd  -domain=$NGROK_DOMAIN -httpAddr=":80" -httpsAddr=":443"
```

然后把ngrok拷贝到树莓派上。用scp拷贝就好了。用winscp来拷贝也行。注意22号端口没开。换成其他端口。

然后执行命令：

树莓派上新建一个配置文件ngrok.conf

```
pi@raspberrypi:~/work/ngrok$ ls
ngrok  ngrok.conf
```

ngrok.conf内容：

```
server_addr: "ngrok.teddyxiong53.ml:4443"
trust_host_root_certs: false
```

```
./ngrok -subdomain demo -config=./ngrok.conf 80
```

树莓派运行打印。

```
Forwarding http://demo.ngrok.teddyxiong53.ml -> 127.0.0.1:80          
Forwarding https://demo.ngrok.teddyxiong53.ml -> 127.0.0.1:80         
Web Interface       127.0.0.1:4040       
# Conn 0            
Avg Conn Time       0.00ms   
```

但是访问并不能成功。

看了下我的freenom上的信息，昨晚我修改的信息没有保存成功。

现在freenom访问特别慢。

在我的电脑上，可以用nslookup查找到dns信息。

```
hlxiong@hlxiong-VirtualBox:~$ nslookup ngrok.teddyxiong53.ml
Server:         127.0.0.1
Address:        127.0.0.1#53

Non-authoritative answer:
Name:   ngrok.teddyxiong53.ml
Address: xx
```



# 参考资料

1、从零教你搭建ngrok服务，解决外网调试本地站点

https://morongs.github.io/2016/12/28/dajian-ngrok/

2、Debian下编译安装Golang

https://www.jianshu.com/p/9c1e685bcb5b

3、Go的三种安装方式

https://github.com/astaxie/build-web-application-with-golang/blob/master/zh/01.1.md

4、三分钟使用Ngrok实现内网穿透,最后有福利喔

https://www.imooc.com/article/79754