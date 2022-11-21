---
title: Linux驱动之音频kernel文档梳理
date: 2022-11-17 11:11:33
tags:
	- Linux驱动

---

--

兜兜转转，发现还是kernel document里的描述是最系统最全面的。

所以把这个文档梳理一下。

层次是这样的：

比较重要的是kernel api、design和soc这3个部分。

```
kernel sound文档
	kernel-api
		alsa-driver-api
			card and device manage
				card management: sound/core/init.c
				device components: sound/core/device.c
				module request and device file entry:
					sound/core/sound.c
				memory management helper:
					sound/core/memory.c
					sound/core/memalloc.c
			pcm api
				pcm core
					sound/core/pcm.c
					sound/core/pcm_lib.c
					sound/core/pcm_native.c
					include/sound/pcm.h
				pcm format helper
					sound/core/pcm_misc.c
				pcm memory management
					sound/core/pcm_memory.c
				pcm dma engine api
					sound/core/pcm_dmaengine.c
					include/sound/dmaengine_pcm.h
					
			control/mixer api
				generic control interface
					sound/core/control.c
				ac97 codec api
					sound/pci/ac97/ac97_codec.c
					sound/pci/ac97/ac97_pcm.c
				virtual master control api
					sound/core/vmaster.c
					include/sound/control.h
			midi api
				raw midi api
					sound/core/rawmidi.c
			proc info api
				proc info interface
					sound/core/info.c
			compress offload
				compress offload api
					sound/core/compress_offload.c
					include/uapi/sound/compress_offload.h
					include/uapi/sound/compress_params.h
					include/sound/compress_driver.h
					
			asoc
				asoc core api
					include/sound/soc.h
					sound/soc/soc-core.c
					sound/soc/soc-devres.c
					sound/soc/soc-io.c
					sound/soc/soc-pcm.c
					sound/soc/soc-ops.c
					sound/soc/soc-compress.c
				asoc dapm api
					sound/soc/soc-dapm.c
					
				asoc dma engine api
					sound/soc/soc-generic-dmaengine-pcm.c
			misc function
				hardware dependent device api
					sound/core/hwdep.c
				jack abstraction layer api
					include/sound/jack.h
					sound/core/jack.c
					sound/core/sock-jack.c
			other helper macros
				include/sound/core.h
				
		writing-an-alsa-driver
	designs
		control-names
		channel-mapping-api
		compress-offload
		timestamping
		jack-controls
		tracepoints
		procfile
		powersave
		oss-emulation
		seq-oss
		
	soc
		overview
		codec
		dai
		dapm
		platform
		machine
		pop-clicks
		clocking
		jack
		dpcm
		codec-to-codec
		
	alsa-configuration
	hd-audio
	cards
```



# kernel-api

## alsa-driver-api

### card and device manage

#### card management: sound/core/init.c

大概1000行。

主要的全局变量有：

```
struct snd_card *snd_cards[SNDRV_CARDS];
	代表了系统里所有的声卡。
	
```



主要的函数有：

```
snd_device_initialize
	被snd_pcm_new_stream等函数调用。
	主要操作是初始化一个device，然后设置为sound_class类型。指定release函数。
snd_card_new
	创建一个声卡。不直接使用。被snd_soc_instantiate_card调用。
snd_card_free
snd_card_register
	也是不直接调用，被snd_soc_instantiate_card调用。
snd_card_info_init
	这个就是创建procfs里的内容。
snd_component_add
	基本没有被使用。只有usb/card.c等处用了。
	
```



#### device components: 

##### sound/core/device.c

200行左右。

主要全局变量：

```
没有
```

主要函数：

```
snd_device_new
	创建一个alsa device
	snd_device 结构体。
	然后挂到card里的list里。
	device的类型可以有：
		control。
		pcm。
		jack
		timer。
		hwdep。
		其他。
	我们重点看pcm和control就好了。
	
snd_device_free
snd_device_register
	这个接口没有怎么用。
snd_device_register_all
	被snd_card_register调用。
	最终是给snd_soc_instantiate_card调用。
```



#### module request and device file entry:

##### sound/core/sound.c

这个算是kernel里alsa的入口。

```
alsa_sound_init
	模块函数，自动被调用。
	注册了char dev和proc fs。
	
```

##### sound/sound_core.c（这个我加的）

```
init_soundcore
	主要作用就是create了 sound_class。
文件的其他部分都是处理oss的。所以不用看。
这个文件的有效部分就50行左右。
```



#### memory management helper:

##### sound/core/memory.c

这个就2个函数：

```
copy_to_user_fromio
copy_from_user_toio
```



##### sound/core/memalloc.c

```
snd_malloc_pages
	在pcm里有使用。
snd_dma_alloc_pages
	这个也有使用。
主要就上面这2个函数。
```



### pcm api

#### pcm core

##### sound/core/pcm.c 

大概1200行。

是一个module了。入口函数 alsa_pcm_init

主要全局变量

```
static LIST_HEAD(snd_pcm_devices);
	这个device 链表。
```

主要函数：

