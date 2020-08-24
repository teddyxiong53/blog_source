---
title: 加密算法（一）aes算法
date: 2018-02-06 22:56:39
tags:
	- 加密

---



打算系统了解一下加密算法。就从常用的aes算法开始。



aes的字面含义是Advanced Encryption Standard（高级加密标准）。是一种对称加密算法。

对称加密就是加密和解密都是用同一个秘钥。

整个过程是这样：

```
hello,ase（明文） --(aes/key加密)--> xxooxx（密文） --网络传输--> （aes/key解密）--->hello，aes
```



# 对称加密和非对称加密的比较

对称加密：

优点：加密速度非常快。适合经常发送数据的场合。

缺点：怎样保证秘钥的安全。

非对称加密：

加密和解密的秘钥是不同的。这种加密算法的数学基础是靠数学上的难解问题来构造。

优点：更加安全。

缺点：加密解密速度慢。

常见的非对称加密算法有RSA和ECC 。

在实际使用中，我们取对称加密和非对称加密的优点。

A用rsa算法加密AES的秘钥，然后传给B，B解密得到aes的秘钥，然后A和B就通过AES来进行加密和解密。



# aes的基本结构

aes为分组密码。

分组密码是指，把明文分为一组一组的。每组长度相等，以后一段段加密，直到把整个数据加密完成。

**在aes的标准里，一个分组的长度只能是128位，就是16字节。**

根据秘钥的长度，秘钥可以有128位、192位、256位。

所以aes就有aes-128，aes-192，aes-256这3种。

根据秘钥长度的不同，推荐的加密轮数也不同。128的加密10轮。256的加密14轮。



每个分组的16字节构造成一个4x4的矩阵。



aes加密有4种模式：

1、ECB模式。Electronic codebook。电子密码本模式。最简单。每个分组都使用相同的秘钥进行加密。

2、CBC模式。Cipher-block chaining。密码分组链接。每个分组在加密之前，会跟一个密码块进行异或操作。（这个密码块叫做初始化向量）。然后再进行加密。完成加密或者解密后，更修改初始化向量的内容。

3、CFB。Cipher Feedback。密文反馈。

4、OFB模式。output Feedback。输出反馈。







# C语言编程示例

```
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <openssl/aes.h>

int main(int argc ,char **argv)
{
    AES_KEY aes;
    unsigned char key[AES_BLOCK_SIZE];//这个就是分组单位，16字节。
    unsigned char iv[AES_BLOCK_SIZE];//init vector
    char *input;
    char *encryptstr;
    char *decryptstr;
    unsigned int len, i;
    int ret;
    if(argc != 2)
    {
        printf("usage: ./test string");
        exit(1);
    }
    //长度凑成16的整数倍。
    len = 0;
    if((strlen(argv[1])+1)%AES_BLOCK_SIZE == 0)
    {
        len = strlen(argv[1])+1;
        
    }
    else 
    {
        len = (strlen(argv[1]) + 1)/AES_BLOCK_SIZE;
        len = (len +1)*AES_BLOCK_SIZE;
    }
    input = (char *)calloc(len, 1);
    if(input == NULL)
    {
        printf("calloc failed \n");
        exit(1);
    }
    strncpy(input, argv[1], strlen(argv[1]));
    //产生128位的key
    for(i=0; i<AES_BLOCK_SIZE; i++)
    {
        key[i] = 32+i;
    }
    for(i=0; i<AES_BLOCK_SIZE; i++)
    {
        iv[i] = 0;
    }
    ret = AES_set_encrypt_key(key, 128, &aes);
    if(ret)
    {
        printf("set encrypt key failed \n");
        exit(1);
    }
    
    encryptstr = (char *)calloc(len, 1);
    if(encryptstr == NULL)
    {
        printf("alloc encryptstr failed ");
        exit(1);
    }
    //加密
    AES_cbc_encrypt(input, encryptstr, len, &aes, iv, AES_ENCRYPT);
    
    printf("the string after encrypt is:%s \n", encryptstr);
    //一般加密后的内容会有奇怪字符，多加几个换行看看。
    printf("\n\n\n");
    //开始解密
    decryptstr = (char *)calloc(len, 1);
    if(decryptstr == NULL)
    {
        printf("decryptstr alloc failed \n");
        exit(1);
    }
    for(i=0; i<AES_BLOCK_SIZE; i++)
    {
        iv[i] = 0;
    }
    ret = AES_set_decrypt_key(key, 128, &aes);
    if(ret < 0)
    {
        printf("decrypt failed\n");
        exit(1);
    }
    //解密
    AES_cbc_encrypt(encryptstr, decryptstr, len ,&aes, iv, AES_DECRYPT);
    printf("the string after decrypt is: %s", decryptstr);
    return 0;
}

```

需要链接libcrypto.a才能编译过。

