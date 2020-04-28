---
title: minidlna分析
date: 2020-04-27 13:15:08
tags:
	- dlna

---

1

代码：https://github.com/azatoth/minidlna

先看minidlnad程序的用法：

```
minidlnad [-d] [-v] [-f config_file]
                [-a listening_ip] [-i network_interface]
                [-p port] [-s serial] [-m model_number]
                [-t notify_interval] [-P pid_filename]
                [-u uid_to_run_as]
                [-w url] [-R] [-L] [-S] [-V] [-h]
```

默认启动的命令是：

```
/usr/sbin/minidlnad -f /etc/minidlna.conf -P /run/minidlna/minidlna.pid
```

-f是指定配置文件。

如果没有指定，则默认也是用/etc/minidlna.conf。

-d选项是表示debug。

-w：指定presentation的url。默认是在80端口上。

-v：verbose输出。

产生uuid的方法：

```
strcpy(uuidvalue+5, "4d696e69-444c-164e-9d41-");
strncat(uuidvalue, mac_str, 12);
```

ssdp的间隔是895秒。

```
runtime_vars.notify_interval = 895;	/* seconds between SSDP announces */
```

配置文件里可以放的选项有：

```
static const struct {
	enum upnpconfigoptions id;
	const char * name;
} optionids[] = {
	{ UPNPIFNAME, "network_interface" },
	{ UPNPLISTENING_IP, "listening_ip" },
	{ UPNPPORT, "port" },
	{ UPNPPRESENTATIONURL, "presentation_url" },
	{ UPNPNOTIFY_INTERVAL, "notify_interval" },
	{ UPNPSYSTEM_UPTIME, "system_uptime" },
	{ UPNPUUID, "uuid"},
	{ UPNPSERIAL, "serial"},
	{ UPNPMODEL_NAME, "model_name"},
	{ UPNPMODEL_NUMBER, "model_number"},
	{ UPNPFRIENDLYNAME, "friendly_name"},
	{ UPNPMEDIADIR, "media_dir"},
	{ UPNPALBUMART_NAMES, "album_art_names"},
	{ UPNPINOTIFY, "inotify" },
	{ UPNPDBDIR, "db_dir" },
	{ UPNPLOGDIR, "log_dir" },
	{ UPNPLOGLEVEL, "log_level" },
	{ UPNPMINISSDPDSOCKET, "minissdpdsocket"},
	{ ENABLE_TIVO, "enable_tivo" },
	{ ENABLE_DLNA_STRICT, "strict_dlna" },
	{ ROOT_CONTAINER, "root_container" }
};

```

然后打开一个socket。进行listen操作。

```
OpenAndConfSSDPReceiveSocket(n_lan_addr, lan_addr);
```

没有listen。

是填入一个多播地址。

```
static int
AddMulticastMembership(int s, in_addr_t ifaddr)
{
	struct ip_mreq imr;	/* Ip multicast membership */
```



```
struct upnphttp
```



参考资料

1、

