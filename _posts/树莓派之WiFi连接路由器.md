---
title: 树莓派之WiFi连接路由器
date: 2018-06-03 10:31:45
tags:
	- 树莓派

---



我的wifi热点是隐藏的。而且我希望得到的是静态的ip地址，这样我telenet到树莓派，就可以避免ip变动的问题了。

1、设置静态ip。编辑/etc/network/interfaces文件。

```
iface wlan0 inet manual
wpa_cli /etc/wpa_supplicant/wpa_supplicant.conf
iface default inet static
address 192.168.0.200
netmask 255.255.255.0
gateway 192.168.0.1
```

2、编辑/etc/wpa_supplicant/wpa_supplicant.conf

```
ctrl_interface=/var/run/wpa_supplicant
ctrl_interface_group=0
ap_scan=2
network={
  ssid="xhl"
  scan_ssid=1
  proto=WPA2
  key_mgmt=WPA-PSK
  pairwise=TKIP
  group=TKIP
  psk="1234567890"
}
```



上面的方法，并没有成功。不知道问题在哪里。暂时不管了。

# 再试一次

这次我没有什么特别要求了。能够连上路由器就好。



# 解决

发现很简单。

raspi-config里，就可以直接配置wifi的东西。配置就可以自动连接了。

这个是需要新的版本才支持的。



# 参考资料

1、玩转树莓派－Raspberry，无线网配置方法

https://blog.csdn.net/wanshiyingg/article/details/52705861

2、Linux下interface文件修改

https://www.cnblogs.com/pied/archive/2013/07/23/3205636.html

3、

https://segmentfault.com/a/1190000011579147



4、

https://wiki.archlinux.org/index.php/WPA_supplicant_(%E7%AE%80%E4%BD%93%E4%B8%AD%E6%96%87)

