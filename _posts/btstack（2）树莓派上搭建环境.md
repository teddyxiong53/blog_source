---
title: btstack（2）树莓派上搭建环境
date: 2018-12-20 11:50:35
tags:
	- 蓝牙
---



我的树莓派蓝牙目前工作是正常的。

要使用这个btstack，就需要把bluez给禁用掉。

方法如下：

```
sudo systemctl stop hciuart
sudo systemctl stop bthelper
sudo systemctl stop bluetooth
```

如果要恢复bluez。重启一下系统是最快的方式。

然后在port/raspi目录下，make -j4 。

运行le_counter。

```
pi@raspberrypi:~/work/bt/btstack-master/port/raspi$ sudo ./le_counter 
Packet Log: /tmp/hci_dump.pklg
Hardware UART without flowcontrol, 921600 baud, H5, BT_REG_EN at GPIOO 128
Phase 1: Download firmware
Phase 2: Main app
BTstack counter 0001
BTstack up and running at B8:27:EB:AA:E4:60
```

手机上用nordic connect软件连接上来。蓝牙名字是le_counter。

手机上点击notify，可以看到打印。

```
pi@raspberrypi:~/work/bt/btstack-master/port/raspi$ sudo ./le_counter 
Packet Log: /tmp/hci_dump.pklg
Hardware UART without flowcontrol, 921600 baud, H5, BT_REG_EN at GPIOO 128
Phase 1: Download firmware
Phase 2: Main app
BTstack counter 0001
BTstack up and running at B8:27:EB:AA:E4:60
BTstack counter 0002
BTstack counter 0003
BTstack counter 0004
BTstack counter 0005
BTstack counter 0006
BTstack counter 0007
BTstack counter 0008
BTstack counter 0009
BTstack counter 0010
BTstack counter 0011
BTstack counter 0012
```

分析一下这个程序的代码。

在/tmp目录下会生成一个文件。不知道具体用途。

```
#define DB_PATH_TEMPLATE (LE_DEVICE_DB_PATH "btstack_at_%s_le_device_db.txt")
```

profile_data这个怎么来的？

看compile_gatt.py生成的。所以是需要编译后才能看到的。

```
./example/Makefile.inc:198:     python ${BTSTACK_ROOT}/tool/compile_gatt.py $< $@
```

是这个样子的。

