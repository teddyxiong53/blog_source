---
title: WiFi之wpa_cli工具用法
date: 2018-06-10 00:37:32
tags:
	- WiFi

---



wp_cli的交互模式的用法。

1、输入wpa_cli。不带任何参数，就会进入到交互模式。

有tab补全功能。

下面是连接到一个网络的做法。

killall wpa_supplicant

wpa_supplicant -i wlan0 -B -c /etc/wpa_supplicant/wpa_supplicant.conf

wpa_supplicant.conf文件里的内容是：

```
ctrl_interface=/var/run/wpa_supplicant
update_config=1
```

只有这2行。不要多东西。

```
> scan
OK
<3>CTRL-EVENT-SCAN-STARTED 
<3>CTRL-EVENT-SCAN-RESULTS 
<3>WPS-AP-AVAILABLE 
> add_network 
0
> set_network 0 ssid "xhl"
OK
> set_network 0 psk "1234567890"
OK
> enable_network 0
OK
<3>CTRL-EVENT-SCAN-STARTED 
<3>CTRL-EVENT-SCAN-RESULTS 
<3>WPS-AP-AVAILABLE 
<3>Trying to associate with 68:db:54:ba:88:ed (SSID='xhl' freq=2412 MHz)
<3>Associated with 68:db:54:ba:88:ed
<3>WPA: Key negotiation completed with 68:db:54:ba:88:ed [PTK=CCMP GTK=TKIP]
<3>CTRL-EVENT-CONNECTED - Connection to 68:db:54:ba:88:ed completed [id=0 id_str=]
> status
bssid=68:db:54:ba:88:ed
freq=2412
ssid=xhl
id=0
mode=station
pairwise_cipher=CCMP
group_cipher=TKIP
key_mgmt=WPA2-PSK
wpa_state=COMPLETED
ip_address=192.168.0.120
p2p_device_address=b8:27:eb:55:1b:9f
address=b8:27:eb:55:1b:9f
uuid=0a4c5abd-a7e2-5c26-9427-4d2856ce6337
> save_config 
OK
> 
> quit 
```

然后看wpa_supplicant.conf内容。

```
$cat wpa_supplicant.conf
ctrl_interface=/var/run/wpa_supplicant
update_config=1

network={
        ssid="xhl"
        psk="1234567890"
}
```

现在网络就配置好了。可以跟路由器连接上了。

# 总结

下面总结一下，我现在要连上路由器。需要做的步骤：

1、wpa_supplicant -i wlan0 -B -c /etc/wpa_supplicant/wpa_supplicant.conf

2、wpa_cli reconfigure

3、sudo ifconfig 192.168.0.200 netmask 255.255.255.0



wpa_cli下面的子命令有136条。

```
> 
Display all 136 possibilities? (y or n)
add_cred                  p2p_cancel                resume
add_network               p2p_connect               roam
all_sta                   p2p_ext_listen            save_config
ap_scan                   p2p_find                  scan
autoscan                  p2p_flush                 scan_interval
blacklist                 p2p_get_passphrase        scan_results
bss                       p2p_group_add             select_network
bss_expire_age            p2p_group_remove          set
bss_expire_count          p2p_invite                set_cred
bss_flush                 p2p_listen                set_network
bssid                     p2p_peer                  signal_poll
chan_switch               p2p_peers                 sim
deauthenticate            p2p_presence_req          sta
disable_network           p2p_prov_disc             sta_autoconnect
disassociate              p2p_reject                status
disconnect                p2p_remove_client         stkstart
dup_network               p2p_serv_disc_cancel_req  suspend
enable_network            p2p_serv_disc_external    tdls_discover
flush                     p2p_serv_disc_req         tdls_setup
ft_ds                     p2p_serv_disc_resp        tdls_teardown
get                       p2p_service_add           terminate
get_capability            p2p_service_del           vendor
get_cred                  p2p_service_flush         wfd_subelem_get
get_network               p2p_service_update        wfd_subelem_set
help                      p2p_set                   wnm_bss_query
ibss_rsn                  p2p_stop_find             wnm_sleep
identity                  p2p_unauthorize           wps_ap_pin
ifname                    passphrase                wps_cancel
interface                 password                  wps_check_pin
interface_add             pin                       wps_er_config
interface_list            ping                      wps_er_learn
interface_remove          pktcnt_poll               wps_er_nfc_config_token
level                     pmksa                     wps_er_pbc
license                   pmksa_flush               wps_er_pin
list_creds                preauthenticate           wps_er_set_config
list_networks             quit                      wps_er_start
log_level                 radio_work                wps_er_stop
logoff                    raw                       wps_nfc
logon                     reassociate               wps_nfc_config_token
mib                       reattach                  wps_nfc_tag_read
new_password              reauthenticate            wps_nfc_token
nfc_get_handover_req      reconfigure               wps_pbc
nfc_get_handover_sel      reconnect                 wps_pin
nfc_report_handover       relog                     wps_reg
note                      remove_cred               
otp                       remove_network            
> 

```

