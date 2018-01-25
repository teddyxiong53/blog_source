---
title: Android启动打印
date: 2018-01-25 21:12:12
tags:
	- Android系统

---



下面的打印是AVD设备，pixel启动的打印。

可以看一下，分析一下启动过程。

```

01-25 13:05:21.970 1172-1172/? I/auditd: type=1403 audit(0.0:2): policy loaded auid=4294967295 ses=4294967295
01-25 13:05:21.970 1172-1172/? W/auditd: type=1404 audit(0.0:3): enforcing=1 old_enforcing=0 auid=4294967295 ses=4294967295
                                         
                                         --------- beginning of system
01-25 13:05:22.562 1173-1173/? I/vold: Vold 3.0 (the awakening) firing up
01-25 13:05:22.562 1173-1173/? V/vold: Detected support for: ext4 vfat
01-25 13:05:22.912 1187-1187/? I/qemu-props: connected to 'boot-properties' qemud service.
01-25 13:05:22.913 1187-1187/? I/qemu-props: receiving..
01-25 13:05:22.913 1187-1187/? I/qemu-props: received: qemu.sf.fake_camera=both
01-25 13:05:22.914 1187-1187/? I/qemu-props: receiving..
01-25 13:05:22.914 1187-1187/? I/qemu-props: received: ro.opengles.version=131072
01-25 13:05:22.915 1187-1187/? I/qemu-props: receiving..
01-25 13:05:22.915 1187-1187/? I/qemu-props: received: dalvik.vm.heapsize=256m
01-25 13:05:22.915 1187-1187/? I/qemu-props: receiving..
01-25 13:05:22.916 1187-1187/? I/qemu-props: received: qemu.hw.mainkeys=0
01-25 13:05:22.916 1187-1187/? I/qemu-props: receiving..
01-25 13:05:22.916 1187-1187/? I/qemu-props: received: qemu.sf.lcd_density=480
01-25 13:05:22.917 1187-1187/? I/qemu-props: receiving..
01-25 13:05:22.917 1187-1187/? I/qemu-props: exiting (5 properties set).
01-25 13:05:23.049 1173-1201/? D/vold: Recognized experimental block major ID 253 as virtio-blk (emulator's virtual SD card device)
01-25 13:05:23.049 1173-1201/? V/vold: /system/bin/sgdisk
01-25 13:05:23.049 1173-1201/? V/vold:     --android-dump
01-25 13:05:23.049 1173-1201/? V/vold:     /dev/block/vold/disk:253,48
                                       
                                       [ 01-25 13:05:23.130  1193: 1193 I/         ]
                                       debuggerd: Jan 11 2016 06:33:54
01-25 13:05:23.145 1184-1184/? I/lowmemorykiller: Using in-kernel low memory killer interface
01-25 13:05:23.146 1198-1198/? I/installd: installd firing up
01-25 13:05:23.160 1192-1192/? I/Netd: Netd 1.0 starting
01-25 13:05:23.167 1192-1192/? D/TetherController: Setting IP forward enable = 0
01-25 13:05:23.168 1242-1242/? I/fingerprintd: Starting fingerprintd
01-25 13:05:23.192 1204-1204/? I/gatekeeperd: Starting gatekeeperd...
01-25 13:05:23.205 1204-1204/? W/gatekeeperd: falling back to software GateKeeper
01-25 13:05:23.431 1186-1186/? I/SurfaceFlinger: SurfaceFlinger is starting
01-25 13:05:23.431 1186-1186/? I/SurfaceFlinger: SurfaceFlinger's main thread ready to run. Initializing graphics H/W...
01-25 13:05:23.444 1186-1186/? E/libEGL: load_driver(/system/lib/egl/libGLES_emulation.so): dlopen failed: library "/system/lib/egl/libGLES_emulation.so" not found
01-25 13:05:23.465 1186-1186/? D/libEGL: loaded /system/lib/egl/libEGL_emulation.so
01-25 13:05:23.466 1186-1186/? D/libEGL: loaded /system/lib/egl/libGLESv1_CM_emulation.so
01-25 13:05:23.469 1186-1186/? D/libEGL: loaded /system/lib/egl/libGLESv2_emulation.so
                                         
                                         [ 01-25 13:05:23.472  1186: 1186 D/         ]
                                         HostConnection::get() New Host Connection established 0xb7052160, tid 1186
01-25 13:05:23.559 1196-1196/? I/mediaserver: ServiceManager: 0xb614c680
01-25 13:05:23.559 1196-1196/? I/AudioFlinger: Using default 3000 mSec as standby time.
                                               
                                               [ 01-25 13:05:23.562  1196: 1196 E/         ]
                                               batterystats service unavailable!
                                               
                                               [ 01-25 13:05:23.562  1196: 1196 E/         ]
                                               batterystats service unavailable!
01-25 13:05:23.573 1196-1196/? I/CameraService: CameraService started (pid=1196)
01-25 13:05:23.573 1196-1196/? I/CameraService: CameraService process starting
                                                
                                                [ 01-25 13:05:23.573  1196: 1196 E/         ]
                                                batterystats service unavailable!
                                                
                                                [ 01-25 13:05:23.573  1196: 1196 E/         ]
                                                batterystats service unavailable!
01-25 13:05:23.577 1196-1196/? D/EmulatedCamera_QemuClient: Emulated camera list: 
01-25 13:05:23.577 1196-1196/? D/EmulatedCamera_FakeCamera: Initialize: Fake camera is facing back
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with auto, 1.000000, 1.000000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with incandescent, 1.380000, 0.600000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with daylight, 1.090000, 0.920000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with twilight, 0.920000, 1.220000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: setWhiteBalanceMode with white balance auto
01-25 13:05:23.577 1196-1196/? D/EmulatedCamera_FakeCamera: Initialize: Fake camera is facing front
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with auto, 1.000000, 1.000000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with incandescent, 1.380000, 0.600000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with daylight, 1.090000, 0.920000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: initializeWhiteBalanceModes with twilight, 0.920000, 1.220000
01-25 13:05:23.577 1196-1196/? V/EmulatedCamera_Device: setWhiteBalanceMode with white balance auto
01-25 13:05:23.578 1196-1196/? I/CameraService: Loaded "Emulated Camera Module" camera module
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:23.578 1196-1196/? I/CameraFlashlight: Opening camera 0
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_Camera: connectCamera
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_FakeDevice: connectDevice
01-25 13:05:23.578 1196-1196/? V/EmulatedCamera_CallbackNotifier: setCallbacks: 0xb75d0505, 0xb75d0dba, 0xb75d0c92, 0xb75d1267 (0xb6159a20)
01-25 13:05:23.578 1196-1196/? I/ServiceManager: Waiting for service SurfaceFlinger...
01-25 13:05:23.592 1186-1186/? E/SurfaceFlinger: hwcomposer module not found
01-25 13:05:23.592 1186-1186/? W/SurfaceFlinger: no suitable EGLConfig found, trying a simpler query
01-25 13:05:23.592 1186-1186/? I/SurfaceFlinger: EGL information:
01-25 13:05:23.592 1186-1186/? I/SurfaceFlinger: vendor    : Android
01-25 13:05:23.592 1186-1186/? I/SurfaceFlinger: version   : 1.4 Android META-EGL
01-25 13:05:23.592 1186-1186/? I/SurfaceFlinger: extensions: EGL_KHR_get_all_proc_addresses EGL_ANDROID_presentation_time EGL_KHR_swap_buffers_with_damage EGL_KHR_image_base EGL_KHR_gl_texture_2D_image EGL_KHR_fence_sync EGL_ANDROID_image_native_buffer 
01-25 13:05:23.592 1186-1186/? I/SurfaceFlinger: Client API: OpenGL_ES
01-25 13:05:23.593 1186-1186/? I/SurfaceFlinger: EGLSurface: 8-8-8-8, config=0xa
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: OpenGL ES informations:
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: vendor    : Google (NVIDIA Corporation)
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: renderer  : Android Emulator OpenGL ES Translator (GeForce GTX 960/PCIe/SSE2)
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: version   : OpenGL ES 2.0 (4.5.0 NVIDIA 350.12)
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: extensions: GL_EXT_debug_marker GL_OES_EGL_image GL_OES_EGL_image_external GL_OES_depth24 GL_OES_depth32 GL_OES_element_index_uint GL_OES_texture_float GL_OES_texture_float_linear GL_OES_compressed_paletted_texture GL_OES_compressed_ETC1_RGB8_texture GL_OES_depth_texture GL_OES_texture_half_float GL_OES_texture_half_float_linear GL_OES_packed_depth_stencil GL_OES_vertex_half_float GL_OES_texture_npot GL_OES_rgb8_rgba8 ANDROID_EMU_CHECKSUM_HELPER_v1 
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: GL_MAX_TEXTURE_SIZE = 16384
01-25 13:05:23.616 1186-1186/? I/SurfaceFlinger: GL_MAX_VIEWPORT_DIMS = 16384
01-25 13:05:23.617 1186-1186/? E/cutils-trace: Error opening trace file: Permission denied (13)
01-25 13:05:23.650 1186-1186/? D/SurfaceFlinger: Set power mode=2, type=0 flinger=0xb7062000
01-25 13:05:23.715 1241-1241/? I/perfprofd: starting Android Wide Profiling daemon
01-25 13:05:23.716 1241-1241/? E/perfprofd: unable to open configuration file /data/data/com.google.android.gms/files/perfprofd.conf
01-25 13:05:23.716 1241-1241/? I/perfprofd: random seed set to 4118640755
01-25 13:05:23.768 1186-1186/? D/SurfaceFlinger: shader cache generated - 24 shaders in 100.910889 ms
01-25 13:05:23.923 1186-1263/? E/SurfaceFlinger: ro.sf.lcd_density must be defined as a build property
01-25 13:05:23.923 1306-1331/? E/libEGL: load_driver(/system/lib/egl/libGLES_emulation.so): dlopen failed: library "/system/lib/egl/libGLES_emulation.so" not found
01-25 13:05:23.924 1306-1331/? D/libEGL: loaded /system/lib/egl/libEGL_emulation.so
01-25 13:05:23.924 1306-1331/? D/libEGL: loaded /system/lib/egl/libGLESv1_CM_emulation.so
01-25 13:05:23.926 1306-1331/? D/libEGL: loaded /system/lib/egl/libGLESv2_emulation.so
                                         
                                         [ 01-25 13:05:23.929  1306: 1331 D/         ]
                                         HostConnection::get() New Host Connection established 0xb62870b0, tid 1331
01-25 13:05:23.933 1173-1201/? V/vold: DISK mbr
01-25 13:05:23.933 1173-1201/? W/vold: disk:253,48 has unknown partition table; trying entire device
01-25 13:05:23.933 1173-1201/? V/vold: /system/bin/blkid
01-25 13:05:23.933 1173-1201/? V/vold:     -c
01-25 13:05:23.933 1173-1201/? V/vold:     /dev/null
01-25 13:05:23.933 1173-1201/? V/vold:     -s
01-25 13:05:23.933 1173-1201/? V/vold:     TYPE
01-25 13:05:23.933 1173-1201/? V/vold:     -s
01-25 13:05:23.933 1173-1201/? V/vold:     UUID
01-25 13:05:23.933 1173-1201/? V/vold:     -s
01-25 13:05:23.933 1173-1201/? V/vold:     LABEL
01-25 13:05:23.933 1173-1201/? V/vold:     /dev/block/vold/disk:253,48
01-25 13:05:23.993 1306-1331/? E/cutils-trace: Error opening trace file: Permission denied (13)
                                               
                                               [ 01-25 13:05:23.994  1186: 1265 D/         ]
                                               HostConnection::get() New Host Connection established 0xb7052a20, tid 1265
                                               
                                               
                                               [ 01-25 13:05:24.192  1186: 1263 D/         ]
                                               HostConnection::get() New Host Connection established 0xb6d0a0e0, tid 1263
01-25 13:05:24.287 1173-1201/? V/vold: /dev/block/vold/disk:253,48: LABEL="SDCARD" UUID="0C03-3A10" TYPE="vfat" 
01-25 13:05:24.579 1196-1196/? E/cutils-trace: Error opening trace file: Permission denied (13)
01-25 13:05:24.579 1196-1196/? V/EmulatedCamera_Preview: setPreviewWindow: current: 0x0 -> new: 0xb6159a30
01-25 13:05:24.580 1196-1196/? V/EmulatedCamera_Camera: setParameters
01-25 13:05:24.580 1196-1196/? D/EmulatedCamera_Camera: +++ New parameter: flash-mode=off
01-25 13:05:24.580 1196-1196/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:24.580 1196-1196/? V/EmulatedCamera_Preview: setPreviewWindow: current: 0xb6159a30 -> new: 0x0
01-25 13:05:24.580 1196-1196/? V/EmulatedCamera_Camera: releaseCamera
01-25 13:05:24.580 1196-1196/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:24.580 1196-1196/? V/EmulatedCamera_FakeDevice: disconnectDevice
01-25 13:05:24.581 1196-1196/? I/CameraFlashlight: Destroying camera 0
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_Camera: closeCamera
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:24.581 1196-1196/? I/CameraFlashlight: Opening camera 1
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_Camera: connectCamera
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_FakeDevice: connectDevice
01-25 13:05:24.581 1196-1196/? V/EmulatedCamera_CallbackNotifier: setCallbacks: 0xb75d0505, 0xb75d0dba, 0xb75d0c92, 0xb75d1267 (0xb6159a20)
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Preview: setPreviewWindow: current: 0x0 -> new: 0xb6159a30
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: setParameters
01-25 13:05:24.582 1196-1196/? D/EmulatedCamera_Camera: +++ New parameter: flash-mode=off
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Preview: setPreviewWindow: current: 0xb6159a30 -> new: 0x0
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: releaseCamera
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_FakeDevice: disconnectDevice
01-25 13:05:24.582 1196-1196/? I/CameraFlashlight: Destroying camera 1
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: closeCamera
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:24.582 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:24.582 1196-1196/? E/CameraService: setUpVendorTags: Vendor tag operations not fully defined. Ignoring definitions.
01-25 13:05:24.582 1196-1196/? I/ServiceManager: Waiting for service media.camera.proxy...
01-25 13:05:24.657 1200-1200/? D/AndroidRuntime: >>>>>> START com.android.internal.os.ZygoteInit uid 0 <<<<<<
01-25 13:05:24.724 1200-1200/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:24.735 1192-1192/? I/iptables: iptables v1.4.20: can't initialize iptables table `nat': Table does not exist (do you need to insmod?)
01-25 13:05:24.735 1192-1192/? I/iptables: Perhaps iptables or your kernel needs to be upgraded.
01-25 13:05:24.737 1192-1192/? I/iptables: iptables terminated by exit(3)
01-25 13:05:24.737 1192-1192/? E/Netd: exec() res=0, status=768 for /system/bin/iptables -w -t nat -N oem_nat_pre 
01-25 13:05:24.740 1192-1192/? I/iptables: iptables v1.4.20: can't initialize iptables table `nat': Table does not exist (do you need to insmod?)
01-25 13:05:24.740 1192-1192/? I/iptables: Perhaps iptables or your kernel needs to be upgraded.
01-25 13:05:24.752 1192-1192/? I/iptables: iptables terminated by exit(3)
01-25 13:05:24.754 1192-1192/? E/Netd: exec() res=0, status=768 for /system/bin/iptables -w -t nat -A PREROUTING -j oem_nat_pre 
01-25 13:05:24.762 1200-1200/? I/art: option[0]=-Xzygote
01-25 13:05:24.762 1200-1200/? I/art: option[1]=-Xcheck:jni
01-25 13:05:24.762 1200-1200/? I/art: option[2]=-Xstacktracefile:/data/anr/traces.txt
01-25 13:05:24.762 1200-1200/? I/art: option[3]=exit
01-25 13:05:24.762 1200-1200/? I/art: option[4]=vfprintf
01-25 13:05:24.762 1200-1200/? I/art: option[5]=sensitiveThread
01-25 13:05:24.762 1200-1200/? I/art: option[6]=-verbose:gc
01-25 13:05:24.762 1200-1200/? I/art: option[7]=-Xms4m
01-25 13:05:24.762 1200-1200/? I/art: option[8]=-Xmx256m
01-25 13:05:24.762 1200-1200/? I/art: option[9]=-agentlib:jdwp=transport=dt_android_adb,suspend=n,server=y
01-25 13:05:24.762 1200-1200/? I/art: option[10]=-Xlockprofthreshold:500
01-25 13:05:24.762 1200-1200/? I/art: option[11]=-Ximage-compiler-option
01-25 13:05:24.762 1200-1200/? I/art: option[12]=--runtime-arg
01-25 13:05:24.762 1200-1200/? I/art: option[13]=-Ximage-compiler-option
01-25 13:05:24.762 1200-1200/? I/art: option[14]=-Xms64m
01-25 13:05:24.762 1200-1200/? I/art: option[15]=-Ximage-compiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[16]=--runtime-arg
01-25 13:05:24.763 1200-1200/? I/art: option[17]=-Ximage-compiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[18]=-Xmx64m
01-25 13:05:24.763 1200-1200/? I/art: option[19]=-Ximage-compiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[20]=--image-classes=/system/etc/preloaded-classes
01-25 13:05:24.763 1200-1200/? I/art: option[21]=-Xcompiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[22]=--runtime-arg
01-25 13:05:24.763 1200-1200/? I/art: option[23]=-Xcompiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[24]=-Xms64m
01-25 13:05:24.763 1200-1200/? I/art: option[25]=-Xcompiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[26]=--runtime-arg
01-25 13:05:24.763 1200-1200/? I/art: option[27]=-Xcompiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[28]=-Xmx512m
01-25 13:05:24.763 1200-1200/? I/art: option[29]=-Ximage-compiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[30]=--instruction-set-variant=x86
01-25 13:05:24.763 1200-1200/? I/art: option[31]=-Xcompiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[32]=--instruction-set-variant=x86
01-25 13:05:24.763 1200-1200/? I/art: option[33]=-Ximage-compiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[34]=--instruction-set-features=default
01-25 13:05:24.763 1200-1200/? I/art: option[35]=-Xcompiler-option
01-25 13:05:24.763 1200-1200/? I/art: option[36]=--instruction-set-features=default
01-25 13:05:24.763 1200-1200/? I/art: option[37]=-Duser.locale=en-US
01-25 13:05:24.763 1200-1200/? I/art: option[38]=--cpu-abilist=x86
01-25 13:05:24.763 1200-1200/? I/art: option[39]=-Xfingerprint:Android/sdk_google_phone_x86/generic_x86:6.0/MASTER/2524533:userdebug/test-keys
01-25 13:05:24.783 1192-1192/? I/iptables: iptables v1.4.20: can't initialize iptables table `nat': Table does not exist (do you need to insmod?)
01-25 13:05:24.783 1192-1192/? I/iptables: Perhaps iptables or your kernel needs to be upgraded.
01-25 13:05:24.784 1192-1192/? I/iptables: iptables terminated by exit(3)
01-25 13:05:24.784 1192-1192/? E/Netd: exec() res=0, status=768 for /system/bin/iptables -w -t nat -N natctrl_nat_POSTROUTING 
01-25 13:05:24.792 1192-1192/? I/iptables: iptables v1.4.20: can't initialize iptables table `nat': Table does not exist (do you need to insmod?)
01-25 13:05:24.792 1192-1192/? I/iptables: Perhaps iptables or your kernel needs to be upgraded.
01-25 13:05:24.792 1192-1192/? I/iptables: iptables terminated by exit(3)
01-25 13:05:24.792 1192-1192/? E/Netd: exec() res=0, status=768 for /system/bin/iptables -w -t nat -A POSTROUTING -j natctrl_nat_POSTROUTING 
01-25 13:05:24.962 1192-1192/? V/NatController: runCmd(/system/bin/iptables -w -F natctrl_FORWARD) res=0
01-25 13:05:24.967 1192-1192/? V/NatController: runCmd(/system/bin/iptables -w -A natctrl_FORWARD -j DROP) res=0
01-25 13:05:24.981 1192-1192/? V/NatController: runCmd(/system/bin/iptables -w -t nat -F natctrl_nat_POSTROUTING) res=3
01-25 13:05:24.998 1200-1200/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:25.157 1200-1200/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:25.157 1200-1200/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:25.160 1200-1200/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:25.193 1200-1200/? I/SamplingProfilerIntegration: Profiling disabled.
01-25 13:05:25.196 1200-1200/? D/Zygote: begin preload
01-25 13:05:25.199 1200-1200/? I/Zygote: Preloading classes...
01-25 13:05:25.400 1192-1192/? W/netd: type=1400 audit(0.0:4): avc: denied { sys_module } for capability=16 scontext=u:r:netd:s0 tcontext=u:r:netd:s0 tclass=capability permissive=0
01-25 13:05:25.404 1192-1192/? E/Netd: cannot find interface dummy0
01-25 13:05:25.405 1192-1192/? D/MDnsDS: MDnsSdListener::Hander starting up
01-25 13:05:25.405 1192-1531/? D/MDnsDS: MDnsSdListener starting to monitor
01-25 13:05:25.405 1192-1531/? D/MDnsDS: Going to poll with pollCount 1
01-25 13:05:25.583 1196-1196/? I/ServiceManager: Waiting for service media.camera.proxy...
01-25 13:05:25.675 1200-1200/? E/Minikin: addFont failed to create font /system/fonts/NanumGothic.ttf
01-25 13:05:25.675 1200-1200/? E/Minikin: addFont failed to create font /system/fonts/DroidSansFallback.ttf
01-25 13:05:25.675 1200-1200/? E/Minikin: addFont failed to create font /system/fonts/MTLmr3m.ttf
01-25 13:05:25.841 1200-1200/? V/DngCreator_JNI: DngCreator_nativeClassInit:
01-25 13:05:25.983 1200-1200/? I/art: Thread[1,tid=1200,Native,Thread*=0xb40b4500,peer=0x12c35100,"main"] recursive attempt to load library "/system/lib/libmedia_jni.so"
01-25 13:05:25.984 1200-1200/? D/MtpDeviceJNI: register_android_mtp_MtpDevice
01-25 13:05:25.984 1200-1200/? I/art: Thread[1,tid=1200,Native,Thread*=0xb40b4500,peer=0x12c35100,"main"] recursive attempt to load library "/system/lib/libmedia_jni.so"
01-25 13:05:25.984 1200-1200/? I/art: Thread[1,tid=1200,Native,Thread*=0xb40b4500,peer=0x12c35100,"main"] recursive attempt to load library "/system/lib/libmedia_jni.so"
01-25 13:05:26.022 1200-1200/? E/EmojiFactory_jni: Failed to load libemoji.so: dlopen failed: library "libemoji.so" not found
01-25 13:05:26.124 1200-1200/? I/System: Loaded time zone names for "" in 22ms (22ms in ICU)
01-25 13:05:26.134 1200-1200/? I/System: Loaded time zone names for "en_US" in 10ms (9ms in ICU)
01-25 13:05:26.146 1200-1200/? I/Zygote: ...preloaded 3831 classes in 947ms.
01-25 13:05:26.146 1200-1200/? I/art: VMRuntime.preloadDexCaches starting
01-25 13:05:26.164 1200-1200/? I/art: VMRuntime.preloadDexCaches strings total=242978 before=43551 after=43551
01-25 13:05:26.164 1200-1200/? I/art: VMRuntime.preloadDexCaches types total=20084 before=6885 after=6911
01-25 13:05:26.164 1200-1200/? I/art: VMRuntime.preloadDexCaches fields total=97951 before=35734 after=35932
01-25 13:05:26.164 1200-1200/? I/art: VMRuntime.preloadDexCaches methods total=169821 before=70760 after=71253
01-25 13:05:26.164 1200-1200/? I/art: VMRuntime.preloadDexCaches finished
01-25 13:05:26.179 1537-1537/? D/idmap: error: no read access to /vendor/overlay: No such file or directory
01-25 13:05:26.211 1200-1200/? I/Zygote: Preloading resources...
01-25 13:05:26.227 1200-1200/? W/Resources: Preloaded drawable resource #0x1080096 (android:drawable/toast_frame) that varies with configuration!!
01-25 13:05:26.238 1200-1200/? W/Resources: Preloaded drawable resource #0x108010c (android:drawable/btn_check_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.238 1200-1200/? W/Resources: Preloaded drawable resource #0x108010b (android:drawable/btn_check_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.240 1200-1200/? W/Resources: Preloaded drawable resource #0x1080109 (android:drawable/btn_check_on_holo_light) that varies with configuration!!
01-25 13:05:26.241 1200-1200/? W/Resources: Preloaded drawable resource #0x1080108 (android:drawable/btn_check_on_holo_dark) that varies with configuration!!
01-25 13:05:26.242 1200-1200/? W/Resources: Preloaded drawable resource #0x1080106 (android:drawable/btn_check_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.244 1200-1200/? W/Resources: Preloaded drawable resource #0x1080105 (android:drawable/btn_check_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.244 1200-1200/? W/Resources: Preloaded drawable resource #0x1080104 (android:drawable/btn_check_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.245 1200-1200/? W/Resources: Preloaded drawable resource #0x1080103 (android:drawable/btn_check_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.245 1200-1200/? W/Resources: Preloaded drawable resource #0x1080102 (android:drawable/btn_check_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x1080101 (android:drawable/btn_check_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f9 (android:drawable/btn_check_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f8 (android:drawable/btn_check_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f4 (android:drawable/btn_check_off_holo_light) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f3 (android:drawable/btn_check_off_holo_dark) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f1 (android:drawable/btn_check_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.247 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f0 (android:drawable/btn_check_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.248 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ef (android:drawable/btn_check_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.249 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ee (android:drawable/btn_check_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.251 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ed (android:drawable/btn_check_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.252 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ec (android:drawable/btn_check_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.256 1200-1200/? W/Resources: Preloaded drawable resource #0x1080109 (android:drawable/btn_check_on_holo_light) that varies with configuration!!
01-25 13:05:26.257 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f4 (android:drawable/btn_check_off_holo_light) that varies with configuration!!
01-25 13:05:26.263 1200-1200/? W/Resources: Preloaded drawable resource #0x108010c (android:drawable/btn_check_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.264 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f9 (android:drawable/btn_check_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.264 1200-1200/? W/Resources: Preloaded drawable resource #0x1080106 (android:drawable/btn_check_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.264 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f1 (android:drawable/btn_check_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.265 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f4 (android:drawable/btn_check_off_holo_light) that varies with configuration!!
01-25 13:05:26.265 1200-1200/? W/Resources: Preloaded drawable resource #0x1080109 (android:drawable/btn_check_on_holo_light) that varies with configuration!!
01-25 13:05:26.265 1200-1200/? W/Resources: Preloaded drawable resource #0x1080104 (android:drawable/btn_check_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.265 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ef (android:drawable/btn_check_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.265 1200-1200/? W/Resources: Preloaded drawable resource #0x1080102 (android:drawable/btn_check_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.266 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ed (android:drawable/btn_check_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.266 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ef (android:drawable/btn_check_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.266 1200-1200/? W/Resources: Preloaded drawable resource #0x1080104 (android:drawable/btn_check_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.266 1200-1200/? W/Resources: Preloaded drawable resource #0x10800e2 (android:drawable/btn_check_holo_light) that varies with configuration!!
01-25 13:05:26.266 1200-1200/? W/Resources: Preloaded drawable resource #0x1080108 (android:drawable/btn_check_on_holo_dark) that varies with configuration!!
01-25 13:05:26.267 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f3 (android:drawable/btn_check_off_holo_dark) that varies with configuration!!
01-25 13:05:26.267 1200-1200/? W/Resources: Preloaded drawable resource #0x108010b (android:drawable/btn_check_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.267 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f8 (android:drawable/btn_check_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.274 1200-1200/? W/Resources: Preloaded drawable resource #0x1080105 (android:drawable/btn_check_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.275 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f0 (android:drawable/btn_check_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.275 1200-1200/? W/Resources: Preloaded drawable resource #0x10800f3 (android:drawable/btn_check_off_holo_dark) that varies with configuration!!
01-25 13:05:26.276 1200-1200/? W/Resources: Preloaded drawable resource #0x1080108 (android:drawable/btn_check_on_holo_dark) that varies with configuration!!
01-25 13:05:26.277 1200-1200/? W/Resources: Preloaded drawable resource #0x1080103 (android:drawable/btn_check_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.277 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ee (android:drawable/btn_check_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.277 1200-1200/? W/Resources: Preloaded drawable resource #0x1080101 (android:drawable/btn_check_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.278 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ec (android:drawable/btn_check_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.278 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ee (android:drawable/btn_check_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.278 1200-1200/? W/Resources: Preloaded drawable resource #0x1080103 (android:drawable/btn_check_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.278 1200-1200/? W/Resources: Preloaded drawable resource #0x10800e1 (android:drawable/btn_check_holo_dark) that varies with configuration!!
01-25 13:05:26.280 1200-1200/? W/Resources: Preloaded drawable resource #0x108019d (android:drawable/btn_radio_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.281 1200-1200/? W/Resources: Preloaded drawable resource #0x108019c (android:drawable/btn_radio_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.281 1200-1200/? W/Resources: Preloaded drawable resource #0x1080199 (android:drawable/btn_radio_on_holo_light) that varies with configuration!!
01-25 13:05:26.281 1200-1200/? W/Resources: Preloaded drawable resource #0x1080198 (android:drawable/btn_radio_on_holo_dark) that varies with configuration!!
01-25 13:05:26.282 1200-1200/? W/Resources: Preloaded drawable resource #0x1080196 (android:drawable/btn_radio_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.282 1200-1200/? W/Resources: Preloaded drawable resource #0x1080195 (android:drawable/btn_radio_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.282 1200-1200/? W/Resources: Preloaded drawable resource #0x1080194 (android:drawable/btn_radio_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.282 1200-1200/? W/Resources: Preloaded drawable resource #0x1080193 (android:drawable/btn_radio_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.283 1200-1200/? W/Resources: Preloaded drawable resource #0x1080192 (android:drawable/btn_radio_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.285 1200-1200/? W/Resources: Preloaded drawable resource #0x1080191 (android:drawable/btn_radio_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.287 1200-1200/? W/Resources: Preloaded drawable resource #0x108018e (android:drawable/btn_radio_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.287 1200-1200/? W/Resources: Preloaded drawable resource #0x108018d (android:drawable/btn_radio_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.288 1200-1200/? W/Resources: Preloaded drawable resource #0x108018b (android:drawable/btn_radio_off_holo_light) that varies with configuration!!
01-25 13:05:26.289 1200-1200/? W/Resources: Preloaded drawable resource #0x108018a (android:drawable/btn_radio_off_holo_dark) that varies with configuration!!
01-25 13:05:26.290 1200-1200/? W/Resources: Preloaded drawable resource #0x1080188 (android:drawable/btn_radio_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.290 1200-1200/? W/Resources: Preloaded drawable resource #0x1080187 (android:drawable/btn_radio_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.291 1200-1200/? W/Resources: Preloaded drawable resource #0x1080186 (android:drawable/btn_radio_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.291 1200-1200/? W/Resources: Preloaded drawable resource #0x1080185 (android:drawable/btn_radio_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.291 1200-1200/? W/Resources: Preloaded drawable resource #0x1080184 (android:drawable/btn_radio_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.291 1200-1200/? W/Resources: Preloaded drawable resource #0x1080183 (android:drawable/btn_radio_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.292 1200-1200/? W/Resources: Preloaded drawable resource #0x108012e (android:drawable/btn_default_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.292 1200-1200/? W/Resources: Preloaded drawable resource #0x108012d (android:drawable/btn_default_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.292 1200-1200/? W/Resources: Preloaded drawable resource #0x108012a (android:drawable/btn_default_normal_holo_light) that varies with configuration!!
01-25 13:05:26.293 1200-1200/? W/Resources: Preloaded drawable resource #0x1080129 (android:drawable/btn_default_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.293 1200-1200/? W/Resources: Preloaded drawable resource #0x1080120 (android:drawable/btn_default_focused_holo_light) that varies with configuration!!
01-25 13:05:26.294 1200-1200/? W/Resources: Preloaded drawable resource #0x108011f (android:drawable/btn_default_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.294 1200-1200/? W/Resources: Preloaded drawable resource #0x108011d (android:drawable/btn_default_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.294 1200-1200/? W/Resources: Preloaded drawable resource #0x108011c (android:drawable/btn_default_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.294 1200-1200/? W/Resources: Preloaded drawable resource #0x108011a (android:drawable/btn_default_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.294 1200-1200/? W/Resources: Preloaded drawable resource #0x1080119 (android:drawable/btn_default_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.296 1200-1200/? W/Resources: Preloaded drawable resource #0x1080129 (android:drawable/btn_default_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.297 1200-1200/? W/Resources: Preloaded drawable resource #0x108011c (android:drawable/btn_default_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.298 1200-1200/? W/Resources: Preloaded drawable resource #0x108012d (android:drawable/btn_default_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.298 1200-1200/? W/Resources: Preloaded drawable resource #0x108011f (android:drawable/btn_default_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.299 1200-1200/? W/Resources: Preloaded drawable resource #0x1080129 (android:drawable/btn_default_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.301 1200-1200/? W/Resources: Preloaded drawable resource #0x1080119 (android:drawable/btn_default_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.302 1200-1200/? W/Resources: Preloaded drawable resource #0x108011c (android:drawable/btn_default_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.302 1200-1200/? W/Resources: Preloaded drawable resource #0x1080121 (android:drawable/btn_default_holo_dark) that varies with configuration!!
01-25 13:05:26.302 1200-1200/? W/Resources: Preloaded drawable resource #0x108012a (android:drawable/btn_default_normal_holo_light) that varies with configuration!!
01-25 13:05:26.302 1200-1200/? W/Resources: Preloaded drawable resource #0x108011d (android:drawable/btn_default_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.303 1200-1200/? W/Resources: Preloaded drawable resource #0x108012e (android:drawable/btn_default_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.303 1200-1200/? W/Resources: Preloaded drawable resource #0x1080120 (android:drawable/btn_default_focused_holo_light) that varies with configuration!!
01-25 13:05:26.303 1200-1200/? W/Resources: Preloaded drawable resource #0x108012a (android:drawable/btn_default_normal_holo_light) that varies with configuration!!
01-25 13:05:26.303 1200-1200/? W/Resources: Preloaded drawable resource #0x108011a (android:drawable/btn_default_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.304 1200-1200/? W/Resources: Preloaded drawable resource #0x108011d (android:drawable/btn_default_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.304 1200-1200/? W/Resources: Preloaded drawable resource #0x1080122 (android:drawable/btn_default_holo_light) that varies with configuration!!
01-25 13:05:26.304 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fe (android:drawable/btn_star_off_normal_holo_light) that varies with configuration!!
01-25 13:05:26.306 1200-1200/? W/Resources: Preloaded drawable resource #0x1080208 (android:drawable/btn_star_on_normal_holo_light) that varies with configuration!!
01-25 13:05:26.307 1200-1200/? W/Resources: Preloaded drawable resource #0x1080204 (android:drawable/btn_star_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.307 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fa (android:drawable/btn_star_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.307 1200-1200/? W/Resources: Preloaded drawable resource #0x108020a (android:drawable/btn_star_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.308 1200-1200/? W/Resources: Preloaded drawable resource #0x1080200 (android:drawable/btn_star_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.308 1200-1200/? W/Resources: Preloaded drawable resource #0x1080206 (android:drawable/btn_star_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.309 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fc (android:drawable/btn_star_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.309 1200-1200/? W/Resources: Preloaded drawable resource #0x1080202 (android:drawable/btn_star_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.309 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f8 (android:drawable/btn_star_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.309 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fe (android:drawable/btn_star_off_normal_holo_light) that varies with configuration!!
01-25 13:05:26.309 1200-1200/? W/Resources: Preloaded drawable resource #0x1080208 (android:drawable/btn_star_on_normal_holo_light) that varies with configuration!!
01-25 13:05:26.310 1200-1200/? W/Resources: Preloaded drawable resource #0x1080204 (android:drawable/btn_star_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.310 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fa (android:drawable/btn_star_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.310 1200-1200/? W/Resources: Preloaded drawable resource #0x108020a (android:drawable/btn_star_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.310 1200-1200/? W/Resources: Preloaded drawable resource #0x1080200 (android:drawable/btn_star_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.311 1200-1200/? W/Resources: Preloaded drawable resource #0x1080206 (android:drawable/btn_star_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.311 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fc (android:drawable/btn_star_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.311 1200-1200/? W/Resources: Preloaded drawable resource #0x1080202 (android:drawable/btn_star_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.312 1200-1200/? W/Resources: Preloaded drawable resource #0x1080204 (android:drawable/btn_star_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.312 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f8 (android:drawable/btn_star_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.312 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fa (android:drawable/btn_star_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.312 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fe (android:drawable/btn_star_off_normal_holo_light) that varies with configuration!!
01-25 13:05:26.312 1200-1200/? W/Resources: Preloaded drawable resource #0x1080208 (android:drawable/btn_star_on_normal_holo_light) that varies with configuration!!
01-25 13:05:26.312 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f3 (android:drawable/btn_star_holo_light) that varies with configuration!!
01-25 13:05:26.313 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fd (android:drawable/btn_star_off_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.313 1200-1200/? W/Resources: Preloaded drawable resource #0x1080207 (android:drawable/btn_star_on_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.313 1200-1200/? W/Resources: Preloaded drawable resource #0x1080203 (android:drawable/btn_star_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.313 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f9 (android:drawable/btn_star_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.313 1200-1200/? W/Resources: Preloaded drawable resource #0x1080209 (android:drawable/btn_star_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.314 1200-1200/? W/Resources: Preloaded drawable resource #0x10801ff (android:drawable/btn_star_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.314 1200-1200/? W/Resources: Preloaded drawable resource #0x1080205 (android:drawable/btn_star_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.314 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fb (android:drawable/btn_star_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.314 1200-1200/? W/Resources: Preloaded drawable resource #0x1080201 (android:drawable/btn_star_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.315 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f7 (android:drawable/btn_star_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.315 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fd (android:drawable/btn_star_off_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.315 1200-1200/? W/Resources: Preloaded drawable resource #0x1080207 (android:drawable/btn_star_on_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.315 1200-1200/? W/Resources: Preloaded drawable resource #0x1080203 (android:drawable/btn_star_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.315 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f9 (android:drawable/btn_star_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.316 1200-1200/? W/Resources: Preloaded drawable resource #0x1080209 (android:drawable/btn_star_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.316 1200-1200/? W/Resources: Preloaded drawable resource #0x10801ff (android:drawable/btn_star_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.316 1200-1200/? W/Resources: Preloaded drawable resource #0x1080205 (android:drawable/btn_star_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.317 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fb (android:drawable/btn_star_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.317 1200-1200/? W/Resources: Preloaded drawable resource #0x1080201 (android:drawable/btn_star_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.317 1200-1200/? W/Resources: Preloaded drawable resource #0x1080203 (android:drawable/btn_star_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.317 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f7 (android:drawable/btn_star_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.318 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f9 (android:drawable/btn_star_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.318 1200-1200/? W/Resources: Preloaded drawable resource #0x10801fd (android:drawable/btn_star_off_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.318 1200-1200/? W/Resources: Preloaded drawable resource #0x1080207 (android:drawable/btn_star_on_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.318 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f2 (android:drawable/btn_star_holo_dark) that varies with configuration!!
01-25 13:05:26.320 1200-1200/? W/Resources: Preloaded drawable resource #0x108023d (android:drawable/btn_toggle_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.320 1200-1200/? W/Resources: Preloaded drawable resource #0x108023c (android:drawable/btn_toggle_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.320 1200-1200/? W/Resources: Preloaded drawable resource #0x108023b (android:drawable/btn_toggle_on_normal_holo_light) that varies with configuration!!
01-25 13:05:26.321 1200-1200/? W/Resources: Preloaded drawable resource #0x108023a (android:drawable/btn_toggle_on_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.321 1200-1200/? W/Resources: Preloaded drawable resource #0x1080239 (android:drawable/btn_toggle_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.321 1200-1200/? W/Resources: Preloaded drawable resource #0x1080238 (android:drawable/btn_toggle_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.321 1200-1200/? W/Resources: Preloaded drawable resource #0x1080237 (android:drawable/btn_toggle_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.321 1200-1200/? W/Resources: Preloaded drawable resource #0x1080236 (android:drawable/btn_toggle_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.322 1200-1200/? W/Resources: Preloaded drawable resource #0x1080235 (android:drawable/btn_toggle_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.322 1200-1200/? W/Resources: Preloaded drawable resource #0x1080234 (android:drawable/btn_toggle_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.322 1200-1200/? W/Resources: Preloaded drawable resource #0x1080232 (android:drawable/btn_toggle_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.322 1200-1200/? W/Resources: Preloaded drawable resource #0x1080231 (android:drawable/btn_toggle_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.323 1200-1200/? W/Resources: Preloaded drawable resource #0x1080230 (android:drawable/btn_toggle_off_normal_holo_light) that varies with configuration!!
01-25 13:05:26.323 1200-1200/? W/Resources: Preloaded drawable resource #0x108022f (android:drawable/btn_toggle_off_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.323 1200-1200/? W/Resources: Preloaded drawable resource #0x108022e (android:drawable/btn_toggle_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.323 1200-1200/? W/Resources: Preloaded drawable resource #0x108022d (android:drawable/btn_toggle_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.323 1200-1200/? W/Resources: Preloaded drawable resource #0x108022c (android:drawable/btn_toggle_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.324 1200-1200/? W/Resources: Preloaded drawable resource #0x108022b (android:drawable/btn_toggle_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.324 1200-1200/? W/Resources: Preloaded drawable resource #0x108022a (android:drawable/btn_toggle_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.324 1200-1200/? W/Resources: Preloaded drawable resource #0x1080229 (android:drawable/btn_toggle_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.324 1200-1200/? W/Resources: Preloaded drawable resource #0x108023b (android:drawable/btn_toggle_on_normal_holo_light) that varies with configuration!!
01-25 13:05:26.325 1200-1200/? W/Resources: Preloaded drawable resource #0x1080237 (android:drawable/btn_toggle_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.325 1200-1200/? W/Resources: Preloaded drawable resource #0x108023d (android:drawable/btn_toggle_on_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.325 1200-1200/? W/Resources: Preloaded drawable resource #0x1080239 (android:drawable/btn_toggle_on_focused_holo_light) that varies with configuration!!
01-25 13:05:26.325 1200-1200/? W/Resources: Preloaded drawable resource #0x108023b (android:drawable/btn_toggle_on_normal_holo_light) that varies with configuration!!
01-25 13:05:26.329 1200-1200/? W/Resources: Preloaded drawable resource #0x1080235 (android:drawable/btn_toggle_on_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.330 1200-1200/? W/Resources: Preloaded drawable resource #0x1080237 (android:drawable/btn_toggle_on_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.330 1200-1200/? W/Resources: Preloaded drawable resource #0x1080230 (android:drawable/btn_toggle_off_normal_holo_light) that varies with configuration!!
01-25 13:05:26.337 1200-1200/? W/Resources: Preloaded drawable resource #0x108022c (android:drawable/btn_toggle_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.338 1200-1200/? W/Resources: Preloaded drawable resource #0x1080232 (android:drawable/btn_toggle_off_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.339 1200-1200/? W/Resources: Preloaded drawable resource #0x108022e (android:drawable/btn_toggle_off_focused_holo_light) that varies with configuration!!
01-25 13:05:26.341 1200-1200/? W/Resources: Preloaded drawable resource #0x1080230 (android:drawable/btn_toggle_off_normal_holo_light) that varies with configuration!!
01-25 13:05:26.342 1200-1200/? W/Resources: Preloaded drawable resource #0x108022a (android:drawable/btn_toggle_off_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.342 1200-1200/? W/Resources: Preloaded drawable resource #0x108022c (android:drawable/btn_toggle_off_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.342 1200-1200/? W/Resources: Preloaded drawable resource #0x1080226 (android:drawable/btn_toggle_holo_light) that varies with configuration!!
01-25 13:05:26.342 1200-1200/? W/Resources: Preloaded drawable resource #0x108023a (android:drawable/btn_toggle_on_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.342 1200-1200/? W/Resources: Preloaded drawable resource #0x1080236 (android:drawable/btn_toggle_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.343 1200-1200/? W/Resources: Preloaded drawable resource #0x108023c (android:drawable/btn_toggle_on_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.343 1200-1200/? W/Resources: Preloaded drawable resource #0x1080238 (android:drawable/btn_toggle_on_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.343 1200-1200/? W/Resources: Preloaded drawable resource #0x108023a (android:drawable/btn_toggle_on_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.343 1200-1200/? W/Resources: Preloaded drawable resource #0x1080234 (android:drawable/btn_toggle_on_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.344 1200-1200/? W/Resources: Preloaded drawable resource #0x1080236 (android:drawable/btn_toggle_on_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.344 1200-1200/? W/Resources: Preloaded drawable resource #0x108022f (android:drawable/btn_toggle_off_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.344 1200-1200/? W/Resources: Preloaded drawable resource #0x108022b (android:drawable/btn_toggle_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.344 1200-1200/? W/Resources: Preloaded drawable resource #0x1080231 (android:drawable/btn_toggle_off_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.344 1200-1200/? W/Resources: Preloaded drawable resource #0x108022d (android:drawable/btn_toggle_off_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.345 1200-1200/? W/Resources: Preloaded drawable resource #0x108022f (android:drawable/btn_toggle_off_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.345 1200-1200/? W/Resources: Preloaded drawable resource #0x1080229 (android:drawable/btn_toggle_off_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.345 1200-1200/? W/Resources: Preloaded drawable resource #0x108022b (android:drawable/btn_toggle_off_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.345 1200-1200/? W/Resources: Preloaded drawable resource #0x1080225 (android:drawable/btn_toggle_holo_dark) that varies with configuration!!
01-25 13:05:26.347 1200-1200/? W/Resources: Preloaded drawable resource #0x108070d (android:drawable/textfield_multiline_default_holo_light) that varies with configuration!!
01-25 13:05:26.347 1200-1200/? W/Resources: Preloaded drawable resource #0x1080711 (android:drawable/textfield_multiline_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.347 1200-1200/? W/Resources: Preloaded drawable resource #0x108070b (android:drawable/textfield_multiline_activated_holo_light) that varies with configuration!!
01-25 13:05:26.348 1200-1200/? W/Resources: Preloaded drawable resource #0x1080713 (android:drawable/textfield_multiline_focused_holo_light) that varies with configuration!!
01-25 13:05:26.348 1200-1200/? W/Resources: Preloaded drawable resource #0x108070d (android:drawable/textfield_multiline_default_holo_light) that varies with configuration!!
01-25 13:05:26.349 1200-1200/? W/Resources: Preloaded drawable resource #0x108070f (android:drawable/textfield_multiline_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.349 1200-1200/? W/Resources: Preloaded drawable resource #0x1080711 (android:drawable/textfield_multiline_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.357 1200-1200/? W/Resources: Preloaded drawable resource #0x10806ff (android:drawable/textfield_default_holo_light) that varies with configuration!!
01-25 13:05:26.357 1200-1200/? W/Resources: Preloaded drawable resource #0x1080705 (android:drawable/textfield_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.357 1200-1200/? W/Resources: Preloaded drawable resource #0x10806f6 (android:drawable/textfield_activated_holo_light) that varies with configuration!!
01-25 13:05:26.357 1200-1200/? W/Resources: Preloaded drawable resource #0x1080708 (android:drawable/textfield_focused_holo_light) that varies with configuration!!
01-25 13:05:26.358 1200-1200/? W/Resources: Preloaded drawable resource #0x10806ff (android:drawable/textfield_default_holo_light) that varies with configuration!!
01-25 13:05:26.358 1200-1200/? W/Resources: Preloaded drawable resource #0x1080703 (android:drawable/textfield_disabled_focused_holo_light) that varies with configuration!!
01-25 13:05:26.358 1200-1200/? W/Resources: Preloaded drawable resource #0x1080705 (android:drawable/textfield_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.358 1200-1200/? W/Resources: Preloaded drawable resource #0x10802a5 (android:drawable/edit_text_holo_light) that varies with configuration!!
01-25 13:05:26.358 1200-1200/? W/Resources: Preloaded drawable resource #0x108070c (android:drawable/textfield_multiline_default_holo_dark) that varies with configuration!!
01-25 13:05:26.359 1200-1200/? W/Resources: Preloaded drawable resource #0x1080710 (android:drawable/textfield_multiline_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.359 1200-1200/? W/Resources: Preloaded drawable resource #0x108070a (android:drawable/textfield_multiline_activated_holo_dark) that varies with configuration!!
01-25 13:05:26.359 1200-1200/? W/Resources: Preloaded drawable resource #0x1080712 (android:drawable/textfield_multiline_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.359 1200-1200/? W/Resources: Preloaded drawable resource #0x108070c (android:drawable/textfield_multiline_default_holo_dark) that varies with configuration!!
01-25 13:05:26.360 1200-1200/? W/Resources: Preloaded drawable resource #0x108070e (android:drawable/textfield_multiline_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.360 1200-1200/? W/Resources: Preloaded drawable resource #0x1080710 (android:drawable/textfield_multiline_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.360 1200-1200/? W/Resources: Preloaded drawable resource #0x10806fe (android:drawable/textfield_default_holo_dark) that varies with configuration!!
01-25 13:05:26.361 1200-1200/? W/Resources: Preloaded drawable resource #0x1080704 (android:drawable/textfield_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.363 1200-1200/? W/Resources: Preloaded drawable resource #0x10806f5 (android:drawable/textfield_activated_holo_dark) that varies with configuration!!
01-25 13:05:26.363 1200-1200/? W/Resources: Preloaded drawable resource #0x1080707 (android:drawable/textfield_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.363 1200-1200/? W/Resources: Preloaded drawable resource #0x10806fe (android:drawable/textfield_default_holo_dark) that varies with configuration!!
01-25 13:05:26.363 1200-1200/? W/Resources: Preloaded drawable resource #0x1080702 (android:drawable/textfield_disabled_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.364 1200-1200/? W/Resources: Preloaded drawable resource #0x1080704 (android:drawable/textfield_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.364 1200-1200/? W/Resources: Preloaded drawable resource #0x10802a4 (android:drawable/edit_text_holo_dark) that varies with configuration!!
01-25 13:05:26.378 1200-1200/? W/Resources: Preloaded drawable resource #0x10806ec (android:drawable/text_select_handle_left) that varies with configuration!!
01-25 13:05:26.379 1200-1200/? W/Resources: Preloaded drawable resource #0x10806f2 (android:drawable/text_select_handle_right) that varies with configuration!!
01-25 13:05:26.379 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e9 (android:drawable/text_edit_paste_window) that varies with configuration!!
01-25 13:05:26.379 1200-1200/? W/Resources: Preloaded drawable resource #0x10802bc (android:drawable/expander_close_holo_dark) that varies with configuration!!
01-25 13:05:26.379 1200-1200/? W/Resources: Preloaded drawable resource #0x10802bd (android:drawable/expander_close_holo_light) that varies with configuration!!
01-25 13:05:26.379 1200-1200/? W/Resources: Preloaded drawable resource #0x10802bc (android:drawable/expander_close_holo_dark) that varies with configuration!!
01-25 13:05:26.380 1200-1200/? W/Resources: Preloaded drawable resource #0x10802c5 (android:drawable/expander_open_holo_dark) that varies with configuration!!
01-25 13:05:26.380 1200-1200/? W/Resources: Preloaded drawable resource #0x10802c0 (android:drawable/expander_group_holo_dark) that varies with configuration!!
01-25 13:05:26.380 1200-1200/? W/Resources: Preloaded drawable resource #0x10802bd (android:drawable/expander_close_holo_light) that varies with configuration!!
01-25 13:05:26.380 1200-1200/? W/Resources: Preloaded drawable resource #0x10802c6 (android:drawable/expander_open_holo_light) that varies with configuration!!
01-25 13:05:26.381 1200-1200/? W/Resources: Preloaded drawable resource #0x10802c1 (android:drawable/expander_group_holo_light) that varies with configuration!!
01-25 13:05:26.408 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b8 (android:drawable/list_selector_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.409 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b8 (android:drawable/list_selector_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.410 1200-1200/? W/Resources: Preloaded drawable resource #0x1080497 (android:drawable/list_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.411 1200-1200/? W/Resources: Preloaded drawable resource #0x1080495 (android:drawable/list_longpressed_holo_dark) that varies with configuration!!
01-25 13:05:26.411 1200-1200/? W/Resources: Preloaded drawable resource #0x1080490 (android:drawable/list_focused_holo) that varies with configuration!!
01-25 13:05:26.411 1200-1200/? W/Resources: Preloaded drawable resource #0x10804bc (android:drawable/list_selector_holo_dark) that varies with configuration!!
01-25 13:05:26.412 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b9 (android:drawable/list_selector_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.412 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b9 (android:drawable/list_selector_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.412 1200-1200/? W/Resources: Preloaded drawable resource #0x1080498 (android:drawable/list_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.412 1200-1200/? W/Resources: Preloaded drawable resource #0x1080496 (android:drawable/list_longpressed_holo_light) that varies with configuration!!
01-25 13:05:26.412 1200-1200/? W/Resources: Preloaded drawable resource #0x1080490 (android:drawable/list_focused_holo) that varies with configuration!!
01-25 13:05:26.413 1200-1200/? W/Resources: Preloaded drawable resource #0x10804bd (android:drawable/list_selector_holo_light) that varies with configuration!!
01-25 13:05:26.413 1200-1200/? W/Resources: Preloaded drawable resource #0x108049a (android:drawable/list_section_divider_holo_light) that varies with configuration!!
01-25 13:05:26.413 1200-1200/? W/Resources: Preloaded drawable resource #0x1080499 (android:drawable/list_section_divider_holo_dark) that varies with configuration!!
01-25 13:05:26.417 1200-1200/? W/Resources: Preloaded drawable resource #0x10804cd (android:drawable/menu_hardkey_panel_holo_dark) that varies with configuration!!
01-25 13:05:26.421 1200-1200/? W/Resources: Preloaded drawable resource #0x10804ce (android:drawable/menu_hardkey_panel_holo_light) that varies with configuration!!
01-25 13:05:26.423 1200-1200/? W/Resources: Preloaded drawable resource #0x10804d5 (android:drawable/menu_submenu_background) that varies with configuration!!
01-25 13:05:26.424 1200-1200/? W/Resources: Preloaded drawable resource #0x10804cc (android:drawable/menu_dropdown_panel_holo_light) that varies with configuration!!
01-25 13:05:26.427 1200-1200/? W/Resources: Preloaded drawable resource #0x10804cb (android:drawable/menu_dropdown_panel_holo_dark) that varies with configuration!!
01-25 13:05:26.429 1200-1200/? W/Resources: Preloaded drawable resource #0x10804d2 (android:drawable/menu_popup_panel_holo_light) that varies with configuration!!
01-25 13:05:26.429 1200-1200/? W/Resources: Preloaded drawable resource #0x10804d1 (android:drawable/menu_popup_panel_holo_dark) that varies with configuration!!
01-25 13:05:26.431 1200-1200/? W/Resources: Preloaded drawable resource #0x10804d2 (android:drawable/menu_popup_panel_holo_light) that varies with configuration!!
01-25 13:05:26.432 1200-1200/? W/Resources: Preloaded drawable resource #0x10804cc (android:drawable/menu_dropdown_panel_holo_light) that varies with configuration!!
01-25 13:05:26.432 1200-1200/? W/Resources: Preloaded drawable resource #0x10804d0 (android:drawable/menu_panel_holo_light) that varies with configuration!!
01-25 13:05:26.432 1200-1200/? W/Resources: Preloaded drawable resource #0x10804d1 (android:drawable/menu_popup_panel_holo_dark) that varies with configuration!!
01-25 13:05:26.433 1200-1200/? W/Resources: Preloaded drawable resource #0x10804cb (android:drawable/menu_dropdown_panel_holo_dark) that varies with configuration!!
01-25 13:05:26.433 1200-1200/? W/Resources: Preloaded drawable resource #0x10804cf (android:drawable/menu_panel_holo_dark) that varies with configuration!!
01-25 13:05:26.433 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fa (android:drawable/spinner_16_outer_holo) that varies with configuration!!
01-25 13:05:26.441 1200-1200/? W/Resources: Preloaded drawable resource #0x10805f9 (android:drawable/spinner_16_inner_holo) that varies with configuration!!
01-25 13:05:26.441 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fc (android:drawable/spinner_48_outer_holo) that varies with configuration!!
01-25 13:05:26.442 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fb (android:drawable/spinner_48_inner_holo) that varies with configuration!!
01-25 13:05:26.444 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fe (android:drawable/spinner_76_outer_holo) that varies with configuration!!
01-25 13:05:26.445 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fd (android:drawable/spinner_76_inner_holo) that varies with configuration!!
01-25 13:05:26.445 1200-1200/? W/Resources: Preloaded drawable resource #0x108055b (android:drawable/progress_bg_holo_dark) that varies with configuration!!
01-25 13:05:26.445 1200-1200/? W/Resources: Preloaded drawable resource #0x108055c (android:drawable/progress_bg_holo_light) that varies with configuration!!
01-25 13:05:26.446 1200-1200/? W/Resources: Preloaded drawable resource #0x108055b (android:drawable/progress_bg_holo_dark) that varies with configuration!!
01-25 13:05:26.446 1200-1200/? W/Resources: Preloaded drawable resource #0x108056c (android:drawable/progress_secondary_holo_dark) that varies with configuration!!
01-25 13:05:26.447 1200-1200/? W/Resources: Preloaded drawable resource #0x108056a (android:drawable/progress_primary_holo_dark) that varies with configuration!!
01-25 13:05:26.447 1200-1200/? W/Resources: Preloaded drawable resource #0x108055d (android:drawable/progress_horizontal_holo_dark) that varies with configuration!!
01-25 13:05:26.447 1200-1200/? W/Resources: Preloaded drawable resource #0x108055c (android:drawable/progress_bg_holo_light) that varies with configuration!!
01-25 13:05:26.448 1200-1200/? W/Resources: Preloaded drawable resource #0x108056d (android:drawable/progress_secondary_holo_light) that varies with configuration!!
01-25 13:05:26.448 1200-1200/? W/Resources: Preloaded drawable resource #0x108056b (android:drawable/progress_primary_holo_light) that varies with configuration!!
01-25 13:05:26.448 1200-1200/? W/Resources: Preloaded drawable resource #0x108055e (android:drawable/progress_horizontal_holo_light) that varies with configuration!!
01-25 13:05:26.449 1200-1200/? W/Resources: Preloaded drawable resource #0x1080576 (android:drawable/progressbar_indeterminate_holo1) that varies with configuration!!
01-25 13:05:26.449 1200-1200/? W/Resources: Preloaded drawable resource #0x1080577 (android:drawable/progressbar_indeterminate_holo2) that varies with configuration!!
01-25 13:05:26.450 1200-1200/? W/Resources: Preloaded drawable resource #0x1080578 (android:drawable/progressbar_indeterminate_holo3) that varies with configuration!!
01-25 13:05:26.451 1200-1200/? W/Resources: Preloaded drawable resource #0x1080579 (android:drawable/progressbar_indeterminate_holo4) that varies with configuration!!
01-25 13:05:26.451 1200-1200/? W/Resources: Preloaded drawable resource #0x108057a (android:drawable/progressbar_indeterminate_holo5) that varies with configuration!!
01-25 13:05:26.452 1200-1200/? W/Resources: Preloaded drawable resource #0x108057b (android:drawable/progressbar_indeterminate_holo6) that varies with configuration!!
01-25 13:05:26.452 1200-1200/? W/Resources: Preloaded drawable resource #0x108057c (android:drawable/progressbar_indeterminate_holo7) that varies with configuration!!
01-25 13:05:26.452 1200-1200/? W/Resources: Preloaded drawable resource #0x108057d (android:drawable/progressbar_indeterminate_holo8) that varies with configuration!!
01-25 13:05:26.452 1200-1200/? W/Resources: Preloaded drawable resource #0x1080560 (android:drawable/progress_indeterminate_horizontal_holo) that varies with configuration!!
01-25 13:05:26.454 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fe (android:drawable/spinner_76_outer_holo) that varies with configuration!!
01-25 13:05:26.455 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fd (android:drawable/spinner_76_inner_holo) that varies with configuration!!
01-25 13:05:26.455 1200-1200/? W/Resources: Preloaded drawable resource #0x1080563 (android:drawable/progress_large_holo) that varies with configuration!!
01-25 13:05:26.457 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fc (android:drawable/spinner_48_outer_holo) that varies with configuration!!
01-25 13:05:26.458 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fb (android:drawable/spinner_48_inner_holo) that varies with configuration!!
01-25 13:05:26.458 1200-1200/? W/Resources: Preloaded drawable resource #0x1080567 (android:drawable/progress_medium_holo) that varies with configuration!!
01-25 13:05:26.460 1200-1200/? W/Resources: Preloaded drawable resource #0x108056a (android:drawable/progress_primary_holo_dark) that varies with configuration!!
01-25 13:05:26.460 1200-1200/? W/Resources: Preloaded drawable resource #0x108056b (android:drawable/progress_primary_holo_light) that varies with configuration!!
01-25 13:05:26.460 1200-1200/? W/Resources: Preloaded drawable resource #0x108056c (android:drawable/progress_secondary_holo_dark) that varies with configuration!!
01-25 13:05:26.462 1200-1200/? W/Resources: Preloaded drawable resource #0x108056d (android:drawable/progress_secondary_holo_light) that varies with configuration!!
01-25 13:05:26.462 1200-1200/? W/Resources: Preloaded drawable resource #0x10805fa (android:drawable/spinner_16_outer_holo) that varies with configuration!!
01-25 13:05:26.462 1200-1200/? W/Resources: Preloaded drawable resource #0x10805f9 (android:drawable/spinner_16_inner_holo) that varies with configuration!!
01-25 13:05:26.462 1200-1200/? W/Resources: Preloaded drawable resource #0x108056f (android:drawable/progress_small_holo) that varies with configuration!!
01-25 13:05:26.463 1200-1200/? W/Resources: Preloaded drawable resource #0x10805db (android:drawable/scrubber_track_holo_dark) that varies with configuration!!
01-25 13:05:26.463 1200-1200/? W/Resources: Preloaded drawable resource #0x10805da (android:drawable/scrubber_secondary_holo) that varies with configuration!!
01-25 13:05:26.463 1200-1200/? W/Resources: Preloaded drawable resource #0x10805d6 (android:drawable/scrubber_primary_holo) that varies with configuration!!
01-25 13:05:26.464 1200-1200/? W/Resources: Preloaded drawable resource #0x10805d8 (android:drawable/scrubber_progress_horizontal_holo_dark) that varies with configuration!!
01-25 13:05:26.464 1200-1200/? W/Resources: Preloaded drawable resource #0x10805dc (android:drawable/scrubber_track_holo_light) that varies with configuration!!
01-25 13:05:26.464 1200-1200/? W/Resources: Preloaded drawable resource #0x10805da (android:drawable/scrubber_secondary_holo) that varies with configuration!!
01-25 13:05:26.464 1200-1200/? W/Resources: Preloaded drawable resource #0x10805d6 (android:drawable/scrubber_primary_holo) that varies with configuration!!
01-25 13:05:26.464 1200-1200/? W/Resources: Preloaded drawable resource #0x10805d9 (android:drawable/scrubber_progress_horizontal_holo_light) that varies with configuration!!
01-25 13:05:26.465 1200-1200/? W/Resources: Preloaded drawable resource #0x10805ca (android:drawable/scrollbar_handle_holo_dark) that varies with configuration!!
01-25 13:05:26.465 1200-1200/? W/Resources: Preloaded drawable resource #0x10805cb (android:drawable/scrollbar_handle_holo_light) that varies with configuration!!
01-25 13:05:26.465 1200-1200/? W/Resources: Preloaded drawable resource #0x1080621 (android:drawable/spinner_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.465 1200-1200/? W/Resources: Preloaded drawable resource #0x108062e (android:drawable/spinner_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.466 1200-1200/? W/Resources: Preloaded drawable resource #0x1080627 (android:drawable/spinner_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.466 1200-1200/? W/Resources: Preloaded drawable resource #0x108061c (android:drawable/spinner_default_holo_dark) that varies with configuration!!
01-25 13:05:26.466 1200-1200/? W/Resources: Preloaded drawable resource #0x1080615 (android:drawable/spinner_background_holo_dark) that varies with configuration!!
01-25 13:05:26.466 1200-1200/? W/Resources: Preloaded drawable resource #0x1080623 (android:drawable/spinner_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.466 1200-1200/? W/Resources: Preloaded drawable resource #0x1080630 (android:drawable/spinner_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.467 1200-1200/? W/Resources: Preloaded drawable resource #0x1080629 (android:drawable/spinner_focused_holo_light) that varies with configuration!!
01-25 13:05:26.468 1200-1200/? W/Resources: Preloaded drawable resource #0x108061e (android:drawable/spinner_default_holo_light) that varies with configuration!!
01-25 13:05:26.468 1200-1200/? W/Resources: Preloaded drawable resource #0x1080616 (android:drawable/spinner_background_holo_light) that varies with configuration!!
01-25 13:05:26.469 1200-1200/? W/Resources: Preloaded drawable resource #0x1080601 (android:drawable/spinner_ab_default_holo_dark) that varies with configuration!!
01-25 13:05:26.469 1200-1200/? W/Resources: Preloaded drawable resource #0x1080603 (android:drawable/spinner_ab_default_holo_light) that varies with configuration!!
01-25 13:05:26.469 1200-1200/? W/Resources: Preloaded drawable resource #0x1080605 (android:drawable/spinner_ab_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.469 1200-1200/? W/Resources: Preloaded drawable resource #0x1080607 (android:drawable/spinner_ab_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.469 1200-1200/? W/Resources: Preloaded drawable resource #0x1080609 (android:drawable/spinner_ab_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.470 1200-1200/? W/Resources: Preloaded drawable resource #0x108060b (android:drawable/spinner_ab_focused_holo_light) that varies with configuration!!
01-25 13:05:26.470 1200-1200/? W/Resources: Preloaded drawable resource #0x108060f (android:drawable/spinner_ab_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.471 1200-1200/? W/Resources: Preloaded drawable resource #0x1080611 (android:drawable/spinner_ab_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.471 1200-1200/? W/Resources: Preloaded drawable resource #0x1080605 (android:drawable/spinner_ab_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.472 1200-1200/? W/Resources: Preloaded drawable resource #0x108060f (android:drawable/spinner_ab_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.472 1200-1200/? W/Resources: Preloaded drawable resource #0x1080609 (android:drawable/spinner_ab_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.472 1200-1200/? W/Resources: Preloaded drawable resource #0x1080601 (android:drawable/spinner_ab_default_holo_dark) that varies with configuration!!
01-25 13:05:26.472 1200-1200/? W/Resources: Preloaded drawable resource #0x108060d (android:drawable/spinner_ab_holo_dark) that varies with configuration!!
01-25 13:05:26.473 1200-1200/? W/Resources: Preloaded drawable resource #0x1080607 (android:drawable/spinner_ab_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.473 1200-1200/? W/Resources: Preloaded drawable resource #0x1080611 (android:drawable/spinner_ab_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.473 1200-1200/? W/Resources: Preloaded drawable resource #0x108060b (android:drawable/spinner_ab_focused_holo_light) that varies with configuration!!
01-25 13:05:26.473 1200-1200/? W/Resources: Preloaded drawable resource #0x1080603 (android:drawable/spinner_ab_default_holo_light) that varies with configuration!!
01-25 13:05:26.473 1200-1200/? W/Resources: Preloaded drawable resource #0x108060e (android:drawable/spinner_ab_holo_light) that varies with configuration!!
01-25 13:05:26.474 1200-1200/? W/Resources: Preloaded drawable resource #0x108061c (android:drawable/spinner_default_holo_dark) that varies with configuration!!
01-25 13:05:26.474 1200-1200/? W/Resources: Preloaded drawable resource #0x108061e (android:drawable/spinner_default_holo_light) that varies with configuration!!
01-25 13:05:26.474 1200-1200/? W/Resources: Preloaded drawable resource #0x1080621 (android:drawable/spinner_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.474 1200-1200/? W/Resources: Preloaded drawable resource #0x1080623 (android:drawable/spinner_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.474 1200-1200/? W/Resources: Preloaded drawable resource #0x1080627 (android:drawable/spinner_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.475 1200-1200/? W/Resources: Preloaded drawable resource #0x1080629 (android:drawable/spinner_focused_holo_light) that varies with configuration!!
01-25 13:05:26.475 1200-1200/? W/Resources: Preloaded drawable resource #0x108062e (android:drawable/spinner_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.475 1200-1200/? W/Resources: Preloaded drawable resource #0x1080630 (android:drawable/spinner_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.475 1200-1200/? W/Resources: Preloaded drawable resource #0x108024e (android:drawable/cab_background_bottom_holo_dark) that varies with configuration!!
01-25 13:05:26.475 1200-1200/? W/Resources: Preloaded drawable resource #0x1080253 (android:drawable/cab_background_top_holo_light) that varies with configuration!!
01-25 13:05:26.476 1200-1200/? W/Resources: Preloaded drawable resource #0x108024f (android:drawable/cab_background_bottom_holo_light) that varies with configuration!!
01-25 13:05:26.476 1200-1200/? W/Resources: Preloaded drawable resource #0x108030e (android:drawable/ic_cab_done_holo_dark) that varies with configuration!!
01-25 13:05:26.476 1200-1200/? W/Resources: Preloaded drawable resource #0x1080252 (android:drawable/cab_background_top_holo_dark) that varies with configuration!!
01-25 13:05:26.476 1200-1200/? W/Resources: Preloaded drawable resource #0x108030f (android:drawable/ic_cab_done_holo_light) that varies with configuration!!
01-25 13:05:26.476 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d6 (android:drawable/btn_cab_done_default_holo_dark) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d9 (android:drawable/btn_cab_done_focused_holo_light) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d7 (android:drawable/btn_cab_done_default_holo_light) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800dc (android:drawable/btn_cab_done_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d8 (android:drawable/btn_cab_done_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800dd (android:drawable/btn_cab_done_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x1080498 (android:drawable/list_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d9 (android:drawable/btn_cab_done_focused_holo_light) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d7 (android:drawable/btn_cab_done_default_holo_light) that varies with configuration!!
01-25 13:05:26.477 1200-1200/? W/Resources: Preloaded drawable resource #0x10800db (android:drawable/btn_cab_done_holo_light) that varies with configuration!!
01-25 13:05:26.478 1200-1200/? W/Resources: Preloaded drawable resource #0x1080497 (android:drawable/list_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.478 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d8 (android:drawable/btn_cab_done_focused_holo_dark) that varies with configuration!!
01-25 13:05:26.478 1200-1200/? W/Resources: Preloaded drawable resource #0x10800d6 (android:drawable/btn_cab_done_default_holo_dark) that varies with configuration!!
01-25 13:05:26.478 1200-1200/? W/Resources: Preloaded drawable resource #0x10800da (android:drawable/btn_cab_done_holo_dark) that varies with configuration!!
01-25 13:05:26.480 1200-1200/? W/Resources: Preloaded drawable resource #0x1080038 (android:drawable/ic_menu_close_clear_cancel) that varies with configuration!!
01-25 13:05:26.483 1200-1200/? W/Resources: Preloaded drawable resource #0x10803bb (android:drawable/ic_menu_copy_holo_dark) that varies with configuration!!
01-25 13:05:26.483 1200-1200/? W/Resources: Preloaded drawable resource #0x10803bc (android:drawable/ic_menu_copy_holo_light) that varies with configuration!!
01-25 13:05:26.484 1200-1200/? W/Resources: Preloaded drawable resource #0x10803bf (android:drawable/ic_menu_cut_holo_dark) that varies with configuration!!
01-25 13:05:26.484 1200-1200/? W/Resources: Preloaded drawable resource #0x10803c0 (android:drawable/ic_menu_cut_holo_light) that varies with configuration!!
01-25 13:05:26.492 1200-1200/? W/Resources: Preloaded drawable resource #0x1080045 (android:drawable/ic_menu_more) that varies with configuration!!
01-25 13:05:26.492 1200-1200/? W/Resources: Preloaded drawable resource #0x10803d9 (android:drawable/ic_menu_moreoverflow_normal_holo_dark) that varies with configuration!!
01-25 13:05:26.492 1200-1200/? W/Resources: Preloaded drawable resource #0x10803d4 (android:drawable/ic_menu_moreoverflow_holo_dark) that varies with configuration!!
01-25 13:05:26.492 1200-1200/? W/Resources: Preloaded drawable resource #0x10803da (android:drawable/ic_menu_moreoverflow_normal_holo_light) that varies with configuration!!
01-25 13:05:26.492 1200-1200/? W/Resources: Preloaded drawable resource #0x10803d5 (android:drawable/ic_menu_moreoverflow_holo_light) that varies with configuration!!
01-25 13:05:26.492 1200-1200/? W/Resources: Preloaded drawable resource #0x10803dd (android:drawable/ic_menu_paste_holo_dark) that varies with configuration!!
01-25 13:05:26.493 1200-1200/? W/Resources: Preloaded drawable resource #0x10803de (android:drawable/ic_menu_paste_holo_light) that varies with configuration!!
01-25 13:05:26.493 1200-1200/? W/Resources: Preloaded drawable resource #0x10803e7 (android:drawable/ic_menu_selectall_holo_light) that varies with configuration!!
01-25 13:05:26.493 1200-1200/? W/Resources: Preloaded drawable resource #0x10803e6 (android:drawable/ic_menu_selectall_holo_dark) that varies with configuration!!
01-25 13:05:26.495 1200-1200/? W/Resources: Preloaded drawable resource #0x108031a (android:drawable/ic_clear_disabled) that varies with configuration!!
01-25 13:05:26.508 1200-1200/? W/Resources: Preloaded drawable resource #0x108031f (android:drawable/ic_clear_normal) that varies with configuration!!
01-25 13:05:26.508 1200-1200/? W/Resources: Preloaded drawable resource #0x1080319 (android:drawable/ic_clear) that varies with configuration!!
01-25 13:05:26.508 1200-1200/? W/Resources: Preloaded drawable resource #0x108031a (android:drawable/ic_clear_disabled) that varies with configuration!!
01-25 13:05:26.508 1200-1200/? W/Resources: Preloaded drawable resource #0x108031f (android:drawable/ic_clear_normal) that varies with configuration!!
01-25 13:05:26.508 1200-1200/? W/Resources: Preloaded drawable resource #0x1080419 (android:drawable/ic_search_api_holo_dark) that varies with configuration!!
01-25 13:05:26.509 1200-1200/? W/Resources: Preloaded drawable resource #0x108041a (android:drawable/ic_search_api_holo_light) that varies with configuration!!
01-25 13:05:26.509 1200-1200/? W/Resources: Preloaded drawable resource #0x108034b (android:drawable/ic_go) that varies with configuration!!
01-25 13:05:26.509 1200-1200/? W/Resources: Preloaded drawable resource #0x1080431 (android:drawable/ic_voice_search_api_holo_dark) that varies with configuration!!
01-25 13:05:26.509 1200-1200/? W/Resources: Preloaded drawable resource #0x1080432 (android:drawable/ic_voice_search_api_holo_light) that varies with configuration!!
01-25 13:05:26.510 1200-1200/? W/Resources: Preloaded drawable resource #0x108026e (android:drawable/dialog_bottom_holo_dark) that varies with configuration!!
01-25 13:05:26.511 1200-1200/? W/Resources: Preloaded drawable resource #0x108026f (android:drawable/dialog_bottom_holo_light) that varies with configuration!!
01-25 13:05:26.511 1200-1200/? W/Resources: Preloaded drawable resource #0x108027c (android:drawable/dialog_middle_holo_dark) that varies with configuration!!
01-25 13:05:26.512 1200-1200/? W/Resources: Preloaded drawable resource #0x108027d (android:drawable/dialog_middle_holo_light) that varies with configuration!!
01-25 13:05:26.513 1200-1200/? W/Resources: Preloaded drawable resource #0x108027e (android:drawable/dialog_top_holo_dark) that varies with configuration!!
01-25 13:05:26.514 1200-1200/? W/Resources: Preloaded drawable resource #0x108027f (android:drawable/dialog_top_holo_light) that varies with configuration!!
01-25 13:05:26.517 1200-1200/? W/Resources: Preloaded drawable resource #0x1080336 (android:drawable/ic_dialog_alert_holo_dark) that varies with configuration!!
01-25 13:05:26.518 1200-1200/? W/Resources: Preloaded drawable resource #0x1080337 (android:drawable/ic_dialog_alert_holo_light) that varies with configuration!!
01-25 13:05:26.529 1200-1200/? W/Resources: Preloaded drawable resource #0x108048c (android:drawable/list_divider_holo_dark) that varies with configuration!!
01-25 13:05:26.529 1200-1200/? W/Resources: Preloaded drawable resource #0x108048d (android:drawable/list_divider_holo_light) that varies with configuration!!
01-25 13:05:26.530 1200-1200/? W/Resources: Preloaded drawable resource #0x108048d (android:drawable/list_divider_holo_light) that varies with configuration!!
01-25 13:05:26.531 1200-1200/? W/Resources: Preloaded drawable resource #0x10800c1 (android:drawable/ab_transparent_dark_holo) that varies with configuration!!
01-25 13:05:26.531 1200-1200/? W/Resources: Preloaded drawable resource #0x10800bf (android:drawable/ab_stacked_transparent_dark_holo) that varies with configuration!!
01-25 13:05:26.533 1200-1200/? W/Resources: Preloaded drawable resource #0x10800a1 (android:drawable/ab_bottom_transparent_dark_holo) that varies with configuration!!
01-25 13:05:26.533 1200-1200/? W/Resources: Preloaded drawable resource #0x10800b7 (android:drawable/ab_solid_dark_holo) that varies with configuration!!
01-25 13:05:26.534 1200-1200/? W/Resources: Preloaded drawable resource #0x10800bc (android:drawable/ab_stacked_solid_dark_holo) that varies with configuration!!
01-25 13:05:26.534 1200-1200/? W/Resources: Preloaded drawable resource #0x108009e (android:drawable/ab_bottom_solid_dark_holo) that varies with configuration!!
01-25 13:05:26.537 1200-1200/? W/Resources: Preloaded drawable resource #0x10800c2 (android:drawable/ab_transparent_light_holo) that varies with configuration!!
01-25 13:05:26.538 1200-1200/? W/Resources: Preloaded drawable resource #0x10800c0 (android:drawable/ab_stacked_transparent_light_holo) that varies with configuration!!
01-25 13:05:26.544 1200-1200/? W/Resources: Preloaded drawable resource #0x10800a2 (android:drawable/ab_bottom_transparent_light_holo) that varies with configuration!!
01-25 13:05:26.544 1200-1200/? W/Resources: Preloaded drawable resource #0x10800b8 (android:drawable/ab_solid_light_holo) that varies with configuration!!
01-25 13:05:26.544 1200-1200/? W/Resources: Preloaded drawable resource #0x10800be (android:drawable/ab_stacked_solid_light_holo) that varies with configuration!!
01-25 13:05:26.545 1200-1200/? W/Resources: Preloaded drawable resource #0x10800a0 (android:drawable/ab_bottom_solid_light_holo) that varies with configuration!!
01-25 13:05:26.545 1200-1200/? W/Resources: Preloaded drawable resource #0x10800b9 (android:drawable/ab_solid_shadow_holo) that varies with configuration!!
01-25 13:05:26.545 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b8 (android:drawable/list_selector_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.545 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b8 (android:drawable/list_selector_disabled_holo_dark) that varies with configuration!!
01-25 13:05:26.545 1200-1200/? W/Resources: Preloaded drawable resource #0x1080490 (android:drawable/list_focused_holo) that varies with configuration!!
01-25 13:05:26.545 1200-1200/? W/Resources: Preloaded drawable resource #0x1080447 (android:drawable/item_background_holo_dark) that varies with configuration!!
01-25 13:05:26.546 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b9 (android:drawable/list_selector_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.546 1200-1200/? W/Resources: Preloaded drawable resource #0x10804b9 (android:drawable/list_selector_disabled_holo_light) that varies with configuration!!
01-25 13:05:26.546 1200-1200/? W/Resources: Preloaded drawable resource #0x1080490 (android:drawable/list_focused_holo) that varies with configuration!!
01-25 13:05:26.546 1200-1200/? W/Resources: Preloaded drawable resource #0x1080448 (android:drawable/item_background_holo_light) that varies with configuration!!
01-25 13:05:26.546 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d1 (android:drawable/fastscroll_thumb_pressed_holo) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802ce (android:drawable/fastscroll_thumb_default_holo) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802cf (android:drawable/fastscroll_thumb_holo) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d1 (android:drawable/fastscroll_thumb_pressed_holo) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802ce (android:drawable/fastscroll_thumb_default_holo) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d7 (android:drawable/fastscroll_track_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d2 (android:drawable/fastscroll_track_default_holo_dark) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d4 (android:drawable/fastscroll_track_holo_dark) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d7 (android:drawable/fastscroll_track_pressed_holo_dark) that varies with configuration!!
01-25 13:05:26.547 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d2 (android:drawable/fastscroll_track_default_holo_dark) that varies with configuration!!
01-25 13:05:26.548 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d8 (android:drawable/fastscroll_track_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.548 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d3 (android:drawable/fastscroll_track_default_holo_light) that varies with configuration!!
01-25 13:05:26.548 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d5 (android:drawable/fastscroll_track_holo_light) that varies with configuration!!
01-25 13:05:26.548 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d8 (android:drawable/fastscroll_track_pressed_holo_light) that varies with configuration!!
01-25 13:05:26.548 1200-1200/? W/Resources: Preloaded drawable resource #0x10802d3 (android:drawable/fastscroll_track_default_holo_light) that varies with configuration!!
01-25 13:05:26.563 1200-1200/? W/Resources: Preloaded drawable resource #0x10802a9 (android:drawable/editbox_dropdown_background_dark) that varies with configuration!!
01-25 13:05:26.563 1200-1200/? W/Resources: Preloaded drawable resource #0x1080726 (android:drawable/textfield_search_selected_holo_dark) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080718 (android:drawable/textfield_search_default_holo_dark) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080728 (android:drawable/textfield_searchview_holo_dark) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080723 (android:drawable/textfield_search_right_selected_holo_dark) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080721 (android:drawable/textfield_search_right_default_holo_dark) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x108072a (android:drawable/textfield_searchview_right_holo_dark) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080727 (android:drawable/textfield_search_selected_holo_light) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080719 (android:drawable/textfield_search_default_holo_light) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080729 (android:drawable/textfield_searchview_holo_light) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080724 (android:drawable/textfield_search_right_selected_holo_light) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x1080722 (android:drawable/textfield_search_right_default_holo_light) that varies with configuration!!
01-25 13:05:26.564 1200-1200/? W/Resources: Preloaded drawable resource #0x108072b (android:drawable/textfield_searchview_right_holo_light) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080726 (android:drawable/textfield_search_selected_holo_dark) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080718 (android:drawable/textfield_search_default_holo_dark) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080723 (android:drawable/textfield_search_right_selected_holo_dark) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080721 (android:drawable/textfield_search_right_default_holo_dark) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080727 (android:drawable/textfield_search_selected_holo_light) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080719 (android:drawable/textfield_search_default_holo_light) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080724 (android:drawable/textfield_search_right_selected_holo_light) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x1080722 (android:drawable/textfield_search_right_default_holo_light) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e3 (android:drawable/tab_unselected_holo) that varies with configuration!!
01-25 13:05:26.565 1200-1200/? W/Resources: Preloaded drawable resource #0x10806de (android:drawable/tab_selected_holo) that varies with configuration!!
01-25 13:05:26.566 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e2 (android:drawable/tab_unselected_focused_holo) that varies with configuration!!
01-25 13:05:26.566 1200-1200/? W/Resources: Preloaded drawable resource #0x10806dd (android:drawable/tab_selected_focused_holo) that varies with configuration!!
01-25 13:05:26.566 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e4 (android:drawable/tab_unselected_pressed_holo) that varies with configuration!!
01-25 13:05:26.566 1200-1200/? W/Resources: Preloaded drawable resource #0x10806df (android:drawable/tab_selected_pressed_holo) that varies with configuration!!
01-25 13:05:26.566 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e4 (android:drawable/tab_unselected_pressed_holo) that varies with configuration!!
01-25 13:05:26.567 1200-1200/? W/Resources: Preloaded drawable resource #0x10806df (android:drawable/tab_selected_pressed_holo) that varies with configuration!!
01-25 13:05:26.567 1200-1200/? W/Resources: Preloaded drawable resource #0x10806d0 (android:drawable/tab_indicator_holo) that varies with configuration!!
01-25 13:05:26.567 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e3 (android:drawable/tab_unselected_holo) that varies with configuration!!
01-25 13:05:26.567 1200-1200/? W/Resources: Preloaded drawable resource #0x10806de (android:drawable/tab_selected_holo) that varies with configuration!!
01-25 13:05:26.567 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e2 (android:drawable/tab_unselected_focused_holo) that varies with configuration!!
01-25 13:05:26.568 1200-1200/? W/Resources: Preloaded drawable resource #0x10806dd (android:drawable/tab_selected_focused_holo) that varies with configuration!!
01-25 13:05:26.568 1200-1200/? W/Resources: Preloaded drawable resource #0x10806e4 (android:drawable/tab_unselected_pressed_holo) that varies with configuration!!
01-25 13:05:26.568 1200-1200/? W/Resources: Preloaded drawable resource #0x10806df (android:drawable/tab_selected_pressed_holo) that varies with configuration!!
01-25 13:05:26.569 1200-1200/? W/Resources: Preloaded drawable resource #0x1080590 (android:drawable/quickcontact_badge_overlay_pressed_dark) that varies with configuration!!
01-25 13:05:26.570 1200-1200/? W/Resources: Preloaded drawable resource #0x1080587 (android:drawable/quickcontact_badge_overlay_focused_dark) that varies with configuration!!
01-25 13:05:26.570 1200-1200/? W/Resources: Preloaded drawable resource #0x108058c (android:drawable/quickcontact_badge_overlay_normal_dark) that varies with configuration!!
01-25 13:05:26.571 1200-1200/? W/Resources: Preloaded drawable resource #0x1080586 (android:drawable/quickcontact_badge_overlay_dark) that varies with configuration!!
01-25 13:05:26.571 1200-1200/? W/Resources: Preloaded drawable resource #0x108058c (android:drawable/quickcontact_badge_overlay_normal_dark) that varies with configuration!!
01-25 13:05:26.572 1200-1200/? W/Resources: Preloaded drawable resource #0x1080590 (android:drawable/quickcontact_badge_overlay_pressed_dark) that varies with configuration!!
01-25 13:05:26.572 1200-1200/? W/Resources: Preloaded drawable resource #0x1080592 (android:drawable/quickcontact_badge_overlay_pressed_light) that varies with configuration!!
01-25 13:05:26.572 1200-1200/? W/Resources: Preloaded drawable resource #0x1080589 (android:drawable/quickcontact_badge_overlay_focused_light) that varies with configuration!!
01-25 13:05:26.572 1200-1200/? W/Resources: Preloaded drawable resource #0x108058e (android:drawable/quickcontact_badge_overlay_normal_light) that varies with configuration!!
01-25 13:05:26.572 1200-1200/? W/Resources: Preloaded drawable resource #0x108058b (android:drawable/quickcontact_badge_overlay_light) that varies with configuration!!
01-25 13:05:26.572 1200-1200/? W/Resources: Preloaded drawable resource #0x108058e (android:drawable/quickcontact_badge_overlay_normal_light) that varies with configuration!!
01-25 13:05:26.573 1200-1200/? W/Resources: Preloaded drawable resource #0x1080592 (android:drawable/quickcontact_badge_overlay_pressed_light) that varies with configuration!!
01-25 13:05:26.573 1200-1200/? W/Resources: Preloaded drawable resource #0x10800b5 (android:drawable/ab_share_pack_material) that varies with configuration!!
01-25 13:05:26.583 1200-1200/? W/Resources: Preloaded drawable resource #0x10800ba (android:drawable/ab_solid_shadow_material) that varies with configuration!!
01-25 13:05:26.585 1196-1196/? I/ServiceManager: Waiting for service media.camera.proxy...
01-25 13:05:26.596 1200-1200/? W/Resources: Preloaded drawable resource #0x1080181 (android:drawable/btn_radio_material_anim) that varies with configuration!!
01-25 13:05:26.596 1200-1200/? W/Resources: Preloaded drawable resource #0x10801f5 (android:drawable/btn_star_material) that varies with configuration!!
01-25 13:05:26.597 1200-1200/? W/Resources: Preloaded drawable resource #0x1080250 (android:drawable/cab_background_bottom_material) that varies with configuration!!
01-25 13:05:26.597 1200-1200/? W/Resources: Preloaded drawable resource #0x1080254 (android:drawable/cab_background_top_material) that varies with configuration!!
01-25 13:05:26.597 1200-1200/? W/Resources: Preloaded drawable resource #0x10802a6 (android:drawable/edit_text_material) that varies with configuration!!
01-25 13:05:26.598 1200-1200/? W/Resources: Preloaded drawable resource #0x10802c2 (android:drawable/expander_group_material) that varies with configuration!!
01-25 13:05:26.599 1200-1200/? W/Resources: Preloaded drawable resource #0x1080329 (android:drawable/ic_commit_search_api_material) that varies with configuration!!
01-25 13:05:26.614 1200-1200/? W/Resources: Preloaded drawable resource #0x1080343 (android:drawable/ic_find_next_material) that varies with configuration!!
01-25 13:05:26.614 1200-1200/? W/Resources: Preloaded drawable resource #0x1080347 (android:drawable/ic_find_previous_material) that varies with configuration!!
01-25 13:05:26.630 1200-1200/? W/Resources: Preloaded drawable resource #0x1080395 (android:drawable/ic_media_route_connecting_material) that varies with configuration!!
01-25 13:05:26.631 1200-1200/? W/Resources: Preloaded drawable resource #0x1080395 (android:drawable/ic_media_route_connecting_material) that varies with configuration!!
01-25 13:05:26.632 1200-1200/? W/Resources: Preloaded drawable resource #0x108039b (android:drawable/ic_media_route_material) that varies with configuration!!
01-25 13:05:26.633 1200-1200/? W/Resources: Preloaded drawable resource #0x10803c7 (android:drawable/ic_menu_find_material) that varies with configuration!!
01-25 13:05:26.633 1200-1200/? W/Resources: Preloaded drawable resource #0x10803e4 (android:drawable/ic_menu_search_material) that varies with configuration!!
01-25 13:05:26.634 1200-1200/? W/Resources: Preloaded drawable resource #0x108049b (android:drawable/list_section_divider_material) that varies with configuration!!
01-25 13:05:26.642 1200-1200/? W/Resources: Preloaded drawable resource #0x10805bf (android:drawable/ratingbar_material) that varies with configuration!!
01-25 13:05:26.644 1200-1200/? W/Resources: Preloaded drawable resource #0x10805c3 (android:drawable/ratingbar_small_material) that varies with configuration!!
01-25 13:05:26.645 1200-1200/? W/Resources: Preloaded drawable resource #0x10805be (android:drawable/ratingbar_indicator_material) that varies with configuration!!
01-25 13:05:26.649 1200-1200/? W/Resources: Preloaded drawable resource #0x10802a6 (android:drawable/edit_text_material) that varies with configuration!!
01-25 13:05:26.649 1200-1200/? W/Resources: Preloaded drawable resource #0x1080633 (android:drawable/spinner_textfield_background_material) that varies with configuration!!
01-25 13:05:26.661 1200-1200/? W/Resources: Preloaded drawable resource #0x10806a3 (android:drawable/switch_thumb_material_anim) that varies with configuration!!
01-25 13:05:26.663 1200-1200/? W/Resources: Preloaded drawable resource #0x108071f (android:drawable/textfield_search_material) that varies with configuration!!
01-25 13:05:26.663 1200-1200/? W/Resources: Preloaded drawable resource #0x10806ed (android:drawable/text_select_handle_left_material) that varies with configuration!!
01-25 13:05:26.663 1200-1200/? W/Resources: Preloaded drawable resource #0x10806f0 (android:drawable/text_select_handle_middle_material) that varies with configuration!!
01-25 13:05:26.664 1200-1200/? W/Resources: Preloaded drawable resource #0x10806f3 (android:drawable/text_select_handle_right_material) that varies with configuration!!
01-25 13:05:26.664 1200-1200/? I/Zygote: ...preloaded 342 resources in 453ms.
01-25 13:05:26.665 1200-1200/? I/Zygote: ...preloaded 41 resources in 1ms.
01-25 13:05:26.665 1200-1200/? E/libEGL: load_driver(/system/lib/egl/libGLES_emulation.so): dlopen failed: library "/system/lib/egl/libGLES_emulation.so" not found
01-25 13:05:26.666 1200-1200/? D/libEGL: loaded /system/lib/egl/libEGL_emulation.so
01-25 13:05:26.666 1200-1200/? D/libEGL: loaded /system/lib/egl/libGLESv1_CM_emulation.so
01-25 13:05:26.669 1200-1200/? D/libEGL: loaded /system/lib/egl/libGLESv2_emulation.so
01-25 13:05:26.673 1200-1200/? I/Zygote: Preloading shared libraries...
01-25 13:05:26.704 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-en-us.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-en-us.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-eu.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-eu.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-hu.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-hu.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-hy.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-hy.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-nb.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-nb.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-nn.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-nn.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-sa.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-sa.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.705 1200-1200/? E/Hyphenator: error loading hyphenation /system/usr/hyphen-data/hyph-und-ethi.pat.txt
                                             java.io.FileNotFoundException: /system/usr/hyphen-data/hyph-und-ethi.pat.txt: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.IoBridge.open(IoBridge.java:452)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207)
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114)
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96)
                                                 at android.text.Hyphenator.init(Hyphenator.java:154)
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207)
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186)
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593)
                                              Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                 at libcore.io.Posix.open(Native Method)
                                                 at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                 at libcore.io.IoBridge.open(IoBridge.java:438)
                                                 at libcore.io.IoUtils$FileReader.<init>(IoUtils.java:207) 
                                                 at libcore.io.IoUtils.readFileAsString(IoUtils.java:114) 
                                                 at android.text.Hyphenator.loadHyphenator(Hyphenator.java:96) 
                                                 at android.text.Hyphenator.init(Hyphenator.java:154) 
                                                 at com.android.internal.os.ZygoteInit.preloadTextResources(ZygoteInit.java:207) 
                                                 at com.android.internal.os.ZygoteInit.preload(ZygoteInit.java:186) 
                                                 at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:593) 
01-25 13:05:26.717 1200-1200/? D/Zygote: end preload
01-25 13:05:26.717 1200-1200/? I/art: Starting a blocking GC Explicit
01-25 13:05:26.721 1200-1200/? I/art: Explicit concurrent mark sweep GC freed 7650(667KB) AllocSpace objects, 84(2MB) LOS objects, 66% free, 2MB/6MB, paused 211us total 3.488ms
01-25 13:05:26.725 1200-1200/? I/art: Starting a blocking GC Explicit
01-25 13:05:26.728 1200-1200/? I/art: Explicit concurrent mark sweep GC freed 1188(71KB) AllocSpace objects, 27(756KB) LOS objects, 66% free, 1237KB/3MB, paused 220us total 2.761ms
01-25 13:05:26.728 1200-1481/? I/art: Starting a blocking GC HeapTrim
01-25 13:05:26.731 1200-1200/? I/art: Starting a blocking GC Background
01-25 13:05:26.741 1200-1200/? I/Zygote: System server process 1538 has been created
01-25 13:05:26.741 1200-1200/? I/Zygote: Accepting command socket connections
01-25 13:05:26.759 1538-1538/? I/InstallerConnection: connecting...
01-25 13:05:26.761 1198-1198/? I/installd: new connection
01-25 13:05:26.858 1538-1538/? I/InstallerConnection: disconnecting...
01-25 13:05:26.859 1198-1198/? E/installd: eof
01-25 13:05:26.859 1198-1198/? E/installd: failed to read size
01-25 13:05:26.859 1198-1198/? I/installd: closing connection
01-25 13:05:26.927 1538-1538/? I/SystemServer: Entered the Android system server!
01-25 13:05:26.998 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.pm.Installer
01-25 13:05:27.013 1538-1538/system_process I/Installer: Waiting for installd to be ready.
01-25 13:05:27.013 1538-1538/system_process I/InstallerConnection: connecting...
01-25 13:05:27.014 1198-1198/? I/installd: new connection
01-25 13:05:27.014 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.am.ActivityManagerService$Lifecycle
01-25 13:05:27.088 1538-1538/system_process I/ActivityManager: Memory class: 256
01-25 13:05:27.094 1538-1554/system_process I/ServiceThread: Enabled StrictMode logging for ActivityManager looper.
01-25 13:05:27.097 1538-1555/system_process I/ServiceThread: Enabled StrictMode logging for android.ui looper.
01-25 13:05:27.131 1538-1538/system_process D/BatteryStatsImpl: Reading daily items from /data/system/batterystats-daily.xml
01-25 13:05:27.190 1538-1538/system_process I/IntentFirewall: Read new rules (A:0 B:0 S:0)
01-25 13:05:27.195 1538-1559/system_process I/ServiceThread: Enabled StrictMode logging for android.display looper.
01-25 13:05:27.197 1538-1538/system_process D/AppOps: AppOpsService published
01-25 13:05:27.198 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.power.PowerManagerService
01-25 13:05:27.200 1538-1561/system_process I/ServiceThread: Enabled StrictMode logging for PowerManagerService looper.
01-25 13:05:27.204 1538-1538/system_process E/PowerManagerService-JNI: Couldn't load power module (No such file or directory)
01-25 13:05:27.204 1538-1538/system_process W/libsuspend: Error writing 'on' to /sys/power/state: Invalid argument
01-25 13:05:27.204 1538-1538/system_process I/libsuspend: Selected wakeup count
01-25 13:05:27.207 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.lights.LightsService
01-25 13:05:27.209 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.display.DisplayManagerService
01-25 13:05:27.252 1538-1538/system_process I/SystemServiceManager: Starting phase 100
01-25 13:05:27.256 1186-1263/? E/SurfaceFlinger: ro.sf.lcd_density must be defined as a build property
01-25 13:05:27.263 1538-1559/system_process I/DisplayManagerService: Display device added: DisplayDeviceInfo{"Built-in Screen": uniqueId="local:0", 1080 x 1920, modeId 1, defaultModeId 1, supportedModes [{id=1, width=1080, height=1920, fps=60.000004}], density 480, 480.0 x 480.0 dpi, appVsyncOff 0, presDeadline 17666666, touch INTERNAL, rotation 0, type BUILT_IN, state UNKNOWN, FLAG_DEFAULT_DISPLAY, FLAG_ROTATES_WITH_CONTENT, FLAG_SECURE, FLAG_SUPPORTS_PROTECTED_BUFFERS}
01-25 13:05:27.265 1186-1186/? D/SurfaceFlinger: Set power mode=2, type=0 flinger=0xb7062000
01-25 13:05:27.265 1186-1186/? D/SurfaceFlinger: Screen type=0 is already mode=2
01-25 13:05:27.266 1538-1559/system_process I/DisplayManagerService: Display device changed state: "Built-in Screen", ON
01-25 13:05:27.267 1538-1538/system_process I/SystemServer: Package Manager
01-25 13:05:27.297 1538-1538/system_process W/SystemConfig: No directory /system/etc/sysconfig, skipping
01-25 13:05:27.334 1538-1538/system_process D/SELinuxMMAC: Using policy file /system/etc/security/mac_permissions.xml
01-25 13:05:27.475 1538-1548/system_process I/art: Background sticky concurrent mark sweep GC freed 16704(1408KB) AllocSpace objects, 22(520KB) LOS objects, 44% free, 2MB/3MB, paused 266us total 110.014ms
01-25 13:05:27.481 1538-1538/system_process E/art: DexFile_getDexOptNeeded file '/system/framework/org.apache.http.legacy.jar' does not exist
01-25 13:05:27.482 1538-1538/system_process W/PackageManager: Library not found: /system/framework/org.apache.http.legacy.jar
01-25 13:05:27.502 1538-1538/system_process D/PackageManager: No files in app dir /vendor/overlay
01-25 13:05:27.517 1538-1538/system_process W/PackageManager: Failed to parse /system/framework/oat: Missing base APK in /system/framework/oat
01-25 13:05:27.517 1538-1538/system_process W/PackageManager: Failed to parse /system/framework/x86: Missing base APK in /system/framework/x86
01-25 13:05:27.583 1538-1538/system_process W/PackageParser: No actions in intent filter at /system/priv-app/Contacts/Contacts.apk Binary XML file line #388
01-25 13:05:27.585 1196-1196/? I/ServiceManager: Waiting for service media.camera.proxy...
01-25 13:05:27.660 1538-1538/system_process W/PackageParser: No actions in intent filter at /system/priv-app/Dialer/Dialer.apk Binary XML file line #172
01-25 13:05:27.682 1538-1538/system_process W/PackageManager: Permission android.permission.DOWNLOAD_WITHOUT_NOTIFICATION from package com.android.providers.downloads in an unknown group android.permission-group.NETWORK
01-25 13:05:27.795 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.ALL_SERVICES from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.OTHER_SERVICES from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.mail from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.cl from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.android from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.androidsecure from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.sierra from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.sierraqa from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.sierrasandbox from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.youtube from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.YouTubeUser from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.talk from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.ig from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.lh2 from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.mobile from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.cp from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.adsense from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.adwords from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.blogger from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.dodgeball from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.gbase from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.groups2 from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.796 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.health from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.jotspot from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.knol from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.news from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.orkut from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.print from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.sitemaps from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.wifi from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.finance from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.local from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.ah from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.notebook from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.writely from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.wise from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.grandcentral from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.speechpersonalization from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.googleapps.permission.GOOGLE_AUTH.speech from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.providers.talk.permission.READ_ONLY from package com.google.android.gsf in an unknown group android.permission-group.MESSAGES
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.providers.talk.permission.WRITE_ONLY from package com.google.android.gsf in an unknown group android.permission-group.MESSAGES
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.gtalkservice.permission.GTALK_SERVICE from package com.google.android.gsf in an unknown group android.permission-group.MESSAGES
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.gtalkservice.permission.SEND_HEARTBEAT from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.permission.BROADCAST_DATA_MESSAGE from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.c2dm.permission.SEND from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.c2dm.permission.RECEIVE from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.xmpp.permission.BROADCAST from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.797 1538-1538/system_process W/PackageManager: Permission com.google.android.xmpp.permission.SEND_RECEIVE from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.798 1538-1538/system_process W/PackageManager: Permission com.google.android.xmpp.permission.XMPP_ENDPOINT_BROADCAST from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.798 1538-1538/system_process W/PackageManager: Permission com.google.android.xmpp.permission.USE_XMPP_ENDPOINT from package com.google.android.gsf in an unknown group android.permission-group.NETWORK
01-25 13:05:27.798 1538-1538/system_process W/PackageManager: Permission com.google.android.providers.gsf.permission.READ_GSERVICES from package com.google.android.gsf in an unknown group android.permission-group.ACCOUNTS
01-25 13:05:28.136 1538-1538/system_process W/PackageManager: Permission com.google.android.gms.permission.ACTIVITY_RECOGNITION from package com.google.android.gms in an unknown group android.permission-group.PERSONAL_INFO
01-25 13:05:28.210 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.USE_CREDENTIALS in package: com.android.settings at: Binary XML file line #55
01-25 13:05:28.210 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.READ_SYNC_SETTINGS in package: com.android.settings at: Binary XML file line #60
01-25 13:05:28.210 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.WRITE_SYNC_SETTINGS in package: com.android.settings at: Binary XML file line #61
01-25 13:05:28.251 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.INSTALL_GRANT_RUNTIME_PERMISSIONS in package: com.android.shell at: Binary XML file line #101
01-25 13:05:28.293 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.CONFIGURE_WIFI_DISPLAY in package: com.android.systemui at: Binary XML file line #119
01-25 13:05:28.529 1538-1538/system_process W/PackageManager: Permission com.google.android.launcher.permission.READ_SETTINGS from package com.google.android.googlequicksearchbox in an unknown group android.permission-group.SYSTEM_TOOLS
01-25 13:05:28.529 1538-1538/system_process W/PackageManager: Permission com.google.android.launcher.permission.WRITE_SETTINGS from package com.google.android.googlequicksearchbox in an unknown group android.permission-group.SYSTEM_TOOLS
01-25 13:05:28.529 1538-1538/system_process W/PackageManager: Permission com.android.launcher.permission.INSTALL_SHORTCUT from package com.google.android.googlequicksearchbox in an unknown group android.permission-group.SYSTEM_TOOLS
01-25 13:05:28.587 1196-1196/? I/ServiceManager: Waiting for service media.camera.proxy...
01-25 13:05:28.768 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.WRITE_CONTACTS in package: com.android.email at: Binary XML file line #40
01-25 13:05:29.007 1538-1538/system_process W/PackageManager: Permission com.android.vending.CHECK_LICENSE from package com.android.vending in an unknown group android.permission-group.NETWORK
01-25 13:05:29.068 1538-1538/system_process W/PackageParser: Ignoring duplicate uses-permissions/uses-permissions-sdk-m: android.permission.WAKE_LOCK in package: com.google.android.apps.maps at: Binary XML file line #96
01-25 13:05:29.264 1538-1538/system_process D/PackageManager: No files in app dir /system/vendor/app
01-25 13:05:29.264 1538-1538/system_process D/PackageManager: No files in app dir /oem/app
01-25 13:05:29.293 1538-1538/system_process W/PackageParser: No actions in intent filter at /data/app/ApiDemos/ApiDemos.apk Binary XML file line #3082
01-25 13:05:29.293 1538-1538/system_process W/PackageParser: No actions in intent filter at /data/app/ApiDemos/ApiDemos.apk Binary XML file line #3088
01-25 13:05:29.293 1538-1538/system_process W/PackageManager: Package com.example.android.apis desires unavailable shared library com.example.will.never.exist; ignoring!
01-25 13:05:29.298 1538-1538/system_process I/SELinux: SELinux: Loaded file_contexts contexts from /file_contexts.
01-25 13:05:29.329 1538-1538/system_process W/PackageParser: Unknown element under <manifest>: meta-data at /data/app/com.teddyxiong53.www.videoviewtest-1/base.apk Binary XML file line #13
01-25 13:05:29.351 1538-1538/system_process W/PackageParser: Unknown element under <manifest>: meta-data at /data/app/com.teddyxiong53.www.bitmaptest-1/base.apk Binary XML file line #11
01-25 13:05:29.371 1538-1538/system_process W/PackageParser: Unknown element under <manifest>: meta-data at /data/app/com.teddyxiong53.www.xhl_simple_view-2/base.apk Binary XML file line #11
01-25 13:05:29.392 1538-1538/system_process D/PackageManager: No files in app dir /data/app-private
01-25 13:05:29.392 1538-1538/system_process W/PackageManager: Package com.google.android.gms desires unavailable shared library com.google.android.ble; ignoring!
01-25 13:05:29.392 1538-1538/system_process W/PackageManager: Package com.example.android.apis desires unavailable shared library com.example.will.never.exist; ignoring!
01-25 13:05:29.392 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.google.android.gsf.login to x86
01-25 13:05:29.401 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.google.android.gsf to x86
01-25 13:05:29.401 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.android.settings to x86
01-25 13:05:29.401 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.android.providers.settings to x86
01-25 13:05:29.401 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.android.server.telecom to x86
01-25 13:05:29.402 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.android.keychain to x86
01-25 13:05:29.402 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.android.location.fused to x86
01-25 13:05:29.402 1538-1538/system_process I/PackageManager: Adjusting ABI for : com.android.inputdevices to x86
01-25 13:05:29.403 1538-1538/system_process I/PackageManager: Time to scan packages: 1.994 seconds
01-25 13:05:29.404 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.voicesearch.SHORTCUTS_ACCESS in package com.google.android.googlequicksearchbox
01-25 13:05:29.404 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.voicesearch.ACCESS_SETTINGS in package com.google.android.googlequicksearchbox
01-25 13:05:29.404 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.ears.permission.WRITE in package com.google.android.googlequicksearchbox
01-25 13:05:29.404 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.apps.googlevoice.permission.AUTO_SEND in package com.google.android.googlequicksearchbox
01-25 13:05:29.404 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.gm.permission.AUTO_SEND in package com.google.android.googlequicksearchbox
01-25 13:05:29.404 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.hangouts.START_HANGOUT in package com.google.android.googlequicksearchbox
01-25 13:05:29.405 1538-1538/system_process W/PackageManager: Unknown permission com.android.chrome.PRERENDER_URL in package com.google.android.googlequicksearchbox
01-25 13:05:29.405 1538-1538/system_process W/PackageManager: Not granting permission com.google.android.googleapps.permission.GOOGLE_AUTH to package com.android.providers.calendar (protectionLevel=2 flags=0x30083e45)
01-25 13:05:29.405 1538-1538/system_process W/PackageManager: Not granting permission com.google.android.googleapps.permission.GOOGLE_AUTH.cl to package com.android.providers.calendar (protectionLevel=2 flags=0x30083e45)
01-25 13:05:29.406 1538-1538/system_process W/PackageManager: Not granting permission android.permission.ACCESS_DOWNLOAD_MANAGER to package com.android.browser (protectionLevel=18 flags=0x3809be45)
01-25 13:05:29.406 1538-1538/system_process W/PackageManager: Not granting permission android.permission.SEND_DOWNLOAD_COMPLETED_INTENTS to package com.android.browser (protectionLevel=2 flags=0x3809be45)
01-25 13:05:29.406 1538-1538/system_process W/PackageManager: Unknown permission com.android.launcher.permission.READ_SETTINGS in package com.google.android.launcher
01-25 13:05:29.406 1538-1538/system_process W/PackageManager: Unknown permission com.android.launcher.permission.WRITE_SETTINGS in package com.google.android.launcher
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission com.google.android.googleapps.permission.GOOGLE_AUTH.mail to package com.android.calendar (protectionLevel=2 flags=0x3009be45)
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.apps.enterprise.dmagent.permission.AutoSyncPermission in package com.google.android.gms
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.hangouts.START_HANGOUT in package com.google.android.gms
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.wearable.READ_SETTINGS in package com.google.android.gms
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.google.android.gm.permission.READ_GMAIL in package com.google.android.gms
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.DELETE_PACKAGES to package com.svox.pico (protectionLevel=18 flags=0x3808be45)
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.READ_CONTACTS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.WRITE_CONTACTS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.ACCESS_COARSE_LOCATION to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.WRITE_EXTERNAL_STORAGE to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.SEND_SMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.RECEIVE_SMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.RECEIVE_MMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.READ_SMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.READ_PHONE_STATE to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.RECORD_AUDIO to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.CAMERA to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.READ_EXTERNAL_STORAGE to package com.example.android.apis because it was previously installed without
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Not granting permission android.permission.CONTROL_KEYGUARD to package com.google.android.gsf.login (protectionLevel=2 flags=0x3048be45)
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.vending.billing.BILLING_ACCOUNT_SERVICE in package com.google.android.gsf.login
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.vending.billing.ADD_CREDIT_CARD in package com.google.android.gsf.login
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.vending.billing.IBillingAccountService.BIND2 in package com.google.android.gsf.login
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.vending.TOS_ACKED in package com.google.android.gsf.login
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.chrome.TOS_ACKED in package com.google.android.gsf.login
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.launcher.permission.READ_SETTINGS in package com.android.settings
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.launcher.permission.WRITE_SETTINGS in package com.android.settings
01-25 13:05:29.407 1538-1538/system_process W/PackageManager: Unknown permission com.android.smspush.WAPPUSH_MANAGER_BIND in package com.android.phone
01-25 13:05:29.408 1538-1538/system_process W/PackageManager: Not granting permission android.permission.BIND_APPWIDGET to package com.android.widgetpreview (protectionLevel=18 flags=0x1808be44)
01-25 13:05:29.443 1538-1538/system_process I/art: Starting a blocking GC Explicit
01-25 13:05:29.453 1538-1538/system_process I/art: Explicit concurrent mark sweep GC freed 11820(774KB) AllocSpace objects, 3(60KB) LOS objects, 33% free, 4MB/6MB, paused 292us total 8.306ms
01-25 13:05:29.454 1538-1538/system_process I/SystemServer: User Service
01-25 13:05:29.457 1184-1184/? I/lowmemorykiller: ActivityManager connected
01-25 13:05:29.458 1538-1538/system_process D/SensorService: nuSensorService starting...
01-25 13:05:29.460 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.BatteryService
01-25 13:05:29.463 1538-1570/system_process D/SensorService: new thread SensorEventAckReceiver
01-25 13:05:29.463 1538-1571/system_process D/SensorService: nuSensorService thread starting...
01-25 13:05:29.474 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.usage.UsageStatsService
01-25 13:05:29.477 1538-1554/system_process E/KernelCpuSpeedReader: Failed to read cpu-freq
                                                                    java.io.FileNotFoundException: /sys/devices/system/cpu/cpu0/cpufreq/stats/time_in_state: open failed: ENOENT (No such file or directory)
                                                                        at libcore.io.IoBridge.open(IoBridge.java:452)
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:76)
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:103)
                                                                        at java.io.FileReader.<init>(FileReader.java:66)
                                                                        at com.android.internal.os.KernelCpuSpeedReader.readDelta(KernelCpuSpeedReader.java:49)
                                                                        at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8002)
                                                                        at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155)
                                                                        at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                        at android.os.Looper.loop(Looper.java:148)
                                                                        at android.os.HandlerThread.run(HandlerThread.java:61)
                                                                        at com.android.server.ServiceThread.run(ServiceThread.java:46)
                                                                     Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                                        at libcore.io.Posix.open(Native Method)
                                                                        at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                                        at libcore.io.IoBridge.open(IoBridge.java:438)
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:76) 
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:103) 
                                                                        at java.io.FileReader.<init>(FileReader.java:66) 
                                                                        at com.android.internal.os.KernelCpuSpeedReader.readDelta(KernelCpuSpeedReader.java:49) 
                                                                        at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8002) 
                                                                        at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155) 
                                                                        at android.os.Handler.dispatchMessage(Handler.java:102) 
                                                                        at android.os.Looper.loop(Looper.java:148) 
                                                                        at android.os.HandlerThread.run(HandlerThread.java:61) 
                                                                        at com.android.server.ServiceThread.run(ServiceThread.java:46) 
