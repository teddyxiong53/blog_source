---
title: 蓝牙之bluetoothd
date: 2020-03-24 17:11:11
tags:
	- 蓝牙

---

--

bluetoothd是一个daemon程序。作用是管理所有的蓝牙设备。

配置信息在**/etc/bluetooth/main.conf** 文件里。

bluez的src目录下，编译得到的就是 bluetoothd这个程序。所以这个是bluez最核心的一个东西。

从src/main.c开始看。

```
main_conf_file_path = CONFIGDIR "/main.conf";
```

当前我在板端找不到一个叫main.conf的文件。所以配置文件是可以没有的。

main函数流程：

```
1、init_defaults
	这个就是生成默认参数。
	discover超时是3分钟。
	main_opts.did_source = 0x0002;		/* USB */
	main_opts.did_vendor = 0x1d6b;		/* Linux Foundation */
	main_opts.did_product = 0x0246;		/* BlueZ */
2、btd_backtrace_init
	空的。调试性质的。
3、event_loop = g_main_loop_new(NULL, FALSE);
	创建一个mainloop。
4、main_conf = load_config(main_conf_file_path);
	读取配置文件。
5、connect_dbus
	连接dbus。
	conn = g_dbus_setup_bus(DBUS_BUS_SYSTEM, BLUEZ_NAME, &err);//org.bluze
	它就等待这发给org.bluez的消息。然后进行处理。
6、adapter_init
	适配器初始化。
	创建一个蓝牙的socket
	fd = socket(PF_BLUETOOTH, SOCK_RAW | SOCK_CLOEXEC | SOCK_NONBLOCK,
								BTPROTO_HCI);
	一个addr。然后进行bind。
	addr.hci.hci_family = AF_BLUETOOTH;
	addr.hci.hci_dev = HCI_DEV_NONE;
	addr.hci.hci_channel = HCI_CHANNEL_CONTROL;
7、btd_device_init
	设备初始化。但是并没有涉及硬件。而是初始化了一下链表。
8、btd_agent_init
	agent初始化。注册了org.bluez.AgentManager1
9、btd_profile_init
	profile初始化。注册了org.bluez.ProfileManager1
10、plugin_init
	插件初始化。
	这个是参数传递进来的字符串。
11、rfkill_init
	这个是打开了open("/dev/rfkill", O_RDWR);
	然后监听上面的事件。
12、g_main_loop_run(event_loop);
	阻塞在这里。然后不断处理消息。
```



参考资料

1、man手册