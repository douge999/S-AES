# 一、项目简介 
### 该项目实现了S-AES算法，是一种简化的AES加密算法，实现对数据的加密。 
# 二、测试结果 
## 1、基本测试 
对输入数据为 四为16进制的数据和4为16进制（16为二进制）的秘钥，选择加密（e）或解密（d）模式进行操作。如下：  
![image](https://github.com/douge999/S-AES/blob/main/image/saes.png)  
## 2、交叉测试 
对输入为56A8（01010110101001000）的数据和89CA（1000100111001010）的秘钥进行加密，我的结果为:  
![image](https://github.com/douge999/S-AES/blob/main/image/jiacha1.png)  
另个小组结果为  
![image]()
结果一样，交叉测试成功。
## 3、扩展功能 
#### 考虑到向实用性扩展，加密算法的数据输入可以是ASII编码字符串(分组为2 Bytes)，对应地输出也可以是ACII字符串(很可能是乱码)。 得到结果如下：  
![image](https://github.com/douge999/S-AES/blob/main/image/kuozhan.png)  
## 4、多重加密 
### （1）双重加密：将S-AES算法通过双重加密进行扩展，分组长度仍然是16 bits，但密钥长度为32 bits。 
测试结果如下：  
![image](https://github.com/douge999/S-AES/blob/main/image/double_saes.png)  
### （2）中间相遇攻击：假设你找到了使用相同密钥的明、密文对(一个或多个)，请尝试使用中间相遇攻击的方法找到正确的密钥Key(K1+K2)。  
对明文为'1010001110110000', '0000011010101011'，对应密文分别为'1001100101100101', '1100011110100100'进行测试，得到结果如下：  
![image](https://github.com/douge999/S-AES/blob/main/image/zhogjiangongjixiangyu.png)  
### （3）三重加密：使用48bits(K1+K2+K3)的模式进行三重加解密。  
测试结果如下：  
![image](https://github.com/douge999/S-AES/blob/main/image/triple_saes.png)  
## 5、工作模式
基于S-AES算法，使用密码分组链(CBC)模式对较长的明文消息进行加密。注意初始向量(16 bits) 的生成，并需要加解密双方共享。   
在CBC模式下进行加密，并尝试对密文分组进行替换或修改，然后进行解密，请对比篡改密文前后的解密结果。  
得到结果如下：  
![image](https://github.com/douge999/S-AES/blob/main/image/cbc.png)  
更改第一个秘钥后，解密结果与原明文不同。  