01-25 13:05:29.478 1538-1554/system_process E/KernelUidCpuTimeReader: Failed to read uid_cputime
                                                                      java.io.FileNotFoundException: /proc/uid_cputime/show_uid_stat: open failed: ENOENT (No such file or directory)
                                                                          at libcore.io.IoBridge.open(IoBridge.java:452)
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:76)
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:103)
                                                                          at java.io.FileReader.<init>(FileReader.java:66)
                                                                          at com.android.internal.os.KernelUidCpuTimeReader.readDelta(KernelUidCpuTimeReader.java:71)
                                                                          at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8031)
                                                                          at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155)
                                                                          at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                          at android.os.Looper.loop(Looper.java:148)
                                                                          at android.os.HandlerThread.run(HandlerThread.java:61)
                                                                          at com.android.server.ServiceThread.run(ServiceThread.java:46)
                                                                       Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                                          at libcore.io.Posix.open(Native Method)
                                                                          at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                                          at libcore.io.IoBridge.open(IoBridge.java:438)
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:76) 
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:103) 
                                                                          at java.io.FileReader.<init>(FileReader.java:66) 
                                                                          at com.android.internal.os.KernelUidCpuTimeReader.readDelta(KernelUidCpuTimeReader.java:71) 
                                                                          at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8031) 
                                                                          at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155) 
                                                                          at android.os.Handler.dispatchMessage(Handler.java:102) 
                                                                          at android.os.Looper.loop(Looper.java:148) 
                                                                          at android.os.HandlerThread.run(HandlerThread.java:61) 
                                                                          at com.android.server.ServiceThread.run(ServiceThread.java:46) 
