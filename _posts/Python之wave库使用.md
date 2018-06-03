---
title: Python之wave库使用
date: 2018-06-02 21:11:23
tags:
	- Python

---



```
#!/usr/bin/python 

import wave

#read file
f = wave.open('./1.wav', 'r')
print f.getnchannels()
print f.getsampwidth()
print f.getframerate()
print f.getnframes()
print f.getcomptype()
print f.getcompname()
print f.getparams()

print f.getmarkers()
print f.tell()
f.setpos(10)
print f.tell()
f.setpos(0)
audio_data = f.readframes(1)
f.close()

#write file
f = wave.open('xx.wav', 'w')
f.setnchannels(2)
f.setsampwidth(1)
f.setframerate(32000)

f.writeframes(audio_data)
f.close()

```

