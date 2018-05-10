---
title: cpp之标准头文件
date: 2018-05-10 21:32:10
tags:
	- cpp

---



```
teddy@teddy-ubuntu:/usr/include/c++/5$ tree -L 1 
.
├── algorithm
├── array
├── atomic
├── backward
├── bits
├── bitset
├── cassert
├── ccomplex
├── cctype
├── cerrno
├── cfenv
├── cfloat
├── chrono
├── cinttypes
├── ciso646
├── climits
├── clocale
├── cmath
├── codecvt
├── complex
├── complex.h
├── condition_variable
├── csetjmp
├── csignal
├── cstdalign
├── cstdarg
├── cstdbool
├── cstddef
├── cstdint
├── cstdio
├── cstdlib
├── cstring
├── ctgmath
├── ctime
├── cwchar
├── cwctype
├── cxxabi.h
├── debug
├── decimal
├── deque
├── exception
├── experimental
├── ext
├── fenv.h
├── forward_list
├── fstream
├── functional
├── future
├── initializer_list
├── iomanip
├── ios
├── iosfwd
├── iostream
├── istream
├── iterator
├── limits
├── list
├── locale
├── map
├── memory
├── mutex
├── new
├── numeric
├── ostream
├── parallel
├── profile
├── queue
├── random
├── ratio
├── regex
├── scoped_allocator
├── set
├── shared_mutex
├── sstream
├── stack
├── stdexcept
├── streambuf
├── string
├── sun
├── system_error
├── tgmath.h
├── thread
├── tr1
├── tr2
├── tuple
├── typeindex
├── typeinfo
├── type_traits
├── unordered_map
├── unordered_set
├── utility
├── valarray
└── vector
```

我们依次看看这些文件的内容。

algorithm

```
#include <utility> // UK-300.
#include <bits/stl_algobase.h>
#include <bits/stl_algo.h>
                               
#ifdef _GLIBCXX_PARALLEL
# include <parallel/algorithm>
#endif
```