01-25 13:05:29.496 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.webkit.WebViewUpdateService
01-25 13:05:29.499 1538-1538/system_process I/SystemServer: Reading configuration...
01-25 13:05:29.499 1538-1538/system_process I/SystemServer: Scheduling Policy
01-25 13:05:29.500 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.telecom.TelecomLoaderService
01-25 13:05:29.527 1538-1538/system_process I/SystemServer: Telephony Registry
01-25 13:05:29.531 1538-1538/system_process I/SystemServer: Entropy Mixer
01-25 13:05:29.532 1538-1538/system_process I/EntropyMixer: Writing entropy...
01-25 13:05:29.543 1538-1538/system_process I/SystemServer: Camera Service
01-25 13:05:29.543 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.camera.CameraService
01-25 13:05:29.558 1538-1574/system_process I/ServiceThread: Enabled StrictMode logging for CameraService_proxy looper.
01-25 13:05:29.559 1538-1538/system_process I/SystemServer: Account Manager
01-25 13:05:29.564 1538-1538/system_process I/SystemServer: Content Manager
01-25 13:05:29.566 1538-1538/system_process I/SystemServer: System Content Providers
01-25 13:05:29.568 1538-1538/system_process W/System: ClassLoader referenced unknown path: /system/priv-app/SettingsProvider/lib/x86
01-25 13:05:29.579 1538-1538/system_process I/SystemServer: Vibrator Service
01-25 13:05:29.581 1538-1538/system_process I/SystemServer: Consumer IR Service
01-25 13:05:29.581 1538-1538/system_process E/ConsumerIrService: Can't open consumer IR HW Module, error: -2
01-25 13:05:29.582 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.AlarmManagerService
01-25 13:05:29.585 1538-1538/system_process W/AlarmManagerService: no wall clock RTC found
01-25 13:05:29.585 1538-1538/system_process D/AlarmManagerService: Kernel timezone updated to 0 minutes west of GMT
01-25 13:05:29.590 1196-1196/? I/AudioPolicyService: AudioPolicyService CSTOR in new mode
01-25 13:05:29.591 1196-1196/? I/APM::ConfigParsingUtils: loadAudioPolicyConfig() loaded /system/etc/audio_policy.conf
01-25 13:05:29.592 1196-1196/? I/AudioFlinger: loadHwModule() Loaded primary audio interface from Generic audio HW HAL (audio) handle 1
01-25 13:05:29.592 1196-1196/? I/AudioFlinger: openOutput(), module 1 Device 2, SamplingRate 44100, Format 0x000001, Channels 3, flags 2
01-25 13:05:29.592 1538-1538/system_process I/SystemServer: Init Watchdog
01-25 13:05:29.593 1538-1538/system_process I/SystemServer: Input Manager
01-25 13:05:29.593 1538-1538/system_process I/InputManager: Initializing input manager, mUseDevInputEventForAudioJack=false
01-25 13:05:29.599 1196-1196/? I/AudioFlinger: AudioStreamOut::open(), mHalFormatIsLinearPcm = 1
01-25 13:05:29.601 1196-1196/? I/AudioFlinger: HAL output buffer size 1024 frames, normal sink buffer size 1024 frames
01-25 13:05:29.615 1196-1196/? I/BufferProvider: found effect "Multichannel Downmix To Stereo" from The Android Open Source Project
01-25 13:05:29.615 1196-1196/? I/AudioFlinger: Using module 1 has the primary audio interface
01-25 13:05:29.615 1196-1579/? I/AudioFlinger: AudioFlinger's thread 0xb44c0000 ready to run
01-25 13:05:29.616 1196-1579/? E/AudioFlinger: no wake lock to update!
01-25 13:05:29.619 1196-1196/? E/audio_hw_generic: Error opening input stream format 1, channel_mask 0010, sample_rate 16000
01-25 13:05:29.619 1196-1580/? I/AudioFlinger: AudioFlinger's thread 0xb42c0000 ready to run
01-25 13:05:29.620 1196-1196/? E/AudioFlinger: int android::load_audio_interface(const char*, audio_hw_device_t**) couldn't load audio hw module audio.r_submix (No such file or directory)
01-25 13:05:29.620 1196-1196/? I/AudioFlinger: loadHwModule() error -2 loading module r_submix 
01-25 13:05:29.620 1196-1196/? W/APM::AudioPolicyManager: could not open HW module r_submix
01-25 13:05:29.620 1196-1196/? W/APM::AudioPolicyManager: Input device 80000100 unreachable
01-25 13:05:29.621 1196-1196/? E/SoundTriggerHwService: couldn't load sound trigger module sound_trigger.primary (No such file or directory)
01-25 13:05:29.621 1196-1196/? I/RadioService: RadioService
01-25 13:05:29.621 1196-1196/? I/RadioService: onFirstRef
01-25 13:05:29.621 1196-1196/? E/RadioService: couldn't load radio module radio.primary (No such file or directory)
01-25 13:05:29.659 1538-1538/system_process I/SystemServer: Window Manager
01-25 13:05:29.673 1538-1559/system_process I/WindowManager: No existing display settings /data/system/display_settings.xml; starting empty
01-25 13:05:29.729 1538-1538/system_process I/InputManager: Starting input manager
01-25 13:05:29.731 1538-1538/system_process I/SystemServer: No Bluetooh Service (emulator)
01-25 13:05:29.731 1538-1538/system_process I/SystemServer: Input Method Service
01-25 13:05:29.740 1538-1587/system_process D/EventHub: No input device configuration file found for device 'Power Button'.
01-25 13:05:29.764 1538-1587/system_process W/EventHub: Unable to disable kernel key repeat for /dev/input/event0: Function not implemented
01-25 13:05:29.764 1538-1587/system_process I/EventHub: New device: id=1, fd=76, path='/dev/input/event0', name='Power Button', classes=0x1, configuration='', keyLayout='/system/usr/keylayout/Generic.kl', keyCharacterMap='/system/usr/keychars/Generic.kcm', builtinKeyboard=false, wakeMechanism=EPOLLWAKEUP, usingClockIoctl=true
01-25 13:05:29.777 1538-1587/system_process W/EventHub: Unable to disable kernel key repeat for /dev/input/event1: Function not implemented
01-25 13:05:29.777 1538-1587/system_process I/EventHub: New device: id=2, fd=77, path='/dev/input/event1', name='qwerty2', classes=0x17, configuration='/system/usr/idc/qwerty2.idc', keyLayout='/system/usr/keylayout/qwerty.kl', keyCharacterMap='/system/usr/keychars/qwerty2.kcm', builtinKeyboard=true, wakeMechanism=EPOLLWAKEUP, usingClockIoctl=true
01-25 13:05:29.777 1538-1587/system_process E/EventHub: could not get driver version for /dev/input/mice, Not a typewriter
01-25 13:05:29.812 1538-1587/system_process I/InputReader: Device added: id=-1, name='Virtual', sources=0x00000301
01-25 13:05:29.813 1538-1587/system_process I/InputReader:   Touch device 'qwerty2' could not query the properties of its associated display.  The device will be inoperable until the display size becomes available.
01-25 13:05:29.814 1538-1587/system_process I/InputReader: Device added: id=0, name='qwerty2', sources=0x00001103
01-25 13:05:29.814 1538-1587/system_process I/InputReader: Device added: id=1, name='Power Button', sources=0x00000101
01-25 13:05:29.824 1538-1538/system_process I/SystemServer: Accessibility Manager
01-25 13:05:29.827 1538-1538/system_process I/ActivityManager: Config changes=1df8 {1.0 ?mcc?mnc en_US ldltr sw360dp w360dp h640dp 480dpi nrml long port ?uimode ?night -touch -keyb/v/h -nav/h s.2}
01-25 13:05:29.829 1186-1186/? E/SurfaceFlinger: ro.sf.lcd_density must be defined as a build property
01-25 13:05:29.829 1186-1186/? D/SurfaceFlinger: Set active config mode=0, type=0 flinger=0xb7062000
01-25 13:05:29.829 1186-1186/? D/SurfaceFlinger: Screen type=0 is already mode=0
01-25 13:05:29.831 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000004
01-25 13:05:29.831 1538-1587/system_process I/InputReader: Device reconfigured: id=0, name='qwerty2', size 1080x1920, orientation 0, mode 1, display id 0
01-25 13:05:29.843 1538-1538/system_process I/ActivityManager: Config changes=508 {1.0 ?mcc?mnc en_US ldltr sw360dp w360dp h568dp 480dpi nrml port ?uimode ?night finger -keyb/v/h -nav/h s.3}
01-25 13:05:29.843 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.MountService$Lifecycle
01-25 13:05:29.851 1538-1588/system_process D/MountService: Thinking about reset, mSystemReady=false, mDaemonConnected=true
01-25 13:05:29.852 1538-1588/system_process D/MountService: Thinking about reset, mSystemReady=false, mDaemonConnected=true
01-25 13:05:29.852 1538-1588/system_process D/CryptdConnector: SND -> {1 cryptfs getfield SystemLocale}
01-25 13:05:29.852 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.UiModeManagerService
01-25 13:05:29.852 1173-1238/? I/Ext4Crypt: ext4 crypto complete called on /data
01-25 13:05:29.852 1173-1238/? I/Ext4Crypt: No master key, so not ext4enc
01-25 13:05:29.853 1538-1590/system_process D/CryptdConnector: RCV <- {200 1 -1}
01-25 13:05:29.862 1538-1588/system_process W/MountService: No primary storage mounted!
01-25 13:05:29.862 1538-1588/system_process D/VoldConnector: SND -> {1 asec list}
01-25 13:05:29.864 1538-1538/system_process I/ActivityManager: Config changes=200 {1.0 ?mcc?mnc en_US ldltr sw360dp w360dp h568dp 480dpi nrml port finger -keyb/v/h -nav/h s.4}
01-25 13:05:29.865 1538-1538/system_process I/SystemServer: LockSettingsService
01-25 13:05:29.866 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.DeviceIdleController
01-25 13:05:29.868 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.devicepolicy.DevicePolicyManagerService$Lifecycle
01-25 13:05:29.871 1538-1589/system_process D/VoldConnector: RCV <- {200 1 asec operation succeeded}
01-25 13:05:29.872 1538-1588/system_process I/PackageManager: No secure containers found
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.voicesearch.SHORTCUTS_ACCESS in package com.google.android.googlequicksearchbox
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.voicesearch.ACCESS_SETTINGS in package com.google.android.googlequicksearchbox
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.ears.permission.WRITE in package com.google.android.googlequicksearchbox
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.apps.googlevoice.permission.AUTO_SEND in package com.google.android.googlequicksearchbox
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.gm.permission.AUTO_SEND in package com.google.android.googlequicksearchbox
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.hangouts.START_HANGOUT in package com.google.android.googlequicksearchbox
01-25 13:05:29.872 1538-1588/system_process W/PackageManager: Unknown permission com.android.chrome.PRERENDER_URL in package com.google.android.googlequicksearchbox
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Not granting permission com.google.android.googleapps.permission.GOOGLE_AUTH to package com.android.providers.calendar (protectionLevel=2 flags=0x30083e45)
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Not granting permission com.google.android.googleapps.permission.GOOGLE_AUTH.cl to package com.android.providers.calendar (protectionLevel=2 flags=0x30083e45)
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Not granting permission android.permission.ACCESS_DOWNLOAD_MANAGER to package com.android.browser (protectionLevel=18 flags=0x3809be45)
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Not granting permission android.permission.SEND_DOWNLOAD_COMPLETED_INTENTS to package com.android.browser (protectionLevel=2 flags=0x3809be45)
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Unknown permission com.android.launcher.permission.READ_SETTINGS in package com.google.android.launcher
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Unknown permission com.android.launcher.permission.WRITE_SETTINGS in package com.google.android.launcher
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Not granting permission com.google.android.googleapps.permission.GOOGLE_AUTH.mail to package com.android.calendar (protectionLevel=2 flags=0x3009be45)
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.apps.enterprise.dmagent.permission.AutoSyncPermission in package com.google.android.gms
01-25 13:05:29.873 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.hangouts.START_HANGOUT in package com.google.android.gms
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.wearable.READ_SETTINGS in package com.google.android.gms
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.google.android.gm.permission.READ_GMAIL in package com.google.android.gms
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.DELETE_PACKAGES to package com.svox.pico (protectionLevel=18 flags=0x3808be45)
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.READ_CONTACTS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.WRITE_CONTACTS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.ACCESS_COARSE_LOCATION to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.WRITE_EXTERNAL_STORAGE to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.SEND_SMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.RECEIVE_SMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.RECEIVE_MMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.READ_SMS to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.READ_PHONE_STATE to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.RECORD_AUDIO to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.CAMERA to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.READ_EXTERNAL_STORAGE to package com.example.android.apis because it was previously installed without
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Not granting permission android.permission.CONTROL_KEYGUARD to package com.google.android.gsf.login (protectionLevel=2 flags=0x3048be45)
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.vending.billing.BILLING_ACCOUNT_SERVICE in package com.google.android.gsf.login
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.vending.billing.ADD_CREDIT_CARD in package com.google.android.gsf.login
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.vending.billing.IBillingAccountService.BIND2 in package com.google.android.gsf.login
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.vending.TOS_ACKED in package com.google.android.gsf.login
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.chrome.TOS_ACKED in package com.google.android.gsf.login
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.launcher.permission.READ_SETTINGS in package com.android.settings
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.launcher.permission.WRITE_SETTINGS in package com.android.settings
01-25 13:05:29.874 1538-1588/system_process W/PackageManager: Unknown permission com.android.smspush.WAPPUSH_MANAGER_BIND in package com.android.phone
01-25 13:05:29.875 1538-1588/system_process W/PackageManager: Not granting permission android.permission.BIND_APPWIDGET to package com.android.widgetpreview (protectionLevel=18 flags=0x1808be44)
01-25 13:05:29.902 1538-1548/system_process W/art: Suspending all threads took: 21.950ms
01-25 13:05:29.909 1538-1553/system_process I/UsageStatsService: User[0] Rollover scheduled @ 2018-01-26 00:00:00(1516924800000)
01-25 13:05:29.912 1538-1548/system_process I/art: Background sticky concurrent mark sweep GC freed 16629(1303KB) AllocSpace objects, 12(240KB) LOS objects, 19% free, 4MB/6MB, paused 28.037ms total 59.437ms
01-25 13:05:29.922 1538-1588/system_process W/MountService: No primary storage defined yet; hacking together a stub
01-25 13:05:29.922 1538-1588/system_process W/MountService: No primary storage defined yet; hacking together a stub
01-25 13:05:29.923 1538-1588/system_process W/MountService: No primary storage mounted!
01-25 13:05:29.924 1538-1538/system_process I/SystemServer: Status Bar
01-25 13:05:29.924 1538-1588/system_process D/VoldConnector: SND -> {2 asec list}
01-25 13:05:29.924 1538-1589/system_process D/VoldConnector: RCV <- {200 2 asec operation succeeded}
01-25 13:05:29.926 1538-1538/system_process I/SystemServer: Clipboard Service
01-25 13:05:29.927 1538-1538/system_process I/SystemServer: NetworkManagement Service
01-25 13:05:29.929 1538-1538/system_process I/SystemServer: Text Service Manager Service
01-25 13:05:29.931 1538-1538/system_process I/SystemServer: Network Score Service
01-25 13:05:29.933 1538-1538/system_process I/SystemServer: NetworkStats Service
01-25 13:05:29.948 1538-1538/system_process I/SystemServer: NetworkPolicy Service
01-25 13:05:29.996 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.wifi.p2p.WifiP2pService
01-25 13:05:30.045 1538-1538/system_process I/WifiP2pService: Registering wifip2p
01-25 13:05:30.048 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.wifi.WifiService
01-25 13:05:30.149 1538-1538/system_process D/HS20: Passpoint is disabled
01-25 13:05:30.166 1538-1538/system_process D/WifiController: isAirplaneModeOn = false, isWifiEnabled = false, isScanningAvailable = false
01-25 13:05:30.167 1538-1538/system_process I/WifiService: Registering wifi
01-25 13:05:30.170 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.wifi.WifiScanningService
01-25 13:05:30.170 1538-1538/system_process I/WifiScanningService: Creating wifiscanner
01-25 13:05:30.170 1538-1538/system_process I/WifiScanningService: Starting wifiscanner
01-25 13:05:30.173 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.wifi.RttService
01-25 13:05:30.173 1538-1538/system_process I/RttService: Creating rttmanager
01-25 13:05:30.173 1538-1538/system_process I/RttService: Starting rttmanager
01-25 13:05:30.174 1538-1538/system_process I/SystemServer: Connectivity Service
01-25 13:05:30.176 1538-1538/system_process D/ConnectivityService: ConnectivityService starting up
01-25 13:05:30.179 1538-1538/system_process D/ConnectivityService: wifiOnly=false
01-25 13:05:30.184 1538-1538/system_process I/SystemServer: Network Service Discovery Service
01-25 13:05:30.186 1538-1538/system_process D/NsdService: Network service discovery enabled true
01-25 13:05:30.188 1538-1538/system_process I/SystemServer: UpdateLock Service
01-25 13:05:30.189 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.notification.NotificationManagerService
01-25 13:05:30.207 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.storage.DeviceStorageMonitorService
01-25 13:05:30.208 1538-1538/system_process I/SystemServer: Location Manager
01-25 13:05:30.211 1538-1538/system_process I/SystemServer: Country Detector
01-25 13:05:30.212 1538-1538/system_process I/SystemServer: Search Service
01-25 13:05:30.213 1538-1538/system_process I/SystemServer: DropBox Service
01-25 13:05:30.214 1538-1538/system_process I/SystemServer: Wallpaper Service
01-25 13:05:30.216 1538-1538/system_process I/SystemServer: Audio Service
01-25 13:05:30.232 1538-1538/system_process W/TelecomManager: Telecom Service not found.
01-25 13:05:30.232 1196-1581/? D/PermissionCache: checking android.permission.MODIFY_AUDIO_SETTINGS for uid=1000 => granted (198 us)
01-25 13:05:30.279 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.DockObserver
01-25 13:05:30.280 1538-1538/system_process W/DockObserver: This kernel does not have dock station support
01-25 13:05:30.281 1538-1538/system_process I/SystemServer: Wired Accessory Manager
01-25 13:05:30.285 1538-1538/system_process W/WiredAccessoryManager: This kernel does not have wired headset support
01-25 13:05:30.285 1538-1538/system_process W/WiredAccessoryManager: This kernel does not have usb audio support
01-25 13:05:30.286 1538-1538/system_process W/WiredAccessoryManager: This kernel does not have HDMI audio support
01-25 13:05:30.287 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.midi.MidiService$Lifecycle
01-25 13:05:30.291 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.usb.UsbService$Lifecycle
01-25 13:05:30.301 1538-1538/system_process E/AlsaCardRecord: Failed to parse line 0 of /proc/asound/cards: ---
01-25 13:05:30.302 1538-1538/system_process I/SystemServer: Serial Service
01-25 13:05:30.303 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.twilight.TwilightService
01-25 13:05:30.306 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.job.JobSchedulerService
01-25 13:05:30.315 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.backup.BackupManagerService$Lifecycle
01-25 13:05:30.316 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.appwidget.AppWidgetService
01-25 13:05:30.324 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.voiceinteraction.VoiceInteractionManagerService
01-25 13:05:30.326 1196-1605/? D/PermissionCache: checking android.permission.CAPTURE_AUDIO_HOTWORD for uid=1000 => granted (66 us)
01-25 13:05:30.326 1538-1538/system_process W/SoundTriggerHelper: listModules status=0, # of modules=0
01-25 13:05:30.327 1538-1538/system_process I/SystemServer: DiskStats Service
01-25 13:05:30.328 1538-1538/system_process I/SystemServer: SamplingProfiler Service
01-25 13:05:30.335 1538-1538/system_process I/SystemServer: NetworkTimeUpdateService
01-25 13:05:30.335 1538-1538/system_process I/SystemServer: CommonTimeManagementService
01-25 13:05:30.336 1538-1538/system_process I/SystemServer: CertBlacklister
01-25 13:05:30.336 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.dreams.DreamManagerService
01-25 13:05:30.339 1538-1538/system_process I/SystemServer: Assets Atlas Service
01-25 13:05:30.340 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.print.PrintManagerService
01-25 13:05:30.343 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.restrictions.RestrictionsManagerService
01-25 13:05:30.344 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.media.MediaSessionService
01-25 13:05:30.347 1538-1538/system_process I/SystemServer: Media Router Service
01-25 13:05:30.348 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.trust.TrustManagerService
01-25 13:05:30.349 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.fingerprint.FingerprintService
01-25 13:05:30.352 1538-1608/system_process D/AssetAtlas: Loaded configuration: SliceMinArea (832x2048) flags=0x2 count=6
                                                          
                                                          [ 01-25 13:05:30.354  1186: 1373 D/         ]
                                                          HostConnection::get() New Host Connection established 0xb7052c80, tid 1373
