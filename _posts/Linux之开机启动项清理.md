---
title: Linux之开机启动项清理
date: 2018-12-12 21:26:10
tags:
	- Linux

---



linux可能安装了很多你用不上的东西。希望不要开机启动。

查看当前开机启动项。

```
systemctl list-unit-files --type=service | grep enabled
```

我当前的启动项有：

```
accounts-daemon.service                    enabled 
anacron-resume.service                     enabled 
anacron.service                            enabled 
autovt@.service                            enabled 
avahi-daemon.service                       enabled 
binfmt-support.service                     enabled 
bluetooth.service                          enabled 
brltty.service                             enabled 
cron.service                               enabled 
cups-browsed.service                       enabled 
cups.service                               enabled 
dbus-org.bluez.service                     enabled 
dbus-org.freedesktop.Avahi.service         enabled 
dbus-org.freedesktop.ModemManager1.service enabled 
dbus-org.freedesktop.nm-dispatcher.service enabled 
dbus-org.freedesktop.thermald.service      enabled 
display-manager.service                    enabled 
dns-clean.service                          enabled 
dnsmasq.service                            enabled 
getty@.service                             enabled 
gpu-manager.service                        enabled 
lightdm.service                            enabled 
lm-sensors.service                         enabled 
ModemManager.service                       enabled 
network-manager.service                    enabled 
networking.service                         enabled 
NetworkManager-dispatcher.service          enabled 
NetworkManager-wait-online.service         enabled 
NetworkManager.service                     enabled 
pppd-dns.service                           enabled 
resolvconf.service                         enabled 
rsyslog.service                            enabled 
snapd.autoimport.service                   enabled 
snapd.core-fixup.service                   enabled 
snapd.seeded.service                       enabled 
snapd.service                              enabled 
snapd.system-shutdown.service              enabled 
ssh.service                                enabled 
sshd.service                               enabled 
syslog.service                             enabled 
systemd-timesyncd.service                  enabled 
thermald.service                           enabled 
ufw.service                                enabled 
unattended-upgrades.service                enabled 
ureadahead.service                         enabled 
whoopsie.service                           enabled 
```



这个命令可以看启动项的耗时情况。

```
systemd-analyze blame
```



# 参考资料

1、Linux 系统开机启动项清理

https://zhuanlan.zhihu.com/p/29148642