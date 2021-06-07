---
title: qemu之编译
date: 2021-05-31 13:43:11
tags:
	- qemu

---

--

我用qemu来跑buildroot里的，但是居然默认不支持图形界面显示。

我就只能自己编译

必选包：

```
sudo apt-get install git libglib2.0-dev libfdt-dev libpixman-1-dev zlib1g-dev
```



可选包：

```
sudo apt-get install git-email                                                      \
libaio-dev libbluetooth-dev libbrlapi-dev libbz2-dev                                \
libcap-dev libcap-ng-dev libcurl4-gnutls-dev libgtk-3-dev                           \
libibverbs-dev libjpeg8-dev libncurses5-dev libnuma-dev                             \
librbd-dev librdmacm-dev                                                            \
libsasl2-dev libsdl1.2-dev libseccomp-dev libsnappy-dev libssh2-1-dev               \
libvde-dev libvdeplug-dev  libxen-dev liblzo2-dev                    \
valgrind xfslibs-dev --fix-missing

```

从这里下载代码，我下载5.2.0的吧。不要太新了。怕有坑。

https://www.qemu.org/download/#source

我就这样配置

```
 ./configure --enable-gtk --enable-sdl 
```

提示：

```
ERROR: Cannot find Ninja
```

需要

```
sudo apt-get install ninja-build  libsdl2-dev -y
```

配置是这样

