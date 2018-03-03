---
title: 树莓派之vcgencmd
date: 2018-03-03 13:26:27
tags:
	- 树莓派

---



https://www.elinux.org/RPI_vcgencmd_usage



vcgencmd不能用`-h`和`--help`来查看帮助信息。很奇葩。

但是用commands子命令可以查看所支持的命令。

```
pi@raspberrypi:~$ vcgencmd commands
commands="vcos, ap_output_control, ap_output_post_processing, vchi_test_init, vchi_test_exit, pm_set_policy, pm_get_status, pm_show_stats, pm_start_logging, pm_stop_logging, version, commands, set_vll_dir, set_backlight, set_logging, get_lcd_info, arbiter, cache_flush, otp_dump, test_result, codec_enabled, get_camera, get_mem, measure_clock, measure_volts, scaling_kernel, scaling_sharpness, get_hvs_asserts, get_throttled, measure_temp, get_config, hdmi_ntsc_freqs, hdmi_adjust_clock, hdmi_status_show, hvs_update_fields, pwm_speedup, force_audio, hdmi_stream_channels, hdmi_channel_map, display_power, read_ring_osc, memtest, dispmanx_list, get_rsts, schmoo, render_bar, disk_notify, inuse_notify, sus_suspend, sus_status, sus_is_enabled, sus_stop_test_thread, egl_platform_switch, mem_validate, mem_oom, mem_reloc_stats, hdmi_cvt, hdmi_timings, file, vctest_memmap, vctest_start, vctest_stop, vctest_set, vctest_get"
```



显示电压，默认就是查询core的电压。

```
pi@raspberrypi:~$ vcgencmd measure_volts
volt=1.3188V
pi@raspberrypi:~$ vcgencmd measure_volts core
volt=1.3188V
pi@raspberrypi:~$ vcgencmd measure_volts sdram_c
volt=1.2000V
pi@raspberrypi:~$ vcgencmd measure_volts sdram_i
volt=1.2000V
pi@raspberrypi:~$ vcgencmd measure_volts sdram_p
volt=1.2250V
```

可以查询的有：

```
arm, core, h264, isp, v3d, uart, pwm, emmc, pixel, vec, hdmi, dpi
```



显示温度

```
pi@raspberrypi:~$ vcgencmd measure_temp
temp=49.9'C
```



查看内存，要sudo权限。

```
pi@raspberrypi:~$ vcgencmd get_mem
error=2 error_msg="Invalid arguments"
pi@raspberrypi:~$ sudo vcgencmd get_mem arm
arm=944M
```



查看gpu内存。

```
pi@raspberrypi:~$ sudo vcgencmd get_mem gpu
gpu=64M
```



查看配置。

```
pi@raspberrypi:~$ sudo vcgencmd get_config
get_config [config|int|str]
pi@raspberrypi:~$ sudo vcgencmd get_config int
arm_freq=1200
audio_pwm_mode=1
config_hdmi_boost=5
core_freq=250
desired_osc_freq=0x36ee80
disable_commandline_tags=2
disable_l2cache=1
enable_uart=1
force_eeprom_read=1
force_pwm_open=1
framebuffer_ignore_alpha=1
framebuffer_swap=1
gpu_freq=300
hdmi_force_cec_address=65535
init_uart_clock=0x2dc6c00
lcd_framerate=60
over_voltage_avs=0x1cfde
overscan_bottom=32
overscan_left=32
overscan_right=32
overscan_top=32
pause_burst_frames=1
program_serial_random=1
program_usb_boot_mode=1
sdram_freq=450
temp_limit=85
```

