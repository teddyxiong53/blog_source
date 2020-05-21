---
title: Linux之alsa-project
date: 2018-05-28 22:03:14
tags:
	- Linux

---



在linux系统目录下。有这些头文件。

```
teddy@teddy-ubuntu:/usr/include/alsa$ tree
.
├── alisp.h
├── asoundef.h
├── asoundlib.h：这个是总的头文件，包括了其他的头文件。
├── conf.h
├── control_external.h
├── control.h
├── error.h
├── global.h
├── hwdep.h
├── iatomic.h
├── input.h
├── mixer_abst.h
├── mixer.h
├── output.h
├── pcm_external.h
├── pcm_extplug.h
├── pcm.h
├── pcm_ioplug.h
├── pcm_old.h
├── pcm_plugin.h
├── pcm_rate.h
├── rawmidi.h
├── seq_event.h
├── seq.h
├── seqmid.h
├── seq_midi_event.h
├── sound
│   ├── asoc.h
│   ├── asound_fm.h
│   ├── emu10k1.h
│   ├── hdsp.h
│   ├── hdspm.h
│   ├── sb16_csp.h
│   ├── sscape_ioctl.h
│   ├── tlv.h
│   └── type_compat.h
├── timer.h
├── topology.h
├── use-case.h
└── version.h
```

我们先不管。后面用到了再分析这些头文件。

```
#include <alsa/asoundlib.h>  

#include <stdio.h>
#include <stdlib.h>


int main(int argc, char const *argv[])
{
	snd_pcm_t *handle;
	FILE *fp;
	fp = fopen("sound.wav", "w");
	if(fp == NULL) {
		printf("open file fail\n");
		return -1;
	}
	int ret;
	ret = snd_pcm_open(&handle, "default", SND_PCM_STREAM_CAPTURE, 0);
	if(ret < 0){
		printf("snd_pcm_open fail\n");
		goto error1;
	}
	snd_pcm_hw_params_t *params;
	snd_pcm_hw_params_alloca(&params);
	//use the default params
	snd_pcm_hw_params_any(handle, params);
	//set interleaved mode
	snd_pcm_hw_params_set_access(handle, params, SND_PCM_ACCESS_RW_INTERLEAVED);
	//set 16bit little endian mode
	snd_pcm_hw_params_set_format(handle, params, SND_PCM_FORMAT_S16_LE);
	//set 2 channel
	snd_pcm_hw_params_set_channels(handle, params, 2);
	unsigned int val,val2;
	val = 44100;
	int dir;
	snd_pcm_hw_params_set_rate_near(handle, params, &val, &dir);
	snd_pcm_uframes_t frames ;
	frames = 32;
	snd_pcm_hw_params_set_period_size_near(handle, params, &frames, &dir);
	//write the params to driver
	ret = snd_pcm_hw_params(handle, params);
	if(ret <0) {
		printf("set params fail, ret:%x\n", ret);
		goto error1;
	}

	snd_pcm_hw_params_get_period_size(params, &frames, &dir);
	int size;
	size = frames * 4;// 2 chn, 2 bytes per sample
	printf("size:%d\n", size);
	char *buffer = malloc(size);
	if(buffer == NULL) {
		printf("malloc fail\n");
		goto error1;
	}
	snd_pcm_hw_params_get_period_time(params , &val, &dir);
	long loops;
	loops = (1000*1000*10) / val;
	int i  = 0;
	while(loops > 0) {
		loops --;
		ret = snd_pcm_readi(handle, buffer, frames);
		i++;
		if(ret == -EPIPE) {
			printf("overrun occured\n");
			snd_pcm_prepare(handle);
		} else if(ret < 0) {
			printf("error:%s\n", snd_strerror(ret));
		} else if(ret != frames) {
			printf("short read, read %d frames\n", ret);
		}
		ret = fwrite(buffer, size, 1,fp);
		if(ret != size) {
			printf("short write, write %d bytes\n", ret);
		} else {
			printf("write ok\n");
		}
	}
	snd_pcm_drain(handle);
	snd_pcm_close(handle);
	fclose(fp);
	free(buffer);
	return 0;
	
error1:
	fclose(fp);
	return -1;
}
```

编译。

```
 gcc test.c -lasound
```



# 参考资料

1、经典alsa 录音和播放程序

https://blog.csdn.net/zd394071264/article/details/8300045