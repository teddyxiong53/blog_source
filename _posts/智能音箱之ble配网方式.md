---
title: 智能音箱之ble配网方式
date: 2020-03-20 14:12:11
tags:
	- 智能音箱
---

1

以rk3308的ble配网作为分析对象。

参考文档《RK3308_RTL8723DS_WIFI_BT_说明文档_V1.20》《Rockchip Linux WIFI BT 开发指南 V4.0 20181126》

蓝牙使用bluez + bluez-alsa来实现A2DP sink、HFP、ble蓝牙配网这3个功能。

需要去掉内核默认的HCI UART driver。因为wifi驱动自己另外写了。

蓝牙使用rk3308的ttys4串口来进行控制。



蓝牙ble配网，需要板端运行一个gatt-server。就是运行一个服务端，这个就是本质。ap配置，是一个基于wifi的服务端。

这个是在bluez的tools/gatt-server.c的基础上修改。所以本质是在板子上启动一个gatt服务器。

增加了给手机端连接的service及对应的characteristic。



操作过程：

板端：

```
1、打开蓝牙，可以用hciconfig hci0 up
2、执行gatt-service程序。
```

手机端：

```
1、安装rk提供的wifi introducer apk。打开扫描。

```

目前是扫描不到。

发现问题了。

是需要先手动执行bluetoothd。

```
# 板端依次执行：
hciconfig hci0 up
# 注意这个的位置，是没有在环境变量里的，所以要带上完整路径。
/usr/libexec/bluetooth/bluetoothd &
# 启动配置程序，则个有对应的package。自己编译出来。
ble_wificonfig
```

现在就可以看到了。

可以用配网程序连接上，并且把wifi信息发送过来。

我觉得需要通过dbus调试来分析过程。

```
export DBUS_SESSION_BUS_ADDRESS="unix:path=/var/run/dbus/system_bus_socket"
dbus-monitor
```

这样就可以观察dbus上的消息了。

如果没有上面那个环境变量设置，dbus-monitor会报错：

```
Failed to open connection to session bus: Using X11 for dbus-daemon autolaunch was disabled at compile time, set your DBUS_SESSION_BUS_ADDRESS instead
```



再看一下ble_wificonfig这个目录。

下面有一个bt_realtek_wificonfig脚本，内容如下：

```
#!/bin/sh

case "$1" in
    start)

    echo "start rtl8723ds bluetooth server"
    bt_pcba_test &
    sleep 7

    echo "start rtl8723ds bluetooth hciconfig"
    hciconfig hci0 up &

    echo "start rtl8723ds bluetooth wifi config"
    /usr/libexec/bluetooth/bluetoothd -C -E -d -n &
    sleep 2
    ble_wificonfig &

        ;;
    stop)
        echo -n "Stopping rtl8723ds bluez5_utils bluetooth server & app"
        killall ble_wificonfig
        sleep 1
        killall bluetoothd
        sleep 1
        if busybox cat /sys/class/rkwifi/chip | grep RTL8723DS; then
        killall rtk_hciattach
        fi
        if busybox cat /sys/class/rkwifi/chip | grep AP6255; then
        killall brcm_patchram_plus1
        fi

        ;;
    *)
        echo "Usage: $0 {start|stop}"
        exit 1
esac

exit $?
```

看到调用了bt_pcba_test。

这个是在/usr/bin目录下的一个脚本。内容是：

```
#!/bin/sh

echo 0 > /sys/class/rfkill/rfkill0/state
sleep 2
echo 1 > /sys/class/rfkill/rfkill0/state
sleep 2

insmod /usr/lib/modules/hci_uart.ko
rtk_hciattach -n -s 115200 /dev/ttyS4 rtk_h5 &
hciconfig hci0 up
```

在代码里，又是从哪里把这个脚本安装到系统里的呢？

直接locate bt_pcba_test。这个是找不到的。

通过grep rtk_hciattach ，发现rkbtwifi目录下有脚本有这个东西。

到packages目录下看，是bt_load_rtk_firmware安装的时候改名为bt_pcba_test。

```
$(INSTALL) -D -m 0755 $(@D)/bt_load_rtk_firmware $(TARGET_DIR)/usr/bin/bt_pcba_test
```

bt_pcba_test里做的事情是：

1、对蓝牙下电再上电。

2、加载hci_uart.ko驱动。

3、把hci接口跟ttyS4关联起来。

4、软件上打开蓝牙接口。

系统里为什么有2个wifi，2个蓝牙？

```
/ # rfkill
ID TYPE      DEVICE          SOFT      HARD
 0 bluetooth bt_default unblocked unblocked
 1 wlan      phy0       unblocked unblocked
 2 wlan      phy1       unblocked unblocked
 3 bluetooth hci0       unblocked unblocked
```



目前系统开机，默认就加载了hci_uart.ko。但是我并没有进行明确的加载操作。

那么是在哪里自动加载的呢？

/etc/init.d/S66load_wifi_modules这个脚本。

有这么一句，看起来比较像。

```
 rk_wifi_init BT_TTY_DEV
```

rk_wifi_init是一个可执行程序。但是这个是加载wifi驱动的。目前系统就2个ko文件。一个蓝牙串口的hci_uart.ko。一个8723.ko。

从dmesg看，大概在开机12秒的时候，自动加载蓝牙的。

