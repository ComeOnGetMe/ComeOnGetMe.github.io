---
layout: post
title:  "解题报告：Google Code Jam 2015 Round1C Q2"
date:   2015-05-15 9：51：22
categories: jekyll update
---

[原题地址在这里][question]

---

####[原题][null-link]
**Problem B. Typewriter Monkey**  
This contest is open for practice. You can try every problem as many times as you like, though we won't keep track of which problems you solve. Read the Quick-Start Guide to get started.
Small input
11 points	
Solve B-small
Large input
22 points	
Solve B-large
Problem

Your publishing house has decided to use monkeys randomly typing at keyboards to write great works of literature. You are the supervisor for one monkey with a keyboard containing K keys, each of which is labeled with an uppercase English letter. (There may be multiple keys displaying the same letter.) The monkey will start with an empty string and repeat the following S times: choose a key from its keyboard uniformly at random and press it, adding a copy of that key's letter to the right end of the string. The final resulting string will have length S.

You have a target word of length L that you are hoping the monkey will type. (The target word will not necessarily be a real English word.) This target word may even appear multiple times in what the monkey types. (Overlapping instances count too -- for example, if "ABA" is the target word and the monkey types "ABABA", that contains two instances of the target.)

You plan to pay the monkey one banana for each instance of the target word that it types. When you go to inspect the monkey's work, you will bring along the minimum number of bananas that you need to ensure that you will always have enough bananas to pay the monkey, no matter what it has typed. Then, you will pay the monkey one banana for each instance of the target word that it actually typed. You will keep the remaining bananas that you brought with you.

What is the expected number of bananas that you will get to keep?  

**Input**

The first line of the input gives the number of test cases, T. T test cases follow. Each consists of three lines. The first contains three space-separated positive integers: K, L, and S. The second contains a string of K uppercase English letters representing the monkey's keyboard. The third contains a string of L uppercase English letters representing the target word.

**Output**

For each test case, output one line containing "Case #x: y", where y is the expected number of bananas you will get to keep after paying the monkey.

y will be considered correct if it is within an absolute or relative error of 10-6 of the correct answer. See the FAQ for an explanation of what that means, and what formats of real numbers we accept.  

**Limits**  
1 ≤ T ≤ 100.  

Small dataset  
1 ≤ K ≤ 7.  
1 ≤ L ≤ S ≤ 7.  

Large dataset  
1 ≤ K ≤ 100.  
1 ≤ L ≤ S ≤ 100.  

**Sample**

Input  
5  
7 6 6  
BANANAS  
MONKEY  
2 3 4  
AA  
AAA  
2 1 2  
AB  
B  
6 2 2  
GOOGLE  
GO  
26 11 100  
ABCDEFGHIJKLMNOPQRSTUVWXYZ  
ROSENCRANTZ  

Output  
Case #1: 0.0  
Case #2: 0.0  
Case #3: 1.0  
Case #4: 0.8888889  
Case #5: 9.0  

Note that Case #5 is not within the limits for the Small dataset.

In Case #1, the monkey has no chance of typing the target word "MONKEY" even once (because his keyboard lacks most of the letters in "MONKEY"), so you do not bring any bananas along when you visit, and of course you do not pay any. Poor monkey!

In Case #2, the monkey is guaranteed to type "AAAA", which has two overlapping instances of the target word "AAA". You will bring two bananas and then pay both.

In Case #3, the monkey will produce the following outputs with equal probability (1/4 each): "AA", "AB", "BA", "BB". These have 0, 1, 1, and 2 instances of the target word, respectively. You must bring 2 bananas to be ready for the "BB" case, but you will on average pay (0 + 1 + 1 + 2) / 4 = 1.

In Case #4, the monkey has a 1/3 chance of typing a "G" first and a 1/3 chance of typing an "O" second, for a 1/9 chance of typing "GO". You will bring one banana and give it up 1/9 of the time.

In Case #5, the monkey could in theory type "ROSENCRANTZ" up to nine times, but the chances of this happening even once are so small that they are negligible compared to the acceptable margin of error for answers.

####[题意][null-link]
说有一只猴子叫灰灰……（此处省略一万字）你给了灰灰一个有 K 个字母的键盘，跟它说了一个长度为 L 的单词（当然它听不懂），然后让它在键盘上敲 S 个键，并答应它每敲出一次这个单词就给他一根香蕉。请求出这 S 个键的输出当中该单词**（最多能出现的次数 - 出现次数的期望）**的值是多少。注意：在 BBB 中，单词BB出现的次数为2（重叠计算）。

####[解法][null-link]
首先，这其实是两个问题，一个是求**期望**，另一个是求**最大值**；他们的差没有什么实际意义，即无法直接求出（也许有方法能够直接求，但未免有点简单问题复杂化）。

先说**期望**。我在答案中看到了有人用 Trie 遍历了所有keyboard输出的情况，据说也不慢（S < 100），但未免太麻烦。其实我们只需要先求出按 L 个键能够按出 target 的概率，再乘以它在 S 个键中能够出现的位置个数就可以了，即 E = P(L) * (S - L + 1) 。这样不用把重叠的情况单拿出来讨论，具体的理论依据在官方的[解析][analysis]中有提到。至于P(L) 的求法，只需要按字母在 target 中的顺序把它在keyboard中的出现频率乘起来就可以了。

再说**最大值**。这里我引入了一个 *Effective Length* 的概念。比如说对于单词 ABA，根据重叠的计数方式其实在第一个单词之后我们只需要在后面再加一个 BA ，整个单词就可以算作出现了两次（ABABA中有两个 ABA）这种情况就定义它的 effective length 为2。具体求的过程中可以直接用暴力的方法，对每个字符判断一下以它开始的子串是否等于它前面的那部分子串，复杂度为 O(L^2)，因为 L 并不大，这个算法还是很快可以得出结果。另：[KMP][KMP]可以在线性时间内算出结果。

AC代码如下：  

####[Python][null-link]
{% highlight python %}
def effectiveLength(word):
	pt=1
	i=0
	while (pt + i) < len(word):
		if word[i] == word[pt+i]:
			i += 1
		else:
			i = 0
			pt += 1
	return pt

for i in xrange(input()):
	[k,l,s] = [int(x) for x in raw_input().split()]
	# Alright, I know here map(int, raw_input().split()) would be more Pythonic
	keyboard = raw_input()
	target = raw_input()
	eff_len = effectiveLength(target)
	maximum = (s - (l - eff_len)) / eff_len

	prob = 1
	result = 0.0
	for char in target:
		prob *= keyboard.count(char) / float(k)
	expectation = prob * (s - l + 1)
	if prob != 0:
		result = maximum - expectation
	print 'Case #{}: {}'.format(i + 1, result)
{% endhighlight %}

[null-link]: chrome://not-a-link
[question]: https://code.google.com/codejam/contest/4244486/dashboard
[analysis]: https://code.google.com/codejam/contest/4244486/dashboard#s=a&a=1
[KMP]: https://www.topcoder.com/community/data-science/data-science-tutorials/introduction-to-string-searching-algorithms/