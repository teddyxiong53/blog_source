---
title: python之xml操作
date: 2021-04-07 13:15:07
tags:
	- python

---

--

python自带了xml包。就叫xml。

有4个模块：

dom。dom对象。这个下面又分minidom和pulldom。主要类有Node、一些Error类、UserDataHandler

parsers。解析器。

sax。simple api for xml的缩写。

etree。element tree xml库。



使用etree。

```
import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
```

查看root节点的信息

```
>>> root.tag
'data'
>>> root.attrib
{}
```

遍历子节点

```
>>> for child in root:
...     print(child.tag, child.attrib)
```

遍历特定子节点

```
    for project in root.iter('project'):
        print(project.attrib)
```



参考资料

1、

https://stackoverflow.com/questions/3593204/how-to-remove-elements-from-xml-using-python

2、官网文档

https://docs.python.org/3/library/xml.etree.elementtree.html#module-xml.etree.ElementTree