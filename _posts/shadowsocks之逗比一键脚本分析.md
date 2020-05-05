---
title: shadowsocks之逗比一键脚本分析
date: 2019-01-12 16:12:59
tags:
	- shadowsocks
---



脚本有大概1500行左右。

```
Server_Speeder_file="/serverspeeder/bin/serverSpeeder.sh"
LotServer_file="/appex/bin/serverSpeeder.sh"
Libsodiumr_file="/usr/local/lib/libsodium.so"
BBR_file="${file}/bbr.sh"
```

第一个执行的函数是check_sys。

```
check_sys(){
	if [[ -f /etc/redhat-release ]]; then
		release="centos"
	elif cat /etc/issue | grep -q -E -i "debian"; then
		release="debian"
```

然后检查系统的的shadowsocks的状态。

```
检查逻辑是：
如果user-config.json存在：
	检查server.py的pid。这里不是用setup安装的，所以系统里不存在sslocal这样的脚本。
	如果pid存在：
		说明ssr存在，且已经启动。
	否则：
		安装了，但是没有启动。
	检查user-config.json里是否有port_password字段。
	如果没有：
		说明是单端口模式
	否则：
		是多端口模式
否则：
	没有安装。
```

然后提示用户输入数字。

1表示安装。

```
逻辑是这样：
检查是否root，不是则exit
如果user-config.json存在，提示已经安装，请检查，最好先卸载当前版本。
然后依次提示用户输入配置信息。
然后开始安装依赖。
	vim unzip net-tools
	python
	设置上海时区
下载ssr
	https://github.com/ToyoDAdoubiBackup/shadowsocksr
	得到manyuser.zip。解压。
	拷贝到/usr/local/shadowsocksr/
下载启动脚本
	https://raw.githubusercontent.com/ToyoDAdoubiBackup/doubi/master/service/ssr_debian
	改名为/etc/init.d/ssr
	添加为开机启动。
	update-rc.d -f ssr defaults
下载jq解析器。
	https://github.com/stedolan/jq
	解析json的。
写入参数到配置文件。
设置iptables
启动：
	/etc/init.d/ssr start
```

颜色提示

```
Error="${Red_font_prefix}[错误]${Font_color_suffix}"
```

Red_font_prefix是：

```
Red_font_prefix="\033[31m" 
```

Font_color_suffix，每次改了颜色后，都要马上恢复。

```
Font_color_suffix="\033[0m"
```

有两种颜色，红色表示错误，绿色表示info和tips（提示）。