```
const uint8_t profile_data[] =
{
    // ATT DB Version
    1,

    // 0x0001 PRIMARY_SERVICE-GAP_SERVICE
    0x0a, 0x00, 0x02, 0x00, 0x01, 0x00, 0x00, 0x28, 0x00, 0x18, 
    // 0x0002 CHARACTERISTIC-GAP_DEVICE_NAME-READ
    0x0d, 0x00, 0x02, 0x00, 0x02, 0x00, 0x03, 0x28, 0x02, 0x03, 0x00, 0x00, 0x2a, 
    // 0x0003 VALUE-GAP_DEVICE_NAME-READ-'LE Counter'
    // READ_ANYBODY
    0x12, 0x00, 0x02, 0x00, 0x03, 0x00, 0x00, 0x2a, 0x4c, 0x45, 0x20, 0x43, 0x6f, 0x75, 0x6e, 0x74, 0x65, 0x72, 
    // add Battery Service
    // #import <battery_service.gatt> -- BEGIN
    // Specification Type org.bluetooth.service.battery_service
    // https://www.bluetooth.com/api/gatt/xmlfile?xmlFileName=org.bluetooth.service.battery_service.xml
    // Battery Service 180F

    // 0x0004 PRIMARY_SERVICE-ORG_BLUETOOTH_SERVICE_BATTERY_SERVICE
    0x0a, 0x00, 0x02, 0x00, 0x04, 0x00, 0x00, 0x28, 0x0f, 0x18, 
    // 0x0005 CHARACTERISTIC-ORG_BLUETOOTH_CHARACTERISTIC_BATTERY_LEVEL-DYNAMIC | READ | NOTIFY
    0x0d, 0x00, 0x02, 0x00, 0x05, 0x00, 0x03, 0x28, 0x12, 0x06, 0x00, 0x19, 0x2a, 
    // 0x0006 VALUE-ORG_BLUETOOTH_CHARACTERISTIC_BATTERY_LEVEL-DYNAMIC | READ | NOTIFY-''
    // READ_ANYBODY
    0x08, 0x00, 0x02, 0x01, 0x06, 0x00, 0x19, 0x2a, 
    // 0x0007 CLIENT_CHARACTERISTIC_CONFIGURATION
    // READ_ANYBODY, WRITE_ANYBODY
    0x0a, 0x00, 0x0e, 0x01, 0x07, 0x00, 0x02, 0x29, 0x00, 0x00, 
    // #import <battery_service.gatt> -- END

    // 0x0008 PRIMARY_SERVICE-GATT_SERVICE
    0x0a, 0x00, 0x02, 0x00, 0x08, 0x00, 0x00, 0x28, 0x01, 0x18, 
    // 0x0009 CHARACTERISTIC-GATT_SERVICE_CHANGED-READ
    0x0d, 0x00, 0x02, 0x00, 0x09, 0x00, 0x03, 0x28, 0x02, 0x0a, 0x00, 0x05, 0x2a, 
    // 0x000a VALUE-GATT_SERVICE_CHANGED-READ-''
    // READ_ANYBODY
    0x08, 0x00, 0x02, 0x00, 0x0a, 0x00, 0x05, 0x2a, 
    // Counter Service

    // 0x000b PRIMARY_SERVICE-0000FF10-0000-1000-8000-00805F9B34FB
    0x18, 0x00, 0x02, 0x00, 0x0b, 0x00, 0x00, 0x28, 0xfb, 0x34, 0x9b, 0x5f, 0x80, 0x00, 0x00, 0x80, 0x00, 0x10, 0x00, 0x00, 0x10, 0xff, 0x00, 0x00, 
    // Counter Characteristic, with read and notify
    // 0x000c CHARACTERISTIC-0000FF11-0000-1000-8000-00805F9B34FB-READ | NOTIFY | DYNAMIC
    0x1b, 0x00, 0x02, 0x00, 0x0c, 0x00, 0x03, 0x28, 0x12, 0x0d, 0x00, 0xfb, 0x34, 0x9b, 0x5f, 0x80, 0x00, 0x00, 0x80, 0x00, 0x10, 0x00, 0x00, 0x11, 0xff, 0x00, 0x00, 
    // 0x000d VALUE-0000FF11-0000-1000-8000-00805F9B34FB-READ | NOTIFY | DYNAMIC-''
    // READ_ANYBODY
    0x16, 0x00, 0x02, 0x03, 0x0d, 0x00, 0xfb, 0x34, 0x9b, 0x5f, 0x80, 0x00, 0x00, 0x80, 0x00, 0x10, 0x00, 0x00, 0x11, 0xff, 0x00, 0x00, 
    // 0x000e CLIENT_CHARACTERISTIC_CONFIGURATION
    // READ_ANYBODY, WRITE_ANYBODY
    0x0a, 0x00, 0x0e, 0x01, 0x0e, 0x00, 0x02, 0x29, 0x00, 0x00, 

    // END
    0x00, 0x00, 
}; // total size 122 bytes 

```



一个service对应的结构体是：

```
typedef struct att_service_handler {
    btstack_linked_item_t * item;
    uint16_t start_handle;
    uint16_t end_handle;
    att_read_callback_t read_callback;
    att_write_callback_t write_callback;
    btstack_packet_handler_t packet_handler;
} att_service_handler_t;
```

电池电量可以读到，是一个加的，也是读一次就减1的。

```
    // simulate battery drain
    battery--;
    if (battery < 50) {
        battery = 100;
    }
```

有必要看看一下编译的过程。

chipset这个目录也需要关注。

brm是树莓派用到的。

这个代码就是用到这里的。

```
        // phase #1 download firmware
        printf("Phase 1: Download firmware\n");

        // phase #2 start main app
        btstack_chipset_bcm_download_firmware(uart_driver, transport_config.baudrate_main, &phase2);

```

把gatt文件转成h文件。

```
# compile .gatt descriptions
%.h: %.gatt
	python ${BTSTACK_ROOT}/tool/compile_gatt.py $< $@
```

我们看看le_counter.gatt这个文件怎么写的。

```

```