01-25 13:05:30.407 1242-1242/? D/PermissionCache: checking android.permission.MANAGE_FINGERPRINT for uid=1000 => granted (168 us)
01-25 13:05:30.407 1242-1242/? V/fingerprintd: nativeOpenHal()
01-25 13:05:30.407 1538-1597/system_process D/WifiApConfigStore: 2G band allowed channels are:1,6,11
                                                                 
                                                                 [ 01-25 13:05:30.408  1538: 1608 D/         ]
                                                                 HostConnection::get() New Host Connection established 0xa10bbcc0, tid 1608
01-25 13:05:30.408 1242-1242/? D/FingerprintHal: ----------------> fingerprint_open ----------------->
01-25 13:05:30.409 1242-1242/? D/FingerprintHal: ----------------> loadFingerprints ----------------->
01-25 13:05:30.409 1242-1242/? E/FingerprintHal: Could not load fingerprints from storage at /data/system/users/0/fpdata/emulator_fingerprint_storage.bin; it has not yet been created.
01-25 13:05:30.409 1242-1242/? D/FingerprintHal: ----------------> set_notify_callback ----------------->
01-25 13:05:30.409 1242-1242/? D/FingerprintHal: fingerprint callback notification set
01-25 13:05:30.409 1242-1242/? V/fingerprintd: fingerprint HAL successfully initialized
01-25 13:05:30.412 1242-1609/? D/FingerprintHal: ----------------> listenerFunction ----------------->
01-25 13:05:30.450 1242-1242/? V/fingerprintd: setActiveGroup(0, /data/system/users/0/fpdata, 27)
01-25 13:05:30.450 1242-1242/? W/FingerprintHal: Setting active finger group not implemented
01-25 13:05:30.456 1538-1538/system_process V/FingerprintService: Fingerprint HAL id: -1222479872
01-25 13:05:30.456 1538-1538/system_process I/SystemServer: BackgroundDexOptService
01-25 13:05:30.457 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.pm.LauncherAppsService
01-25 13:05:30.462 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.media.projection.MediaProjectionManagerService
01-25 13:05:30.490 1538-1548/system_process I/art: Background sticky concurrent mark sweep GC freed 3664(247KB) AllocSpace objects, 2(40KB) LOS objects, 0% free, 11MB/11MB, paused 9.760ms total 52.365ms
01-25 13:05:30.500 1538-1538/system_process I/WindowManager: SAFE MODE not enabled
01-25 13:05:30.501 1538-1538/system_process I/SystemServiceManager: Starting com.android.server.MmsServiceBroker
01-25 13:05:30.534 1538-1608/system_process D/AssetAtlas: Rendered atlas in 123.78ms (2.55+121.23ms)
01-25 13:05:30.622 1538-1538/system_process E/LockSettingsStorage: Cannot read file java.io.FileNotFoundException: /data/system/gatekeeper.password.key: open failed: ENOENT (No such file or directory)
01-25 13:05:30.622 1538-1538/system_process E/LockSettingsStorage: Cannot read file java.io.FileNotFoundException: /data/system/password.key: open failed: ENOENT (No such file or directory)
01-25 13:05:30.622 1538-1538/system_process E/LockSettingsStorage: Cannot read file java.io.FileNotFoundException: /data/system/gatekeeper.pattern.key: open failed: ENOENT (No such file or directory)
01-25 13:05:30.623 1538-1538/system_process E/LockSettingsStorage: Cannot read file java.io.FileNotFoundException: /data/system/gatekeeper.gesture.key: open failed: ENOENT (No such file or directory)
01-25 13:05:30.623 1538-1538/system_process E/LockSettingsStorage: Cannot read file java.io.FileNotFoundException: /data/system/gesture.key: open failed: ENOENT (No such file or directory)
01-25 13:05:30.623 1538-1538/system_process I/SystemServiceManager: Starting phase 480
01-25 13:05:30.632 1538-1538/system_process I/SystemServiceManager: Starting phase 500
01-25 13:05:30.634 1538-1538/system_process I/WifiService: WifiService starting up with Wi-Fi disabled
01-25 13:05:30.638 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:30.640 1538-1538/system_process I/WifiScanningService: Registering wifiscanner
01-25 13:05:30.642 1538-1538/system_process I/RttService: Registering rttmanager
01-25 13:05:30.697 1538-1538/system_process V/KeyValueBackupJob: Scheduling k/v pass in 240 minutes
01-25 13:05:30.728 1538-1538/system_process V/BackupManagerService: Starting with transport android/com.android.internal.backup.LocalTransport
01-25 13:05:30.728 1538-1538/system_process V/BackupManagerService: Found transports: 2
01-25 13:05:30.730 1538-1538/system_process I/BackupManagerService: Found stale backup journal, scheduling
01-25 13:05:30.761 1538-1561/system_process W/KeyguardServiceDelegate: onScreenTurningOn(): no keyguard service!
01-25 13:05:30.761 1538-1554/system_process E/KernelCpuSpeedReader: Failed to read cpu-freq
                                                                    java.io.FileNotFoundException: /sys/devices/system/cpu/cpu0/cpufreq/stats/time_in_state: open failed: ENOENT (No such file or directory)
                                                                        at libcore.io.IoBridge.open(IoBridge.java:452)
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:76)
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:103)
                                                                        at java.io.FileReader.<init>(FileReader.java:66)
                                                                        at com.android.internal.os.KernelCpuSpeedReader.readDelta(KernelCpuSpeedReader.java:49)
                                                                        at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8002)
                                                                        at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155)
                                                                        at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                        at android.os.Looper.loop(Looper.java:148)
                                                                        at android.os.HandlerThread.run(HandlerThread.java:61)
                                                                        at com.android.server.ServiceThread.run(ServiceThread.java:46)
                                                                     Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                                        at libcore.io.Posix.open(Native Method)
                                                                        at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                                        at libcore.io.IoBridge.open(IoBridge.java:438)
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:76) 
                                                                        at java.io.FileInputStream.<init>(FileInputStream.java:103) 
                                                                        at java.io.FileReader.<init>(FileReader.java:66) 
                                                                        at com.android.internal.os.KernelCpuSpeedReader.readDelta(KernelCpuSpeedReader.java:49) 
                                                                        at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8002) 
                                                                        at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155) 
                                                                        at android.os.Handler.dispatchMessage(Handler.java:102) 
                                                                        at android.os.Looper.loop(Looper.java:148) 
                                                                        at android.os.HandlerThread.run(HandlerThread.java:61) 
                                                                        at com.android.server.ServiceThread.run(ServiceThread.java:46) 
01-25 13:05:30.762 1538-1554/system_process E/KernelUidCpuTimeReader: Failed to read uid_cputime
                                                                      java.io.FileNotFoundException: /proc/uid_cputime/show_uid_stat: open failed: ENOENT (No such file or directory)
                                                                          at libcore.io.IoBridge.open(IoBridge.java:452)
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:76)
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:103)
                                                                          at java.io.FileReader.<init>(FileReader.java:66)
                                                                          at com.android.internal.os.KernelUidCpuTimeReader.readDelta(KernelUidCpuTimeReader.java:71)
                                                                          at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8031)
                                                                          at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155)
                                                                          at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                          at android.os.Looper.loop(Looper.java:148)
                                                                          at android.os.HandlerThread.run(HandlerThread.java:61)
                                                                          at com.android.server.ServiceThread.run(ServiceThread.java:46)
                                                                       Caused by: android.system.ErrnoException: open failed: ENOENT (No such file or directory)
                                                                          at libcore.io.Posix.open(Native Method)
                                                                          at libcore.io.BlockGuardOs.open(BlockGuardOs.java:186)
                                                                          at libcore.io.IoBridge.open(IoBridge.java:438)
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:76) 
                                                                          at java.io.FileInputStream.<init>(FileInputStream.java:103) 
                                                                          at java.io.FileReader.<init>(FileReader.java:66) 
                                                                          at com.android.internal.os.KernelUidCpuTimeReader.readDelta(KernelUidCpuTimeReader.java:71) 
                                                                          at com.android.internal.os.BatteryStatsImpl.updateCpuTimeLocked(BatteryStatsImpl.java:8031) 
                                                                          at com.android.internal.os.BatteryStatsImpl$MyHandler.handleMessage(BatteryStatsImpl.java:155) 
                                                                          at android.os.Handler.dispatchMessage(Handler.java:102) 
                                                                          at android.os.Looper.loop(Looper.java:148) 
                                                                          at android.os.HandlerThread.run(HandlerThread.java:61) 
                                                                          at com.android.server.ServiceThread.run(ServiceThread.java:46) 
