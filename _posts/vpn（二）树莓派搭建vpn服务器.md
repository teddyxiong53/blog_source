---
title: vpn（二）树莓派搭建vpn服务器
date: 2018-04-20 10:45:20
tags:
	- vpn

---



前面一篇文章，我们了解了vpn的基本概念，现在我们就看看在树莓派上怎么搭建一个vpn服务器。

1、安装openvpn。

```
sudo apt-get install openvpn
```

2、拷贝easy-rsa工具到openvpn目录下。

```
root@raspberrypi:/usr/share# cp ./easy-rsa/ /etc/openvpn/ -rf
```

3、编辑/etc/openvpn/easy-rsa/vars文件。

```
只把其中一行，export KEY_SIZE=2048改为1024， 2048要运算很久。
```

```
root@raspberrypi:/etc/openvpn/easy-rsa# source ./vars 
NOTE: If you run ./clean-all, I will be doing a rm -rf on /etc/openvpn/easy-rsa/keys
```

4、生成秘钥。

```
root@raspberrypi:/etc/openvpn/easy-rsa# ./clean-all
root@raspberrypi:/etc/openvpn/easy-rsa# ./build-ca
Generating a 1024 bit RSA private key
...........++++++
.........................................................++++++
writing new private key to 'ca.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [US]:
State or Province Name (full name) [CA]:
Locality Name (eg, city) [SanFrancisco]:
Organization Name (eg, company) [Fort-Funston]:
Organizational Unit Name (eg, section) [MyOrganizationalUnit]:
Common Name (eg, your name or your server's hostname) [Fort-Funston CA]:
Name [EasyRSA]:
Email Address [me@myhost.mydomain]:
root@raspberrypi:/etc/openvpn/easy-rsa# 
```

然后生成服务器秘钥。

```
root@raspberrypi:/etc/openvpn/easy-rsa# ./build-key-server test_vpn
Generating a 1024 bit RSA private key
....++++++
.......++++++
writing new private key to 'test_vpn.key'
-----
You are about to be asked to enter information that will be incorporated
into your certificate request.
What you are about to enter is what is called a Distinguished Name or a DN.
There are quite a few fields but you can leave some blank
For some fields there will be a default value,
If you enter '.', the field will be left blank.
-----
Country Name (2 letter code) [US]:
State or Province Name (full name) [CA]:
Locality Name (eg, city) [SanFrancisco]:
Organization Name (eg, company) [Fort-Funston]:
Organizational Unit Name (eg, section) [MyOrganizationalUnit]:
Common Name (eg, your name or your server's hostname) [test_vpn]:
Name [EasyRSA]:
Email Address [me@myhost.mydomain]:

Please enter the following 'extra' attributes
to be sent with your certificate request
A challenge password []:040253
An optional company name []:
Using configuration from /etc/openvpn/easy-rsa/openssl-1.0.0.cnf
Check that the request matches the signature
Signature ok
The Subject's Distinguished Name is as follows
countryName           :PRINTABLE:'US'
stateOrProvinceName   :PRINTABLE:'CA'
localityName          :PRINTABLE:'SanFrancisco'
organizationName      :PRINTABLE:'Fort-Funston'
organizationalUnitName:PRINTABLE:'MyOrganizationalUnit'
commonName            :T61STRING:'test_vpn'
name                  :PRINTABLE:'EasyRSA'
emailAddress          :IA5STRING:'me@myhost.mydomain'
Certificate is to be certified until Apr 17 04:24:32 2028 GMT (3650 days)
Sign the certificate? [y/n]:y


1 out of 1 certificate requests certified, commit? [y/n]y
Write out database with 1 new entries
Data Base Updated
root@raspberrypi:/etc/openvpn/easy-rsa# 
```

然后生成客户端秘钥。

```
./build-key-pass client1
```

里面密码输入123456 。

然后生成dh。

```
root@raspberrypi:/etc/openvpn/easy-rsa# ./build-dh 
Generating DH parameters, 1024 bit long safe prime, generator 2
This is going to take a long time
```

5、配置openvpn服务器。

在/etc/server.conf文件，内容如下：

```
root@raspberrypi:/etc/openvpn# cat server.conf 
local 192.168.0.109
port 1194
proto udp
dev tun

ca /etc/openvpn/easy-rsa/keys/ca.crt
cert /etc/openvpn/easy-rsa/keys/server.crt
key /etc/openvpn/easy-rsa/keys/server.key
dh /etc/openvpn/easy-rsa/keys/dh1024.perm

server 10.8.0.0 255.255.255.0

push "redirect-gateway def1 bypass-dhcp"
push "dhcp-option DNS 192.168.0.1"

duplicate-cn 

keepalive 10 120

comp-lzo

user nobody
group nogroup

persist-key
persist-tun

status opensvn-status.log
log openvpn.log

verb 3
```

先测试一下配置是否有语法错误。

```
openvpn server.conf
```

如果有错误，改正。

然后启动服务。

```
service openvpn restart
```

6、openvpn客户端配置。

新建一个/etc/openvpn/clientconfig/client.conf文件。

```
client
dev tun
proto udp
remote #写到这里，我发现没法继续参考了。我并没有一个域名。
```







# 参考资料

1、这篇文章有些地方讲得不清楚，我做到一半发现做不下去。

http://shumeipai.nxez.com/2013/10/26/raspberry-pi-make-a-vpn-gateway-router.html

2、在树莓派上建立VPN（一）：如何以及为何建立一个VPN服务器？

https://www.linuxidc.com/Linux/2014-05/102450.htm/

3、树莓派搭建Openvpn（一）

主要是参考这篇文章。

https://blog.csdn.net/wxlguitar/article/details/51175872