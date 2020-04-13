---
title: Android刷机之magisk
date: 2020-04-08 11:29:51
tags:
	- Android

---

1

https://github.com/topjohnwu/Magisk

这个是一个kotlin写的app，代码量不大，只有不到700个文件。

在Android8.0以后，比较通用的root方法就是使用magisk工具进行破解。

破解的流程是：

1、解锁bootloader。或者通过特殊的方法绕过avb验证。

解锁后在启动过程如果出现镜像校验失败也会继续启动，因此就可以刷入非官方镜像。

2、从官方的update包里提取出boot.img。通过magisk工具对boot.img打补丁。

3、把boot.img刷入手机，就完成了root。后续可以在magisk里进行root权限管理。

我手里一台用magisk root过的LG G7，进入shell（shell在magisk保证授权了root权限）。查看mount。可以看到内容非常多。绝大部分都是magisk进行 的mount。很精准地对每个文件进行 了mount。



```
/dev/root on / type ext4 (ro,seclabel,relatime,block_validity,delalloc,barrier,user_xattr)
/dev/block/sde4 on /vendor/firmware_mnt type vfat (ro,context=u:object_r:firmware_file:s0,relatime,gid=1000,fmask=0337,dmask=0227,codepage=437,iocharset=iso8859-1,shortname=lower,errors=remount-ro)
/dev/block/sde8 on /vendor/dsp type ext4 (ro,seclabel,nosuid,nodev,relatime,data=ordered)
/dev/block/sda5 on /mnt/vendor/persist type ext4 (rw,seclabel,nosuid,nodev,noatime,data=ordered)
/dev/block/sda15 on /mnt/product/els type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,errors=continue,data=ordered)
/dev/block/sda3 on /mnt/vendor/sns type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,errors=continue,data=ordered)
/dev/block/sda2 on /mnt/vendor/persist-lg type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,errors=continue,data=ordered)
/dev/block/sda1 on /mnt/vendor/mpt type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,errors=continue,data=ordered)
/dev/block/sda13 on /mnt/product/srtc type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,errors=continue,data=ordered)
/dev/block/sda8 on /mnt/vendor/power type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,errors=continue,data=ordered)
/dev/block/sda12 on /mnt/product/fota type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,data=ordered)
/dev/block/sda16 on /mnt/product/quality type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,data=ordered)
/dev/block/sda17 on /mnt/vendor/eri type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,data=ordered)
tmpfs on /storage type tmpfs (rw,seclabel,nosuid,nodev,noexec,relatime,size=1852672k,nr_inodes=463168,mode=755,gid=1000)
adb on /dev/usb-ffs/adb type functionfs (rw,relatime)
/dev/block/sda23 on /data type ext4 (rw,seclabel,nosuid,nodev,noatime,noauto_da_alloc,resgid=1065,data=ordered)
```

查看/dev/block/by-name下面的分区结构。

```
ALIGN_TO_128K_1 -> /dev/block/sdd1                 
ALIGN_TO_128K_2 -> /dev/block/sdf1                 
abl_a -> /dev/block/sde7                           
abl_b -> /dev/block/sde28                          
akmu_a -> /dev/block/sde10                         
akmu_b -> /dev/block/sde31                         
aop_a -> /dev/block/sde1                           
aop_b -> /dev/block/sde22                          
apdp -> /dev/block/sde46                           
boot_a -> /dev/block/sde11                         
boot_b -> /dev/block/sde32                         
carrier -> /dev/block/sda18                        
cdt -> /dev/block/sdd2                             
cmnlib64_a -> /dev/block/sde13                     
cmnlib64_b -> /dev/block/sde34                     
cmnlib_a -> /dev/block/sde12                       
cmnlib_b -> /dev/block/sde33                       
ddr -> /dev/block/sdd3                             
devcfg_a -> /dev/block/sde14                       
devcfg_b -> /dev/block/sde35                       
devinfo -> /dev/block/sde44                        
dip -> /dev/block/sde45                            
drm -> /dev/block/sda2                             
dsp_a -> /dev/block/sde8                           
dsp_b -> /dev/block/sde29                          
dtbo_a -> /dev/block/sde18                         
dtbo_b -> /dev/block/sde39                         
eksst -> /dev/block/sda10                          
els -> /dev/block/sda15                            
encrypt -> /dev/block/sda9                         
eri -> /dev/block/sda17                            
fota -> /dev/block/sda12                           
frp -> /dev/block/sdg1                             
fsc -> /dev/block/sdf5                             
fsg -> /dev/block/sdf4                             
ftm -> /dev/block/sda7                             
grow -> /dev/block/sda24                           
hyp_a -> /dev/block/sde3                           
hyp_b -> /dev/block/sde24                          
keymaster_a -> /dev/block/sde9                     
keymaster_b -> /dev/block/sde30                    
laf_a -> /dev/block/sde16                          
laf_b -> /dev/block/sde37                          
limits -> /dev/block/sde49                         
logdump -> /dev/block/sde53                        
logfs -> /dev/block/sde51                          
mdtp_a -> /dev/block/sde6                          
mdtp_b -> /dev/block/sde27                         
mdtpsecapp_a -> /dev/block/sde5                    
mdtpsecapp_b -> /dev/block/sde26                   
misc -> /dev/block/sda6                            
modem_a -> /dev/block/sde4                         
modem_b -> /dev/block/sde25                        
modemst1 -> /dev/block/sdf2                        
modemst2 -> /dev/block/sdf3                        
mpt -> /dev/block/sda1                             
msadp -> /dev/block/sde47                          
operatorlogging -> /dev/block/sda16                
persist -> /dev/block/sda5                         
power -> /dev/block/sda8                           
pstore -> /dev/block/sda14                         
qupfw_a -> /dev/block/sde15                        
qupfw_b -> /dev/block/sde36                        
raw_resources_a -> /dev/block/sde20                
raw_resources_b -> /dev/block/sde41                
rct -> /dev/block/sda11                            
sec -> /dev/block/sde43                            
sid_a -> /dev/block/sde21                          
sid_b -> /dev/block/sde42                          
sns -> /dev/block/sda3                             
spunvm -> /dev/block/sde48                         
srtc -> /dev/block/sda13                           
ssd -> /dev/block/sda4                             
sti -> /dev/block/sde52                            
storsec_a -> /dev/block/sde19                      
storsec_b -> /dev/block/sde40                      
system_a -> /dev/block/sda21                       
system_b -> /dev/block/sda22                       
toolsfv -> /dev/block/sde50                        
tz_a -> /dev/block/sde2                            
tz_b -> /dev/block/sde23                           
userdata -> /dev/block/sda23                       
vbmeta_a -> /dev/block/sde17                       
vbmeta_b -> /dev/block/sde38                       
vendor_a -> /dev/block/sda19                       
vendor_b -> /dev/block/sda20                       
xbl_a -> /dev/block/sdb1                           
xbl_b -> /dev/block/sdc1                           
xbl_config_a -> /dev/block/sdb2                    
xbl_config_b -> /dev/block/sdc2                    
```