01-25 13:05:30.776 1538-1538/system_process I/ActivityManager: System now ready
01-25 13:05:30.778 1538-1538/system_process I/SystemServer: Making services ready
01-25 13:05:30.778 1538-1538/system_process I/SystemServiceManager: Starting phase 550
01-25 13:05:30.781 1538-1588/system_process D/MountService: Thinking about reset, mSystemReady=true, mDaemonConnected=true
01-25 13:05:30.781 1538-1588/system_process D/VoldConnector: SND -> {3 volume reset}
01-25 13:05:30.781 1538-1554/system_process I/ActivityManager: Force stopping com.android.providers.media appid=10005 user=-1: vold reset
01-25 13:05:30.781 1173-1237/? D/vold: Recognized experimental block major ID 253 as virtio-blk (emulator's virtual SD card device)
01-25 13:05:30.781 1173-1237/? V/vold: /system/bin/sgdisk
01-25 13:05:30.781 1173-1237/? V/vold:     --android-dump
01-25 13:05:30.781 1173-1237/? V/vold:     /dev/block/vold/disk:253,48
01-25 13:05:30.781 1538-1589/system_process D/VoldConnector: RCV <- {651 emulated 7}
01-25 13:05:30.781 1538-1589/system_process D/VoldConnector: RCV <- {659 emulated}
01-25 13:05:30.781 1538-1589/system_process D/VoldConnector: RCV <- {650 emulated 2 "" ""}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {651 emulated 0}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {651 public:253,48 7}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {659 public:253,48}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {649 disk:253,48}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {640 disk:253,48 5}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {641 disk:253,48 104857600}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {642 disk:253,48 Virtual}
01-25 13:05:30.782 1538-1589/system_process D/VoldConnector: RCV <- {644 disk:253,48 /sys//devices/pci0000:00/0000:00:05.0/virtio3/block/vdd}
01-25 13:05:30.783 1538-1538/system_process I/SystemServer: WebViewFactory preparation
01-25 13:05:30.786 1538-1538/system_process I/Zygote: Process: zygote socket opened, supported ABIS: x86
01-25 13:05:30.786 1200-1542/? I/art: Starting a blocking GC HeapTrim
01-25 13:05:30.788 1173-1237/? V/vold: DISK mbr
01-25 13:05:30.788 1173-1237/? W/vold: disk:253,48 has unknown partition table; trying entire device
01-25 13:05:30.788 1173-1237/? V/vold: /system/bin/blkid
01-25 13:05:30.788 1173-1237/? V/vold:     -c
01-25 13:05:30.788 1173-1237/? V/vold:     /dev/null
01-25 13:05:30.788 1173-1237/? V/vold:     -s
01-25 13:05:30.788 1173-1237/? V/vold:     TYPE
01-25 13:05:30.788 1173-1237/? V/vold:     -s
01-25 13:05:30.788 1173-1237/? V/vold:     UUID
01-25 13:05:30.789 1173-1237/? V/vold:     -s
01-25 13:05:30.789 1173-1237/? V/vold:     LABEL
01-25 13:05:30.789 1173-1237/? V/vold:     /dev/block/vold/disk:253,48
01-25 13:05:30.789 1538-1538/system_process I/ActivityManager: Start proc 1620:WebViewLoader-x86/1037 [android.webkit.WebViewFactory$RelroFileCreator] for 
01-25 13:05:30.802 1620-1620/? V/WebViewFactory: RelroFileCreator (64bit = false),  32-bit lib: /system/app/webview/webview.apk!/lib/x86/libwebviewchromium.so, 64-bit lib: 
01-25 13:05:30.809 1173-1237/? V/vold: /dev/block/vold/disk:253,48: LABEL="SDCARD" UUID="0C03-3A10" TYPE="vfat" 
01-25 13:05:30.809 1538-1589/system_process D/VoldConnector: RCV <- {650 public:253,48 0 "disk:253,48" ""}
01-25 13:05:30.809 1538-1589/system_process D/VoldConnector: RCV <- {651 public:253,48 0}
01-25 13:05:30.809 1538-1589/system_process D/VoldConnector: RCV <- {643 disk:253,48}
01-25 13:05:30.809 1538-1589/system_process D/VoldConnector: RCV <- {200 3 Command succeeded}
01-25 13:05:30.810 1538-1588/system_process D/VoldConnector: SND -> {4 volume user_added 0 0}
01-25 13:05:30.811 1538-1589/system_process D/VoldConnector: RCV <- {200 4 Command succeeded}
01-25 13:05:30.811 1538-1538/system_process I/ActivityManager: Start proc 1633:com.android.systemui/u0a13 for service com.android.systemui/.SystemUIService
01-25 13:05:30.812 1538-1538/system_process D/NetworkManagement: enabling bandwidth control
01-25 13:05:30.815 1538-1556/system_process V/MountService: Found primary storage at VolumeInfo{emulated}:
                                                                type=EMULATED diskId=null partGuid=null mountFlags=0 mountUserId=-1 
                                                                state=UNMOUNTED 
                                                                fsType=null fsUuid=null fsLabel=null 
                                                                path=null internalPath=null 
01-25 13:05:30.819 1538-1588/system_process D/VoldConnector: SND -> {5 volume mount emulated 3 -1}
01-25 13:05:30.819 1173-1237/? V/vold: Waiting for FUSE to spin up...
01-25 13:05:30.820 1538-1589/system_process D/VoldConnector: RCV <- {651 emulated 1}
01-25 13:05:30.823 1538-1589/system_process D/VoldConnector: RCV <- {656 emulated /data/media}
01-25 13:05:30.823 1538-1589/system_process D/VoldConnector: RCV <- {655 emulated /storage/emulated}
01-25 13:05:30.870 1173-1237/? V/vold: Waiting for FUSE to spin up...
01-25 13:05:30.882 1633-1633/com.android.systemui W/System: ClassLoader referenced unknown path: /system/priv-app/SystemUI/lib/x86
01-25 13:05:30.922 1538-1589/system_process D/VoldConnector: RCV <- {651 emulated 2}
01-25 13:05:30.922 1538-1589/system_process D/VoldConnector: RCV <- {200 5 Command succeeded}
01-25 13:05:30.925 1538-1588/system_process D/VoldConnector: SND -> {6 volume mount public:253,48 2 0}
01-25 13:05:30.926 1173-1237/? V/vold: /system/bin/blkid
01-25 13:05:30.926 1173-1237/? V/vold:     -c
01-25 13:05:30.926 1173-1237/? V/vold:     /dev/null
01-25 13:05:30.926 1173-1237/? V/vold:     -s
01-25 13:05:30.926 1173-1237/? V/vold:     TYPE
01-25 13:05:30.926 1173-1237/? V/vold:     -s
01-25 13:05:30.926 1173-1237/? V/vold:     UUID
01-25 13:05:30.926 1173-1237/? V/vold:     -s
01-25 13:05:30.926 1173-1237/? V/vold:     LABEL
01-25 13:05:30.926 1173-1237/? V/vold:     /dev/block/vold/public:253,48
01-25 13:05:30.926 1538-1589/system_process D/VoldConnector: RCV <- {651 public:253,48 1}
01-25 13:05:30.937 1538-1554/system_process I/ActivityManager: Start proc 1673:com.android.externalstorage/u0a6 for broadcast com.android.externalstorage/.MountReceiver
01-25 13:05:30.944 1633-1633/com.android.systemui V/SystemUIService: Starting SystemUI services.
01-25 13:05:30.963 1173-1237/? V/vold: /dev/block/vold/public:253,48: LABEL="SDCARD" UUID="0C03-3A10" TYPE="vfat" 
01-25 13:05:30.963 1173-1237/? V/vold: /system/bin/fsck_msdos
01-25 13:05:30.963 1173-1237/? V/vold:     -p
01-25 13:05:30.963 1173-1237/? V/vold:     -f
01-25 13:05:30.963 1173-1237/? V/vold:     /dev/block/vold/public:253,48
01-25 13:05:30.964 1538-1589/system_process D/VoldConnector: RCV <- {652 public:253,48 vfat}
01-25 13:05:30.964 1538-1589/system_process D/VoldConnector: RCV <- {653 public:253,48 0C03-3A10}
01-25 13:05:30.964 1538-1589/system_process D/VoldConnector: RCV <- {654 public:253,48 SDCARD}
01-25 13:05:30.964 1673-1673/com.android.externalstorage W/System: ClassLoader referenced unknown path: /system/priv-app/ExternalStorageProvider/lib/x86
01-25 13:05:30.966 1673-1673/com.android.externalstorage D/ExternalStorage: After updating volumes, found 1 active roots
01-25 13:05:30.967 1673-1673/com.android.externalstorage D/ExternalStorage: After updating volumes, found 1 active roots
01-25 13:05:31.038 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.038 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.038 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -F st_penalty_log 
01-25 13:05:31.040 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.047 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.047 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -F st_penalty_log 
01-25 13:05:31.049 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.051 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.051 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -F st_penalty_reject 
01-25 13:05:31.053 1620-1620/? I/art: System.exit called, status: 0
01-25 13:05:31.053 1620-1620/? I/AndroidRuntime: VM exiting with result code 0, cleanup skipped.
01-25 13:05:31.053 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.061 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.061 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -F st_penalty_reject 
01-25 13:05:31.064 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.071 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.071 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -F st_clear_caught 
01-25 13:05:31.075 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.082 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.082 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -F st_clear_caught 
01-25 13:05:31.089 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.102 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.102 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -F st_clear_detect 
01-25 13:05:31.104 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.108 1173-1237/? I/fsck_msdos: ** /dev/block/vold/public:253,48
01-25 13:05:31.109 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.109 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -F st_clear_detect 
01-25 13:05:31.111 1173-1237/? I/fsck_msdos: ** Phase 1 - Read and Compare FATs
01-25 13:05:31.111 1173-1237/? I/fsck_msdos: Attempting to allocate 794 KB for FAT
01-25 13:05:31.117 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.117 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.117 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -X st_penalty_log 
01-25 13:05:31.120 1633-1709/com.android.systemui E/WVMExtractor: Failed to open libwvm.so: dlopen failed: library "libwvm.so" not found
01-25 13:05:31.121 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.123 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.123 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -X st_penalty_log 
01-25 13:05:31.129 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.129 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.129 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -X st_penalty_reject 
01-25 13:05:31.132 1173-1237/? I/fsck_msdos: Attempting to allocate 794 KB for FAT
01-25 13:05:31.135 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.135 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.135 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -X st_penalty_reject 
01-25 13:05:31.140 1173-1237/? I/fsck_msdos: ** Phase 2 - Check Cluster Chains
01-25 13:05:31.141 1173-1237/? I/fsck_msdos: ** Phase 3 - Checking Directories
01-25 13:05:31.142 1173-1237/? I/fsck_msdos: ** Phase 4 - Checking for Lost Files
01-25 13:05:31.142 1173-1237/? I/fsck_msdos: 14 files, 100789 free (201578 clusters)
01-25 13:05:31.148 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.151 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.151 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -X st_clear_caught 
01-25 13:05:31.148 1173-1237/? I/Vold: Filesystem check completed OK
01-25 13:05:31.151 1538-1589/system_process D/VoldConnector: RCV <- {656 public:253,48 /mnt/media_rw/0C03-3A10}
01-25 13:05:31.151 1538-1589/system_process D/VoldConnector: RCV <- {655 public:253,48 /storage/0C03-3A10}
01-25 13:05:31.160 1173-1237/? V/vold: Waiting for FUSE to spin up...
01-25 13:05:31.161 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.161 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.161 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -X st_clear_caught 
01-25 13:05:31.167 1192-1534/? I/iptables: iptables: No chain/target/match by that name.
01-25 13:05:31.168 1192-1534/? I/iptables: iptables terminated by exit(1)
01-25 13:05:31.168 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/iptables -w -X st_clear_detect 
01-25 13:05:31.179 1192-1534/? I/ip6tables: ip6tables: No chain/target/match by that name.
01-25 13:05:31.182 1192-1534/? I/ip6tables: ip6tables terminated by exit(1)
01-25 13:05:31.182 1192-1534/? E/Netd: exec() res=0, status=256 for /system/bin/ip6tables -w -X st_clear_detect 
01-25 13:05:31.211 1538-1589/system_process D/VoldConnector: RCV <- {651 public:253,48 2}
01-25 13:05:31.211 1538-1589/system_process D/VoldConnector: RCV <- {200 6 Command succeeded}
01-25 13:05:31.225 1673-1673/com.android.externalstorage D/ExternalStorage: After updating volumes, found 2 active roots
01-25 13:05:31.227 1673-1673/com.android.externalstorage D/ExternalStorage: After updating volumes, found 2 active roots
01-25 13:05:31.228 1673-1673/com.android.externalstorage D/ExternalStorage: After updating volumes, found 2 active roots
01-25 13:05:31.270 1196-1196/? W/OMXNodeInstance: [f:google.mpeg2.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.276 1196-1196/? W/OMXNodeInstance: [10:google.mpeg4.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.277 1196-1196/? W/OMXNodeInstance: [11:google.h263.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.285 1196-1196/? D/SoftAVCDec: Number of CPU cores: 2
01-25 13:05:31.289 1196-1196/? W/OMXNodeInstance: [12:google.h264.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.289 1196-1196/? D/SoftAVCDec: Number of CPU cores: 2
01-25 13:05:31.298 1196-1196/? D/SoftHEVC: Number of CPU cores: 2
01-25 13:05:31.300 1196-1196/? D/SoftHEVC: Initializing decoder
01-25 13:05:31.307 1196-1196/? D/SoftHEVC: Set number of cores to 2
01-25 13:05:31.307 1196-1196/? D/SoftHEVC: Ittiam decoder version number: @(#)Id:HEVCDEC_production Ver:04.04 Released by ITTIAM Build: Jan 11 2016 @ 06:34:43
01-25 13:05:31.308 1196-1196/? W/OMXNodeInstance: [13:google.hevc.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.308 1196-1196/? D/SoftHEVC: Freeing codec memory
01-25 13:05:31.308 1196-1196/? D/SoftHEVC: Number of CPU cores: 2
01-25 13:05:31.308 1196-1196/? D/SoftHEVC: Initializing decoder
01-25 13:05:31.308 1196-1196/? D/SoftHEVC: Set number of cores to 2
01-25 13:05:31.308 1196-1196/? D/SoftHEVC: Ittiam decoder version number: @(#)Id:HEVCDEC_production Ver:04.04 Released by ITTIAM Build: Jan 11 2016 @ 06:34:43
01-25 13:05:31.309 1196-1196/? D/SoftHEVC: In SoftHEVC::~SoftHEVC
01-25 13:05:31.309 1196-1196/? D/SoftHEVC: Freeing codec memory
01-25 13:05:31.358 1196-1196/? W/OMXNodeInstance: [14:google.vp8.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.360 1196-1196/? W/OMXNodeInstance: [15:google.vp9.decoder] component does not support metadata mode; using fallback
01-25 13:05:31.365 1196-1196/? I/SoftMPEG4Encoder: Construct SoftMPEG4Encoder
01-25 13:05:31.365 1196-1196/? W/ACodec: do not know color format 0x7f000789 = 2130708361
01-25 13:05:31.377 1196-1196/? W/ACodec: do not know color format 0x7f000789 = 2130708361
01-25 13:05:31.378 1196-1196/? I/SoftMPEG4Encoder: Construct SoftMPEG4Encoder
01-25 13:05:31.378 1196-1196/? W/ACodec: do not know color format 0x7f000789 = 2130708361
01-25 13:05:31.382 1196-1196/? W/ACodec: do not know color format 0x7f000789 = 2130708361
01-25 13:05:31.383 1196-1196/? W/MediaCodecList: unable to open media codecs configuration xml file: /etc/media_codecs_performance.xml
01-25 13:05:31.383 1196-1196/? W/MediaCodecList: unable to open media codecs configuration xml file: /data/misc/media/media_codecs_profiling_results.xml
01-25 13:05:31.384 1633-1714/com.android.systemui I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.427 1633-1814/com.android.systemui I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.519 1633-1825/com.android.systemui I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.521 1538-1538/system_process D/PermissionMonitor: Monitoring
01-25 13:05:31.523 1538-1538/system_process D/PermissionMonitor: Users: 1, Apps: 53
01-25 13:05:31.525 1538-1538/system_process I/SystemServiceManager: Starting phase 600
01-25 13:05:31.526 1538-1604/system_process E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:31.526 1538-1604/system_process E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:31.529 1538-1538/system_process I/BackupManagerService: Backup enabled => true
01-25 13:05:31.548 1196-1196/? I/AudioFlinger: systemReady
01-25 13:05:31.548 1538-1831/system_process E/WVMExtractor: Failed to open libwvm.so: dlopen failed: library "libwvm.so" not found
01-25 13:05:31.553 1538-1839/system_process I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.558 1538-1538/system_process I/ActivityManager: Start proc 1833:com.google.android.googlequicksearchbox:interactor/u0a14 for service com.google.android.googlequicksearchbox/com.google.android.voiceinteraction.GsaVoiceInteractionService
01-25 13:05:31.560 1538-1538/system_process E/InputMethodManagerService: Ignoring updateSystemUiLocked due to an invalid token. uid:1000 token:null
01-25 13:05:31.565 1538-1538/system_process I/ActivityManager: Start proc 1848:com.android.inputmethod.latin/u0a34 for service com.android.inputmethod.latin/.LatinIME
01-25 13:05:31.565 1538-1538/system_process V/InputMethodManagerService: Adding window token: android.os.Binder@97fb140
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: Reset GPS properties, previous size = 0
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_HOST=supl.google.com
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_PORT=7275
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: NTP_SERVER=north-america.pool.ntp.org
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_VER=0x20000
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_MODE=1
01-25 13:05:31.571 1538-1553/system_process W/GpsLocationProvider: Could not open GPS configuration file /etc/gps.conf
01-25 13:05:31.571 1538-1553/system_process D/GpsLocationProvider: GPS properties reloaded, size = 5
01-25 13:05:31.571 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:31.577 1538-1538/system_process E/FlpHardwareProvider: Error hw_get_module 'flp': -2
01-25 13:05:31.578 1538-1538/system_process E/LocationManagerService: FLP HAL not supported
01-25 13:05:31.581 1538-1538/system_process E/ActivityRecognitionHardware: Error hw_get_module: -2
01-25 13:05:31.582 1538-1538/system_process E/LocationManagerService: Hardware Activity-Recognition not supported.
01-25 13:05:31.593 1538-1554/system_process I/ActivityManager: Start proc 1861:com.google.android.gms.persistent/u0a7 for broadcast com.google.android.gms/com.google.android.location.internal.NlpNetworkProviderSettingsUpdateReceiver
01-25 13:05:31.597 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:31.602 1538-1538/system_process I/CommonTimeManagementService: No common time service detected on this platform.  Common time services will be unavailable.
01-25 13:05:31.602 1538-1538/system_process I/MmsServiceBroker: Delay connecting to MmsService until an API is called
01-25 13:05:31.603 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000020
01-25 13:05:31.603 1538-1538/system_process D/MountService: onStartUser 0
01-25 13:05:31.603 1538-1538/system_process D/VoldConnector: SND -> {7 volume user_started 0}
01-25 13:05:31.604 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000010
01-25 13:05:31.604 1173-1237/? D/vold: Linking /storage/emulated/0 to /mnt/user/0/primary
01-25 13:05:31.604 1538-1589/system_process D/VoldConnector: RCV <- {200 7 Command succeeded}
01-25 13:05:31.634 1538-1538/system_process I/ActivityManager: Start proc 1870:com.android.phone/1001 for added application com.android.phone
01-25 13:05:31.634 1538-1538/system_process I/ActivityManager: START u0 {act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10000000 cmp=com.google.android.googlequicksearchbox/com.google.android.launcher.GEL} from uid 0 on display 0
01-25 13:05:31.642 1538-1588/system_process D/MountService: Volume public:253,48 broadcasting mounted to UserHandle{0}
01-25 13:05:31.653 1538-1538/system_process I/ActivityManager: Start proc 1891:com.google.android.googlequicksearchbox/u0a14 for activity com.google.android.googlequicksearchbox/com.google.android.launcher.GEL
01-25 13:05:31.656 1538-1538/system_process I/SystemServer: Enabled StrictMode for system server main thread.
01-25 13:05:31.656 1538-1588/system_process D/MountService: Volume emulated broadcasting mounted to UserHandle{0}
01-25 13:05:31.661 1538-1538/system_process D/RttService: SCAN_AVAILABLE : 1
01-25 13:05:31.664 1538-1614/system_process D/RttService: DefaultState got{ when=-1ms what=160513 target=com.android.internal.util.StateMachine$SmHandler }
01-25 13:05:31.671 1861-1877/? E/art: Failed sending reply to debugger: Broken pipe
01-25 13:05:31.671 1861-1877/? I/art: Debugger is no longer active
01-25 13:05:31.673 1538-1538/system_process I/Choreographer: Skipped 55 frames!  The application may be doing too much work on its main thread.
01-25 13:05:31.678 1633-1644/com.android.systemui I/art: Background partial concurrent mark sweep GC freed 73(3KB) AllocSpace objects, 0(0B) LOS objects, 38% free, 6MB/10MB, paused 7.831ms total 76.909ms
01-25 13:05:31.746 1538-1898/system_process I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.752 1870-1870/? W/System: ClassLoader referenced unknown path: /system/priv-app/TeleService/lib/x86
01-25 13:05:31.768 1861-1861/? W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:31.776 1538-1553/system_process I/ActivityManager: Start proc 1914:com.android.printspooler/u0a44 for service com.android.printspooler/.model.PrintSpoolerService
01-25 13:05:31.784 1538-1555/system_process W/WindowManager: Keyguard drawn timeout. Setting mKeyguardDrawComplete
01-25 13:05:31.786 1538-1538/system_process W/System: ClassLoader referenced unknown path: /system/priv-app/Telecom/lib/x86
01-25 13:05:31.861 1870-1870/? W/System: ClassLoader referenced unknown path: /system/priv-app/TelephonyProvider/lib/x86
01-25 13:05:31.877 1538-1928/system_process I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.903 1914-1914/? I/PrintSpoolerService: No existing print spooler state.
01-25 13:05:31.926 1633-1633/com.android.systemui D/skia: --- SkImageDecoder::Factory returned null
01-25 13:05:31.926 1633-1633/com.android.systemui D/skia: --- SkImageDecoder::Factory returned null
01-25 13:05:31.976 1538-1932/system_process I/OMXClient: Using client-side OMX mux.
01-25 13:05:31.995 1870-1870/? D/TelephonyProvider: dbh.onOpen: ok, queried table=siminfo
01-25 13:05:31.995 1870-1870/? D/TelephonyProvider: dbh.onOpen: ok, queried table=carriers
01-25 13:05:32.007 1538-1937/system_process I/OMXClient: Using client-side OMX mux.
01-25 13:05:32.039 1633-1633/com.android.systemui I/vol.Events: writeEvent collection_started
01-25 13:05:32.047 1633-1940/com.android.systemui I/vol.Events: writeEvent external_ringer_mode_changed normal
01-25 13:05:32.051 1633-1940/com.android.systemui I/vol.Events: writeEvent internal_ringer_mode_changed normal
01-25 13:05:32.081 1538-1943/system_process I/OMXClient: Using client-side OMX mux.
01-25 13:05:32.089 1538-1538/system_process E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:32.106 1538-1946/system_process I/ActivityManager: Start proc 1948:android.process.acore/u0a2 for content provider com.android.providers.contacts/.CallLogProvider
01-25 13:05:32.109 1633-1940/com.android.systemui I/vol.Events: writeEvent level_changed STREAM_ALARM 6
01-25 13:05:32.110 1538-1538/system_process E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:32.111 1633-1940/com.android.systemui I/vol.Events: writeEvent level_changed STREAM_BLUETOOTH_SCO 7
01-25 13:05:32.111 1633-1940/com.android.systemui I/vol.Events: writeEvent level_changed STREAM_MUSIC 11
01-25 13:05:32.112 1633-1940/com.android.systemui I/vol.Events: writeEvent level_changed STREAM_RING 5
01-25 13:05:32.112 1538-1538/system_process I/Telecom: Class: TelecomSystem.INSTANCE being set
01-25 13:05:32.112 1633-1940/com.android.systemui I/vol.Events: writeEvent level_changed STREAM_SYSTEM 5
01-25 13:05:32.112 1538-1538/system_process E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:32.113 1633-1940/com.android.systemui I/vol.Events: writeEvent level_changed STREAM_VOICE_CALL 4
01-25 13:05:32.125 1538-1538/system_process D/GpsNetInitiatedHandler: location enabled :true
01-25 13:05:32.125 1538-1538/system_process V/WiredAccessoryManager: init()
01-25 13:05:32.126 1633-1633/com.android.systemui D/StorageNotification: Notifying about private volume: VolumeInfo{private}:
                                                                             type=PRIVATE diskId=null partGuid=null mountFlags=0 mountUserId=-1 
                                                                             state=MOUNTED 
                                                                             fsType=null fsUuid=null fsLabel=null 
                                                                             path=/data internalPath=null 
01-25 13:05:32.127 1633-1633/com.android.systemui D/StorageNotification: Notifying about public volume: VolumeInfo{public:253,48}:
                                                                             type=PUBLIC diskId=disk:253,48 partGuid=null mountFlags=VISIBLE 
                                                                             mountUserId=0 state=MOUNTED 
                                                                             fsType=vfat fsUuid=0C03-3A10 fsLabel=SDCARD 
                                                                             path=/storage/0C03-3A10 internalPath=/mnt/media_rw/0C03-3A10 
01-25 13:05:32.153 1948-1948/? W/System: ClassLoader referenced unknown path: /system/priv-app/ContactsProvider/lib/x86
01-25 13:05:32.159 1186-1373/? D/PermissionCache: checking android.permission.HARDWARE_TEST for uid=1000 => granted (1192 us)
01-25 13:05:32.173 1538-1554/system_process I/ActivityManager: Start proc 1977:com.android.music/u0a39 for broadcast com.android.music/.MediaButtonIntentReceiver
01-25 13:05:32.174 1848-1848/com.android.inputmethod.latin I/LatinIME: Hardware accelerated drawing: true
01-25 13:05:32.192 1538-1538/system_process V/BackupManagerService: Connected to transport ComponentInfo{android/com.android.internal.backup.LocalTransportService}
01-25 13:05:32.192 1538-1538/system_process V/BackupManagerService: Registering transport android/com.android.internal.backup.LocalTransportService::android/com.android.internal.backup.LocalTransport = android.app.backup.BackupTransport$TransportImpl@f907bf3
                                                                    
                                                                    [ 01-25 13:05:32.217  1538: 1538 D/         ]
                                                                    HostConnection::get() New Host Connection established 0x9f816230, tid 1538
01-25 13:05:32.226 1977-1977/? W/System: ClassLoader referenced unknown path: /system/app/Music/lib/x86
01-25 13:05:32.293 1633-1644/com.android.systemui W/art: Suspending all threads took: 55.256ms
01-25 13:05:32.311 1633-1644/com.android.systemui I/art: Background sticky concurrent mark sweep GC freed 10601(727KB) AllocSpace objects, 0(0B) LOS objects, 8% free, 9MB/10MB, paused 57.570ms total 66.533ms
01-25 13:05:32.335 1848-1848/com.android.inputmethod.latin W/InputAttributes: No editor info for this field. Bug?
01-25 13:05:32.379 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:32.381 1870-2011/? E/DcSwitchStateMachine-0: DctController is not ready
01-25 13:05:32.392 1538-1927/system_process I/ActivityManager: Start proc 2017:android.process.media/u0a5 for content provider com.android.providers.media/.MediaProvider
01-25 13:05:32.392 1538-1599/system_process E/ConnectivityService: Failed to find Messenger in unregisterNetworkFactory
01-25 13:05:32.401 1848-1999/com.android.inputmethod.latin I/LatinIME:LogUtils: Dictionary info: dictionary = contacts.en_US ; version = 1516885532 ; date = ?
01-25 13:05:32.402 1538-1599/system_process D/ConnectivityService: Got NetworkFactory Messenger for Telephony
01-25 13:05:32.413 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:32.439 2017-2017/? W/System: ClassLoader referenced unknown path: /system/priv-app/MediaProvider/lib/x86
01-25 13:05:32.442 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:32.447 1870-1870/? D/CarrierConfigLoader: CarrierConfigLoader has started
01-25 13:05:32.448 1870-1870/? E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:32.454 1538-1904/system_process I/StatusBarManagerService: registerStatusBar bar=com.android.internal.statusbar.IStatusBar$Stub$Proxy@ded72d2
01-25 13:05:32.529 1948-1948/? W/System: ClassLoader referenced unknown path: /system/app/UserDictionaryProvider/lib/x86
01-25 13:05:32.534 1870-1870/? I/Telephony: TtyManager: updateUiTtyMode -1 -> 0
01-25 13:05:32.541 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:32.550 1538-1904/system_process D/AlarmManagerService: Kernel timezone updated to 0 minutes west of GMT
01-25 13:05:32.557 1538-1648/system_process D/AlarmManagerService: Setting time of day to sec=1516885533
01-25 13:05:33.841 1538-1648/system_process W/AlarmManagerService: Unable to set rtc to 1516885533: No such device
01-25 13:05:33.842 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:33.886 1870-1870/? D/TelephonyDebugService: TelephonyDebugService()
01-25 13:05:33.895 1870-1870/? D/CarrierConfigLoader: mHandler: 12 phoneId: 0
01-25 13:05:33.902 1870-1870/? E/PhoneInterfaceManager: [PhoneIntfMgr] getIccId: No UICC
01-25 13:05:33.925 1538-1552/system_process I/Telecom: PhoneAccountRegistrar: New phone account registered: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ]
01-25 13:05:33.931 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:33.939 1538-1552/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:33.941 1870-1870/? I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}
01-25 13:05:33.946 1870-1870/? I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:33.951 1870-1870/? I/Telephony: TelecomAccountRegistry: Unregistering phone account ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}.
01-25 13:05:33.969 1538-1552/system_process W/Telecom: : No account found for the calling user
01-25 13:05:34.008 1633-1644/com.android.systemui I/art: Background sticky concurrent mark sweep GC freed 2040(101KB) AllocSpace objects, 0(0B) LOS objects, 0% free, 10MB/10MB, paused 8.556ms total 50.211ms
01-25 13:05:34.024 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.024 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration mccmnc='310260' fromServiceState=true
01-25 13:05:34.032 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration defaultMccMnc=
01-25 13:05:34.032 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration: mcc=310, mnc=260
01-25 13:05:34.032 1870-1870/com.android.phone D/MccTable: WIFI_COUNTRY_CODE set to us
01-25 13:05:34.052 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:34.057 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:34.057 1538-1904/system_process I/WifiService: WifiService trying to set country code to us with persist set to true
01-25 13:05:34.112 1633-1633/com.android.systemui E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:34.114 1538-1992/system_process D/ConnectivityService: listenForNetwork for Listen from uid/pid:10013/1633 for NetworkRequest [ id=3, legacyType=-1, [] ]
01-25 13:05:34.118 1633-1633/com.android.systemui I/CameraManagerGlobal: Connecting to camera service
01-25 13:05:34.119 1196-1605/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.119 1196-1605/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.119 1196-1605/? I/CameraService: getCameraCharacteristics: Switching to HAL1 shim implementation...
01-25 13:05:34.120 1196-1605/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.120 1196-1605/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.120 1196-1605/? I/CameraService: CameraService::connect call (PID 1196 "media", camera ID 0) for HAL version default and Camera API version 1
01-25 13:05:34.120 1196-1605/? E/CameraService: getCameraPriorityFromProcState: Received invalid process state -1 from ActivityManagerService!
01-25 13:05:34.120 1196-1605/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.120 1196-1605/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.137 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:34.138 1870-1870/com.android.phone E/PhoneInterfaceManager: [PhoneIntfMgr] getIccId: No UICC
01-25 13:05:34.138 1196-2054/? E/WVMExtractor: Failed to open libwvm.so: dlopen failed: library "libwvm.so" not found
01-25 13:05:34.139 1538-1992/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:34.139 1196-2053/? D/NuPlayerDriver: notifyListener_l(0xb4866000), (1, 0, 0)
01-25 13:05:34.148 1538-1992/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:34.149 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}
01-25 13:05:34.149 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:34.151 1538-1892/system_process W/Telecom: : No account found for the calling user
01-25 13:05:34.157 1196-2059/? D/NuPlayerDriver: notifyListener_l(0xb4866060), (1, 0, 0)
01-25 13:05:34.157 1196-1605/? I/CameraClient: Opening camera 0
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_Camera: connectCamera
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_FakeDevice: connectDevice
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier: setCallbacks: 0xb75d0505, 0xb75d0dba, 0xb75d0c92, 0xb75d1267 (0xb48660c0)
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier: enableMessage: msg_type = 0xc0d
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ERROR
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_FOCUS
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ZOOM
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_METADATA
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier: **** Currently enabled messages:
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ERROR
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_FOCUS
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ZOOM
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_METADATA
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier: disableMessage: msg_type = 0xffff
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ERROR
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_SHUTTER
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_FOCUS
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ZOOM
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_FRAME
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_VIDEO_FRAME
01-25 13:05:34.157 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_POSTVIEW_FRAME
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_RAW_IMAGE
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_COMPRESSED_IMAGE
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_RAW_IMAGE_NOTIFY
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_METADATA
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_CallbackNotifier: **** Currently enabled messages:
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_Camera: cancelPicture
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_Camera: releaseCamera
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_FakeDevice: disconnectDevice
01-25 13:05:34.158 1196-1605/? I/CameraFlashlight: Destroying camera 0
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_Camera: closeCamera
01-25 13:05:34.158 1196-1605/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:34.158 1196-1605/? I/CameraService: disconnect: Disconnected client for camera 0 for PID 1196
01-25 13:05:34.158 1196-1605/? D/NuPlayerDriver: reset(0xb4866000)
01-25 13:05:34.158 1196-1605/? D/NuPlayerDriver: notifyListener_l(0xb4866000), (8, 0, 0)
01-25 13:05:34.158 1196-2053/? D/NuPlayerDriver: notifyResetComplete(0xb4866000)
01-25 13:05:34.159 1196-1605/? D/NuPlayerDriver: reset(0xb4866060)
01-25 13:05:34.159 1196-1605/? D/NuPlayerDriver: notifyListener_l(0xb4866060), (8, 0, 0)
01-25 13:05:34.160 1196-2059/? D/NuPlayerDriver: notifyResetComplete(0xb4866060)
01-25 13:05:34.160 1196-1605/? E/CameraService: disconnect: Disconnect called on already disconnected client for device 0
01-25 13:05:34.160 1196-1581/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.160 1196-1581/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.160 1196-1581/? I/CameraService: getCameraCharacteristics: Switching to HAL1 shim implementation...
01-25 13:05:34.160 1196-1581/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.160 1196-1581/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.160 1196-1581/? I/CameraService: CameraService::connect call (PID 1196 "media", camera ID 1) for HAL version default and Camera API version 1
01-25 13:05:34.160 1196-1581/? E/CameraService: getCameraPriorityFromProcState: Received invalid process state -1 from ActivityManagerService!
01-25 13:05:34.160 1196-1581/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.160 1196-1581/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.164 1870-2011/com.android.phone E/DcSwitchStateMachine-0: EVENT_DATA_DISALLOWED failed, com.android.internal.telephony.CommandException: REQUEST_NOT_SUPPORTED
01-25 13:05:34.175 1196-2061/? D/NuPlayerDriver: notifyListener_l(0xb6159d80), (1, 0, 0)
01-25 13:05:34.180 1196-2063/? D/NuPlayerDriver: notifyListener_l(0xb6159d20), (1, 0, 0)
01-25 13:05:34.180 2017-2017/android.process.media W/System: ClassLoader referenced unknown path: /system/priv-app/DownloadProvider/lib/x86
01-25 13:05:34.180 1196-1581/? I/CameraClient: Opening camera 1
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_Camera: connectCamera
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_FakeDevice: connectDevice
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier: setCallbacks: 0xb75d0505, 0xb75d0dba, 0xb75d0c92, 0xb75d1267 (0xb6159e40)
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier: enableMessage: msg_type = 0xc0d
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ERROR
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_FOCUS
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ZOOM
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_METADATA
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier: **** Currently enabled messages:
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ERROR
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_FOCUS
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ZOOM
01-25 13:05:34.180 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_METADATA
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier: disableMessage: msg_type = 0xffff
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ERROR
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_SHUTTER
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_FOCUS
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_ZOOM
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_FRAME
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_VIDEO_FRAME
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_POSTVIEW_FRAME
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_RAW_IMAGE
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_COMPRESSED_IMAGE
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_RAW_IMAGE_NOTIFY
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier:     CAMERA_MSG_PREVIEW_METADATA
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_CallbackNotifier: **** Currently enabled messages:
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_Camera: cancelPicture
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_Camera: releaseCamera
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_FakeDevice: disconnectDevice
01-25 13:05:34.181 1196-1581/? I/CameraFlashlight: Destroying camera 1
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_Camera: closeCamera
01-25 13:05:34.181 1196-1581/? V/EmulatedCamera_Camera: doStopPreview
01-25 13:05:34.181 1196-1581/? I/CameraService: disconnect: Disconnected client for camera 1 for PID 1196
01-25 13:05:34.181 1196-1581/? D/NuPlayerDriver: reset(0xb6159d80)
01-25 13:05:34.181 1196-1581/? D/NuPlayerDriver: notifyListener_l(0xb6159d80), (8, 0, 0)
01-25 13:05:34.181 1196-2061/? D/NuPlayerDriver: notifyResetComplete(0xb6159d80)
01-25 13:05:34.181 1196-1581/? D/NuPlayerDriver: reset(0xb6159d20)
01-25 13:05:34.181 1196-1581/? D/NuPlayerDriver: notifyListener_l(0xb6159d20), (8, 0, 0)
01-25 13:05:34.181 1196-2063/? D/NuPlayerDriver: notifyResetComplete(0xb6159d20)
01-25 13:05:34.181 1196-1581/? E/CameraService: disconnect: Disconnect called on already disconnected client for device 1
01-25 13:05:34.181 1196-1606/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.181 1196-1606/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.182 1196-1605/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.182 1196-1605/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.188 1196-1581/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.188 1196-1581/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.188 1196-1196/? V/EmulatedCamera_Camera: getCameraInfo
01-25 13:05:34.188 1196-1196/? V/EmulatedCamera_BaseCamera: getCameraInfo
01-25 13:05:34.208 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.230 1186-1910/? E/SurfaceFlinger: ro.sf.lcd_density must be defined as a build property
01-25 13:05:34.234 1633-2068/com.android.systemui D/OpenGLRenderer: Use EGL_SWAP_BEHAVIOR_PRESERVED: true
01-25 13:05:34.234 1633-2068/com.android.systemui D/OpenGLRenderer: profile bars disabled
01-25 13:05:34.234 1633-2068/com.android.systemui D/OpenGLRenderer: ambientRatio = 1.50
01-25 13:05:34.236 1870-2011/com.android.phone E/DcSwitchStateMachine-0: EVENT_DATA_DISALLOWED failed, com.android.internal.telephony.CommandException: REQUEST_NOT_SUPPORTED
                                                                         
                                                                         [ 01-25 13:05:34.239  1633: 1633 D/         ]
                                                                         HostConnection::get() New Host Connection established 0xb40083c0, tid 1633
01-25 13:05:34.243 1633-1633/com.android.systemui D/PhoneStatusBar: disable: < EXPAND* icons alerts system_info BACK* HOME* RECENT* clock SEARCH* quick_settings >
01-25 13:05:34.249 1861-1861/com.google.android.gms.persistent I/MultiDex: VM with version 2.1.0 has multidex support
01-25 13:05:34.249 1861-1861/com.google.android.gms.persistent I/MultiDex: install
01-25 13:05:34.249 1861-1861/com.google.android.gms.persistent I/MultiDex: VM has multidex support, MultiDex support library is disabled.
01-25 13:05:34.257 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration mccmnc='310260' fromServiceState=false
01-25 13:05:34.258 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration defaultMccMnc=
01-25 13:05:34.258 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration: mcc=310, mnc=260
01-25 13:05:34.258 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration updateConfig config={1.0 310mcc260mnc ?locale ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/?}
01-25 13:05:34.258 1538-1648/system_process I/ActivityManager: Config changes=3 {1.0 310mcc260mnc en_US ldltr sw360dp w360dp h568dp 480dpi nrml port finger -keyb/v/h -nav/h s.5}
01-25 13:05:34.292 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:34.292 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.292 1186-1373/? D/PermissionCache: checking android.permission.READ_FRAME_BUFFER for uid=1000 => granted (1123 us)
01-25 13:05:34.325 1186-1186/? E/EGL_emulation: tid 1186: eglCreateSyncKHR(1294): error 0x3004 (EGL_BAD_ATTRIBUTE)
01-25 13:05:34.429 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:34.430 1538-1892/system_process I/ActivityManager: Start proc 2072:com.google.android.googlequicksearchbox:search/u0a14 for service com.google.android.googlequicksearchbox/com.google.android.hotword.service.HotwordService
01-25 13:05:34.434 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:34.435 1633-1633/com.android.systemui D/PhoneStatusBar: heads up is enabled
01-25 13:05:34.439 1870-1870/com.android.phone E/PhoneInterfaceManager: [PhoneIntfMgr] getIccId: No UICC
01-25 13:05:34.440 1538-1552/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}(addr: tel:*********** -> tel:)(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))(subAddr: tel:*********** -> tel:)]
01-25 13:05:34.459 1538-1552/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:34.459 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}
01-25 13:05:34.459 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:34.482 2072-2080/? E/art: Failed writing handshake bytes (-1 of 14): Broken pipe
01-25 13:05:34.483 2072-2080/? I/art: Debugger is no longer active
01-25 13:05:34.526 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.527 1538-1927/system_process W/Telecom: : No account found for the calling user
01-25 13:05:34.559 1870-1870/com.android.phone D/TelephonyProvider: subIdString = -2 subId = -2
01-25 13:05:34.578 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:34.578 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.593 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:34.596 1870-1870/com.android.phone E/PhoneInterfaceManager: [PhoneIntfMgr] getIccId: No UICC
01-25 13:05:34.597 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is still not available
01-25 13:05:34.599 1538-1904/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:34.625 1538-1904/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:34.625 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}
01-25 13:05:34.625 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:34.627 1538-2069/system_process W/Telecom: : No account found for the calling user
01-25 13:05:34.633 1870-2011/com.android.phone E/DcSwitchStateMachine-0: EVENT_DATA_DISALLOWED failed, com.android.internal.telephony.CommandException: REQUEST_NOT_SUPPORTED
01-25 13:05:34.640 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration mccmnc='310260' fromServiceState=false
01-25 13:05:34.640 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration defaultMccMnc=310260
01-25 13:05:34.640 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration: mcc=310, mnc=260
01-25 13:05:34.640 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration updateConfig config={1.0 310mcc260mnc ?locale ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/?}
01-25 13:05:34.710 1633-1633/com.android.systemui I/Choreographer: Skipped 36 frames!  The application may be doing too much work on its main thread.
01-25 13:05:34.711 1633-1633/com.android.systemui D/ViewRootImpl: changeCanvasOpacity: opaque=true
01-25 13:05:34.849 1538-1892/system_process I/ActivityManager: Start proc 2091:com.google.process.gapps/u0a7 for content provider com.google.android.gsf/.gservices.GservicesProvider
01-25 13:05:34.858 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.862 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration mccmnc='310260' fromServiceState=false
01-25 13:05:34.865 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration defaultMccMnc=310260
01-25 13:05:34.865 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration: mcc=310, mnc=260
01-25 13:05:34.865 1870-1870/com.android.phone D/MccTable: updateMccMncConfiguration updateConfig config={1.0 310mcc260mnc ?locale ?layoutDir ?swdp ?wdp ?hdp ?density ?lsize ?long ?orien ?uimode ?night ?touch ?keyb/?/? ?nav/?}
                                                           
                                                           [ 01-25 13:05:34.877  1633: 2068 D/         ]
                                                           HostConnection::get() New Host Connection established 0xa3479410, tid 2068
01-25 13:05:34.881 1633-2068/com.android.systemui I/OpenGLRenderer: Initialized EGL, version 1.4
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is available: 310260
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: Reset GPS properties, previous size = 5
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_HOST=supl.google.com
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_PORT=7275
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: NTP_SERVER=north-america.pool.ntp.org
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_VER=0x20000
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_MODE=1
01-25 13:05:34.911 1538-1553/system_process W/GpsLocationProvider: Could not open GPS configuration file /etc/gps.conf
01-25 13:05:34.911 1538-1553/system_process D/GpsLocationProvider: GPS properties reloaded, size = 5
01-25 13:05:34.911 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:34.915 2091-2091/? W/System: ClassLoader referenced unknown path: /system/priv-app/GoogleServicesFramework/lib/x86
01-25 13:05:34.934 1633-2068/com.android.systemui W/EGL_emulation: eglSurfaceAttrib not implemented
01-25 13:05:34.934 1633-2068/com.android.systemui W/OpenGLRenderer: Failed to set EGL_SWAP_BEHAVIOR on surface 0xa1af3340, error=EGL_SUCCESS
01-25 13:05:34.958 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:34.966 1633-2068/com.android.systemui W/EGL_emulation: eglSurfaceAttrib not implemented
01-25 13:05:34.966 1633-2068/com.android.systemui W/OpenGLRenderer: Failed to set EGL_SWAP_BEHAVIOR on surface 0xa1af3380, error=EGL_SUCCESS
01-25 13:05:34.977 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:34.979 2091-2091/? I/GservicesProvider: Gservices pushing to system: true; secure/global: true
01-25 13:05:34.982 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is available: 310260
01-25 13:05:34.982 1538-1553/system_process D/GpsLocationProvider: Reset GPS properties, previous size = 5
01-25 13:05:34.983 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_HOST=supl.google.com
01-25 13:05:34.983 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_PORT=7275
01-25 13:05:34.983 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: NTP_SERVER=north-america.pool.ntp.org
01-25 13:05:34.984 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_VER=0x20000
01-25 13:05:34.984 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_MODE=1
01-25 13:05:34.984 1538-1553/system_process W/GpsLocationProvider: Could not open GPS configuration file /etc/gps.conf
01-25 13:05:34.984 1538-1553/system_process D/GpsLocationProvider: GPS properties reloaded, size = 5
01-25 13:05:34.984 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:35.000 1870-1870/com.android.phone D/CarrierConfigLoader: update config for phoneId: 0 simState: LOADED
01-25 13:05:35.000 1870-1870/com.android.phone D/CarrierServiceBindHelper: update binding for phoneId: 0 simState: LOADED
01-25 13:05:35.000 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:35.006 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.009 1870-1870/com.android.phone I/Telephony: AccountEntry: updateVideoPauseSupport -- mcc/mnc for sub: {id=1, iccId=89014103211118510720 simSlotIndex=0 displayName=Android carrierName=Android nameSource=0 iconTint=-16746133 dataRoaming=0 iconBitmap=android.graphics.Bitmap@f1d87d4 mcc 310 mnc 260}
01-25 13:05:35.010 1538-1927/system_process I/Telecom: PhoneAccountRegistrar: New phone account registered: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ]
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is available: 310260
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: Reset GPS properties, previous size = 5
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_HOST=supl.google.com
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_PORT=7275
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: NTP_SERVER=north-america.pool.ntp.org
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_VER=0x20000
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_MODE=1
01-25 13:05:35.042 1538-1553/system_process W/GpsLocationProvider: Could not open GPS configuration file /etc/gps.conf
01-25 13:05:35.042 1538-1553/system_process D/GpsLocationProvider: GPS properties reloaded, size = 5
01-25 13:05:35.042 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:35.051 1538-1927/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.052 2091-2091/? I/GoogleHttpClient: GMS http client unavailable, use old client
01-25 13:05:35.055 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}
01-25 13:05:35.055 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.058 1870-1870/com.android.phone I/Telephony: TelecomAccountRegistry: Unregistering phone account ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e0184adedf913b076626646d3f52c3b49c39ad6d], UserHandle{0}.
01-25 13:05:35.062 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:35.066 1891-1891/com.google.android.googlequicksearchbox V/Launcher: LauncherAppState inited
01-25 13:05:35.075 1538-1927/system_process W/Telecom: : No account found for the calling user
01-25 13:05:35.080 1948-2010/android.process.acore I/ContactLocale: AddressBook Labels [en-US]: [, A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z, Α, Β, Γ, Δ, Ε, Ζ, Η, Θ, Ι, Κ, Λ, Μ, Ν, Ξ, Ο, Π, Ρ, Σ, Τ, Υ, Φ, Χ, Ψ, Ω, , А, Б, В, Г, Д, Ђ, Е, Є, Ж, З, И, І, Й, Ј, К, Л, Љ, М, Н, Њ, О, П, Р, С, Т, Ћ, У, Ф, Х, Ц, Ч, Џ, Ш, Щ, Ю, Я, , א, ב, ג, ד, ה, ו, ז, ח, ט, י, כ, ל, מ, נ, ס, ע, פ, צ, ק, ר, ש, ת, , ا, ب, ت, ث, ج, ح, خ, د, ذ, ر, ز, س, ش, ص, ض, ط, ظ, ع, غ, ف, ق, ك, ل, م, ن, ه, و, ي, , ก, ข, ฃ, ค, ฅ, ฆ, ง, จ, ฉ, ช, ซ, ฌ, ญ, ฎ, ฏ, ฐ, ฑ, ฒ, ณ, ด, ต, ถ, ท, ธ, น, บ, ป, ผ, ฝ, พ, ฟ, ภ, ม, ย, ร, ฤ, ล, ฦ, ว, ศ, ษ, ส, ห, ฬ, อ, ฮ, , ㄱ, ㄴ, ㄷ, ㄹ, ㅁ, ㅂ, ㅅ, ㅇ, ㅈ, ㅊ, ㅋ, ㅌ, ㅍ, ㅎ, , あ, か, さ, た, な, は, ま, や, ら, わ, #, ]
01-25 13:05:35.144 1633-1633/com.android.systemui W/KeyguardUpdateMonitor: invalid subId in handleSimStateChange()
01-25 13:05:35.145 1891-1891/com.google.android.googlequicksearchbox D/Launcher.Model: Old launcher provider: content://com.google.android.launcher.oldhome.settings/favorites?notify=true
01-25 13:05:35.145 1891-1891/com.google.android.googlequicksearchbox D/Launcher.Model: Old launcher provider does not exist.
01-25 13:05:35.204 1861-1861/com.google.android.gms.persistent W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:35.205 1861-1861/com.google.android.gms.persistent W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:35.213 1633-1633/com.android.systemui W/KeyguardUpdateMonitor: invalid subId in handleServiceStateChange()
01-25 13:05:35.226 1861-1861/com.google.android.gms.persistent W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:35.227 1861-1861/com.google.android.gms.persistent W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:35.243 1538-1551/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:35.244 1633-1633/com.android.systemui I/Choreographer: Skipped 31 frames!  The application may be doing too much work on its main thread.
01-25 13:05:35.301 2072-2120/? E/ActivityThread: Failed to find provider info for com.google.android.partnersetup.rlzappprovider
01-25 13:05:35.344 1633-1633/com.android.systemui W/KeyguardUpdateMonitor: invalid subId in handleServiceStateChange()
01-25 13:05:35.344 1633-1633/com.android.systemui W/KeyguardUpdateMonitor: invalid subId in handleSimStateChange()
01-25 13:05:35.345 1633-1633/com.android.systemui W/KeyguardUpdateMonitor: invalid subId in handleSimStateChange()
01-25 13:05:35.474 1861-1861/com.google.android.gms.persistent V/JNIHelp: Registering com/google/android/gms/org/conscrypt/NativeCrypto's 254 native methods...
01-25 13:05:35.484 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:35.498 1861-1882/com.google.android.gms.persistent I/art: Background sticky concurrent mark sweep GC freed 16898(1229KB) AllocSpace objects, 2(40KB) LOS objects, 8% free, 3MB/3MB, paused 9.064ms total 242.404ms
01-25 13:05:35.546 1833-1833/com.google.android.googlequicksearchbox:interactor W/KeyphraseEnrollmentInfo: Enrollment application doesn't support keyphrases
01-25 13:05:35.558 1848-1999/com.android.inputmethod.latin I/LatinIME:LogUtils: Dictionary info: dictionary = userunigram.en_US ; version = 1516885535 ; date = ?
01-25 13:05:35.572 1848-1999/com.android.inputmethod.latin I/LatinIME:LogUtils: Dictionary info: dictionary = UserHistoryDictionary.en_US ; version = 1516885535 ; date = ?
01-25 13:05:35.593 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is available: 310260
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: Reset GPS properties, previous size = 5
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_HOST=supl.google.com
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_PORT=7275
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: NTP_SERVER=north-america.pool.ntp.org
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_VER=0x20000
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_MODE=1
01-25 13:05:35.597 1538-1553/system_process W/GpsLocationProvider: Could not open GPS configuration file /etc/gps.conf
01-25 13:05:35.597 1538-1553/system_process D/GpsLocationProvider: GPS properties reloaded, size = 5
01-25 13:05:35.597 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:35.609 1861-1882/com.google.android.gms.persistent I/art: Background partial concurrent mark sweep GC freed 3908(235KB) AllocSpace objects, 0(0B) LOS objects, 39% free, 3MB/5MB, paused 274us total 109.982ms
01-25 13:05:35.626 1538-1553/system_process D/GpsLocationProvider: received SIM related action: 
01-25 13:05:35.627 1538-1553/system_process D/GpsLocationProvider: SIM MCC/MNC is available: 310260
01-25 13:05:35.627 1538-1553/system_process D/GpsLocationProvider: Reset GPS properties, previous size = 5
01-25 13:05:35.631 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_HOST=supl.google.com
01-25 13:05:35.631 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_PORT=7275
01-25 13:05:35.631 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: NTP_SERVER=north-america.pool.ntp.org
01-25 13:05:35.631 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_VER=0x20000
01-25 13:05:35.631 1538-1553/system_process D/GpsLocationProvider: GpsParamsResource: SUPL_MODE=1
01-25 13:05:35.631 1538-1553/system_process W/GpsLocationProvider: Could not open GPS configuration file /etc/gps.conf
01-25 13:05:35.632 1538-1553/system_process D/GpsLocationProvider: GPS properties reloaded, size = 5
01-25 13:05:35.632 1538-1553/system_process E/GpsLocationProvider: no AGPS interface in set_agps_server
01-25 13:05:35.639 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.646 1870-1870/com.android.phone I/Telephony: AccountEntry: updateVideoPauseSupport -- mcc/mnc for sub: {id=1, iccId=89014103211118510720 simSlotIndex=0 displayName=Android carrierName=Android nameSource=0 iconTint=-16746133 dataRoaming=0 iconBitmap=android.graphics.Bitmap@75dfca3 mcc 310 mnc 260}
01-25 13:05:35.647 1538-1552/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:35.647 1848-1999/com.android.inputmethod.latin I/LatinIME:LogUtils: Dictionary info: dictionary = main:en ; version = 54 ; date = 1414726273
01-25 13:05:35.668 1538-1552/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.669 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}
01-25 13:05:35.669 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.673 1861-1861/com.google.android.gms.persistent I/ProviderInstaller: Installed default security provider GmsCore_OpenSSL
01-25 13:05:35.681 1538-1904/system_process W/Telecom: : No account found for the calling user
01-25 13:05:35.710 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.719 1870-1870/com.android.phone I/Telephony: AccountEntry: updateVideoPauseSupport -- mcc/mnc for sub: {id=1, iccId=89014103211118510720 simSlotIndex=0 displayName=Android carrierName=Android nameSource=0 iconTint=-16746133 dataRoaming=0 iconBitmap=android.graphics.Bitmap@b2b2b2a mcc 310 mnc 260}
01-25 13:05:35.720 1538-1892/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:35.739 1538-1892/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.742 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}
01-25 13:05:35.742 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.744 1538-1927/system_process W/Telecom: : No account found for the calling user
01-25 13:05:35.744 1870-1870/com.android.phone D/CarrierConfigLoader: mHandler: 7 phoneId: 0
01-25 13:05:35.745 1870-1870/com.android.phone E/CarrierConfigLoader: Failed to get package version for: com.android.carrierconfig
01-25 13:05:35.745 1870-1870/com.android.phone D/CarrierConfigLoader: Binding to com.android.carrierconfig for phone 0
01-25 13:05:35.746 1538-1551/system_process W/ActivityManager: Unable to start service Intent { act=android.service.carrier.CarrierService pkg=com.android.carrierconfig } U=0: not found
01-25 13:05:35.747 1538-1538/system_process I/Telecom: PhoneAccountRegistrar: SimCallManager queried, returning: null
01-25 13:05:35.747 1870-1870/com.android.phone D/CarrierServiceBindHelper: mHandler: 0
01-25 13:05:35.747 1870-1870/com.android.phone D/CarrierServiceBindHelper: Binding to phoneId: 0
01-25 13:05:35.747 1870-1870/com.android.phone D/CarrierServiceBindHelper: No carrier app for: 0
01-25 13:05:35.750 1538-1648/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:35.751 1891-2116/com.google.android.googlequicksearchbox W/Launcher: setApplicationContext called twice! old=com.google.android.velvet.VelvetApplication@3bfe106 new=com.google.android.velvet.VelvetApplication@3bfe106
01-25 13:05:35.759 1538-1648/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.803 1891-1891/com.google.android.googlequicksearchbox I/GEL: handleIntent(Intent { act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10000000 cmp=com.google.android.googlequicksearchbox/com.google.android.launcher.GEL })
01-25 13:05:35.807 1861-2138/com.google.android.gms.persistent D/NativeLibraryUtils: Install completed successfully. count=13 extracted=0
01-25 13:05:35.824 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.831 1538-1648/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:35.847 1870-1870/com.android.phone I/Telephony: AccountEntry: updateVideoPauseSupport -- mcc/mnc for sub: {id=1, iccId=89014103211118510720 simSlotIndex=0 displayName=Android carrierName=Android nameSource=0 iconTint=-16746133 dataRoaming=0 iconBitmap=android.graphics.Bitmap@335d8cd mcc 310 mnc 260}
01-25 13:05:35.851 1186-1265/? E/SurfaceFlinger: ro.sf.lcd_density must be defined as a build property
01-25 13:05:35.854 1891-2151/com.google.android.googlequicksearchbox D/OpenGLRenderer: Use EGL_SWAP_BEHAVIOR_PRESERVED: true
01-25 13:05:35.856 1538-1648/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
                                                       
                                                       [ 01-25 13:05:35.862  1891: 1891 D/         ]
                                                       HostConnection::get() New Host Connection established 0xacbedee0, tid 1891
