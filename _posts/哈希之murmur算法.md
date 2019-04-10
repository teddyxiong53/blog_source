---
title: 哈希之murmur算法
date: 2019-04-10 16:05:31
tags:
	- 哈希

---



什么是murmur 哈希算法？它的优点是什么？

具体算法如何实现？

优点

```
1、高运算性能。比安全散列算法快几十倍。例如md5、sha1这些就是安全哈希算法。
2、低碰撞率。
3、随机性非常好。
```

缺点

```
不保证安全性。
```



2008年才发明的。

现在被很多标准库采纳了。

是一种非加密的哈希算法。

适用于一般的哈希检索操作。



```
static uint32_t dict_hash_murmur(char *key, size_t len)
{
    if(!key || !len) {
        return 0;
    }
    uint32_t h,k;
    uint32_t seed = 0x0badcafe;//magic number
    uint32_t m = 0x5bd1e995;//magic number
    uint32_t r = 24;//magic number

    h = seed ^len;
    uint8_t *data;
    data = (uint8_t *)key;
    while (len >=4 )
    {
        k = *(uint32_t *)data;
        k *= m;
        k ^= k>>r;
        k *= m;

        h *= m;
        h ^= k;

        data += 4;
        len -= 4;
    }
    switch (len)
    {
    case 3://注意下面都没有break，这样故意这样的。
        h ^= data[2] <<16;
    case 2:
        h ^= data[1] << 8;
    case 1:
        h ^= data[0];
        h *= m;
    }
    h ^= h>>13;
    h *= m;
    h ^- h>>15;
    return h;
}
```

这个算法是从https://github.com/gozfree/gear-lib 这个里面找的。





参考资料

1、MurmurHash算法

https://blog.csdn.net/yangguosb/article/details/79516364

2、哈希表之简易数学原理和简易实现（史上最简单易懂的哈希表介绍）

https://blog.csdn.net/stpeace/article/details/38615647