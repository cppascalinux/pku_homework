# 爬楼梯
## 时间限制：2s
## 空间限制：512mb
## 题目背景
老M是一个知名的混元形意太极大师。经常会有弟子前来拜师学艺，但他们必须经过严格的入学考试：爬楼梯。
## 题目描述
老M的道场有$n$个平台排成一列，第$i$个平台的高度为$h_i$，从第$i$个平台爬楼梯到第$i+1$个平台所需要消耗的体力为$|{h_i-h_{i+1}}|$。  
当第$j$个弟子来拜师学艺时，老M会指定一个区间$[l_j,r_j]$，取出这个区间内的所有平台，并使用内功将他们重新排列(**不改变原序列**)，使得爬完所有楼梯消耗的体力值之和最大，即$\max{\sum_{i=l_j}^{r_j-1}|p_i-p_{i+1}}|$，其中$p_i$表示将$[l_j,r_j]$中所有$h_i$重新排列得到的序列。但老M在忙着打MMA，因此他想请你计算这个最大值。
## 输入格式
第一行两个正整数$n$，$m$，分别表示平台的个数与操作总数  
第二行$n$个正整数$h_1\sim h_n$，表示平台的高度  
接下来$m$行，每行2个正整数$l$，$r$（保证$l<r$），表示有新的弟子来拜师学艺，你需要回答区间$[l,r]$的答案  
## 输出格式
$m$行,每行一个正整数，表示询问的答案
## 样例输入
```
4 4
3 2 2 4
1 3
1 4
2 4
2 3
```
## 样例输出
```
2
5
4
0
```
## 样例解释
第一次询问，一种最优的方案为2 3 2  
第二次询问，一种最优的方案为3 2 4 2  
第三次询问，一种最优的方案为2 4 2  
第四次询问，一种最优的方案为2 2  
## 数据范围
对于所有数据，有$2\le n,m\le200000,1\le h_i\le10^9$，保证询问的$l<r$  
|子任务编号|附加限制|分值|
|:-:|:-:|:-:|
|1|$n,m\le10$|5|
|2|$h_i\le2$|10|
|3|$h_i\le3$|20|
|4|$n,m\le2000$|25|
|5|无|40|