01-25 13:05:35.874 1538-1648/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.875 1891-1891/com.google.android.googlequicksearchbox W/SearchServiceClient: Attempt to handover from detached client
01-25 13:05:35.875 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}
01-25 13:05:35.875 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.877 1538-1904/system_process W/Telecom: : No account found for the calling user
01-25 13:05:35.882 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Unregistering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.885 1870-1870/com.android.phone I/Telephony: AccountEntry: updateVideoPauseSupport -- mcc/mnc for sub: {id=1, iccId=89014103211118510720 simSlotIndex=0 displayName=Android carrierName=Android nameSource=0 iconTint=-16746133 dataRoaming=0 iconBitmap=android.graphics.Bitmap@558a6ef mcc 310 mnc 260}
01-25 13:05:35.885 1538-1892/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:35.892 1538-1892/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.893 1870-1870/com.android.phone I/Telephony: AccountEntry: Registered phoneAccount: [[ ] PhoneAccount: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0} Capabilities: 54 Schemes: tel voicemail ] with handle: ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}
01-25 13:05:35.893 1870-1870/com.android.phone I/Telephony: PstnIncomingCallNotifier: Registering: Handler (com.android.internal.telephony.gsm.GSMPhone) {a38c1fa}
01-25 13:05:35.908 1891-1891/com.google.android.googlequicksearchbox W/Launcher: setApplicationContext called twice! old=com.google.android.velvet.VelvetApplication@3bfe106 new=com.google.android.velvet.VelvetApplication@3bfe106
01-25 13:05:35.912 1538-1648/system_process W/Telecom: : No account found for the calling user
01-25 13:05:35.913 1870-1870/com.android.phone I/NotificationMgr: updateMwi(): subId 1 update to false
01-25 13:05:35.917 1538-1538/system_process V/BackupManagerService: Connected to transport ComponentInfo{com.google.android.gms/com.google.android.gms.backup.BackupTransportService}
01-25 13:05:35.918 2072-2072/com.google.android.googlequicksearchbox:search W/TRUiThreadExecutor: Task does not implement UiTask: com.google.common.g.a.p@84406b9
01-25 13:05:35.918 1538-1538/system_process V/BackupManagerService: Registering transport com.google.android.gms/.backup.BackupTransportService::com.google.android.gms/.backup.BackupTransportService = com.android.internal.backup.IBackupTransport$Stub$Proxy@b1791ff
01-25 13:05:35.919 1538-1992/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:35.928 1538-1992/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:35.948 1891-1891/com.google.android.googlequicksearchbox I/GEL: handleIntent(Intent { act=android.intent.action.MAIN cat=[android.intent.category.HOME] flg=0x10000000 cmp=com.google.android.googlequicksearchbox/com.google.android.launcher.GEL })
01-25 13:05:35.983 1538-2069/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:35.984 1538-1927/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:35.996 1538-1927/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:36.004 1538-1648/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:36.045 1538-1648/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:36.049 1861-1861/com.google.android.gms.persistent I/GCoreNlp: shouldConfirmNlp, NLP off. Ensuring opt-in disabled
01-25 13:05:36.059 1538-1552/system_process I/Telecom: PhoneAccountRegistrar: [ComponentInfo{com.android.phone/com.android.services.telephony.TelephonyConnectionService}, [e2f7d48dd2b5ca523e7313cf4ba0f6ea830b6281], UserHandle{0}(icon: Icon(typ=BITMAP size=57x72) -> Icon(typ=BITMAP size=57x72))]
01-25 13:05:36.068 1538-1552/system_process I/Telecom: : Sending phone-account intent as user
01-25 13:05:36.075 1870-1870/com.android.phone D/TelephonyProvider: subIdString = 1 subId = 1
                                                                    
                                                                    [ 01-25 13:05:36.115  1891: 2151 D/         ]
                                                                    HostConnection::get() New Host Connection established 0xaec52b40, tid 2151
01-25 13:05:36.124 1891-2151/com.google.android.googlequicksearchbox I/OpenGLRenderer: Initialized EGL, version 1.4
                                                                                       
                                                                                       [ 01-25 13:05:36.162  1186: 2125 D/         ]
                                                                                       HostConnection::get() New Host Connection established 0xb673e690, tid 2125
01-25 13:05:36.208 1538-1927/system_process D/ConnectivityService: registerNetworkAgent NetworkAgentInfo{ ni{[type: MOBILE[UMTS], state: CONNECTED/CONNECTED, reason: connected, extra: epc.tmobile.com, roaming: false, failover: false, isAvailable: true]}  network{100}  lp{{InterfaceName: eth0 LinkAddresses: [10.0.2.15/32,]  Routes: [0.0.0.0/0 -> 10.0.2.2 eth0,] DnsAddresses: [10.0.2.3,] Domains: null MTU: 1500 TcpBufferSizes: 58254,349525,1048576,58254,349525,1048576}}  nc{[ Transports: CELLULAR Capabilities: MMS&SUPL&FOTA&IMS&CBS&IA&INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN LinkUpBandwidth>=384Kbps LinkDnBandwidth>=384Kbps Specifier: <1>]}  Score{10}  everValidated{false}  lastValidated{false}  created{false} lingering{false} explicitlySelected{false} acceptUnvalidated{false} everCaptivePortalDetected{false} lastCaptivePortalDetected{false} }
01-25 13:05:36.208 1538-1599/system_process D/ConnectivityService: NetworkAgentInfo [MOBILE (UMTS) - 100] EVENT_NETWORK_INFO_CHANGED, going from null to CONNECTED
01-25 13:05:36.212 1538-1599/system_process D/ConnectivityService: Adding iface eth0 to network 100
01-25 13:05:36.216 1891-2151/com.google.android.googlequicksearchbox W/EGL_emulation: eglSurfaceAttrib not implemented
01-25 13:05:36.216 1891-2151/com.google.android.googlequicksearchbox W/OpenGLRenderer: Failed to set EGL_SWAP_BEHAVIOR on surface 0xab3250e0, error=EGL_SUCCESS
                                                                                       
                                                                                       [ 01-25 13:05:36.242  1186: 1910 D/         ]
                                                                                       HostConnection::get() New Host Connection established 0xb673e560, tid 1910
01-25 13:05:36.320 1538-1904/system_process D/ConnectivityService: setProvNotificationVisible: E visible=false networkType=0 action=com.android.internal.telephony.PROVISION0
01-25 13:05:36.320 1538-1904/system_process D/ConnectivityService: setProvNotificationVisibleIntent SIGN_IN visible=false networkType=MOBILE extraInfo=null highPriority=false
01-25 13:05:36.334 1538-1559/system_process W/WindowManager: App freeze timeout expired.
01-25 13:05:36.334 1538-1559/system_process W/WindowManager: Force clearing freeze: AppWindowToken{ce20eaf token=Token{399168e ActivityRecord{2fe689 u0 com.google.android.googlequicksearchbox/com.google.android.launcher.GEL t54}}}
01-25 13:05:36.334 1538-1559/system_process I/WindowManager: Screen frozen for +2s71ms due to AppWindowToken{ce20eaf token=Token{399168e ActivityRecord{2fe689 u0 com.google.android.googlequicksearchbox/com.google.android.launcher.GEL t54}}}
01-25 13:05:36.336 1538-1599/system_process D/ConnectivityService: Setting MTU size: eth0, 1500
01-25 13:05:36.338 1538-1599/system_process D/ConnectivityService: Adding Route [0.0.0.0/0 -> 10.0.2.2 eth0] to network 100
01-25 13:05:36.360 1538-1599/system_process D/ConnectivityService: Setting Dns servers for network 100 to [/10.0.2.3]
01-25 13:05:36.413 1538-1599/system_process D/ConnectivityService: notifyType IP_CHANGED for NetworkAgentInfo [MOBILE (UMTS) - 100]
01-25 13:05:36.417 1538-1599/system_process D/ConnectivityService: scheduleUnvalidatedPrompt 100
01-25 13:05:36.417 1538-1599/system_process D/ConnectivityService: rematching NetworkAgentInfo [MOBILE (UMTS) - 100]
01-25 13:05:36.417 1538-1599/system_process D/ConnectivityService:    accepting network in place of null
01-25 13:05:36.427 1538-1599/system_process D/ConnectivityService: Switching to new default network: NetworkAgentInfo{ ni{[type: MOBILE[UMTS], state: CONNECTED/CONNECTED, reason: connected, extra: epc.tmobile.com, roaming: false, failover: false, isAvailable: true]}  network{100}  lp{{InterfaceName: eth0 LinkAddresses: [10.0.2.15/32,]  Routes: [0.0.0.0/0 -> 10.0.2.2 eth0,] DnsAddresses: [10.0.2.3,] Domains: null MTU: 1500 TcpBufferSizes: 58254,349525,1048576,58254,349525,1048576}}  nc{[ Transports: CELLULAR Capabilities: MMS&SUPL&FOTA&IMS&CBS&IA&INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN LinkUpBandwidth>=384Kbps LinkDnBandwidth>=384Kbps Specifier: <1>]}  Score{10}  everValidated{false}  lastValidated{false}  created{true} lingering{false} explicitlySelected{false} acceptUnvalidated{false} everCaptivePortalDetected{false} lastCaptivePortalDetected{false} }
01-25 13:05:36.456 1538-1927/system_process I/ActivityManager: Start proc 2167:com.google.android.gms/u0a7 for service com.google.android.gms/.usagereporting.service.UsageReportingService
01-25 13:05:36.505 1538-1559/system_process I/ActivityManager: Displayed com.google.android.googlequicksearchbox/com.google.android.launcher.GEL: +3s584ms
01-25 13:05:36.535 1192-1534/? V/IdletimerController: runCmd(/system/bin/ip6tables -w -t raw -A idletimer_raw_PREROUTING -i eth0 -j IDLETIMER --timeout 10 --label 0 --send_nl_msg 1) res_ipv4=0, res_ipv6=0
01-25 13:05:36.561 1538-2161/system_process D/NetworkMonitor/NetworkAgentInfo [MOBILE (UMTS) - 100]: Checking http://connectivitycheck.gstatic.com/generate_204 on epc.tmobile.com, connectivitycheck.gstatic.com=203.208.43.95,2401:3800:4001:807::100f
01-25 13:05:36.607 1192-1534/? V/IdletimerController: runCmd(/system/bin/ip6tables -w -t mangle -A idletimer_mangle_POSTROUTING -o eth0 -j IDLETIMER --timeout 10 --label 0 --send_nl_msg 1) res_ipv4=0, res_ipv6=0
01-25 13:05:36.632 2167-2167/com.google.android.gms W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:36.651 1538-1599/system_process D/ConnectivityService: Setting tx/rx TCP buffers to 58254,349525,1048576,58254,349525,1048576
01-25 13:05:36.655 1538-1599/system_process D/CSLegacyTypeTracker: Sending CONNECTED broadcast for type 0 NetworkAgentInfo [MOBILE (UMTS) - 100] isDefaultNetwork=true
01-25 13:05:36.655 1538-1599/system_process D/ConnectivityService: sendStickyBroadcast: action=android.net.conn.CONNECTIVITY_CHANGE
01-25 13:05:36.658 1538-1599/system_process D/ConnectivityService: notifyType PRECHECK for NetworkAgentInfo [MOBILE (UMTS) - 100]
01-25 13:05:36.658 1538-1554/system_process V/KeyguardServiceDelegate: *** Keyguard started
01-25 13:05:36.661 1633-2052/com.android.systemui D/ConnectivityManager.CallbackHandler: CM callback handler got msg 524290
01-25 13:05:36.668 1538-1554/system_process W/KeyguardServiceDelegate: onScreenTurningOn(): no keyguard service!
01-25 13:05:36.668 1538-1558/system_process D/Tethering: MasterInitialState.processMessage what=3
01-25 13:05:36.676 1538-1538/system_process V/KeyguardServiceDelegate: *** Keyguard connected (yay!)
01-25 13:05:36.678 1633-2052/com.android.systemui D/ConnectivityManager.CallbackHandler: CM callback handler got msg 524289
01-25 13:05:36.681 2167-2167/com.google.android.gms I/MultiDex: VM with version 2.1.0 has multidex support
01-25 13:05:36.681 2167-2167/com.google.android.gms I/MultiDex: install
01-25 13:05:36.681 2167-2167/com.google.android.gms I/MultiDex: VM has multidex support, MultiDex support library is disabled.
01-25 13:05:36.694 1538-1551/system_process V/KeyguardServiceDelegate: **** SHOWN CALLED ****
01-25 13:05:36.732 1633-1633/com.android.systemui D/PhoneStatusBar: disable: < expand* icons alerts system_info back* home* recent* clock search* quick_settings >
01-25 13:05:36.741 1538-2161/system_process D/NetworkMonitor/NetworkAgentInfo [MOBILE (UMTS) - 100]: isCaptivePortal: ret=204 headers={null=[HTTP/1.1 204 No Content], Content-Length=[0], Date=[Thu, 25 Jan 2018 13:05:34 GMT], X-Android-Received-Millis=[1516885536733], X-Android-Response-Source=[NETWORK 204], X-Android-Selected-Protocol=[http/1.1], X-Android-Sent-Millis=[1516885536630]}
                                                                                                     
                                                                                                     [ 01-25 13:05:36.744  1538: 1559 D/         ]
                                                                                                     HostConnection::get() New Host Connection established 0x9daaa5a0, tid 1559
01-25 13:05:36.745 1538-1599/system_process D/ConnectivityService: setProvNotificationVisibleIntent null visible=false networkType=MOBILE extraInfo=null highPriority=false
01-25 13:05:36.745 1538-1599/system_process D/ConnectivityService: NetworkAgentInfo [MOBILE (UMTS) - 100] validation  passed
01-25 13:05:36.745 1538-1599/system_process D/ConnectivityService: rematching NetworkAgentInfo [MOBILE (UMTS) - 100]
01-25 13:05:36.745 1538-1599/system_process D/ConnectivityService: notifyType CAP_CHANGED for NetworkAgentInfo [MOBILE (UMTS) - 100]
01-25 13:05:36.745 1538-1599/system_process D/ConnectivityService: sendStickyBroadcast: action=android.net.conn.INET_CONDITION_ACTION
01-25 13:05:36.746 1633-2052/com.android.systemui D/ConnectivityManager.CallbackHandler: CM callback handler got msg 524294
01-25 13:05:36.758 1186-2125/? I/SurfaceFlinger: Boot is finished (12043 ms)
01-25 13:05:36.766 1891-2151/com.google.android.googlequicksearchbox V/RenderScript: 0xa0c3c000 Launching thread(s), CPUs 2
01-25 13:05:36.769 1538-1548/system_process I/art: Background sticky concurrent mark sweep GC freed 13049(1634KB) AllocSpace objects, 4(80KB) LOS objects, 10% free, 14MB/15MB, paused 3.030ms total 114.499ms
01-25 13:05:36.802 1306-1331/? E/Surface: getSlotFromBufferLocked: unknown buffer: 0xb61b1000
01-25 13:05:37.179 1538-1559/system_process I/SystemServiceManager: Starting phase 1000
01-25 13:05:37.195 1891-2116/com.google.android.googlequicksearchbox D/WidgetsModel: com.google.android.googlequicksearchbox is filtered and not added to the widget tray.
01-25 13:05:37.291 1538-1593/system_process E/NetdConnector: NDC Command {23 bandwidth setiquota eth0 9223372036854775807} took too long (607ms)
01-25 13:05:37.351 1861-1861/com.google.android.gms.persistent I/GCoreNlp: shouldConfirmNlp, NLP off. Ensuring opt-in disabled
01-25 13:05:37.373 1538-2069/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:37.391 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:37.423 1861-1861/com.google.android.gms.persistent W/GmsBackupAccountManager: Backup account not found in gmscore.
01-25 13:05:37.442 2167-2167/com.google.android.gms W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:37.442 2167-2167/com.google.android.gms W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:37.448 2167-2167/com.google.android.gms W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:37.449 2167-2167/com.google.android.gms W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:37.457 1861-1861/com.google.android.gms.persistent I/GCoreNlp: shouldConfirmNlp, NLP off. Ensuring opt-in disabled
01-25 13:05:37.472 2167-2167/com.google.android.gms V/JNIHelp: Registering com/google/android/gms/org/conscrypt/NativeCrypto's 254 native methods...
01-25 13:05:37.481 2167-2167/com.google.android.gms I/ProviderInstaller: Installed default security provider GmsCore_OpenSSL
01-25 13:05:37.491 1861-2221/com.google.android.gms.persistent I/Backup: [BackupTransportMigratorService] Starting migration...
01-25 13:05:37.493 1861-2221/com.google.android.gms.persistent E/Backup: [LegacyBackupAccountManager] Fail to get legacy transport context.
                                                                         android.content.pm.PackageManager$NameNotFoundException: Application package com.google.android.backup not found
                                                                             at android.app.ContextImpl.createPackageContextAsUser(ContextImpl.java:1703)
                                                                             at android.app.ContextImpl.createPackageContext(ContextImpl.java:1679)
                                                                             at android.content.ContextWrapper.createPackageContext(ContextWrapper.java:746)
                                                                             at android.content.ContextWrapper.createPackageContext(ContextWrapper.java:746)
                                                                             at com.google.android.gms.backup.as.<init>(SourceFile:47)
                                                                             at com.google.android.gms.backup.BackupTransportMigratorService.a(SourceFile:150)
                                                                             at com.google.android.gms.backup.BackupTransportMigratorService.onHandleIntent(SourceFile:82)
                                                                             at android.app.IntentService$ServiceHandler.handleMessage(IntentService.java:66)
                                                                             at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                             at android.os.Looper.loop(Looper.java:148)
                                                                             at android.os.HandlerThread.run(HandlerThread.java:61)
01-25 13:05:37.494 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:37.494 1861-2221/com.google.android.gms.persistent W/Backup: [LegacyBackupAccountManager] No google accounts found!
01-25 13:05:37.506 2167-2223/com.google.android.gms D/NativeLibraryUtils: Install completed successfully. count=13 extracted=0
01-25 13:05:37.693 2228-2228/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:37.694 2228-2228/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:37.706 2228-2228/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:37.720 1861-1861/com.google.android.gms.persistent D/GeofencerStateMachine: Creating GeofencerStateMachine
01-25 13:05:37.731 2228-2228/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:37.731 2228-2228/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:37.732 2228-2228/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:37.741 2228-2228/? D/AndroidRuntime: Calling main entry com.android.commands.wm.Wm
01-25 13:05:37.743 2228-2228/? D/AndroidRuntime: Shutting down VM
01-25 13:05:37.746 2228-2240/? E/art: Thread attaching while runtime is shutting down: Binder_1
01-25 13:05:37.746 2228-2240/? I/AndroidRuntime: NOTE: attach of thread 'Binder_1' failed
01-25 13:05:37.761 2230-2230/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:37.762 2230-2230/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:37.764 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:37.775 2230-2230/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:37.797 2230-2230/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:37.797 2230-2230/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:37.798 2230-2230/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:37.805 2230-2230/? D/AndroidRuntime: Calling main entry com.android.commands.wm.Wm
01-25 13:05:37.806 2230-2230/? D/AndroidRuntime: Shutting down VM
01-25 13:05:37.811 2230-2248/? E/art: Thread attaching while runtime is shutting down: Binder_1
01-25 13:05:37.811 2230-2248/? I/AndroidRuntime: NOTE: attach of thread 'Binder_1' failed
01-25 13:05:37.883 2233-2233/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:37.886 2233-2233/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:37.896 2233-2233/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:37.910 2233-2233/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:37.910 2233-2233/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:37.912 2233-2233/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:37.921 2233-2233/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:37.931 2233-2233/? I/art: System.exit called, status: 0
01-25 13:05:37.931 2233-2233/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:37.940 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Starting service, intent=Intent { act=com.google.android.location.reporting.ACTION_UPDATE_WORLD cmp=com.google.android.gms/com.google.android.location.reporting.service.DispatchingService (has extras) }, extras=Bundle[{receiverAction=android.location.PROVIDERS_CHANGED}]
01-25 13:05:37.954 1538-1551/system_process I/ActivityManager: Start proc 2260:com.google.android.apps.maps/u0a38 for broadcast com.google.android.apps.maps/com.google.android.apps.gmm.iamhere.ble.StartBleServiceReceiver
01-25 13:05:37.982 2260-2260/com.google.android.apps.maps W/System: ClassLoader referenced unknown path: /system/app/Maps/lib/x86
01-25 13:05:38.107 2273-2273/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:38.107 2273-2273/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:38.117 2273-2273/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:38.134 2273-2273/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:38.134 2273-2273/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:38.135 2273-2273/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:38.141 2273-2273/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:38.148 1198-1198/? I/installd: free_cache(67714) avail 665190400
01-25 13:05:38.171 1861-1861/com.google.android.gms.persistent V/GeofencerHelper: Initializing geofence's system cache.
01-25 13:05:38.176 2273-2273/? I/art: System.exit called, status: 0
01-25 13:05:38.176 2273-2273/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:38.228 1861-2286/com.google.android.gms.persistent E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:38.346 2288-2288/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:38.348 2288-2288/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:38.358 2288-2288/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:38.363 1538-1559/system_process I/art: Starting a blocking GC Explicit
01-25 13:05:38.381 1538-1559/system_process I/art: Explicit concurrent mark sweep GC freed 12852(991KB) AllocSpace objects, 16(7MB) LOS objects, 33% free, 6MB/10MB, paused 1.446ms total 17.754ms
01-25 13:05:38.381 1538-1548/system_process I/art: WaitForGcToComplete blocked for 16.156ms for cause HeapTrim
01-25 13:05:38.395 2288-2288/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:38.395 2288-2288/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:38.396 2288-2288/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:38.406 2288-2288/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:38.414 1198-1198/? I/installd: free_cache(507654) avail 665116672
01-25 13:05:38.516 1861-1882/com.google.android.gms.persistent W/art: Suspending all threads took: 89.207ms
01-25 13:05:38.532 2288-2288/? I/art: System.exit called, status: 0
01-25 13:05:38.532 2288-2288/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:38.655 1861-1882/com.google.android.gms.persistent I/art: Background sticky concurrent mark sweep GC freed 3523(360KB) AllocSpace objects, 6(120KB) LOS objects, 5% free, 5MB/5MB, paused 227.652ms total 475.469ms
01-25 13:05:38.676 1538-1597/system_process D/WifiNative-HAL: Failing getSupportedFeatureset because HAL isn't started
01-25 13:05:38.703 2300-2300/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:38.704 2300-2300/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:38.707 1861-1861/com.google.android.gms.persistent I/GCoreUlr: DispatchingService.onCreate()
01-25 13:05:38.720 2300-2300/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:38.741 2300-2300/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:38.741 2300-2300/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:38.742 2300-2300/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:38.752 2300-2300/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:38.756 1198-1198/? I/installd: free_cache(4256) avail 664629248
01-25 13:05:38.766 2300-2300/? I/art: System.exit called, status: 0
01-25 13:05:38.766 2300-2300/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:38.796 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:38.886 1861-1861/com.google.android.gms.persistent W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:38.886 1861-1861/com.google.android.gms.persistent W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:38.924 1861-2221/com.google.android.gms.persistent W/GmsBackupAccountManager: Backup account not found in gmscore.
01-25 13:05:38.942 2319-2319/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:38.943 2319-2319/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:38.950 1861-2221/com.google.android.gms.persistent I/Backup: [BackupTransportMigratorService] Component name not found : com.google.android.backuptransport/com.google.android.backup.BackupTransportService
01-25 13:05:38.954 1861-2242/com.google.android.gms.persistent D/GeofenceStateCache: Recovered 0 geofences.
01-25 13:05:38.954 1861-2221/com.google.android.gms.persistent I/Backup: [BackupTransportMigratorService] Component name not found : com.google.android.backup/com.google.android.backup.BackupTransportService
01-25 13:05:38.954 1861-2221/com.google.android.gms.persistent I/Backup: [BackupTransportMigratorService] Successfully migrated to use GMS BackupTransportService!
01-25 13:05:38.965 2319-2319/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:38.982 2319-2319/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:38.982 2319-2319/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:38.984 2319-2319/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:38.992 2319-2319/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:38.996 1198-1198/? I/installd: free_cache(29133) avail 664616960
01-25 13:05:39.004 2319-2319/? I/art: System.exit called, status: 0
01-25 13:05:39.004 2319-2319/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:39.096 1861-2324/com.google.android.gms.persistent I/GCoreUlr: WorldUpdater received intent Intent { act=com.google.android.location.reporting.ACTION_UPDATE_WORLD cmp=com.google.android.gms/com.google.android.location.reporting.service.DispatchingService (has extras) } with receiverAction android.location.PROVIDERS_CHANGED
01-25 13:05:39.140 1861-2242/com.google.android.gms.persistent I/GeofencerStateMachine: Network location disabled.
01-25 13:05:39.144 2260-2270/com.google.android.apps.maps W/art: Suspending all threads took: 6.825ms
01-25 13:05:39.163 1861-2324/com.google.android.gms.persistent I/GCoreUlr: WorldUpdater:android.location.PROVIDERS_CHANGED: Ensuring that reporting is stopped because of reasons: (no Google accounts)
01-25 13:05:39.178 1861-1882/com.google.android.gms.persistent W/art: Suspending all threads took: 14.585ms
01-25 13:05:39.178 2337-2337/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:39.180 2337-2337/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:39.183 1861-1882/com.google.android.gms.persistent I/art: Background partial concurrent mark sweep GC freed 7734(653KB) AllocSpace objects, 6(120KB) LOS objects, 39% free, 5MB/9MB, paused 15.477ms total 495.170ms
01-25 13:05:39.188 1861-2324/com.google.android.gms.persistent I/GCoreUlr: Unbound from all location providers
01-25 13:05:39.188 1861-2324/com.google.android.gms.persistent I/GCoreUlr: Place inference reporting - stopped
01-25 13:05:39.201 2337-2337/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:39.218 2337-2337/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:39.218 2337-2337/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:39.219 2337-2337/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:39.226 1861-2284/com.google.android.gms.persistent I/Scheduler: Use legacy PeriodicScheduler
01-25 13:05:39.231 2337-2337/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:39.236 1198-1198/? I/installd: free_cache(3076) avail 664559616
01-25 13:05:39.244 2337-2337/? I/art: System.exit called, status: 0
01-25 13:05:39.244 2337-2337/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:39.400 2358-2358/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:39.401 2358-2358/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:39.412 2358-2358/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:39.430 2358-2358/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:39.430 2358-2358/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:39.430 2358-2358/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:39.439 2358-2358/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:39.445 1198-1198/? I/installd: free_cache(4271) avail 664555520
01-25 13:05:39.453 2358-2358/? I/art: System.exit called, status: 0
01-25 13:05:39.453 2358-2358/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:39.460 1861-2309/com.google.android.gms.persistent W/Settings: Setting airplane_mode_on has moved from android.provider.Settings.System to android.provider.Settings.Global, returning read-only value.
01-25 13:05:39.462 1861-2309/com.google.android.gms.persistent W/Settings: Setting airplane_mode_on has moved from android.provider.Settings.System to android.provider.Settings.Global, returning read-only value.
01-25 13:05:39.471 1861-2284/com.google.android.gms.persistent W/InstanceID/Rpc: Found 10007
01-25 13:05:39.472 1861-1861/com.google.android.gms.persistent I/GAv4-SVC: Google Analytics 8.4.89 is starting up.
01-25 13:05:39.598 1861-1861/com.google.android.gms.persistent E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:39.598 1861-1861/com.google.android.gms.persistent I/BleScanCompatLib: Building BLE scanner compat:  'L/M' hardware access layer is not available: BluetoothAdapter is null.
01-25 13:05:39.600 1861-1861/com.google.android.gms.persistent E/BleScanCompatLib: Unable to read constant String ACTION_BLE_STATE_CHANGED via reflection
                                                                                   java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.Class java.lang.Object.getClass()' on a null object reference
                                                                                       at com.google.android.gms.blescanner.f.b.c(SourceFile:109)
                                                                                       at com.google.android.gms.blescanner.e.a.<init>(SourceFile:76)
                                                                                       at com.google.android.gms.blescanner.c.b.a(SourceFile:59)
                                                                                       at com.google.android.location.places.i.b.a(SourceFile:69)
                                                                                       at com.google.android.location.places.i.k.<init>(SourceFile:155)
                                                                                       at com.google.android.location.places.service.aa.<init>(SourceFile:157)
                                                                                       at com.google.android.location.places.service.PlaceDetectionService.onCreate(SourceFile:46)
                                                                                       at android.app.ActivityThread.handleCreateService(ActivityThread.java:2877)
                                                                                       at android.app.ActivityThread.-wrap4(ActivityThread.java)
                                                                                       at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1427)
                                                                                       at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                                       at android.os.Looper.loop(Looper.java:148)
                                                                                       at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                                       at java.lang.reflect.Method.invoke(Native Method)
                                                                                       at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                                       at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.602 1861-1861/com.google.android.gms.persistent I/BleScanCompatLib: BLE 'JB+' software access layer enabled