```
[   12.927819] hci_uart: loading out-of-tree module taints kernel.
[   12.930438] Bluetooth: HCI UART driver ver 2.2.d448471.20181218-171515
[   12.930507] Bluetooth: HCI H4 protocol initialized
[   12.930530] Bluetooth: HCI Realtek H5 protocol initialized
[   12.930552] rtk_btcoex: rtk_btcoex_init: version: 1.2
[   12.930569] rtk_btcoex: create workqueue
[   12.930586] rtk_btcoex: Coex over UDP
[   12.931059] rtk_btcoex: alloc buffers 1792, 2432 for ev and l2
[   13.618641] Bluetooth: h5_open
[   13.618700] Bluetooth: hci_uart_register_dev
[   13.620833] rtk_btcoex: Open BTCOEX
[   13.620899] rtk_btcoex: create_udpsocket: connect_port: 30001
```

是靠/etc/init.d/S98_lunch_init这个脚本来做的。

```
case "$1" in
  start)
        aplay /usr/lib/silence.wav
        source /oem/RkLunch.sh #这里是启动我们的应用程序的。
        #recovery test
        if [ -e "/oem/rockchip_test/auto_reboot.sh" ]; then
            mkdir /data/cfg/rockchip_test
            cp /oem/rockchip_test/auto_reboot.sh /data/cfg/rockchip_test
        fi
        source /data/cfg/rockchip_test/auto_reboot.sh &
        bt_realtek_start &
```

bt_realtek_start 这个就是启动蓝牙的了。

/usr/bin/bt_realtek_start

```
#!/bin/sh

echo 0 > /sys/class/rfkill/rfkill0/state

sleep 2

echo 1 > /sys/class/rfkill/rfkill0/state

sleep 2

insmod /usr/lib/modules/hci_uart.ko

rtk_hciattach -n -s 115200 /dev/ttyS4 rtk_h5 &

hciconfig hci0 up

/usr/libexec/bluetooth/bluetoothd --compat -n  &
sleep 1
sdptool add A2SNK
sleep 1
hciconfig hci0 up
sleep 1
hciconfig hci0 piscan
sleep 1
hciconfig hci0 name 'realtek_bt'
sleep 1
hciconfig hci0 down
sleep 1
hciconfig hci0 up
sleep 2
bluealsa --profile=a2dp-sink & 
sleep 1
bluealsa-aplay --profile-a2dp 00:00:00:00:00:00 & 
sleep 1
```

但是目前开机后，hciconfig查看，是关闭状态的。

也没有看到蓝牙相关的进程启动。

bt_realtek_start 这个启动会失败的。

而bt_start.sh这个脚本是可以正常启动的。

```
/usr/libexec/bluetooth/bluetoothd --compat -n -d&
#sleep 1
sdptool add A2SNK
#sleep 1
hciconfig hci0 up
sleep 1
hciconfig hci0 piscan
sleep 1
hciconfig hci0 class 0x240404
#sleep 1
#hciconfig hci0 name 'sayinfo_bt'
#sleep 1
hciconfig hci0 down
#sleep 2
hciconfig hci0 up
#sleep 2
bluealsa --profile=a2dp-sink &
sleep 1
bluealsa-aplay --profile-a2dp 00:00:00:00:00:00 &
```

bt_start.sh这个没有明确加载hci_uart.ko啊。

但是执行后，确实hci_uart.ko被加载了。

再重启，看到不执行脚本，默认hci_uart.ko也是被加载的。

那么bt_realtek_start的问题应该就是重复加载的问题了。

而且我当前的版本的bt_realtek_start的后面的带blue的进程启动都被注释掉了。

为什么不一样呢？

external/rkwifibt/bt_realtek_start 这里就是原始的样子。这个后半部分都是注释的。

按道理应该是注释的。

蓝牙地址如果没有配置，会随机生成一个。

```
Realtek Bluetooth ERROR: vendor storage read bt addr failed, generate one
```



ble_wificonfig里的gatt-service.c文件分析



这个打印出来的名字是：

```
printf("gatt-service unique name: %s\n",
				dbus_bus_get_unique_name(connection));
```

```
gatt-service unique name: :1.5
```

这个名字挺奇怪的。

注册的服务：

```
Registered service: /service1
```

发送广播：

```
static void send_advertise(){
        printf("send_advertise\n");
```

板端执行：

```
/usr/libexec/bluetooth/bluetoothd -C &
hciconfig hci0 up
./ble_wificonfig 
```



用nordic connect这个手机app来连接上来。

可以看到有3个服务：

```
1800
	这个是GAP的。存放了蓝牙名字等信息。
1801
	这个是通用属性。
其他
	这个就是真正进行配网的。里面的UUID定义比较随意，没有发现明显规律。
	app也无法解释，所以显示为unknown。
```

![1589012208603](../images/random_name/1589012208603.png)



依次分析最后一个service下面的characteristic。

```
1、device context。
	这个是试图从板端读取设备信息。当前实现是读取/data/property.txt文件。
	当前没有这个文件。
2、获取wifi list。
	这个是从板端获取所有扫描到的wifi热点信息。
	这个比较特殊，因为它支持notify。
	
```







这个长度为什么改了好几次，最后为什么改为134？

```
#define BLE_SEND_MAX_LEN (134) //(20) //(512)
```



参考资料

1、

https://blog.csdn.net/z497544849/article/details/94575987