```
qemu 5.2.0

                   Install prefix: /usr/local
                   BIOS directory: share/qemu
                    firmware path: /usr/local/share/qemu-firmware
                 binary directory: bin
                library directory: lib
                 module directory: lib/qemu
                libexec directory: libexec
                include directory: include
                 config directory: /usr/local/etc
            local state directory: /usr/local/var
                 Manual directory: share/man
                    Doc directory: /usr/local/share/doc
                  Build directory: /home/teddy/work/tools/qemu-5.2.0/build
                      Source path: /home/teddy/work/tools/qemu-5.2.0
                       GIT binary: git
                   GIT submodules: 
                       C compiler: cc
                  Host C compiler: cc
                     C++ compiler: c++
                          ARFLAGS: rv
                           CFLAGS: -O2 -g
                         CXXFLAGS: -O2 -g
                      QEMU_CFLAGS: -U_FORTIFY_SOURCE -D_FORTIFY_SOURCE=2 -m64 -mcx16 -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE_SOURCE -Wstrict-prototypes -Wredundant-decls -Wundef -Wwrite-strings -Wmissing-prototypes -fno-strict-aliasing -fno-common -fwrapv  -Wold-style-declaration -Wold-style-definition -Wtype-limits -Wformat-security -Wformat-y2k -Winit-self -Wignored-qualifiers -Wempty-body -Wnested-externs -Wendif-labels -Wexpansion-to-defined -Wno-missing-include-dirs -Wno-shift-negative-value -Wno-psabi -fstack-protector-strong
                     QEMU_LDFLAGS: -Wl,--warn-common -Wl,-z,relro -Wl,-z,now -m64  -fstack-protector-strong
                             make: make
                           python: /usr/bin/python3 (version: 3.8)
                     sphinx-build: NO
                      genisoimage: /usr/bin/genisoimage
                    slirp support: internal
                             smbd: "/usr/sbin/smbd"
                   module support: NO
                         host CPU: x86_64
                  host endianness: little
                      target list: aarch64-softmmu alpha-softmmu arm-softmmu avr-softmmu cris-softmmu hppa-softmmu i386-softmmu m68k-softmmu microblazeel-softmmu microblaze-softmmu mips64el-softmmu mips64-softmmu mipsel-softmmu mips-softmmu moxie-softmmu nios2-softmmu or1k-softmmu ppc64-softmmu ppc-softmmu riscv32-softmmu riscv64-softmmu rx-softmmu s390x-softmmu sh4eb-softmmu sh4-softmmu sparc64-softmmu sparc-softmmu tricore-softmmu x86_64-softmmu xtensaeb-softmmu xtensa-softmmu aarch64_be-linux-user aarch64-linux-user alpha-linux-user armeb-linux-user arm-linux-user cris-linux-user hppa-linux-user i386-linux-user m68k-linux-user microblazeel-linux-user microblaze-linux-user mips64el-linux-user mips64-linux-user mipsel-linux-user mips-linux-user mipsn32el-linux-user mipsn32-linux-user nios2-linux-user or1k-linux-user ppc64le-linux-user ppc64-linux-user ppc-linux-user riscv32-linux-user riscv64-linux-user s390x-linux-user sh4eb-linux-user sh4-linux-user sparc32plus-linux-user sparc64-linux-user sparc-linux-user x86_64-linux-user xtensaeb-linux-user xtensa-linux-user
                    gprof enabled: NO
                   sparse enabled: NO
                   strip binaries: YES
                         profiler: NO
                     static build: NO
                      SDL support: YES
                SDL image support: NO
                      GTK support: YES
                   GTK GL support: NO
                           pixman: YES
                      VTE support: NO
                     TLS priority: "NORMAL"
                   GNUTLS support: NO
                        libgcrypt: YES
                             hmac: YES
                              XTS: YES
                           nettle: NO
                         libtasn1: NO
                              PAM: NO
                    iconv support: YES
                   curses support: YES
                    virgl support: NO
                     curl support: YES
                  mingw32 support: NO
                    Audio drivers: pa oss
             Block whitelist (rw): 
             Block whitelist (ro): 
                   VirtFS support: YES
            build virtiofs daemon: YES
                Multipath support: NO
                      VNC support: YES
                 VNC SASL support: YES
                 VNC JPEG support: YES
                  VNC PNG support: YES
                      xen support: YES
                 xen ctrl version: 41100
                   brlapi support: YES
                    Documentation: NO
                              PIE: YES
                      vde support: YES
                   netmap support: NO
                Linux AIO support: YES
           Linux io_uring support: NO
               ATTR/XATTR support: YES
                    Install blobs: YES
                      KVM support: YES
                      HAX support: NO
                      HVF support: NO
                     WHPX support: NO
                      TCG support: YES
                TCG debug enabled: NO
                  TCG interpreter: NO
              malloc trim support: YES
                     RDMA support: NO
                   PVRDMA support: NO
                      fdt support: system
                       membarrier: NO
                   preadv support: YES
                        fdatasync: YES
                          madvise: YES
                    posix_madvise: YES
                   posix_memalign: YES
                libcap-ng support: YES
             vhost-kernel support: YES
                vhost-net support: YES
             vhost-crypto support: YES
               vhost-scsi support: YES
              vhost-vsock support: YES
               vhost-user support: YES
    vhost-user-blk server support: YES
            vhost-user-fs support: YES
               vhost-vdpa support: YES
                   Trace backends: log
                    spice support: NO
                      rbd support: YES
                   xfsctl support: YES
                smartcard support: NO
                      U2F support: NO
                           libusb: NO
                    usb net redir: NO
                   OpenGL support: NO
                   OpenGL dmabufs: NO
                 libiscsi support: NO
                   libnfs support: NO
                build guest agent: YES
                  seccomp support: YES
                coroutine backend: ucontext
                   coroutine pool: YES
                debug stack usage: NO
                  mutex debugging: NO
                     crypto afalg: NO
                GlusterFS support: NO
                             gcov: NO
                      TPM support: YES
                   libssh support: NO
                    QOM debugging: YES
             Live block migration: YES
                      lzo support: YES
                   snappy support: YES
                    bzip2 support: YES
                    lzfse support: NO
                     zstd support: NO
                NUMA host support: YES
                          libxml2: NO
                 memory allocator: system
                avx2 optimization: YES
             avx512f optimization: NO
              replication support: YES
                    bochs support: YES
                    cloop support: YES
                      dmg support: YES
                  qcow v1 support: YES
                      vdi support: YES
                    vvfat support: YES
                      qed support: YES
                parallels support: YES
                 sheepdog support: NO
                         capstone: internal
                  libpmem support: NO
                libdaxctl support: NO
                          libudev: YES
                  default devices: YES
                   plugin support: NO
                  fuzzing support: NO
                              gdb: /usr/bin/gdb
                 thread sanitizer: NO
                         rng-none: NO
                    Linux keyring: YES
```

编译需要较长的时间。

我还是只编译arm和x86_64这2个架构的。

```
 ./configure --enable-sdl --target-list="x86_64-softmmu"
```

这样需要编译的文件，就减少到2800个左右。本来是8400个左右。

但是这样编译了，还是不行。

我还是继续编译看看。

```
 ./configure --enable-sdl --with-sdlabi=2.0 --target-list="x86_64-softmmu"
```

--with-sdlabi=2.0是错误的。不能配置成功。

先完全卸载掉qemu

```
sudo apt-get purge --auto-remove qemu-system-x86
```

再重新make install看看。

```
 ./configure --enable-gtk --enable-vte --target-list="x86_64-softmmu"
```



```
sudo apt-get install libvte-2.91-dev
```



今天浪费了我很多时间。

其实不用去指定Display。默认就有显示的。

但是默认的start-qemu.sh。使用exec来执行qemu-system-x86_64。导致界面一直显示不出来。

我手动执行下面的语句，就一切正常了。

```
qemu-system-x86_64 -M pc -kernel bzImage -drive file=rootfs.ext2,if=virtio,format=raw -append "rootwait root=/dev/vda console=tty1 console=ttyS0"  -net nic,model=virtio -net user
```



# 参考资料

1、

https://wiki.qemu.org/Hosts/Linux#Building_QEMU_for_Linux