01-25 13:05:39.605 1861-1861/com.google.android.gms.persistent E/BleScanCompatLib: Unable to read constant String ACTION_BLE_STATE_CHANGED via reflection
                                                                                   java.lang.NullPointerException: Attempt to invoke virtual method 'java.lang.Class java.lang.Object.getClass()' on a null object reference
                                                                                       at com.google.android.gms.blescanner.f.b.c(SourceFile:109)
                                                                                       at com.google.android.gms.blescanner.e.a.<init>(SourceFile:76)
                                                                                       at com.google.android.location.places.i.b.a(SourceFile:75)
                                                                                       at com.google.android.location.places.i.k.<init>(SourceFile:155)
                                                                                       at com.google.android.location.places.service.aa.<init>(SourceFile:157)
                                                                                       at com.google.android.location.places.service.PlaceDetectionService.onCreate(SourceFile:46)
                                                                                       at android.app.ActivityThread.handleCreateService(ActivityThread.java:2877)
                                                                                       at android.app.ActivityThread.-wrap4(ActivityThread.java)
                                                                                       at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1427)
                                                                                       at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                                       at android.os.Looper.loop(Looper.java:148)
                                                                                       at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                                       at java.lang.reflect.Method.invoke(Native Method)
                                                                                       at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                                       at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.623 1538-1597/system_process D/WifiNative-HAL: Failing getSupportedFeatureset because HAL isn't started
01-25 13:05:39.625 1861-2242/com.google.android.gms.persistent W/GeofencerStateMachine: Ignoring removeGeofence because network location is disabled.
01-25 13:05:39.639 2371-2371/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:39.641 2371-2371/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:39.652 2371-2371/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:39.658 1861-2375/com.google.android.gms.persistent I/Places: b.c:195: PlacesBleScanner stop()
01-25 13:05:39.658 1861-2375/com.google.android.gms.persistent I/BleScanCompatLib: Scan : No clients left, canceling alarm.
01-25 13:05:39.660 1861-1861/com.google.android.gms.persistent I/GCoreUlr: DispatchingService.onDestroy()
01-25 13:05:39.660 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Stopping handler for UlrDispSvcFast
01-25 13:05:39.662 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Unbound from all location providers
01-25 13:05:39.662 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Place inference reporting - stopped
01-25 13:05:39.680 2371-2371/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:39.680 2371-2371/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:39.680 2371-2371/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:39.687 2371-2371/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:39.695 1198-1198/? I/installd: free_cache(928751) avail 664485888
01-25 13:05:39.859 1538-1552/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? false
01-25 13:05:39.940 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=344 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.access(BlockGuardOs.java:67)
                                                                            at java.io.File.doAccess(File.java:281)
                                                                            at java.io.File.exists(File.java:361)
                                                                            at android.app.ContextImpl.createFilesDirLocked(ContextImpl.java:418)
                                                                            at android.app.ContextImpl.getFilesDir(ContextImpl.java:441)
                                                                            at android.app.ContextImpl.openFileInput(ContextImpl.java:383)
                                                                            at android.content.ContextWrapper.openFileInput(ContextWrapper.java:177)
                                                                            at com.google.android.apps.gmm.shared.i.h.a(PG:250)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8693)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.940 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=344 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.open(BlockGuardOs.java:182)
                                                                            at libcore.io.IoBridge.open(IoBridge.java:438)
                                                                            at java.io.FileInputStream.<init>(FileInputStream.java:76)
                                                                            at android.app.ContextImpl.openFileInput(ContextImpl.java:384)
                                                                            at android.content.ContextWrapper.openFileInput(ContextWrapper.java:177)
                                                                            at com.google.android.apps.gmm.shared.i.h.a(PG:250)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8693)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.941 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=343 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.fstat(BlockGuardOs.java:132)
                                                                            at libcore.io.IoBridge.open(IoBridge.java:441)
                                                                            at java.io.FileInputStream.<init>(FileInputStream.java:76)
                                                                            at android.app.ContextImpl.openFileInput(ContextImpl.java:384)
                                                                            at android.content.ContextWrapper.openFileInput(ContextWrapper.java:177)
                                                                            at com.google.android.apps.gmm.shared.i.h.a(PG:250)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8693)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.941 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=323 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.read(BlockGuardOs.java:229)
                                                                            at libcore.io.IoBridge.read(IoBridge.java:468)
                                                                            at java.io.FileInputStream.read(FileInputStream.java:177)
                                                                            at java.io.BufferedInputStream.read(BufferedInputStream.java:290)
                                                                            at java.io.DataInputStream.read(DataInputStream.java:63)
                                                                            at com.google.r.k.d(PG:1187)
                                                                            at com.google.r.k.a(PG:2107)
                                                                            at com.google.w.a.a.do.<init>(PG:23)
                                                                            at com.google.w.a.a.do.a(PG:405)
                                                                            at com.google.r.v.a(PG:1161)
                                                                            at com.google.r.y.a(PG:2188)
                                                                            at com.google.r.e.b(PG:170)
                                                                            at com.google.r.e.b(PG:15188)
                                                                            at com.google.android.apps.gmm.shared.i.h.a(PG:251)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8693)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.941 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=297 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.read(BlockGuardOs.java:229)
                                                                            at libcore.io.IoBridge.read(IoBridge.java:468)
                                                                            at java.io.FileInputStream.read(FileInputStream.java:177)
                                                                            at java.io.BufferedInputStream.read(BufferedInputStream.java:290)
                                                                            at java.io.DataInputStream.read(DataInputStream.java:63)
                                                                            at com.google.r.k.d(PG:1187)
                                                                            at com.google.r.k.c(PG:18147)
                                                                            at com.google.r.k.d(PG:583)
                                                                            at com.google.w.a.a.do.<init>(PG:40)
                                                                            at com.google.w.a.a.do.a(PG:405)
                                                                            at com.google.r.v.a(PG:1161)
                                                                            at com.google.r.y.a(PG:2188)
                                                                            at com.google.r.e.b(PG:170)
                                                                            at com.google.r.e.b(PG:15188)
                                                                            at com.google.android.apps.gmm.shared.i.h.a(PG:251)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8693)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.941 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=186 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.access(BlockGuardOs.java:67)
                                                                            at java.io.File.doAccess(File.java:281)
                                                                            at java.io.File.exists(File.java:361)
                                                                            at android.app.ContextImpl.createFilesDirLocked(ContextImpl.java:418)
                                                                            at android.app.ContextImpl.getFilesDir(ContextImpl.java:441)
                                                                            at android.app.ContextImpl.getFileStreamPath(ContextImpl.java:549)
                                                                            at android.content.ContextWrapper.getFileStreamPath(ContextWrapper.java:193)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8701)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.941 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=186 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.access(BlockGuardOs.java:67)
                                                                            at java.io.File.doAccess(File.java:281)
                                                                            at java.io.File.exists(File.java:361)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8703)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.941 2260-2260/com.google.android.apps.maps D/StrictMode: StrictMode policy violation; ~duration=186 ms: android.os.StrictMode$StrictModeDiskReadViolation: policy=65567 violation=2
                                                                            at android.os.StrictMode$AndroidBlockGuardPolicy.onReadFromDisk(StrictMode.java:1263)
                                                                            at libcore.io.BlockGuardOs.stat(BlockGuardOs.java:292)
                                                                            at java.io.File.lastModified(File.java:569)
                                                                            at com.google.android.apps.gmm.map.m.q.a(PG:8704)
                                                                            at com.google.android.apps.gmm.shared.f.a.a(PG:48)
                                                                            at com.google.android.apps.gmm.map.m.e.a(PG:1531)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:244)
                                                                            at com.google.android.apps.gmm.base.app.a.a(PG:2265)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.a(PG:206)
                                                                            at com.google.android.apps.gmm.base.app.GoogleMapsApplication.onCreate(PG:174)
                                                                            at android.app.Instrumentation.callApplicationOnCreate(Instrumentation.java:1013)
                                                                            at android.app.ActivityThread.handleBindApplication(ActivityThread.java:4707)
                                                                            at android.app.ActivityThread.-wrap1(ActivityThread.java)
                                                                            at android.app.ActivityThread$H.handleMessage(ActivityThread.java:1405)
                                                                            at android.os.Handler.dispatchMessage(Handler.java:102)
                                                                            at android.os.Looper.loop(Looper.java:148)
                                                                            at android.app.ActivityThread.main(ActivityThread.java:5417)
                                                                            at java.lang.reflect.Method.invoke(Native Method)
                                                                            at com.android.internal.os.ZygoteInit$MethodAndArgsCaller.run(ZygoteInit.java:726)
                                                                            at com.android.internal.os.ZygoteInit.main(ZygoteInit.java:616)
