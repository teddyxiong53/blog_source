---
title: amlogic之uboot分析
date: 2021-05-12 09:59:34
tags:
	- amlogic
---

--

printenv得到的输出

```
EnableSelinux=enforcing
active_slot=normal
aml_dt=axg_s400_v03
baudrate=115200
bcb_cmd=get_valid_slot;
boot_part=boot
bootargs=init=/init console=ttyS0,115200 no_console_suspend earlycon=aml_uart,0xff803000 ramoops.pstore_en=1 ramoops.record_size=0x8000 ramoops.console_size=0x4000 reboot_mode_android=normal logo=osd0,loaded,0x3d800000 vout=panel,enable panel_type=lcd_0 lcd_ctrl=0x00000083 osd_reverse=0 video_reverse=0 androidboot.selinux=enforcing androidboot.firstboot=1 jtag=disable androidboot.hardware=amlogic androidboot.bootloader=01.01.210511.172127 androidboot.build.expect.baseband=N/A androidboot.serialno=AMLA113DS400001
bootcmd=run storeboot
bootdelay=1
bootloader_version=01.01.210511.172127
cmdline_keys=if keyman init 0x1234; then if keyman read usid ${loadaddr} str; then setenv bootargs ${bootargs} androidboot.serialno=${usid};setenv serial ${usid};else setenv bootargs ${bootargs} androidboot.serialno=1234567890;setenv serial 1234567890;fi;if keyman read mac ${loadaddr} str; then setenv bootargs ${bootargs} mac=${mac} androidboot.mac=${mac};fi;if keyman read deviceid ${loadaddr} str; then setenv bootargs ${bootargs} androidboot.deviceid=${deviceid};fi;fi;
cvbs_drv=0
cvbsmode=576cvbs
display_bpp=16
display_color_bg=0
display_color_fg=0xffff
display_color_index=16
display_height=1024
display_layer=osd0
display_width=768
dtb_mem_addr=0x1000000
ethact=dwmac.ff3f0000
ethaddr=02:99:37:47:db:b9
factory_reset_poweroff_protect=echo wipe_data=${wipe_data}; echo wipe_cache=${wipe_cache};if test ${wipe_data} = failed; then run init_display; run storeargs;if mmcinfo; then run recovery_from_sdcard;fi;if usb start 0; then run recovery_from_udisk;fi;run recovery_from_flash;fi; if test ${wipe_cache} = failed; then run init_display; run storeargs;if mmcinfo; then run recovery_from_sdcard;fi;if usb start 0; then run recovery_from_udisk;fi;run recovery_from_flash;fi; 
fb_addr=0x3d800000
fb_height=1024
fb_width=768
fdt_high=0x20000000
firstboot=1
fs_type=rootfstype=ramfs
gatewayip=10.18.9.1
hdmimode=1080p60hz
hostname=arm_gxbb
init_display=get_rebootmode;echo reboot_mode:::: ${reboot_mode};if test ${reboot_mode} = quiescent; then setenv reboot_mode_android quiescent;run storeargs;setenv bootargs ${bootargs} androidboot.quiescent=1;osd open;osd clear;else if test ${reboot_mode} = recovery_quiescent; then setenv reboot_mode_android quiescent;run storeargs;setenv bootargs ${bootargs} androidboot.quiescent=1;osd open;osd clear;else setenv reboot_mode_android normal;run storeargs;osd open;osd clear;imgread pic logo bootup $loadaddr;bmp display $bootup_offset;bmp scale;vout output ${outputmode};fi;fi;
initargs=init=/init console=ttyS0,115200 no_console_suspend earlycon=aml_uart,0xff803000 ramoops.pstore_en=1 ramoops.record_size=0x8000 ramoops.console_size=0x4000 
initrd_high=3e000000
ipaddr=10.18.9.97
irremote_update=if irkey 2500000 0xe31cfb04 0xb748fb04; then echo read irkey ok!; if itest ${irkey_value} == 0xe31cfb04; then run update;else if itest ${irkey_value} == 0xb748fb04; then run update;\
fi;fi;fi;
jtag=disable
lcd_ctrl=0x00000083
loadaddr=1080000
lock=10101000
netmask=255.255.255.0
osd_reverse=0
outputmode=panel
panel_type=lcd_0
partiton_mode=normal
preboot=run bcb_cmd; run factory_reset_poweroff_protect;run upgrade_check;i2c mw 1f 3.1 0 2;i2c mw 1f 1.1 fc 2;run init_display;run storeargs;run switch_bootmode;
reboot_mode=cold_boot
reboot_mode_android=normal
recovery_from_flash=setenv bootargs ${bootargs} ${fs_type} aml_dt=${aml_dt} recovery_part={recovery_part} recovery_offset={recovery_offset};if imgread kernel ${recovery_part} ${loadaddr} ${recovery_offset}; then wipeisb; bootm ${loadaddr}; fi;
recovery_from_sdcard=if fatload mmc 0 ${loadaddr} aml_autoscript; then autoscr ${loadaddr}; fi;if fatload mmc 0 ${loadaddr} recovery.img; then if fatload mmc 0 ${dtb_mem_addr} dtb.img; then echo sd dtb.img loaded; fi;wipeisb; setenv bootargs ${bootargs} ${fs_type};bootm ${loadaddr};fi;
recovery_from_udisk=if fatload usb 0 ${loadaddr} aml_autoscript; then autoscr ${loadaddr}; fi;if fatload usb 0 ${loadaddr} recovery.img; then if fatload usb 0 ${dtb_mem_addr} dtb.img; then echo udisk dtb.img loaded; fi;wipeisb; setenv bootargs ${bootargs} ${fs_type};bootm ${loadaddr};fi;
recovery_offset=0
recovery_part=recovery
rpmb_state=0
sdc_burning=sdc_burn ${sdcburncfg}
sdcburncfg=aml_sdc_burn.ini
serial=AMLA113DS400001
serverip=10.18.9.113
slot-suffixes=-1
stderr=serial
stdin=serial
stdout=serial
storeargs=get_bootloaderversion;setenv bootargs ${initargs} reboot_mode_android=${reboot_mode_android} logo=${display_layer},loaded,${fb_addr} vout=${outputmode},enable panel_type=${panel_type} lcd_ctrl=${lcd_ctrl} osd_reverse=${osd_reverse} video_reverse=${video_reverse} androidboot.selinux=${EnableSelinux} androidboot.firstboot=${firstboot} jtag=${jtag}; setenv bootargs ${bootargs} androidboot.hardware=amlogic androidboot.bootloader=${bootloader_version} androidboot.build.expect.baseband=N/A;run cmdline_keys;
storeboot=get_system_as_root_mode;echo system_mode: ${system_mode};if test ${system_mode} = 1; then setenv bootargs ${bootargs} ro rootwait skip_initramfs;else setenv bootargs ${bootargs} ${fs_type};fi;if imgread kernel ${boot_part} ${loadaddr}; then bootm ${loadaddr}; fi;run storeargs;run update;
switch_bootmode=get_rebootmode;if test ${reboot_mode} = factory_reset; then setenv reboot_mode_android normal;run storeargs;run recovery_from_flash;else if test ${reboot_mode} = update; then setenv reboot_mode_android normal;run storeargs;run update;else if test ${reboot_mode} = quiescent; then setenv reboot_mode_android quiescent;run storeargs;setenv bootargs ${bootargs} androidboot.quiescent=1;else if test ${reboot_mode} = recovery_quiescent; then setenv reboot_mode_android quiescent;run storeargs;setenv bootargs ${bootargs} androidboot.quiescent=1;run recovery_from_flash;else if test ${reboot_mode} = cold_boot; then setenv reboot_mode_android normal;run storeargs;else if test ${reboot_mode} = fastboot; then setenv reboot_mode_android normal;run storeargs;fastboot;fi;fi;fi;fi;fi;fi;
try_auto_burn=update 700 750;
update=run usb_burning; run sdc_burning; if mmcinfo; then run recovery_from_sdcard;fi;if usb start 0; then run recovery_from_udisk;fi;run recovery_from_flash;
upgrade_check=echo recovery_status=${recovery_status};if itest.s "${recovery_status}" == "in_progress"; then run storeargs; run recovery_from_flash;else fi;echo upgrade_step=${upgrade_step}; if itest ${upgrade_step} == 3; then run init_display; run storeargs; run update;else fi;
upgrade_key=if gpio input GPIOAO_3; then echo detect upgrade key; run update;fi;
upgrade_step=2
usb_burning=update 1000
usid=AMLA113DS400001
video_reverse=0
wipe_cache=successful
wipe_data=successful

```



参考资料

1、

