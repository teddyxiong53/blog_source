---
title: 蓝牙之hcitool
date: 2018-11-28 11:38:05
tags:
	- 蓝牙

---



```
root@raspberrypi:~# hcitool -h
hcitool - HCI Tool ver 5.43
Usage:
        hcitool [options] <command> [command parameters]
Options:
        --help  Display help
        -i dev  HCI device
Commands:
        dev     Display local devices
        inq     Inquire remote devices
        scan    Scan for remote devices
        name    Get name from remote device
        info    Get information from remote device
        spinq   Start periodic inquiry
        epinq   Exit periodic inquiry
        cmd     Submit arbitrary HCI commands
        con     Display active connections
        cc      Create connection to remote device
        dc      Disconnect from remote device
        sr      Switch master/slave role
        cpt     Change connection packet type
        rssi    Display connection RSSI
        lq      Display link quality
        tpl     Display transmit power level
        afh     Display AFH channel map
        lp      Set/display link policy settings
        lst     Set/display link supervision timeout
        auth    Request authentication
        enc     Set connection encryption
        key     Change connection link key
        clkoff  Read clock offset
        clock   Read local or remote clock
        lescan  Start LE scan
        leinfo  Get LE remote information
        lewladd Add device to LE White List
        lewlrm  Remove device from LE White List
        lewlsz  Read size of LE White List
        lewlclr Clear LE White List
        lerladd Add device to LE Resolving List
        lerlrm  Remove device from LE Resolving List
        lerlclr Clear LE Resolving List
        lerlsz  Read size of LE Resolving List
        lerlon  Enable LE Address Resolution
        lerloff Disable LE Address Resolution
        lecc    Create a LE Connection
        ledc    Disconnect a LE Connection
        lecup   LE Connection Update
```

查看本机蓝牙设备。

```
root@raspberrypi:~# hcitool dev
Devices:
        hci1    00:1A:7D:DA:71:13
        hci0    B8:27:EB:AA:E4:60
```

扫描周围的蓝牙。

```
root@raspberrypi:~# hcitool scan
Scanning ...
        D0:31:10:9F:0E:96       n/a
        08:EB:ED:81:FB:86       SoundBox Pro
        64:A2:F9:1F:12:2B       OnePlus 6
        D0:31:10:FE:B7:D2       n/a.lus 6
        FC:58:FA:A8:D3:BE       POP
        18:F0:E4:ED:AC:DA       小米手机
        18:F0:E4:E9:B6:56       小米手机
        08:EB:ED:B6:82:34       SoundBox Pro
        34:D7:12:92:1A:B0       坚果 Pro 2
        B4:0B:44:F4:16:8D       xhl_bt
        50:8F:4C:00:3B:89       红米
```

查询某个蓝牙的信息。

```
root@raspberrypi:~# hcitool info B4:0B:44:F4:16:8D 
Requesting information ...
        BD Address:  B4:0B:44:F4:16:8D
        OUI Company: Smartisan Technology Co., Ltd. (B4-0B-44)
        Device Name: xhl_bt
        LMP Version:  (0x9) LMP Subversion: 0x2be
        Manufacturer: Qualcomm (29)
        Features page 0: 0xff 0xfe 0x8f 0xfe 0xd8 0x3f 0x5b 0x87
                <3-slot packets> <5-slot packets> <encryption> <slot offset> 
                <timing accuracy> <role switch> <hold mode> <sniff mode> 
                <RSSI> <channel quality> <SCO link> <HV2 packets> 
                <HV3 packets> <u-law log> <A-law log> <CVSD> <paging scheme> 
                <power control> <transparent SCO> <broadcast encrypt> 
                <EDR ACL 2 Mbps> <EDR ACL 3 Mbps> <enhanced iscan> 
                <interlaced iscan> <interlaced pscan> <inquiry with RSSI> 
                <extended SCO> <AFH cap. slave> <AFH class. slave> 
                <LE support> <3-slot EDR ACL> <5-slot EDR ACL> 
                <sniff subrating> <pause encryption> <AFH cap. master> 
                <AFH class. master> <EDR eSCO 2 Mbps> <extended inquiry> 
                <LE and BR/EDR> <simple pairing> <encapsulated PDU> 
                <non-flush flag> <LSTO> <inquiry TX power> <EPC> 
                <extended features> 
        Features page 1: 0x0f 0x00 0x00 0x00 0x00 0x00 0x00 0x00
```

查看当前的活跃的连接。

```
root@raspberrypi:~# hcitool con
Connections:
```



hcitool lescan

这个扫描出大量的设备。



参考资料

1、

https://www.cnblogs.com/zjutlitao/p/9576589.html

