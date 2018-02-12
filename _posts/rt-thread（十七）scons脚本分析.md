---
title: rt-thread（十七）scons脚本分析
date: 2018-02-12 11:27:37
tags:
	- rt-thread
	- scons

---



现在分析scons脚本。

menuconfig是这里进来的。

```
    if env['PLATFORM'] != 'win32':
        AddOption('--menuconfig', 
                    dest = 'menuconfig',
                    action = 'store_true',
                    default = False,
                    help = 'make menuconfig for RT-Thread BSP')
        if GetOption('menuconfig'):
            from menuconfig import menuconfig
            menuconfig(Rtt_Root)
            exit(0)
```



自己来写这个编译脚本。建立目录结构如下。

```
pi@raspberrypi:~/work/test/scons$ tree
.
├── bsp
│   └── qemu-vexpress-a9
│       ├── rtconfig.py
│       ├── SConscript
│       └── SConstruct
└── tools
    └── building.py
```

先从SConstruct开始写。

先写这样：

```
import os,sys,rtconfig

if os.getenv('RTT_ROOT'):
    RTT_ROOT = os.getenv('RTT_ROOT')
else:
    RTT_ROOT = os.path.normpath(os.getcwd() + '/../..')
sys.path = sys.path + [os.path.join(RTT_ROOT, 'tools')]
from building import *

```

在bsp/qemu-express-a9目录下执行scons，不报错。说明：

1、直接引入本目录的rtconfig可以。虽然这个文件是空的。

2、sys.path添加了tools目录马上可以生效，所以可以引入tools目录下的building.py，也是空的。



接下来要使用rtconfig.py里的东西了。我定义一下。

```
import os
ARCH='arm'
CPU='vexpress-a9'
CROSS_TOOL='gcc'

PLATFORM = 'gcc'
EXEC_PATH='/usr/bin'

BUILD='debug'

PREFIX='arm-none-eabi-'
CC = PREFIX + 'gcc'
CXX = PREFIX + 'g++'
AS = PREFIX + 'gcc'
AR = PREFIX + 'ar'
LINK = PREFIX + 'gcc'
TARGET_EXT = 'elf'
SIZE = PREFIX + 'size'
OBJDUMP = PREFIX + 'objdump'
OBJCPY = PREFIX + 'objcopy'

DEVICE = ' -march=armv7-a -marm -msoft-flaot'
CFLAGS = DEVICE + ' -Wall'
AFLAGS = ' -c' + DEVICE + ' -x assembler-with-cpp -D__ASSEMBLER__'
LINK_SCRIPT = 'link.lds'
LFLAGS = DEVICE + ' -nostartfiles -Wl,--gc-sections,-Map=rtthread.map,-cref,-u,system_vectors' + ' -T %s' % LINK_SCRIPT

CPATH = ''
LPATH = ''
AFLAGS += ' -gdwarf-2'
CFLAGS += ' -g -gdwarf-2'

if BUILD == 'debug':
    CFLAGS += ' -O0'
else:
    CLFAGS += ' -O2'
    
CXXFLAGS = CFLAGS
POST_ACTION = OBJCPY + ' -O binary $TARGET rtthread.bin\n' + SIZE + ' $TARGET \n'
```

接下来要看：

```
env = Environment(tools = ['mingw'],
    AS   = rtconfig.AS, ASFLAGS = rtconfig.AFLAGS,
    CC   = rtconfig.CC, CCFLAGS = rtconfig.CFLAGS,
    CXX  = rtconfig.CXX, CXXFLAGS = rtconfig.CXXFLAGS,
    AR   = rtconfig.AR, ARFLAGS = '-rc',
    LINK = rtconfig.LINK, LINKFLAGS = rtconfig.LFLAGS)
```

Environment这个类在哪里呢？我们打开scons的源代码目录看看。

从mingw看Windows的安装目录是这个。 /c/Python27/Lib/site-packages/scons-2.4.1/SCons。

```
Environment = Base
```

Environment其实是Base的别名。

AS这些东西在scons源代码了又是如何体现的呢？

```
dict = {
            'ASFLAGS'       : SCons.Util.CLVar(''),
            'CFLAGS'        : SCons.Util.CLVar(''),
            'CCFLAGS'       : SCons.Util.CLVar(''),
            'CXXFLAGS'      : SCons.Util.CLVar(''),
            'CPPDEFINES'    : [],
            'CPPFLAGS'      : SCons.Util.CLVar(''),
            'CPPPATH'       : [],
            'FRAMEWORKPATH' : SCons.Util.CLVar(''),
            'FRAMEWORKS'    : SCons.Util.CLVar(''),
            'LIBPATH'       : [],
            'LIBS'          : [],
            'LINKFLAGS'     : SCons.Util.CLVar(''),
            'RPATH'         : [],
        }
```

tools=['mingw']又是怎么体现的呢？在scons/tools目录下有个mingw.py的文件。

再看：

```
Export('RTT_ROOT')
Export('rtconfig')
```

Export这个符号又是如何体现的呢？

在`scons/Script/__init__.py`里。这里就把输出给外面用的符号整理了一下。

我们用的时候会这样：

```
from Scons.Script import *
```



现在我们开始写building.py的内容。

```
import os,sys,string
from SCons.Script import *

BuildOptions = {}
Projects = []
Rtt_Root = ''
Env = None

def start_handling_includes(self, t=None):
    print "start_handling_includes"
    
def stop_handling_includes(self, t=None):
    print "stop_handling_includes"
PatchedPreProcess = SCons.cpp.PreProcessor
PatchedPreProcess.start_handling_includes = start_handling_includes
PatchedPreProcess.stop_handling_includes = stop_handling_includes

def BuildLibInstallAction(target, source, env):
    print "BuildLibInstallAction"
    
def PrepareBuilding(env, root_directory, has_libcpu=False, remove_components=[]):
    import SCons.cpp
    import rtconfig
    global BuildOptions
    global Projects
    global Env
    global Rtt_Root
    
    Env = env
    Rtt_Root = os.path.abspath(root_directory)
    os.environ['PATH'] = rtconfig.EXEC_PATH + ':' + os.environ['PATH']
    env.PrependENVPath('PATH', rtconfig.EXEC_PATH)
    #print os.getenv('CPPPATH')
    env.Append(CPPPATH=[str(Dir('#').abspath)])
    #print os.getenv('CPPPATH')
    
    act = SCons.Action.Action(BuildLibInstallAction, "install libs")
    bld = Builder(action=act)
    Env.Append(BUILDERS = {'BuildLib':bld})
    
    PreProcessor = PatchedPreProcess()
    
    f = file('rtconfig.h', 'r')
    contents = f.read()
    f.close()
    #print contents
    PreProcessor.process_contents(contents)
    BuildOptions = PreProcessor.cpp_namespace
    #print BuildOptions
    
    bsp_vdir = 'build'
    kernel_vdir = 'build/kernel'
    objs = SConscript('SConscript', variant_dir=bsp_vdir, duplicate=0)
    print objs
```

写到这个样子，准备编译的工作完成了。

自己写一个简单的实用scons工程例子。以后就尽量用scons来做自己的工程。

