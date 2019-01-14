---
title: Python之unittest
date: 2017-09-29 20:17:06
tags:
	- Python
	- unittest

---



unittest的基本使用方法：

1、import unittest

2、定义一个继承自unittest.TestCase的测试用例类。

3、定义setUp和tearDown，在每个测试用例前后做一些工作。

4、定义测试用例，名字以test开头。

5、一个测试用例应该只测试一个内容，要很明确。主要是调用assertEqual、assertRaises等断言方法。

6、调用unittest.main方法来启动测试。

7、如果测试通过，则不显示任何东西，可以用-v选项来显示打印。



看一个简单的例子。

```
import random
import unittest

class TestSequenceFunctions(unittest.TestCase):
	def setUp(self):
		print "xhl test begin"
		self.seq = range(10)
		
	def test_shuffle(self):
		random.shuffle(self.seq)
		self.seq.sort()
		self.assertEqual(self.seq, range(10))
		self.assertRaises(TypeError, random.shuffle, (1,2,3))
		
	def test_choice(self):
		element = random.choice(self.seq)
		self.assertTrue(element in self.seq)
		
	def test_error(self):
		element = random.choice(self.seq)
		self.assertTrue(element not in self.seq)
		
	def tearDown(self):
		print "xhl test end"
		
if __name__ == '__main__':
	unittest.main()
	
```

执行结果如下：

```
pi@raspberrypi:~/work/test/python$ python test.py 
xhl test begin
xhl test end
.xhl test begin
Fxhl test end
xhl test begin
xhl test end
.
======================================================================
FAIL: test_error (__main__.TestSequenceFunctions)
----------------------------------------------------------------------
Traceback (most recent call last):
  File "test.py", line 21, in test_error
    self.assertTrue(element not in self.seq)
AssertionError: False is not true

----------------------------------------------------------------------
Ran 3 tests in 0.002s

FAILED (failures=1)
```



参考资料

1、