查看cmdline

```
judyln:/dev/block/by-name # cat /proc/cmdline
rcupdate.rcu_expedited=1 video=vfb:640x400,bpp=32,memsize=3072000 msm_rtb.filter=0x237 ehci-hcd.park=3 lpm_levels.sleep_disabled=1 service_locator.enable=1 swiotlb=2048 androidboot.configfs=true firmware_class.path=/vendor/firmware_mnt/image loop.max_part=7 androidboot.usbcontroller=a600000.dwc3 ignore_loglevel androidboot.hardware=judyln buildvariant=user kswitch androidboot.dlcomplete=0 androidboot.product.lge.bootreasoncode=0x0 lge.bootreason=NORMAL_MODE androidboot.vendor.lge.hw.revision=rev_10 androidboot.vendor.lge.hw.subrev=subrev_2 androidboot.vendor.lge.hw.cable=NO_INIT androidboot.vendor.lge.plmn=VZW_POSTPAID androidboot.product.lge.ddr_size=4262068224 androidboot.vendor.lge.ddr_info=0x11000506 lge.crash_handler=off androidboot.product.lge.hiddenreset=0 androidboot.product.lge.device_color=BK androidboot.revision=12 androidboot.vendor.lge.fingerprint_sensor=1 androidboot.vendor.lge.gyro=1 androidboot.vendor.lge.nfc.vendor=nxp androidboot.vendor.lge.dtv=0 androidboot.vendor.lge.fmradio=1 androidboot.vendor.lge.wmc=2 androidboot.vendor.lge.capsensor=1 androidboot.vendor.lge.hydra=Prime androidboot.vendor.lge.ant_rev=NA_CDMA androidboot.vendor.lge.ant_match=TRUE androidboot.vendor.lge.model.name=LM-G710VM androidboot.vendor.lge.id=0 wled_strings=0,1,2,3 androidboot.verifiedbootstate=orange androidboot.keymaster=1 dm="1 vroot none ro 1,0 8256088 verity 1 PARTUUID=77942275-b238-ef63-9a3e-e95c5c8e6e2d PARTUUID=77942275-b238-ef63-9a3e-e95c5c8e6e2d 4096 4096 1032011 1032011 sha1 1a1982c0bcf36307d443c02ffd0c0d318c843ac8 bb750e831ee3d1c9449060522137c0985efba8b44ace631957f68db49c98195e 10 restart_on_corruption ignore_zero_blocks use_fec_from_device PARTUUID=77942275-b238-ef63-9a3e-e95c5c8e6e2d fec_roots 2 fec_blocks 1040138 fec_start 1040138" root=/dev/dm-0 androidboot.vbmeta.device=PARTUUID=c07f1c2f-442e-449f-64d5-55a1c94f71a1 androidboot.vbmeta.avb_version=1.0 androidboot.vbmeta.device_state=unlocked androidboot.vbmeta.hash_alg=sha256 androidboot.vbmeta.size=3264 androidboot.vbmeta.digest=7a7ecee53ff574b7ae31a3f41cd330454dba23ada9265091af625f7f07e81ea3 androidboot.vbmeta.invalidate_on_error=yes androidboot.veritymode=enforcing androidboot.bootdevice=1d84000.ufshc androidboot.serialno=LMG710VMfd7de137 androidboot.baseband=msm msm_drm.dsi_display0=dsi_sw49410_rev1_dsc_1440_3120_cmd_display: androidboot.slot_suffix=_a skip_initramfs rootwait ro init=/init  androidboot.dtbo_idx=1
```



sda有24个分区。

sdb有2个分区。

sdc有2个分区。

sdd有3个分区。

sde有53个分区。

sdf有5个分区。

sdg有1个分区。



参考资料

1、Magisk root 原理分析之一 ：Magisk Andorid Root 流程

https://blog.csdn.net/pen_cil/article/details/102872285