01-25 13:05:39.994 1538-1538/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:40.003 2017-2017/android.process.media D/MediaScannerReceiver: action: android.intent.action.MEDIA_MOUNTED path: /storage/0C03-3A10
01-25 13:05:40.015 1538-1648/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? false
01-25 13:05:40.045 2260-2270/com.google.android.apps.maps W/art: Suspending all threads took: 6.633ms
01-25 13:05:40.125 2260-2352/com.google.android.apps.maps W/com.google.a.a.b.d.a: Application name is not set. Call Builder#setApplicationName.
01-25 13:05:40.138 2260-2396/com.google.android.apps.maps W/ActivityThread: ClassLoader.loadClass: The class loader returned by Thread.getContextClassLoader() may fail for processes that host multiple applications. You should explicitly specify a context class loader. For example: Thread.setContextClassLoader(getClass().getClassLoader());
01-25 13:05:40.148 2017-2017/android.process.media D/MediaScannerReceiver: action: android.intent.action.MEDIA_MOUNTED path: /storage/emulated/0
01-25 13:05:40.164 2260-2352/com.google.android.apps.maps E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:40.198 1538-1904/system_process I/ActivityManager: Start proc 2402:com.android.settings/1000 for broadcast com.android.settings/.sim.SimSelectNotification
01-25 13:05:40.213 2402-2402/? W/System: ClassLoader referenced unknown path: /system/priv-app/Settings/lib/x86
01-25 13:05:40.326 2167-2167/com.google.android.gms I/CheckinService: Checkin interval check for package: unspecified last checkin: 1500180484670 min interval config: 0 actual interval: 16705055656
01-25 13:05:40.362 2167-2418/com.google.android.gms I/EventLogService: Aggregate from 1516857333087 (log), 1516857333087 (data)
01-25 13:05:40.543 1538-2069/system_process I/ActivityManager: Start proc 2424:com.android.calendar/u0a20 for broadcast com.android.calendar/.widget.CalendarAppWidgetService$CalendarFactory
01-25 13:05:40.550 2424-2424/? W/System: ClassLoader referenced unknown path: /system/app/Calendar/lib/x86
01-25 13:05:40.628 2424-2424/? D/ExtensionsFactory: No custom extensions.
01-25 13:05:40.644 1538-2069/system_process I/ActivityManager: Start proc 2442:com.android.deskclock/u0a24 for broadcast com.android.deskclock/.AlarmInitReceiver
01-25 13:05:40.656 1538-1648/system_process I/ActivityManager: Start proc 2455:com.android.providers.calendar/u0a1 for content provider com.android.providers.calendar/.CalendarProvider2
01-25 13:05:40.664 2455-2455/? W/System: ClassLoader referenced unknown path: /system/priv-app/CalendarProvider/lib/x86
01-25 13:05:40.666 2442-2442/? W/System: ClassLoader referenced unknown path: /system/app/DeskClock/lib/x86
01-25 13:05:40.689 2455-2455/? I/CalendarProvider2: Created com.android.providers.calendar.CalendarAlarmManager@98b79cf(com.android.providers.calendar.CalendarProvider2@49a1f5c)
01-25 13:05:40.691 1538-1551/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:40.712 2442-2442/? V/AlarmClock: AlarmInitReceiver android.intent.action.TIME_SET
01-25 13:05:40.737 2442-2472/? V/AlarmClock: AlarmInitReceiver finished
01-25 13:05:41.152 1538-1648/system_process I/ActivityManager: Start proc 2478:com.android.messaging/u0a48 for broadcast com.android.messaging/.receiver.DefaultSmsSubscriptionChangeReceiver
01-25 13:05:41.159 2478-2478/? W/System: ClassLoader referenced unknown path: /system/app/messaging/lib/x86
01-25 13:05:41.350 2478-2496/? I/MessagingAppDataModel: Fixup: Send failed - 0 Download failed - 0
01-25 13:05:41.408 2478-2478/? I/MessagingApp: Carrier config changed. Reloading MMS config.
01-25 13:05:41.466 2478-2494/? W/MessagingApp: canonicalizeMccMnc: invalid mccmnc:null ,null
01-25 13:05:41.486 1861-1861/com.google.android.gms.persistent D/WearableService: callingUid 10007, callindPid: 1861
01-25 13:05:41.492 1538-1892/system_process D/MmsServiceBroker: getCarrierConfigValues() by com.android.messaging
01-25 13:05:41.492 1538-1892/system_process W/MmsServiceBroker: MmsService not connected. Try connecting...
01-25 13:05:41.492 1538-1538/system_process I/MmsServiceBroker: Connecting to MmsService
01-25 13:05:41.492 1538-1538/system_process W/ContextImpl: Calling a method in the system process without a qualified user: android.app.ContextImpl.bindService:1285 com.android.server.MmsServiceBroker.tryConnecting:240 com.android.server.MmsServiceBroker.-wrap3:-1 com.android.server.MmsServiceBroker$1.handleMessage:82 android.os.Handler.dispatchMessage:102 
01-25 13:05:41.493 1870-1870/com.android.phone W/System: ClassLoader referenced unknown path: /system/priv-app/MmsService/lib/x86
01-25 13:05:41.495 1870-1870/com.android.phone D/MmsService: onCreate
01-25 13:05:41.496 1538-1538/system_process I/MmsServiceBroker: MmsService connected
01-25 13:05:41.496 1870-2103/com.android.phone D/MmsService: getCarrierConfigValues
01-25 13:05:41.496 1870-2103/com.android.phone I/MmsService: mms config for sub 1: null
01-25 13:05:41.496 2478-2494/? I/MessagingApp: Carrier configs loaded: Bundle[{maxImageHeight=1944, maxMessageSize=1048576, maxImageWidth=2592}] from resources+system for subId=1
01-25 13:05:41.497 1870-2504/com.android.phone I/MmsService: MmsConfigManager loads in background mcc/mnc: 310/260
01-25 13:05:41.500 2478-2503/? I/MessagingAppDataModel: SyncMessagesAction: Starting batch for messages from 1516856952952 to 1516885541328 (message update limit = 80, message scan limit = 4000)
01-25 13:05:41.521 2478-2498/? W/MessagingApp: canonicalizeMccMnc: invalid mccmnc:null ,null
01-25 13:05:41.526 1538-2069/system_process D/MmsServiceBroker: getCarrierConfigValues() by com.android.messaging
01-25 13:05:41.526 1870-2106/com.android.phone D/MmsService: getCarrierConfigValues
01-25 13:05:41.526 1870-2106/com.android.phone I/MmsService: mms config for sub 1: Bundle[{httpSocketTimeout=60000, aliasMinChars=2, smsToMmsTextThreshold=-1, enableSMSDeliveryReports=true, maxMessageTextSize=-1, supportMmsContentDisposition=true, enabledTransID=false, aliasEnabled=false, supportHttpCharsetHeader=false, allowAttachAudio=true, smsToMmsTextLengthThreshold=-1, recipientLimit=2147483647, uaProfTagName=x-wap-profile, aliasMaxChars=48, maxImageHeight=480, enableMMSDeliveryReports=false, userAgent=, config_cellBroadcastAppLinks=true, maxSubjectLength=40, httpParams=, enableGroupMms=true, emailGatewayNumber=, maxMessageSize=307200, naiSuffix=, enableMMSReadReports=false, maxImageWidth=640, uaProfUrl=, enabledMMS=true, enabledNotifyWapMMSC=false, sendMultipartSmsAsSeparateMessages=false, enableMultipartSMS=true}]
01-25 13:05:41.526 2478-2498/? I/MessagingApp: Carrier configs loaded: Bundle[{httpSocketTimeout=60000, aliasMinChars=2, smsToMmsTextThreshold=-1, enableSMSDeliveryReports=true, maxMessageTextSize=-1, supportMmsContentDisposition=true, enabledTransID=false, aliasEnabled=false, supportHttpCharsetHeader=false, allowAttachAudio=true, smsToMmsTextLengthThreshold=-1, recipientLimit=2147483647, uaProfTagName=x-wap-profile, aliasMaxChars=48, maxImageHeight=480, enableMMSDeliveryReports=false, userAgent=, config_cellBroadcastAppLinks=true, maxSubjectLength=40, httpParams=, enableGroupMms=true, emailGatewayNumber=, maxMessageSize=307200, naiSuffix=, enableMMSReadReports=false, maxImageWidth=640, uaProfUrl=, enabledMMS=true, enabledNotifyWapMMSC=false, sendMultipartSmsAsSeparateMessages=false, enableMultipartSMS=true}] from resources+system for subId=1
01-25 13:05:41.532 2478-2498/? W/MessagingApp: canonicalizeMccMnc: invalid mccmnc:null ,null
01-25 13:05:41.535 1861-1861/com.google.android.gms.persistent E/GmsWearableNodeHelper: GoogleApiClient connection failed: ConnectionResult{statusCode=API_UNAVAILABLE, resolution=null, message=null}
01-25 13:05:41.541 1538-1648/system_process D/MmsServiceBroker: getCarrierConfigValues() by com.android.messaging
01-25 13:05:41.543 1870-2103/com.android.phone D/MmsService: getCarrierConfigValues
01-25 13:05:41.543 1870-2103/com.android.phone I/MmsService: mms config for sub 1: Bundle[{httpSocketTimeout=60000, aliasMinChars=2, smsToMmsTextThreshold=-1, enableSMSDeliveryReports=true, maxMessageTextSize=-1, supportMmsContentDisposition=true, enabledTransID=false, aliasEnabled=false, supportHttpCharsetHeader=false, allowAttachAudio=true, smsToMmsTextLengthThreshold=-1, recipientLimit=2147483647, uaProfTagName=x-wap-profile, aliasMaxChars=48, maxImageHeight=480, enableMMSDeliveryReports=false, userAgent=, config_cellBroadcastAppLinks=true, maxSubjectLength=40, httpParams=, enableGroupMms=true, emailGatewayNumber=, maxMessageSize=307200, naiSuffix=, enableMMSReadReports=false, maxImageWidth=640, uaProfUrl=, enabledMMS=true, enabledNotifyWapMMSC=false, sendMultipartSmsAsSeparateMessages=false, enableMultipartSMS=true}]
01-25 13:05:41.548 2478-2498/? I/MessagingApp: Carrier configs loaded: Bundle[{httpSocketTimeout=60000, aliasMinChars=2, smsToMmsTextThreshold=-1, enableSMSDeliveryReports=true, maxMessageTextSize=-1, supportMmsContentDisposition=true, enabledTransID=false, aliasEnabled=false, supportHttpCharsetHeader=false, allowAttachAudio=true, smsToMmsTextLengthThreshold=-1, recipientLimit=2147483647, uaProfTagName=x-wap-profile, aliasMaxChars=48, maxImageHeight=480, enableMMSDeliveryReports=false, userAgent=, config_cellBroadcastAppLinks=true, maxSubjectLength=40, httpParams=, enableGroupMms=true, emailGatewayNumber=, maxMessageSize=307200, naiSuffix=, enableMMSReadReports=false, maxImageWidth=640, uaProfUrl=, enabledMMS=true, enabledNotifyWapMMSC=false, sendMultipartSmsAsSeparateMessages=false, enableMultipartSMS=true}] from resources+system for subId=1
01-25 13:05:41.555 2167-2506/com.google.android.gms D/LocationInitializer: Restart initialization of location
01-25 13:05:41.576 1861-2505/com.google.android.gms.persistent E/MDM: [88] b.run: Couldn't connect to Google API client: ConnectionResult{statusCode=API_UNAVAILABLE, resolution=null, message=null}
01-25 13:05:41.614 2478-2507/? I/MessagingAppDataModel: SyncMessagesAction: All messages now in sync
01-25 13:05:41.634 2478-2495/? W/art: Long monitor contention event with owner method=void java.util.LinkedHashMap.addNewEntry(java.lang.Object, java.lang.Object, int, int) from LinkedHashMap.java:184 waiters=0 for 147ms
01-25 13:05:41.681 1861-2508/com.google.android.gms.persistent E/copresGcore: WifiMedium: Wifi is not supported!!
01-25 13:05:41.734 2455-2455/? I/CalendarProvider2: Sending notification intent: Intent { act=android.intent.action.PROVIDER_CHANGED dat=content://com.android.calendar }
01-25 13:05:41.734 2455-2455/? W/ContentResolver: Failed to get type for: content://com.android.calendar (Unknown URL content://com.android.calendar)
01-25 13:05:41.748 1538-1927/system_process D/CountryDetector: The first listener is added
01-25 13:05:41.792 2167-2512/com.google.android.gms W/IcingInternalCorpora: getNumBytesRead when not calculated.
01-25 13:05:41.813 1861-1861/com.google.android.gms.persistent D/AuthorizationBluetoothService: Received GmsCore event: Intent { act=com.google.android.gms.INITIALIZE flg=0x10 pkg=com.google.android.gms cmp=com.google.android.gms/.auth.be.proximity.authorization.bt.AuthorizationBluetoothService$AutoStarter }.
01-25 13:05:41.816 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:41.820 1861-1861/com.google.android.gms.persistent D/a: Opening database auth.proximity.permit_store...
01-25 13:05:41.822 1861-2508/com.google.android.gms.persistent E/copresGcore: ObfuscatedGaiaIdLookup: Could not load ObfuscatedGaiaIds: /data/user/0/com.google.android.gms/files/copresence_gaia_id: open failed: ENOENT (No such file or directory)
01-25 13:05:41.823 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:41.849 1861-1861/com.google.android.gms.persistent E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:41.880 1861-2508/com.google.android.gms.persistent E/BluetoothAdapter: Bluetooth binder is null
01-25 13:05:41.881 1861-1861/com.google.android.gms.persistent V/GLSActivity: AuthDelegateWrapperCreated with selected intent: Intent { cmp=com.google.android.gms/.auth.DefaultAuthDelegateService }
01-25 13:05:41.883 1861-1861/com.google.android.gms.persistent V/GLSActivity: AuthDelegateWrapperCreated with selected intent: Intent { cmp=com.google.android.gms/.auth.DefaultAuthDelegateService }
01-25 13:05:41.887 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:41.888 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:41.891 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:41.952 2167-2167/com.google.android.gms I/CheckinService: Checkin interval check for package: unspecified last checkin: 1500180484670 min interval config: 0 actual interval: 16705057282
01-25 13:05:41.976 2167-2528/com.google.android.gms I/CheckinService: Disabling old GoogleServicesFramework version
01-25 13:05:42.029 2167-2529/com.google.android.gms I/CheckinService: Checking schedule, now: 1516885542029 next: 1500221336361
01-25 13:05:42.030 2167-2529/com.google.android.gms I/CheckinService: active receiver: enabled
01-25 13:05:42.030 2167-2529/com.google.android.gms I/CheckinService: Preparing to send checkin request
01-25 13:05:42.030 2167-2529/com.google.android.gms I/EventLogService: Accumulating logs since 1516885540372
01-25 13:05:42.055 1538-1552/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:42.055 2167-2167/com.google.android.gms E/MDM: [1] SitrepService.a: No Google accounts; deferring server state update.
01-25 13:05:42.076 2167-2536/com.google.android.gms I/iu.SyncManager: SYNC; picasa accounts
01-25 13:05:42.080 2167-2167/com.google.android.gms D/NetworkLogImpl: Loaded NetworkSpeedPredictor
01-25 13:05:42.081 2167-2167/com.google.android.gms I/iu.Environment: update connectivity state; isNetworkMetered? true*, isRoaming? false, isBackgroundDataAllowed? true*
01-25 13:05:42.087 2167-2536/com.google.android.gms I/iu.UploadsManager: num queued entries: 0
01-25 13:05:42.087 2167-2536/com.google.android.gms I/iu.UploadsManager: num updated entries: 0
01-25 13:05:42.089 2167-2536/com.google.android.gms I/iu.SyncManager: NEXT; no task
01-25 13:05:42.098 1861-1861/com.google.android.gms.persistent D/GCM: COMPAT: Multi user not supported
01-25 13:05:42.106 2167-2529/com.google.android.gms I/CheckinRequestBuilder: Checkin reason type: 12 attempt count: 1
01-25 13:05:42.110 2167-2540/com.google.android.gms W/InstanceID/Rpc: Found 10007
01-25 13:05:42.114 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:42.115 2167-2529/com.google.android.gms E/ActivityThread: Failed to find provider info for com.google.android.wearable.settings
01-25 13:05:42.142 2167-2167/com.google.android.gms D/GCM: COMPAT: Multi user not supported
01-25 13:05:42.283 1538-1551/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:42.284 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:42.317 1861-2548/com.google.android.gms.persistent D/GCM: GcmService start Intent { act=com.google.android.c2dm.intent.REGISTER pkg=com.google.android.gms cmp=com.google.android.gms/.gcm.GcmService (has extras) } com.google.android.c2dm.intent.REGISTER
01-25 13:05:42.320 1861-2548/com.google.android.gms.persistent I/GCM: GCM config loaded
01-25 13:05:42.344 1538-1904/system_process I/ActivityManager: Start proc 2553:com.google.android.gms.unstable/u0a7 for service com.google.android.gms/.droidguard.DroidGuardService
01-25 13:05:42.357 1861-1861/com.google.android.gms.persistent V/UserPresentBroadcastReceiver: Received Intent { act=android.intent.action.USER_PRESENT flg=0x24000010 cmp=com.google.android.gms/.auth.trustagent.UserPresentBroadcastReceiver }.
01-25 13:05:42.360 2553-2553/? W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:42.365 2553-2553/? I/MultiDex: VM with version 2.1.0 has multidex support
01-25 13:05:42.365 2553-2553/? I/MultiDex: install
01-25 13:05:42.365 2553-2553/? I/MultiDex: VM has multidex support, MultiDex support library is disabled.
01-25 13:05:42.372 1538-1538/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:42.383 1538-2570/system_process I/ActivityManager: Start proc 2573:com.android.keychain/1000 for service com.android.keychain/.KeyChainService
01-25 13:05:42.409 2553-2553/? W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:42.409 2553-2553/? W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:42.414 2553-2553/? W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:42.414 2553-2553/? W/System: ClassLoader referenced unknown path: /system/priv-app/PrebuiltGmsCore/lib/x86
01-25 13:05:42.434 2553-2553/? V/JNIHelp: Registering com/google/android/gms/org/conscrypt/NativeCrypto's 254 native methods...
01-25 13:05:42.440 2553-2553/? I/ProviderInstaller: Installed default security provider GmsCore_OpenSSL
01-25 13:05:42.487 1538-2587/system_process I/RecoverySystem: No recovery log file
01-25 13:05:42.498 2573-2573/? W/System: ClassLoader referenced unknown path: /system/app/KeyChain/lib/x86
01-25 13:05:42.498 1538-1648/system_process I/ActivityManager: Start proc 2589:com.android.dialer/u0a4 for broadcast com.android.dialer/.calllog.CallLogReceiver
01-25 13:05:42.503 1538-2587/system_process I/BootReceiver: Copying audit failures to DropBox
01-25 13:05:42.504 1538-2587/system_process I/BootReceiver: Checking for fsck errors
01-25 13:05:42.524 2589-2589/? W/System: ClassLoader referenced unknown path: /system/priv-app/Dialer/lib/x86
01-25 13:05:42.538 2553-2564/? W/art: Suspending all threads took: 6.979ms
01-25 13:05:42.539 2553-2596/? D/NativeLibraryUtils: Install completed successfully. count=13 extracted=0
01-25 13:05:42.541 2553-2564/? I/art: Background partial concurrent mark sweep GC freed 9055(675KB) AllocSpace objects, 2(40KB) LOS objects, 39% free, 4MB/7MB, paused 7.359ms total 18.160ms
01-25 13:05:42.583 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:42.593 2553-2566/? I/GoogleURLConnFactory: Using platform SSLCertificateSocketFactory
01-25 13:05:42.622 1196-1581/? D/WVCdm: Instantiating CDM.
01-25 13:05:42.623 1196-1196/? I/WVCdm: CdmEngine::OpenSession
01-25 13:05:42.624 1196-1196/? I/WVCdm: Level3 Library Sep 28 2015 13:08:28
01-25 13:05:42.625 1196-1196/? W/WVCdm: Could not read /data/mediadrm/IDM1013/ay64.dat2: No such file or directory
01-25 13:05:42.625 1196-1196/? W/WVCdm: Could not load liboemcrypto.so. Falling back to L3.  dlopen failed: library "liboemcrypto.so" not found
01-25 13:05:42.626 1196-1196/? W/WVCdm: DeviceFiles::RetrieveHashedFile: /data/mediadrm/IDM1013/L3/cert.bin does not exist
01-25 13:05:42.628 2553-2605/? W/DroidGuardService: Waiting for device certificate provisioning.
                                                    com.google.android.gms.droidguard.e.c: Waiting for provisioning response from server.
                                                        at com.google.android.gms.droidguard.q.run(SourceFile:99)
                                                        at java.util.concurrent.ThreadPoolExecutor.runWorker(ThreadPoolExecutor.java:1113)
                                                        at java.util.concurrent.ThreadPoolExecutor$Worker.run(ThreadPoolExecutor.java:588)
                                                        at java.lang.Thread.run(Thread.java:818)
01-25 13:05:42.681 1196-1605/? I/WVCdm: Level3 Library Sep 28 2015 13:08:28
01-25 13:05:42.682 1196-1605/? W/WVCdm: Could not read /data/mediadrm/IDM1013/ay64.dat2: No such file or directory
01-25 13:05:42.682 1196-1605/? W/WVCdm: Could not load liboemcrypto.so. Falling back to L3.  dlopen failed: library "liboemcrypto.so" not found
01-25 13:05:42.684 2553-2608/? I/GoogleURLConnFactory: Using platform SSLCertificateSocketFactory
01-25 13:05:42.693 2589-2589/? D/ExtensionsFactory: No custom extensions.
01-25 13:05:42.718 1870-1870/com.android.phone V/OtaStartupReceiver: onOtaspChanged: mOtaspMode=3
01-25 13:05:42.719 1538-1597/system_process D/WIFI: Registering NetworkFactory
01-25 13:05:42.719 1538-1597/system_process D/WIFI_UT: Registering NetworkFactory
01-25 13:05:42.719 1538-1599/system_process D/ConnectivityService: Got NetworkFactory Messenger for WIFI
01-25 13:05:42.719 1538-1599/system_process D/ConnectivityService: Got NetworkFactory Messenger for WIFI_UT
01-25 13:05:42.720 1538-1597/system_process D/WIFI: got request NetworkRequest [ id=1, legacyType=-1, [ Capabilities: INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN] ] with score 50
01-25 13:05:42.720 1538-1597/system_process D/WIFI_UT: got request NetworkRequest [ id=1, legacyType=-1, [ Capabilities: INTERNET&NOT_RESTRICTED&TRUSTED&NOT_VPN] ] with score 50
01-25 13:05:42.747 1538-1552/system_process I/ActivityManager: Start proc 2613:com.android.managedprovisioning/u0a8 for broadcast com.android.managedprovisioning/.BootReminder
01-25 13:05:42.753 2613-2613/? W/System: ClassLoader referenced unknown path: /system/priv-app/ManagedProvisioning/lib/x86
01-25 13:05:43.064 2017-2628/android.process.media W/MediaScanner: Error opening directory '/oem/media/', skipping: No such file or directory.
01-25 13:05:43.213 2371-2371/? I/art: System.exit called, status: 0
01-25 13:05:43.213 2371-2371/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:43.351 2632-2632/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:43.352 2632-2632/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:43.363 2632-2632/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:43.386 2632-2632/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:43.386 2632-2632/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:43.387 2632-2632/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:43.396 2632-2632/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:43.405 1198-1198/? I/installd: free_cache(4267) avail 663736320
01-25 13:05:43.416 2632-2632/? I/art: System.exit called, status: 0
01-25 13:05:43.416 2632-2632/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:43.573 2643-2643/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:43.574 2643-2643/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:43.587 2643-2643/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:43.613 2643-2643/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:43.613 2643-2643/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:43.619 2643-2643/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:43.630 2643-2643/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:43.636 1198-1198/? I/installd: free_cache(3079) avail 663740416
01-25 13:05:43.648 2643-2643/? I/art: System.exit called, status: 0
01-25 13:05:43.648 2643-2643/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:43.783 2167-2629/com.google.android.gms D/FileApkUtils: Spent 25ms computing apk sha1.
01-25 13:05:43.783 2167-2629/com.google.android.gms D/FileApkUtils: Module already staged or being staged:chimera-modules/MapsModule.apk
01-25 13:05:43.803 2654-2654/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:43.804 2654-2654/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:43.807 2167-2629/com.google.android.gms D/DexOptUtils: Module /data/user/0/com.google.android.gms/app_chimera/chimera-module-root/module-a3e4fba11e705727c59ff3116ef21fa4834b9f56/MapsModule.apk is already optimized. Bailing.
01-25 13:05:43.808 2167-2629/com.google.android.gms D/FileApkUtils: Keeping up-to-date module: module-a3e4fba11e705727c59ff3116ef21fa4834b9f56
01-25 13:05:43.808 2167-2629/com.google.android.gms D/ChimeraCfgMgr: Reading stored module config
01-25 13:05:43.812 2167-2656/com.google.android.gms I/iu.UploadsManager: #reloadSettings(); account: -1; IU: disabled; IS: disabled; IS account: -1; photoWiFi: true; videoWiFi: true; roam: false; battery: true; size: STANDARD; maxMobile: 157286400
01-25 13:05:43.821 2654-2654/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:43.833 2167-2629/com.google.android.gms D/GmsModuleFndr: Beginning GMS chimera module scan
01-25 13:05:43.853 2654-2654/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:43.853 2654-2654/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:43.854 2167-2629/com.google.android.gms D/GmsModuleFndr: Module pkg com.google.android.gms.policy_test_support not installed, skipping
01-25 13:05:43.857 2167-2629/com.google.android.gms D/GmsModuleFndr: Module pkg com.google.android.play.games not installed, skipping
01-25 13:05:43.856 2654-2654/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:43.860 2167-2629/com.google.android.gms D/GmsModuleFndr: Module pkg com.google.android.apps.kids.familylink not installed, skipping
01-25 13:05:43.860 2167-2629/com.google.android.gms D/ChimeraCfgMgr: Beginning module configuration check
01-25 13:05:43.863 2167-2629/com.google.android.gms D/ChimeraCfgMgr: Module APKs unchanged, check complete
01-25 13:05:43.872 2654-2654/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:43.890 1198-1198/? I/installd: free_cache(3085) avail 663736320
01-25 13:05:43.906 2654-2654/? I/art: System.exit called, status: 0
01-25 13:05:43.906 2654-2654/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:43.915 2167-2656/com.google.android.gms I/iu.UploadsManager: End new media; added: 0, uploading: 0, time: 103 ms
01-25 13:05:43.964 2167-2167/com.google.android.gms I/CheckinService: Checkin interval check for package: unspecified last checkin: 1500180484670 min interval config: 0 actual interval: 16705059293
01-25 13:05:43.993 2167-2670/com.google.android.gms I/GCoreUlr: Starting service, intent=Intent { act=com.google.android.location.reporting.ACTION_UPDATE_WORLD cmp=com.google.android.gms/com.google.android.location.reporting.service.DispatchingService (has extras) }, extras=Bundle[{receiverAction=android.intent.action.BOOT_COMPLETED}]
01-25 13:05:43.996 2167-2167/com.google.android.gms D/SystemUpdateService: onCreate
01-25 13:05:44.005 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.016 1861-1861/com.google.android.gms.persistent I/GCoreUlr: DispatchingService.onCreate()
01-25 13:05:44.037 2167-2167/com.google.android.gms D/SystemUpdateService: onStartCommand: intent: Intent { cmp=com.google.android.gms/.update.SystemUpdateService (has extras) }
01-25 13:05:44.042 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.gass from APK com.google.android.gms
01-25 13:05:44.047 2167-2167/com.google.android.gms D/BootCompletedReceiver: Will schedule periodic tasks:android.intent.action.BOOT_COMPLETED.
01-25 13:05:44.048 2167-2167/com.google.android.gms D/BootCompletedReceiver: Got an BootCompleted event.
01-25 13:05:44.053 2167-2167/com.google.android.gms D/BootCompletedReceiver: Will NOT schedule AdAttestation signal task because it's disabled.
01-25 13:05:44.059 2167-2681/com.google.android.gms I/SystemUpdateService: cancelUpdate (empty URL)
01-25 13:05:44.059 2167-2681/com.google.android.gms I/SystemUpdateService: active receiver: disabled
01-25 13:05:44.069 1861-2682/com.google.android.gms.persistent I/GCoreUlr: WorldUpdater received intent Intent { act=com.google.android.location.reporting.ACTION_UPDATE_WORLD cmp=com.google.android.gms/com.google.android.location.reporting.service.DispatchingService (has extras) } with receiverAction android.intent.action.BOOT_COMPLETED
01-25 13:05:44.086 2167-2684/com.google.android.gms V/AuthZen: Handling intent: android.intent.action.BOOT_COMPLETED
01-25 13:05:44.115 2674-2674/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:44.116 2674-2674/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:44.124 2167-2684/com.google.android.gms D/AuthZenEventHandler: Handling event: android.intent.action.BOOT_COMPLETED
01-25 13:05:44.133 2674-2674/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:44.150 2674-2674/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:44.150 2674-2674/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:44.151 2674-2674/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:44.157 2167-2684/com.google.android.gms W/BaseAppContext: Using Auth Proxy for data requests.
01-25 13:05:44.162 2674-2674/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:44.178 2167-2167/com.google.android.gms D/SystemUpdateService: onDestroy
01-25 13:05:44.180 1198-1198/? I/installd: free_cache(3082) avail 663728128
01-25 13:05:44.193 2674-2674/? I/art: System.exit called, status: 0
01-25 13:05:44.193 2674-2674/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:44.218 1861-1861/com.google.android.gms.persistent W/Auth: [FRP,FrpUpdateIntentService] Received invalid intent action: com.google.android.gms.auth.ACTION_INVALID
01-25 13:05:44.235 2167-2684/com.google.android.gms E/BaseAppContext: Tried to stop global GMSCore RequestQueue. This is likely unintended, so ignoring.
01-25 13:05:44.240 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.245 2167-2684/com.google.android.gms D/AuthZenTransactionCache: Initialized cache in: /data/user/0/com.google.android.gms/files
01-25 13:05:44.245 2167-2684/com.google.android.gms D/AuthZenTransactionCache: Clearing transaction cache
01-25 13:05:44.273 1861-1861/com.google.android.gms.persistent V/GLSActivity: AuthDelegateWrapperCreated with selected intent: Intent { cmp=com.google.android.gms/.auth.DefaultAuthDelegateService }
01-25 13:05:44.278 1861-1861/com.google.android.gms.persistent D/PersistentNotificationBroadcastReceiver: Received intent: Intent { act=android.intent.action.BOOT_COMPLETED flg=0x8000010 cmp=com.google.android.gms/.common.notification.PersistentNotificationBroadcastReceiver (has extras) }
01-25 13:05:44.279 1538-1648/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.283 1538-1552/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.284 1538-2069/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.295 1861-2682/com.google.android.gms.persistent I/GCoreUlr: WorldUpdater:android.intent.action.BOOT_COMPLETED: Ensuring that reporting is stopped because of reasons: (no Google accounts)
01-25 13:05:44.303 1861-2682/com.google.android.gms.persistent I/GCoreUlr: Unbound from all location providers
01-25 13:05:44.303 1861-2682/com.google.android.gms.persistent I/GCoreUlr: Place inference reporting - stopped
01-25 13:05:44.334 1861-1861/com.google.android.gms.persistent I/GCoreUlr: DispatchingService.onDestroy()
01-25 13:05:44.334 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Stopping handler for UlrDispSvcFast
01-25 13:05:44.337 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Unbound from all location providers
01-25 13:05:44.337 1861-1861/com.google.android.gms.persistent I/GCoreUlr: Place inference reporting - stopped
01-25 13:05:44.397 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.415 2701-2701/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:44.417 2701-2701/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:44.418 1538-1599/system_process D/ConnectivityService: handlePromptUnvalidated 100
01-25 13:05:44.430 2424-2424/com.android.calendar D/AlertReceiver: onReceive: a=android.intent.action.BOOT_COMPLETED Intent { act=android.intent.action.BOOT_COMPLETED flg=0x8000010 cmp=com.android.calendar/.alerts.AlertReceiver (has extras) }
01-25 13:05:44.430 2701-2701/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:44.433 2072-2399/com.google.android.googlequicksearchbox:search I/SearchServiceFactory: refreshing search history.
01-25 13:05:44.436 2442-2442/com.android.deskclock V/AlarmClock: AlarmInitReceiver android.intent.action.BOOT_COMPLETED
01-25 13:05:44.447 2442-2472/com.android.deskclock V/AlarmClock: AlarmInitReceiver - Reset timers and clear stopwatch data
01-25 13:05:44.450 2424-2721/com.android.calendar D/AlertService: 0 Action = android.intent.action.BOOT_COMPLETED
01-25 13:05:44.451 2701-2701/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:44.451 2701-2701/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:44.452 2701-2701/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:44.458 2701-2701/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:44.460 1198-1198/? I/installd: free_cache(3084) avail 663703552
01-25 13:05:44.464 2424-2721/com.android.calendar D/AlertService: Scheduling next alarm with AlarmScheduler. sEventReminderReceived: null
01-25 13:05:44.473 2701-2701/? I/art: System.exit called, status: 0
01-25 13:05:44.473 2701-2701/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:44.477 2424-2721/com.android.calendar D/AlarmScheduler: No events found starting within 1 week.
01-25 13:05:44.495 2442-2472/com.android.deskclock V/AlarmClock: AlarmInitReceiver finished
01-25 13:05:44.505 1538-1552/system_process I/ActivityManager: Start proc 2743:com.android.email/u0a28 for broadcast com.android.email/.service.EmailBroadcastReceiver
01-25 13:05:44.525 2743-2749/? E/art: Failed writing handshake bytes (-1 of 14): Broken pipe
01-25 13:05:44.526 2743-2749/? I/art: Debugger is no longer active
01-25 13:05:44.532 2072-2399/com.google.android.googlequicksearchbox:search I/WebViewFactory: Loading com.android.webview version 44.0.2403.119 (code 246011910)
01-25 13:05:44.536 2743-2743/? W/System: ClassLoader referenced unknown path: /system/app/Email/lib/x86
01-25 13:05:44.541 2072-2399/com.google.android.googlequicksearchbox:search W/System: ClassLoader referenced unknown path: /system/app/webview/lib/x86
01-25 13:05:44.629 2740-2740/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:44.630 2740-2740/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:44.639 2740-2740/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:44.659 2740-2740/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:44.659 2740-2740/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:44.659 2740-2740/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:44.667 2740-2740/? D/AndroidRuntime: Calling main entry com.android.commands.pm.Pm
01-25 13:05:44.682 2072-2399/com.google.android.googlequicksearchbox:search I/LibraryLoader: Time to load native libraries: 62 ms (timestamps 2336-2398)
01-25 13:05:44.683 2072-2399/com.google.android.googlequicksearchbox:search I/LibraryLoader: Expected native library version number "",actual native library version number ""
01-25 13:05:44.723 2072-2399/com.google.android.googlequicksearchbox:search W/art: Attempt to remove non-JNI local reference, dumping thread
01-25 13:05:44.761 1538-1564/system_process I/ActivityManager: Start proc 2766:com.android.defcontainer/u0a3 for service com.android.defcontainer/.DefaultContainerService
01-25 13:05:44.783 1538-1564/system_process W/PackageParser: Unknown element under <manifest>: meta-data at /data/app/vmdl23057665.tmp/base.apk Binary XML file line #11
01-25 13:05:44.813 1538-1992/system_process I/ActivityManager: Start proc 2781:com.android.exchange/u0a30 for service com.android.exchange/.service.EasService
01-25 13:05:44.829 2781-2781/? W/System: ClassLoader referenced unknown path: /system/app/Exchange2/lib/x86
01-25 13:05:44.831 2743-2797/? D/ActivityThread: Loading provider com.android.email.provider;com.android.email.notifier: com.android.email.provider.EmailProvider
01-25 13:05:44.832 2743-2799/? D/ActivityThread: Loading provider com.android.email.provider;com.android.email.notifier: com.android.email.provider.EmailProvider
01-25 13:05:44.873 1198-1198/? I/SELinux: SELinux: Loaded file_contexts contexts from /file_contexts.
01-25 13:05:44.873 1538-1564/system_process I/PackageManager.DexOptimizer: Running dexopt (dex2oat) on: /data/app/vmdl23057665.tmp/base.apk pkg=com.teddyxiong53.www.xhl_simple_view isa=x86 vmSafeMode=false debuggable=true oatDir = /data/app/vmdl23057665.tmp/oat
01-25 13:05:44.938 1538-2069/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.938 1538-1552/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.977 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.977 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:44.985 1538-1927/system_process W/ActivityManager: Unable to start service Intent { cmp=com.android.email/.service.AttachmentService } U=0: not found
01-25 13:05:44.987 1538-1904/system_process W/ActivityManager: Unable to start service Intent { cmp=com.android.email/.service.AttachmentService } U=0: not found
01-25 13:05:44.992 1538-1992/system_process W/ActivityManager: Unable to start service Intent { cmp=com.android.email/.service.AttachmentService } U=0: not found
01-25 13:05:44.996 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.000 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.001 1848-1848/com.android.inputmethod.latin I/SystemBroadcastReceiver: Boot has been completed
01-25 13:05:45.001 1848-1848/com.android.inputmethod.latin I/SystemBroadcastReceiver: toggleAppIcon() : FLAG_SYSTEM = true
01-25 13:05:45.008 2743-2804/? I/Email: Observing account changes for notifications
01-25 13:05:45.018 1538-1551/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.019 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.053 2167-2807/com.google.android.gms D/LocationInitializer: Restart initialization of location
01-25 13:05:45.062 1861-1861/com.google.android.gms.persistent D/AuthorizationBluetoothService: Received GmsCore event: Intent { act=com.google.android.gms.INITIALIZE flg=0x10 pkg=com.google.android.gms cmp=com.google.android.gms/.auth.be.proximity.authorization.bt.AuthorizationBluetoothService$AutoStarter }.
01-25 13:05:45.069 1538-2069/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.071 1861-1861/com.google.android.gms.persistent V/GLSActivity: AuthDelegateWrapperCreated with selected intent: Intent { cmp=com.google.android.gms/.auth.DefaultAuthDelegateService }
01-25 13:05:45.071 1861-1861/com.google.android.gms.persistent V/GLSActivity: AuthDelegateWrapperCreated with selected intent: Intent { cmp=com.google.android.gms/.auth.DefaultAuthDelegateService }
01-25 13:05:45.073 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.077 1538-2069/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.079 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.084 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.085 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.100 2424-2424/com.android.calendar D/AlertReceiver: onReceive: a=android.intent.action.PROVIDER_CHANGED Intent { act=android.intent.action.PROVIDER_CHANGED dat=content://com.android.calendar flg=0x10 cmp=com.android.calendar/.alerts.AlertReceiver }
01-25 13:05:45.110 2424-2811/com.android.calendar D/AlertService: 0 Action = android.intent.action.PROVIDER_CHANGED
01-25 13:05:45.120 2072-2399/com.google.android.googlequicksearchbox:search W/Search.SearchUrlHelper: Auth token not ready, no auth header set.
01-25 13:05:45.136 2743-2743/? E/ActivityThread: Service com.android.email.service.EmailBroadcastProcessorService has leaked ServiceConnection com.android.emailcommon.service.ServiceProxy$ProxyConnection@5663cb7 that was originally bound here
                                                 android.app.ServiceConnectionLeaked: Service com.android.email.service.EmailBroadcastProcessorService has leaked ServiceConnection com.android.emailcommon.service.ServiceProxy$ProxyConnection@5663cb7 that was originally bound here
                                                     at android.app.LoadedApk$ServiceDispatcher.<init>(LoadedApk.java:1092)
                                                     at android.app.LoadedApk.getServiceDispatcher(LoadedApk.java:986)
                                                     at android.app.ContextImpl.bindServiceCommon(ContextImpl.java:1303)
                                                     at android.app.ContextImpl.bindService(ContextImpl.java:1286)
                                                     at android.content.ContextWrapper.bindService(ContextWrapper.java:604)
                                                     at com.android.emailcommon.service.ServiceProxy.setTask(ServiceProxy.java:181)
                                                     at com.android.emailcommon.service.ServiceProxy.test(ServiceProxy.java:224)
                                                     at com.android.email.service.EmailServiceUtils.isServiceAvailable(EmailServiceUtils.java:160)
                                                     at com.android.email.provider.AccountReconciler.reconcileAccountsInternal(AccountReconciler.java:171)
                                                     at com.android.email.provider.AccountReconciler.reconcileAccounts(AccountReconciler.java:115)
                                                     at com.android.email.service.EmailBroadcastProcessorService.reconcileAndStartServices(EmailBroadcastProcessorService.java:305)
                                                     at com.android.email.service.EmailBroadcastProcessorService.onBootCompleted(EmailBroadcastProcessorService.java:295)
                                                     at com.android.email.service.EmailBroadcastProcessorService.onHandleIntent(EmailBroadcastProcessorService.java:130)
                                                     at android.app.IntentService$ServiceHandler.handleMessage(IntentService.java:66)
                                                     at android.os.Handler.dispatchMessage(Handler.java:102)
                                                     at android.os.Looper.loop(Looper.java:148)
                                                     at android.os.HandlerThread.run(HandlerThread.java:61)
01-25 13:05:45.139 2781-2781/? I/Exchange: EasService.onCreate
01-25 13:05:45.140 2803-2803/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:45.140 2803-2803/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:45.140 2803-2803/? W/dex2oat: /system/bin/dex2oat --zip-fd=6 --zip-location=base.apk --oat-fd=7 --oat-location=/data/app/vmdl23057665.tmp/oat/x86/base.odex --instruction-set=x86 --instruction-set-variant=x86 --instruction-set-features=default --runtime-arg -Xms64m --runtime-arg -Xmx512m --swap-fd=8 --debuggable
01-25 13:05:45.146 2803-2803/? I/dex2oat: /system/bin/dex2oat --debuggable
01-25 13:05:45.146 2803-2803/? E/cutils-trace: Error opening trace file: Permission denied (13)
01-25 13:05:45.156 2781-2817/? I/Exchange: RestartPingTask
01-25 13:05:45.173 2781-2781/? I/Exchange: RestartPingsTask did not start any pings.
01-25 13:05:45.173 2781-2781/? I/Exchange: PSS stopIfIdle
01-25 13:05:45.173 2781-2781/? I/Exchange: PSS has no active accounts; stopping service.
01-25 13:05:45.214 2072-2399/com.google.android.googlequicksearchbox:search W/art: Attempt to remove non-JNI local reference, dumping thread
01-25 13:05:45.219 1538-1598/system_process D/WifiService: New client listening to asynchronous messages
01-25 13:05:45.234 1861-1861/com.google.android.gms.persistent I/GoogleURLConnFactory: Using platform SSLCertificateSocketFactory
01-25 13:05:45.245 2781-2781/? I/Exchange: onDestroy
01-25 13:05:45.250 1861-2823/com.google.android.gms.persistent I/PhenotypeConfigurator: Scheduling Phenotype every 14400 seconds, with flex of 1800 seconds
01-25 13:05:45.265 1861-1861/com.google.android.gms.persistent V/UserPresentBroadcastReceiver: Received Intent { act=android.intent.action.USER_PRESENT flg=0x24000010 cmp=com.google.android.gms/.auth.trustagent.UserPresentBroadcastReceiver }.
01-25 13:05:45.295 1861-2831/com.google.android.gms.persistent I/PhenotypeConfigurator: Scheduling Phenotype for one-off execution 2754 seconds from now (1516885545294)
01-25 13:05:45.307 2167-2833/com.google.android.gms D/LocationInitializer: Restart initialization of location
01-25 13:05:45.317 2803-2803/? I/dex2oat: dex2oat took 178.447ms (threads: 2) arena alloc=134KB java alloc=70KB native alloc=1001KB free=1814KB
01-25 13:05:45.319 1861-1861/com.google.android.gms.persistent D/AuthorizationBluetoothService: Received GmsCore event: Intent { act=com.google.android.gms.INITIALIZE flg=0x10 pkg=com.google.android.gms cmp=com.google.android.gms/.auth.be.proximity.authorization.bt.AuthorizationBluetoothService$AutoStarter }.
01-25 13:05:45.322 1538-1554/system_process I/ActivityManager: Force stopping com.teddyxiong53.www.xhl_simple_view appid=10059 user=-1: uninstall pkg
01-25 13:05:45.367 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.367 1861-1861/com.google.android.gms.persistent V/GLSActivity: AuthDelegateWrapperCreated with selected intent: Intent { cmp=com.google.android.gms/.auth.DefaultAuthDelegateService }
01-25 13:05:45.367 1538-1552/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.368 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.369 1538-1992/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.372 1538-1927/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.372 1538-1564/system_process I/PackageManager: Package com.teddyxiong53.www.xhl_simple_view codePath changed from /data/app/com.teddyxiong53.www.xhl_simple_view-2 to /data/app/com.teddyxiong53.www.xhl_simple_view-1; Retaining data and using new
01-25 13:05:45.374 1538-1564/system_process W/PackageManager: Code path for com.teddyxiong53.www.xhl_simple_view changing from /data/app/com.teddyxiong53.www.xhl_simple_view-2 to /data/app/com.teddyxiong53.www.xhl_simple_view-1
01-25 13:05:45.374 1538-1564/system_process W/PackageManager: Resource path for com.teddyxiong53.www.xhl_simple_view changing from /data/app/com.teddyxiong53.www.xhl_simple_view-2 to /data/app/com.teddyxiong53.www.xhl_simple_view-1
01-25 13:05:45.378 1538-1554/system_process I/ActivityManager: Force stopping com.teddyxiong53.www.xhl_simple_view appid=10059 user=-1: replace pkg
01-25 13:05:45.430 1538-1564/system_process W/Settings: Setting install_non_market_apps has moved from android.provider.Settings.Global to android.provider.Settings.Secure, returning read-only value.
01-25 13:05:45.430 1538-1564/system_process I/art: Starting a blocking GC Explicit
01-25 13:05:45.453 1538-1564/system_process I/art: Explicit concurrent mark sweep GC freed 25666(1450KB) AllocSpace objects, 9(200KB) LOS objects, 33% free, 7MB/10MB, paused 1.179ms total 22.157ms
01-25 13:05:45.469 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/base.apk, retcode=-1
01-25 13:05:45.470 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_dependencies_apk.apk, retcode=-1
01-25 13:05:45.470 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_0_apk.apk, retcode=-1
01-25 13:05:45.470 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_1_apk.apk, retcode=-1
01-25 13:05:45.470 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_2_apk.apk, retcode=-1
01-25 13:05:45.473 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_3_apk.apk, retcode=-1
01-25 13:05:45.473 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_4_apk.apk, retcode=-1
01-25 13:05:45.474 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_5_apk.apk, retcode=-1
01-25 13:05:45.474 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_6_apk.apk, retcode=-1
01-25 13:05:45.474 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_7_apk.apk, retcode=-1
01-25 13:05:45.474 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_8_apk.apk, retcode=-1
01-25 13:05:45.475 1538-1564/system_process W/PackageManager: Couldn't remove dex file for package:  at location /data/app/com.teddyxiong53.www.xhl_simple_view-2/split_lib_slice_9_apk.apk, retcode=-1
01-25 13:05:45.475 1198-1198/? E/installd: Couldn't opendir /data/app/vmdl23057665.tmp: No such file or directory
01-25 13:05:45.478 1538-1564/system_process I/ActivityManager: Force stopping com.teddyxiong53.www.xhl_simple_view appid=10059 user=0: pkg removed
01-25 13:05:45.479 2740-2740/? I/art: System.exit called, status: 0
01-25 13:05:45.479 2740-2740/? I/AndroidRuntime: VM exiting with result code 0.
01-25 13:05:45.489 1538-1538/system_process D/JobSchedulerService: Receieved: android.intent.action.PACKAGE_REMOVED
01-25 13:05:45.491 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000010
01-25 13:05:45.495 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000010
01-25 13:05:45.498 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000010
01-25 13:05:45.549 1870-1870/com.android.phone D/CarrierServiceBindHelper: Receive action: android.intent.action.PACKAGE_REMOVED
01-25 13:05:45.561 1870-1870/com.android.phone D/CarrierServiceBindHelper: Receive action: android.intent.action.PACKAGE_ADDED
01-25 13:05:45.561 1870-1870/com.android.phone D/CarrierServiceBindHelper: Receive action: android.intent.action.PACKAGE_REPLACED
01-25 13:05:45.562 1870-1870/com.android.phone D/CarrierServiceBindHelper: mHandler: 3
01-25 13:05:45.562 1870-1870/com.android.phone D/CarrierServiceBindHelper: mHandler: 3
01-25 13:05:45.562 1870-1870/com.android.phone D/CarrierServiceBindHelper: mHandler: 3
01-25 13:05:45.562 1870-1870/com.android.phone D/CarrierConfigLoader: mHandler: 9 phoneId: 0
01-25 13:05:45.623 1538-1904/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:45.683 2167-2178/com.google.android.gms W/SQLiteConnectionPool: A SQLiteConnection object for database '/data/user/0/com.google.android.gms/databases/networkstatistics.sqlite' was leaked!  Please fix your application to end transactions in progress properly and to close the database when it is no longer needed.
01-25 13:05:45.777 2167-2167/com.google.android.gms D/SnetService: snet destroyed
01-25 13:05:45.780 1891-2116/com.google.android.googlequicksearchbox D/WidgetsModel: com.google.android.googlequicksearchbox is filtered and not added to the widget tray.
01-25 13:05:45.927 2861-2861/? D/AndroidRuntime: >>>>>> START com.android.internal.os.RuntimeInit uid 0 <<<<<<
01-25 13:05:45.929 2861-2861/? D/AndroidRuntime: CheckJNI is ON
01-25 13:05:45.941 2861-2861/? D/ICU: No timezone override file found: /data/misc/zoneinfo/current/icu/icu_tzdata.dat
01-25 13:05:45.946 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.games from APK com.google.android.gms
01-25 13:05:45.947 2167-2862/com.google.android.gms D/PackageBroadcastService: Received broadcast action=android.intent.action.PACKAGE_REMOVED and uri=com.teddyxiong53.www.xhl_simple_view
01-25 13:05:45.953 1861-1861/com.google.android.gms.persistent E/NetworkScheduler.SchedulerReceiver: Invalid parameter app
01-25 13:05:45.953 1861-1861/com.google.android.gms.persistent E/NetworkScheduler.SchedulerReceiver: Invalid package name : Perhaps you didn't include a PendingIntent in the extras?
01-25 13:05:45.966 2573-2573/com.android.keychain W/ContextImpl: Calling a method in the system process without a qualified user: android.app.ContextImpl.startService:1221 android.content.ContextWrapper.startService:581 android.content.ContextWrapper.startService:581 com.android.keychain.KeyChainBroadcastReceiver.onReceive:12 android.app.ActivityThread.handleReceiver:2725 
01-25 13:05:45.972 2861-2861/? E/memtrack: Couldn't load memtrack module (No such file or directory)
01-25 13:05:45.972 2861-2861/? E/android.os.Debug: failed to load memtrack module: -2
01-25 13:05:45.979 2861-2861/? I/Radio-JNI: register_android_hardware_Radio DONE
01-25 13:05:45.993 2861-2861/? D/AndroidRuntime: Calling main entry com.android.commands.am.Am
01-25 13:05:46.000 1538-1892/system_process I/ActivityManager: START u0 {act=android.intent.action.MAIN cat=[android.intent.category.LAUNCHER] flg=0x10000000 cmp=com.teddyxiong53.www.xhl_simple_view/.MainActivity} from uid 0 on display 0
01-25 13:05:46.006 2167-2877/com.google.android.gms D/PackageBroadcastService: Received broadcast action=android.intent.action.PACKAGE_ADDED and uri=com.teddyxiong53.www.xhl_simple_view
01-25 13:05:46.014 2861-2861/? D/AndroidRuntime: Shutting down VM
01-25 13:05:46.017 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.games from APK com.google.android.gms
01-25 13:05:46.026 2878-2878/? I/art: Not late-enabling -Xcheck:jni (already on)
01-25 13:05:46.028 1538-1648/system_process I/ActivityManager: Start proc 2878:com.teddyxiong53.www.xhl_simple_view/u0a59 for activity com.teddyxiong53.www.xhl_simple_view/.MainActivity
01-25 13:05:46.047 2878-2884/? E/art: Failed sending reply to debugger: Broken pipe
01-25 13:05:46.047 2878-2884/? I/art: Debugger is no longer active
01-25 13:05:46.049 2167-2686/com.google.android.gms I/Icing: Storage manager: low false usage 1.60MB avail 634.39MB capacity 779.29MB
01-25 13:05:46.090 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.gass from APK com.google.android.gms
01-25 13:05:46.108 2167-2167/com.google.android.gms D/AsyncTaskServiceImpl: Submit a task: k
01-25 13:05:46.126 2893-2893/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.126 2893-2893/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.126 2893-2893/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_dependencies_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_dependencies_apk.apk@classes.dex
01-25 13:05:46.126 2893-2893/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_dependencies_apk.apk@classes.dex: Permission denied
01-25 13:05:46.126 2893-2893/? I/dex2oat: dex2oat took 938.320us (threads: 2) 
01-25 13:05:46.134 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_dependencies_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_dependencies_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.146 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.gass from APK com.google.android.gms
01-25 13:05:46.165 1538-1551/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.186 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.vision from APK com.google.android.gms
01-25 13:05:46.186 2167-2901/com.google.android.gms D/k: Processing package: com.teddyxiong53.www.xhl_simple_view
01-25 13:05:46.254 1891-2151/com.google.android.googlequicksearchbox E/Surface: getSlotFromBufferLocked: unknown buffer: 0xaec746b0
01-25 13:05:46.275 2167-2901/com.google.android.gms D/GassUtils: Found app info for package com.teddyxiong53.www.xhl_simple_view:1. Hash: 907aea2085f73d1399d37c964d4224ad97a4f0a406668377cb8e118fd10e2d7e
01-25 13:05:46.275 2167-2901/com.google.android.gms D/k: Found info for package com.teddyxiong53.www.xhl_simple_view in db.
01-25 13:05:46.327 1538-1992/system_process I/ActivityManager: Start proc 2907:com.svox.pico/u0a43 for broadcast com.svox.pico/.VoiceDataInstallerReceiver
01-25 13:05:46.361 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.362 2167-2895/com.google.android.gms I/PeopleContactsSync: triggerPendingContactsCleanup: no accounts
01-25 13:05:46.370 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.376 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.378 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.gass from APK com.google.android.gms
01-25 13:05:46.378 2167-2921/com.google.android.gms D/PackageBroadcastService: Received broadcast action=android.intent.action.PACKAGE_REPLACED and uri=com.teddyxiong53.www.xhl_simple_view
01-25 13:05:46.385 2167-2167/com.google.android.gms D/AsyncTaskServiceImpl: Submit a task: k
01-25 13:05:46.405 2922-2922/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.405 2922-2922/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.405 2922-2922/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_0_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_0_apk.apk@classes.dex
01-25 13:05:46.405 2922-2922/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_0_apk.apk@classes.dex: Permission denied
01-25 13:05:46.405 2922-2922/? I/dex2oat: dex2oat took 1.141ms (threads: 2) 
01-25 13:05:46.406 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_0_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_0_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.415 2167-2895/com.google.android.gms I/PeopleDatabaseHelper: cleanUpNonGplusAccounts done.
01-25 13:05:46.420 2167-2901/com.google.android.gms D/k: Processing package: com.teddyxiong53.www.xhl_simple_view
01-25 13:05:46.421 2925-2925/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.421 2925-2925/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.421 2925-2925/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_1_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_1_apk.apk@classes.dex
01-25 13:05:46.421 2925-2925/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_1_apk.apk@classes.dex: Permission denied
01-25 13:05:46.421 2925-2925/? I/dex2oat: dex2oat took 589.940us (threads: 2) 
01-25 13:05:46.422 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_1_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_1_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.437 2928-2928/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.437 2928-2928/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.437 2928-2928/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_2_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_2_apk.apk@classes.dex
01-25 13:05:46.437 2928-2928/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_2_apk.apk@classes.dex: Permission denied
01-25 13:05:46.437 2928-2928/? I/dex2oat: dex2oat took 284.220us (threads: 2) 
01-25 13:05:46.438 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_2_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_2_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.451 2167-2167/com.google.android.gms D/ChimeraCfgMgr: Loading module com.google.android.gms.vision from APK com.google.android.gms
01-25 13:05:46.452 2930-2930/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.452 2930-2930/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.452 2930-2930/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_3_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_3_apk.apk@classes.dex
01-25 13:05:46.452 2930-2930/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_3_apk.apk@classes.dex: Permission denied
01-25 13:05:46.452 2930-2930/? I/dex2oat: dex2oat took 290.640us (threads: 2) 
01-25 13:05:46.453 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_3_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_3_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.454 2167-2901/com.google.android.gms D/GassUtils: Found app info for package com.teddyxiong53.www.xhl_simple_view:1. Hash: 907aea2085f73d1399d37c964d4224ad97a4f0a406668377cb8e118fd10e2d7e
01-25 13:05:46.454 2167-2901/com.google.android.gms D/k: Found info for package com.teddyxiong53.www.xhl_simple_view in db.
01-25 13:05:46.462 2072-2906/com.google.android.googlequicksearchbox:search I/UpdateIcingCorporaServi: Updating corpora: APPS=com.teddyxiong53.www.xhl_simple_view, CONTACTS=MAYBE
01-25 13:05:46.468 2933-2933/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.469 2933-2933/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.469 2933-2933/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_4_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_4_apk.apk@classes.dex
01-25 13:05:46.469 2933-2933/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_4_apk.apk@classes.dex: Permission denied
01-25 13:05:46.469 2933-2933/? I/dex2oat: dex2oat took 1.686ms (threads: 2) 
01-25 13:05:46.471 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_4_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_4_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.476 1861-1861/com.google.android.gms.persistent E/NetworkScheduler.SchedulerReceiver: Invalid parameter app
01-25 13:05:46.476 1861-1861/com.google.android.gms.persistent E/NetworkScheduler.SchedulerReceiver: Invalid package name : Perhaps you didn't include a PendingIntent in the extras?
01-25 13:05:46.483 2937-2937/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.483 2937-2937/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.483 2937-2937/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_5_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_5_apk.apk@classes.dex
01-25 13:05:46.483 2937-2937/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_5_apk.apk@classes.dex: Permission denied
01-25 13:05:46.483 2937-2937/? I/dex2oat: dex2oat took 834.060us (threads: 2) 
01-25 13:05:46.483 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_5_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_5_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.499 2942-2942/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.499 2942-2942/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.501 2942-2942/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_6_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_6_apk.apk@classes.dex
01-25 13:05:46.501 2942-2942/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_6_apk.apk@classes.dex: Permission denied
01-25 13:05:46.501 2942-2942/? I/dex2oat: dex2oat took 2.656ms (threads: 2) 
01-25 13:05:46.503 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_6_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_6_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.512 2945-2945/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.512 2945-2945/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.512 2945-2945/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_7_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_7_apk.apk@classes.dex
01-25 13:05:46.512 2945-2945/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_7_apk.apk@classes.dex: Permission denied
01-25 13:05:46.512 2945-2945/? I/dex2oat: dex2oat took 312.780us (threads: 2) 
01-25 13:05:46.513 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_7_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_7_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.514 1538-1892/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.516 2167-2895/com.google.android.gms I/PeopleContactsSync: triggerPendingContactsCleanup: no accounts
01-25 13:05:46.528 2948-2948/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.528 2948-2948/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.528 2948-2948/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_8_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_8_apk.apk@classes.dex
01-25 13:05:46.529 2948-2948/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_8_apk.apk@classes.dex: Permission denied
01-25 13:05:46.529 2948-2948/? I/dex2oat: dex2oat took 293.530us (threads: 2) 
01-25 13:05:46.532 1538-1551/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.533 2167-2895/com.google.android.gms I/PeopleContactsSync: triggerPendingContactsCleanup: no accounts
01-25 13:05:46.536 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_8_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_8_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.549 2951-2951/? W/dex2oat: Unexpected CPU variant for X86 using defaults: x86
01-25 13:05:46.549 2951-2951/? W/dex2oat: Mismatch between dex2oat instruction set features (ISA: X86 Feature string: smp,-ssse3,-sse4.1,-sse4.2,-avx,-avx2) and those of dex2oat executable (ISA: X86 Feature string: smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2) for the command line:
01-25 13:05:46.550 2951-2951/? W/dex2oat: /system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_9_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_9_apk.apk@classes.dex
01-25 13:05:46.550 2951-2951/? E/dex2oat: Failed to create oat file: /data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_9_apk.apk@classes.dex: Permission denied
01-25 13:05:46.550 2951-2951/? I/dex2oat: dex2oat took 304.760us (threads: 2) 
01-25 13:05:46.550 2878-2878/? W/art: Failed execv(/system/bin/dex2oat --runtime-arg -classpath --runtime-arg  --debuggable --instruction-set=x86 --instruction-set-features=smp,ssse3,-sse4.1,-sse4.2,-avx,-avx2 --runtime-arg -Xrelocate --boot-image=/system/framework/boot.art --runtime-arg -Xms64m --runtime-arg -Xmx512m --instruction-set-variant=x86 --instruction-set-features=default --dex-file=/data/app/com.teddyxiong53.www.xhl_simple_view-1/split_lib_slice_9_apk.apk --oat-file=/data/dalvik-cache/x86/data@app@com.teddyxiong53.www.xhl_simple_view-1@split_lib_slice_9_apk.apk@classes.dex) because non-0 exit status
01-25 13:05:46.551 2878-2878/? W/System: ClassLoader referenced unknown path: /data/app/com.teddyxiong53.www.xhl_simple_view-1/lib/x86
01-25 13:05:46.553 2878-2878/? I/InstantRun: starting instant run server: is main process
01-25 13:05:46.580 1186-1265/? E/SurfaceFlinger: ro.sf.lcd_density must be defined as a build property
01-25 13:05:46.580 2878-2954/? D/OpenGLRenderer: Use EGL_SWAP_BEHAVIOR_PRESERVED: true
                                                 
                                                 [ 01-25 13:05:46.592  2878: 2878 D/         ]
                                                 HostConnection::get() New Host Connection established 0xb2f7f230, tid 2878
01-25 13:05:46.651 1538-1552/system_process I/AccountManagerService: getTypesVisibleToCaller: isPermitted? true
01-25 13:05:46.653 2167-2686/com.google.android.gms I/Icing: updateResources: need to parse f{com.google.android.gms}
                                                             
                                                             [ 01-25 13:05:46.716  2878: 2954 D/         ]
                                                             HostConnection::get() New Host Connection established 0xaec52af0, tid 2954
01-25 13:05:46.721 2878-2954/? I/OpenGLRenderer: Initialized EGL, version 1.4
01-25 13:05:46.790 2878-2954/? W/EGL_emulation: eglSurfaceAttrib not implemented
01-25 13:05:46.790 2878-2954/? W/OpenGLRenderer: Failed to set EGL_SWAP_BEHAVIOR on surface 0xaab15120, error=EGL_SUCCESS
01-25 13:05:46.937 1538-1559/system_process I/ActivityManager: Displayed com.teddyxiong53.www.xhl_simple_view/.MainActivity: +921ms
01-25 13:05:46.988 2167-2686/com.google.android.gms I/Icing: Internal init done: storage state 0
01-25 13:05:47.028 2167-2686/com.google.android.gms I/Icing: Post-init done
01-25 13:05:47.440 2072-2906/com.google.android.googlequicksearchbox:search I/UpdateIcingCorporaServi: UpdateCorporaTask done [took 978 ms] updated apps [took 978 ms] 
01-25 13:05:48.473 2167-2686/com.google.android.gms I/Icing: Indexing 320165C3F7D8BC58F4832236E93ABB0120291E70 from com.google.android.gms
01-25 13:05:48.489 2167-2686/com.google.android.gms D/Icing: Loaded CLD2 Version V2.0 - 20141016
01-25 13:05:48.492 2167-2686/com.google.android.gms I/Icing: Indexing EFF1C1B9160EC36BD56CF39015B064BF6AC2BBD2 from com.google.android.googlequicksearchbox
01-25 13:05:48.509 2167-2686/com.google.android.gms I/Icing: Indexing done 320165C3F7D8BC58F4832236E93ABB0120291E70
01-25 13:05:48.516 2167-2686/com.google.android.gms I/Icing: Indexing done EFF1C1B9160EC36BD56CF39015B064BF6AC2BBD2
01-25 13:05:50.146 2424-2811/com.android.calendar I/GlobalDismissManager: no sender configured
01-25 13:05:50.147 2424-2811/com.android.calendar D/AlertService: Beginning updateAlertNotification
01-25 13:05:50.158 2424-2811/com.android.calendar D/AlertService: No fired or scheduled alerts
01-25 13:05:50.167 2424-2811/com.android.calendar D/AlertService: Scheduling next alarm with AlarmScheduler. sEventReminderReceived: null
01-25 13:05:50.173 2424-2811/com.android.calendar D/AlarmScheduler: No events found starting within 1 week.
01-25 13:05:52.106 1538-1587/system_process I/InputReader: Reconfiguring input devices.  changes=0x00000010
01-25 13:05:52.117 2167-3032/com.google.android.gms D/PackageBroadcastService: Received broadcast action=android.intent.action.PACKAGE_CHANGED and uri=com.google.android.gms
01-25 13:05:52.124 2167-3032/com.google.android.gms I/PackageBroadcastService: Null package name or gms related package.  Ignoreing.
01-25 13:05:52.127 2072-3034/com.google.android.googlequicksearchbox:search I/UpdateIcingCorporaServi: Updating corpora: APPS=com.google.android.gms, CONTACTS=MAYBE
01-25 13:05:52.156 2167-2686/com.google.android.gms I/Icing: updateResources: need to parse f{com.google.android.gms}
01-25 13:05:52.156 2072-3034/com.google.android.googlequicksearchbox:search I/UpdateIcingCorporaServi: UpdateCorporaTask done [took 29 ms] updated apps [took 29 ms] 
01-25 13:05:52.178 1861-1861/com.google.android.gms.persistent I/GCoreNlp: shouldConfirmNlp, NLP off. Ensuring opt-in disabled
01-25 13:05:52.192 1891-2116/com.google.android.googlequicksearchbox D/WidgetsModel: com.google.android.googlequicksearchbox is filtered and not added to the widget tray.
01-25 13:05:53.115 2167-3056/com.google.android.gms I/iu.UploadsManager: End new media; added: 0, uploading: 0, time: 30 ms
01-25 13:05:53.264 2167-2686/com.google.android.gms I/Icing: Indexing 320165C3F7D8BC58F4832236E93ABB0120291E70 from com.google.android.gms
01-25 13:05:53.265 2167-2686/com.google.android.gms I/Icing: Indexing done 320165C3F7D8BC58F4832236E93ABB0120291E70
01-25 13:05:54.825 1538-1992/system_process I/ActivityManager: Killing 1673:com.android.externalstorage/u0a6 (adj 15): empty #17
01-25 13:05:59.437 1538-1554/system_process I/ActivityManager: Waited long enough for: ServiceRecord{89191d u0 com.google.android.googlequicksearchbox/com.google.android.velvet.VelvetBackgroundTasksImpl$Service}
01-25 13:05:59.464 1538-1554/system_process I/ActivityManager: Waited long enough for: ServiceRecord{38cd563 u0 com.android.calendar/.alerts.InitAlarmsService}
01-25 13:06:02.089 2167-2528/com.google.android.gms I/CheckinService: Done disabling old GoogleServicesFramework version
01-25 13:06:05.285 1538-1892/system_process I/ActivityManager: Killing 1914:com.android.printspooler/u0a44 (adj 15): empty #17
01-25 13:06:12.138 2167-2540/com.google.android.gms E/GCM: Failed registration SERVICE_NOT_AVAILABLE alarm=76800000
01-25 13:06:14.508 2424-2738/com.android.calendar D/InitAlarmsService: Clearing and rescheduling alarms.
01-25 13:06:14.520 1538-1648/system_process I/ActivityManager: Killing 2402:com.android.settings/1000 (adj 15): empty #17

```

