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

DEVICE = ' -march=armv7-a -marm -msoft-float'
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