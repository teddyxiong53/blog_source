---
title: python之实用代码片段
date: 2017-07-22 23:59:09
tags:
	- python

---

## 格式化打印

特点是用{}来占位。

```
print "Sent: {}".format(data)
```



## 取得某个目录下所有某个后缀的文件

```
import glob
files = glob.glob("./*.jpg")
print files
```



## 去除文件里相同的行

```
read_dir = "./in.txt"
write_dir = "./out.txt"

lines_seen = set()

with open(write_dir, "w") as fout:
    with open (read_dir, "r") as fin:
        for line in fin:
            if line not in lines_seen:
                print(line)
                fout.write(line)
                lines_seen.add(line)
```

## 查看Python shell里当前的变量

用dir()就可以了。

```
In [3]: dir()       
Out[3]:             
['In',              
 'Out',             
 '_',               
 '_1',              
 '__',              
 '___',             
 '__builtin__',     
 '__builtins__',    
 '__name__',        
 '_dh',             
 '_i',              
 '_i1',             
 '_i2',             
 '_i3',             
 '_ih',             
 '_ii',             
 '_iii',            
 '_oh',             
 'crawler',         
 'exit',            
 'fetch',           
 'get_ipython',     
 'item',            
 'quit',            
 'request',         
 'response',        
 'scrapy',          
 'sel',             
 'settings',        
 'shelp',           
 'spider',          
 'view']                   
```

