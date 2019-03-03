---
layout: 	post
title:  	"解题报告：Google Code Jam 2015 Round1C Q3"
date:   	2015-05-16 12：58：22
author: 	"Zhipeng"
tags:
    - Google code jam
---

> [原题地址在这里][question]


## 原题

**Problem C. Less Money, More Problems** 

Up until today, the nation you live in has used D different positive integer denominations of coin for all transactions. Today, the queen got angry when a subject tried to pay his taxes with a giant sack of low-valued coins, and she just decreed that no more than C coins of any one denomination may be used in any one purchase. For instance, if C = 2 and the existing denominations are 1 and 5, it is possible to buy something of value 11 by using two 5s and one 1, or something of value 12 by using two 5s and two 1s, but it is impossible to buy something of value 9 or 17.

You cannot directly challenge the queen's decree, but you happen to be in charge of the mint, and you can issue new denominations of coin. You want to make it possible for any item of positive value at most V to be purchased under the queen's new rules. (Note that this may not necessarily have been possible before the queen's decree.) Moreover, you want to introduce as few new denominations as possible, and your final combined set of pre-existing and new denominations may not have any repeats.

What is the smallest number of new denominations required?  

**Input**

The first line of the input gives the number of test cases, T. T test cases follow. Each consists of one line with three space-separated values C, D, and V, followed by another line with D distinct space-separated values representing the preexisting denominations, in ascending order.  

**Output**

For each test case, output one line containing "Case #x: y", where x is the test case number (starting from 1) and y is the minimum number of new denominations required, as described above.  

**Limits**  

1 ≤ T ≤ 100.  
Each existing denomination ≤ V.  

Small dataset  

C = 1.  
1 ≤ D ≤ 5.  
1 ≤ V ≤ 30.  

Large dataset  

1 ≤ C ≤ 100.  
1 ≤ D ≤ 100.  
1 ≤ V ≤ 109.    

**Sample**

Input  
 
4  
1 2 3  
1 2  
1 3 6  
1 2 5  
2 1 3  
3  
1 6 100  
1 5 10 25 50 100  

Output  

Case #1: 0  
Case #2: 1  
Case #3: 1  
Case #4: 3  

Note that Cases #3 and #4 are not within the limits for the Small dataset.

In Case #1, it is already possible to make all the required values (1, 2, and 3) using at most one copy of each of the existing denominations.

In Case #2, it suffices to add a denomination of either 3 or 4 -- whichever you choose, only one new denomination is required.

In Case #3, the optimal solution is to add a denomination of 1.

## 题意

女王交给你一个任务：让你为这个国家设计一套新版硬币，对于面额的要求是：  
	1. 现有的 D 种面额需要保留；  
	2. 新版硬币在每种面额的硬币最多使用 C 个的情况下，能够达到的最大价值至少是 V 。  

举例：C, D, V = 1，3，6；三种面额分别为1，2，5。首先从1和2我们能够得到3，但由于每种硬币只能用一次，而第三种面额就是5，所以这种情况下我们没法凑出4，因而我们需要加入面额为4的新硬币。加入之后，我们能够凑出的价值为 5 + 4 = 9，已经超过了所要求的6，输出1，完工。  

## 解法

难度仍然只在于想清楚过程。运用归纳法的思想，从最小的面额开始把硬币按大小顺序一个个放到钱包里，假设用钱包中现有的硬币我可以凑出任何小于等于 N 的数，那我们只需要看下一个硬币的面额是否大于或等于 （N + 1）：如果小于，那么我们只需要将下一个硬币添加到我们的钱包当中并更新 N 即可；如果大于，我们必须额外添加面值为（N + 1）的硬币，原因如下：
第一，用后面的硬币是不可能凑出（N + 1）的，因为它们全部大于（N + 1）；第二，用已有的硬币凑不出（N + 1）来，我们必须添加新的；第三，如果新硬币的面值小于（N + 1），那么添加后钱包所能凑出的数额将会小于添加面值为（N + 1）的硬币之后它所能凑出的数额。所以结论是，此时**最优解**就是添加面值为（N + 1）的硬币。  

想清楚以后，写其实不难。当时做的时候我还在想用一些比如 `deque` 或者 `set` 之类的结构去实现，但其实只需要维护一个所能表示的最大值（integer）即可。更新的时候只需要另 can_reach <- can_reach + (new_coin) * C 。我一开始没想通，最后差一点时间写完……有点遗憾。复杂度在这里其实无关紧要了，简单分析一下结构，粗略来看，每个 loop 当中 reach 都会变大 C 倍，所以最次就是 O(logV) 的时间复杂度。代码如下：  

## Python

{% highlight python %}

for tc in xrange(input()):
	c,d,v = map(int, raw_input().split())
	coins = [int(x) for x in raw_input().split()]

	reach = 0
	result = 0
	while reach < v:
		if len(coins) != 0:
			coin = coins[0]
		else:
			break
		if coin > (reach + 1):
			result += 1
			reach += (reach + 1) * c
		else:
			reach += coin * c
			coins.pop(0)

	# This WHILE loop can be combined with the previous one
	while reach < v:
		result += 1
		reach += (reach + 1) * c
	print 'Case #{}: {}'.format(tc + 1, result)

{% endhighlight %}

[null-link]: chrome://not-a-link
[question]: https://code.google.com/codejam/contest/4244486/dashboard