```
alsa_pcm_init
	入口函数。
	procfs里pcm相关部分的初始化。
	snd_ctl_register_ioctl 注册control。
snd_pcm_new
	新建一个pcm instance。
	被soc_new_pcm调用。
snd_pcm_new_internal
	这个跟上面的什么关系？
	都是调用_snd_pcm_new。就一个bool参数不一样。
	表示pcm只给internal用途。
	
```



##### sound/core/pcm_lib.c

大概2600行。

作用是作为util工具。所以里面都是纯函数。

主要全局变量：

```
无
```

主要函数：（函数都是snd_pcm开头。参数主要是snd_pcm_substream指针， snd_pcm_runtime指针）

```
snd_pcm_playback_silence
	给ringbuffer都填入静音数据。
snd_pcm_update_state
snd_pcm_update_hw_ptr
```



##### sound/core/pcm_native.c

大概3700行。

主要全局变量

```
struct file_operations snd_pcm_f_ops[2]
	主要就是对外输出这个结构体。
	文件里的其余部分就是这个结构体里函数的实现。
	
```



##### include/sound/pcm.h

1400行左右。

```
struct snd_pcm_hardware 
	rate、channel等参数。
struct snd_pcm_ops 
	open、read、write等
	mmap、prepare、trigger。
struct snd_pcm_runtime 
struct snd_pcm_substream 
struct snd_pcm 
struct snd_pcm_chmap

```



#### pcm format helper

##### sound/core/pcm_misc.c

大概600行。

主要全局变量

```
struct pcm_format_data pcm_formats[]
	各种格式的定义。
	然后配套了一堆的函数围绕这个数组工作。
```



#### pcm memory management

##### sound/core/pcm_memory.c

不管。

#### pcm dma engine api

##### sound/core/pcm_dmaengine.c

##### include/sound/dmaengine_pcm.h


### control/mixer api

#### generic control interface

##### sound/core/control.c

大概2000行。

函数都以snd_ctl开头。

```
snd_ctl_create
	被snd_card_new调用。
	
```



#### ac97 codec api

##### sound/pci/ac97/ac97_codec.c

##### sound/pci/ac97/ac97_pcm.c

#### virtual master control api

##### sound/core/vmaster.c

##### include/sound/control.h

### midi api

#### raw midi api

##### sound/core/rawmidi.c

### proc info api

#### proc info interface

##### sound/core/info.c



### compress offload

#### compress offload api

##### sound/core/compress_offload.c

##### include/uapi/sound/compress_offload.h

##### include/uapi/sound/compress_params.h

##### include/sound/compress_driver.h


### asoc

#### asoc core api

##### include/sound/soc.h（重要）

```
SOC_DOUBLE_VALUE
	一堆这样的工具赋值宏。
	360行左右。
然后一堆snd_soc开头的函数声明。

struct snd_soc_jack_pin
struct snd_soc_jack_zone
struct snd_soc_jack_gpio
struct snd_soc_jack

struct snd_soc_pcm_stream
struct snd_soc_ops
struct snd_soc_compr_ops

struct snd_soc_component_driver
struct snd_soc_component
	这2个结构体是最重要的。
struct snd_soc_codec 
struct snd_soc_codec_driver 

struct snd_soc_platform_driver 
struct snd_soc_dai_link_component 
struct snd_soc_platform
struct snd_soc_dai_link 

struct snd_soc_codec_conf 

struct snd_soc_card 
struct snd_soc_pcm_runtime 
struct soc_mixer_control


```



##### sound/soc/soc-core.c（重要）

大概4000行。

模块入口snd_soc_init

全局变量

```
static LIST_HEAD(platform_list);
static LIST_HEAD(codec_list);
static LIST_HEAD(component_list);
	3个重要链表。
	
```

函数

```
snd_soc_instantiate_card
	这个虽然是内部函数，但是非常关键。声卡的主要初始化在这里完成。
	
```



##### sound/soc/soc-devres.c

提供devm开头的函数。

devm_snd_soc_register_card 这个非常重要。



##### sound/soc/soc-io.c

提供snd_soc_read 、snd_soc_write这些函数。



##### sound/soc/soc-pcm.c

大概3000行

soc_new_pcm

##### sound/soc/soc-ops.c



##### sound/soc/soc-compress.c



#### asoc dapm api

##### sound/soc/soc-dapm.c

4400行。




#### asoc dma engine api

##### sound/soc/soc-generic-dmaengine-pcm.c

### misc function
#### hardware dependent device api
##### sound/core/hwdep.c



#### jack abstraction layer api
##### include/sound/jack.h
##### sound/core/jack.c
##### sound/core/sock-jack.c
### other helper macros
#### include/sound/core.h

## writing-an-alsa-driver
# designs
## control-names
## channel-mapping-api
## compress-offload
## timestamping
## jack-controls
## tracepoints
## procfile（重要）

都在/proc/asound目录下。



## powersave
## oss-emulation
## seq-oss


# soc
## overview
## codec
## dai
## dapm
## platform
## machine
## pop-clicks
## clocking
## jack
## dpcm
## codec-to-codec

# alsa-configuration
# hd-audio
# cards

