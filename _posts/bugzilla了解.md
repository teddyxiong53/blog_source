---
title: bugzilla了解
date: 2018-01-31 23:54:58
tags:
	- bug

---



对于带名字里带zilla的软件都有一种好感。

bugzilla是开源免费的bug管理工具。



# 安装

1、bugzilla是一个web应用。所以需要Apache做容器。还需要mysql。

```
sudo apt-get install apache2 mysql perl postfix 
```

2、下载bugzilla的代码。

https://ftp.mozilla.org/pub/mozilla.org/webtools/bugzilla-5.0.2.tar.gz

大概3M，不多。

3、解压，运行里面的check perl的脚本，发现有一堆的modules需要安装，又是下载又是编译的，很慢。

```
 GD Chart::Lines Template::Plugin::GD::Image GD::Text GD::Graph MIME::Parser PatchReader Net::LDAP Authen::Radius SOAP::Lite XMLRPC::Lite JSON::RPC Test::Taint HTML::Scrubber Encode::Detect Email::Reply HTML::FormatText::WithLinks TheSchwartz Daemon::Generic mod_perl2 Apache2::SizeLimit IO::Scalar Cache::Memcached File::Which
```

