---
title: python之弱引用
date: 2019-09-04 10:20:03
tags:
	- python
---

1

python的gc是基于引用计数的。

python里的弱引用，跟c++等语言的弱引用的目的是一致的，都是为了解决循环引用的问题。

```
import sys, weakref
class Man:
    def __init__(self, name):
        self.name = name
    def test(self):
        print "this is a test"

def callback(self): #need one param for this function
    print "callback"
    
o = Man("xx")
p = weakref.proxy(o, callback)
p.test()
o=None
p.test()
```

循环引用，打破循环。

```
import weakref
import gc
from pprint import pprint

class Graph(object):
    def __init__(self, name):
        self.name = name
        self.other = None
    def set_next(self, other):
        print "%s.set_next(%r)" % (self.name, other)
        self.other = other

    def all_nodes(self):
        yield self
        n = self.other
        while n and n.name != self.name:
            yield n
            n = n.other
        if n is self:
            yield n
        return

    def __str__(self):
        return "->".join(n.name for n in self.all_nodes())

    def __repr__(self):
        return "<%s at 0x%x name=%s>" % (self.__class__.__name__, id(self), self.name)

    def __del__(self):
        print "Deleting %s" % self.name

def collect_and_show_garbage():
    print "collecting ..."
    n = gc.collect()
    print "unreachable objects:", n
    print "garbage:"
    pprint(gc.garbage)

def demo(graph_factory):
    print "set up graph"
    one = graph_factory("one")
    two = graph_factory("two")
    three = graph_factory("three")
    one.set_next(two)
    two.set_next(three)
    three.set_next(one)

    print
    print "Graph:"
    print str(one)
    collect_and_show_garbage()

    print
    three = None
    two = None
    print "after two ref removed"
    print str(one)
    collect_and_show_garbage()

    print
    print "removing last ref"
    one = None
    collect_and_show_garbage()

gc.set_debug(gc.DEBUG_LEAK)
print "setting up the circle"
print
demo(Graph)
print "breaking the cycle and clean up garbage"
print
gc.garbage[0].set_next(None)
while gc.garbage:
    del gc.garbage[0]
print collect_and_show_garbage()


```

运行输出：

```
hlxiong@hlxiong-VirtualBox:~/work/test/python$ python test.py 
setting up the circle

set up graph
one.set_next(<Graph at 0x7fa3728b3c10 name=two>)
two.set_next(<Graph at 0x7fa3728b3c50 name=three>)
three.set_next(<Graph at 0x7fa3728b3bd0 name=one>)

Graph:
one->two->three->one
collecting ...
unreachable objects: 0
garbage:
[]

after two ref removed
one->two->three->one
collecting ...
unreachable objects: 0
garbage:
[]

removing last ref
collecting ...
gc: uncollectable <Graph 0x7fa3728b3bd0>
gc: uncollectable <Graph 0x7fa3728b3c10>
gc: uncollectable <Graph 0x7fa3728b3c50>
gc: uncollectable <dict 0x7fa372929b40>
gc: uncollectable <dict 0x7fa372929c58>
gc: uncollectable <dict 0x7fa372929a28>
unreachable objects: 6
garbage:
[<Graph at 0x7fa3728b3bd0 name=one>,
 <Graph at 0x7fa3728b3c10 name=two>,
 <Graph at 0x7fa3728b3c50 name=three>,
 {'name': 'one', 'other': <Graph at 0x7fa3728b3c10 name=two>},
 {'name': 'two', 'other': <Graph at 0x7fa3728b3c50 name=three>},
 {'name': 'three', 'other': <Graph at 0x7fa3728b3bd0 name=one>}]
breaking the cycle and clean up garbage

one.set_next(None)
Deleting two
Deleting three
Deleting one
collecting ...
unreachable objects: 0
garbage:
[]
None
```

我的机器上的运行表现跟原作者的表现不一样。

原文里显示不能正常回收，我这里是正常回收了。





参考资料

1、

https://segmentfault.com/a/1190000005729873