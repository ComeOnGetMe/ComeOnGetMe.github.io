---
layout: post
title:  "Google Code Jam 2015 Round1C Q1"
date:   2015-05-13 17：49：22
categories: jekyll update
---

[地址在这里][question]

---

####[原题][null-link]
Problem A. Brattleship

You're about to play a simplified "battleship" game with your little brother. The board for this game is a rectangular grid with R rows and C columns. At the start of the game, you will close your eyes, and you will keep them closed until the end of the game. Your little brother will take a single rectangular 1 x W ship and place it horizontally somewhere on the board. The ship must always fit entirely on the board, with each cell of the ship occupying exactly one of the grid's cells, and it can never be rotated.

In each turn of the game, you name a cell on the board, and your little brother tells you whether that is a hit (one of the cells occupied by the ship) or a miss. (Your little brother doesn't say which part of the ship was hit -- just that the cell you named has a part of the ship in it.) You have perfect memory, and can keep track of all the information he has given you. Once you have named all of the cells occupied by the ship, the game is over (the ship is sunk), and your score is the number of turns taken. Your goal is to minimize your score.

Although the ship is not supposed to be moved once it is placed, you know that your little brother, who is a brat, plans to cheat by changing the location of the ship whenever he wants, as long as the ship remains horizontal and completely on the board, and the new location is consistent with all the information he has given so far. For example, for a 1x4 board and 1x2 ship, your little brother could initially place the ship such that it overlaps the leftmost two columns. If your first guess was row 1, column 2, he could choose to secretly move the ship to the rightmost two columns, and tell you that (1, 2) was a miss. If your next guess after that was (1, 3), though, then he could not say that was also a miss and move the ship back to its original location, since that would be inconsistent with what he said about (1, 2) earlier.

Not only do you know that your little brother will cheat, he knows that you know. If you both play optimally (you to minimize your score, him to maximize it), what is the lowest score that you can guarantee you will achieve, regardless of what your little brother does?
Input

The first line of the input gives the number of test cases, T. T lines follow, each with three space-separated integers R, C, and W: the number of rows and columns of the board, followed by the width of the ship.

Output

For each test case, output one line containing "Case #x: y", where x is the test case number (starting from 1) and y is the minimum score you can guarantee.

Limits  
1 ≤ W ≤ C.

Small dataset  
T = 55.  
R = 1.
1 ≤ C ≤ 10.  

Large dataset  
1 ≤ T ≤ 100. 
1 ≤ R ≤ 20.  
1 ≤ C ≤ 20.  

Sample Input   
 
3  
1 4 2  
1 7 7  
2 5 1  

Output  

Case #1: 3  
Case #2: 7  
Case #3: 10  

In Case #1, the board has one row and four columns, and the ship takes up one row and two columns. One optimal strategy is for you to start by naming cell (1, 2):

If your little brother says it is a hit, then the other cell of the 1x2 ship must be in either (1, 1) or (1, 3), and you just have to name both. If you happen to correctly name the cell where the other part of the ship is, your little brother will just reposition the ship so that (1, 2) is still hit, but your guess is a miss. Notice that your little brother can still move the ship even after it has been hit, as long as the new position is not inconsistent with the information he has already given.

If your little brother says it is a miss, then the only remaining consistent scenario is that the ship is in (1, 3) and (1, 4), and your little brother will be unable to change this from now on; you just need to name those two cells.

So no matter what your little brother does after you say (1, 2), you can finish the game in two more moves after that, for a total of three moves.

Moreover, a three-move solution is optimal, because it is impossible to guarantee a finish in only two moves: without loss of generality, pick a first move. No matter what you pick, there is still a 1x2 area open and your little brother can just move the ship there and claim that you missed. It is impossible for you to sink that ship, which has not yet been hit, with only one more move.

In Case #2, the ship completely fills in the board and so your little brother has only one place to put it. All you have to do is name every cell.

In Case #3, your little brother can always move the 1x1 ship to a cell you have not tried yet, so you must name all 10 cells, only finally getting a hit (and immediately sinking the ship) on the last one.

####[题意解析][null-link]
简单翻译一下就是，你和基友在玩一个新游戏叫做‘战船’。具体玩法是，你全程闭眼，他会在一个 R x C 的棋盘上某处放一只 1 x W 的船，（R，C，W 你们会事先商量好）然后每回合你可以炸掉棋盘上的任意一格；如果打中战船，基友会说‘hit’，反之则说‘miss’；直到战船所在的每一个格子都被击中，游戏结束。

本来游戏规则就到这为止，但是你的基友很烂，他会耍赖：每次等你开炮之后，无论船是否被击中，只要还有其他地方让船能够避开攻击，他都会将船移动过去并说‘miss’。问在两个人都非常聪明的情况下，你最少需要多少回合才能保证把整艘船击沉？

####[解法][null-link]
这个题难度主要在于想清楚游戏过程。我们在炸格子的过程中，实际上基友会不断地移动船的位置，直到船无处可逃为止。很快能够注意到因为船始终是横置的，所以行数 R 对游戏结果的影响不大，对于最后一行以外的其他行，我们只需要每 W 格炸掉一格就可以排除掉整行（这时候基友会将船移动到下一行）。那么对于这（R-1）行，我们只需要炸（R-1）x（C/W）次，就可以将问题简化为 1 x C 的问题。

剩下就是怎样解决 1 x C 的问题了。假设 C 远大于 W，我们仍然可以每 W 格炸一次来排除掉大部分的位置（这个过程中基友仍然会说miss）。需要注意的是，当剩下的格子数小于或等于 2W 时，我们最少需要 W+1 次来保证炸光整条船。

~~~

☐☐☒☐☐☐ (miss) -> ☐☐☒☒☐☐ (hit) -> ☐☐☒☒☒☐ (hit) -> ☐☐☒☒☒☒ (hit)

~~~

如图，C = 6，W = 3的情况，首先我们在靠近中间的位置炸一格，基友说miss（这里如果说hit，结果也是一样的。why？），我们便确定是在右边的三格，即总共需要炸四次可以结束游戏。对于其他 W 和 C 的值，只要 W < C <= 2W，总次数都是 W+1 次，不清楚的同学们可以自己去画一下。

讲得这里这个题思路就非常清晰了，也不需要再回头去看数据大小了，因为只有加减乘除，无论Input多大，只要没有Overflow我们都可以通过这个过程很快的得出答案。以下为代码：

####[Python][null-link]
{% highlight python %}

def solution(r,c,w):
	if r!=1:
		return solution(1,c,w) + (r-1) * (c/w)		# Actually here we can have
	elif c > 2*w:						# a generalized function
		tmp = c / w - 1					# to figure out the result
		return solution(1,c - tmp * w, w) + tmp		# and thus don't need to divide
	elif c > w:						# it into 4 cases.
		return w + 1
	else:
		return w

{% endhighlight %}

[null-link]: chrome://not-a-link
[question]: https://code.google.com/codejam/contest/4244486/dashboard
