Title: Strategy Pattern -- 把演算法則整個換掉
Slug: strategy
Category: Design Pattern
Author: twmht

###用的時間點
strategy 是 "戰略" 的意思，泛指與敵方對峙時的作戰策略以及解決問題的方法等。在程式設計裡，不妨把它視為 "運算法則"。
###如何設計
任何一種程式都是為了解決問題而撰寫出來，解決問題時需要實作一些特定的運算法則。在 Strategy Pattern 之下，可以更換實作運算法則的部份而且不留痕跡。切換整個運算法則，簡化改採其它方法來解決同樣問題的動作。

###程式範例
設計電腦遊戲 "剪刀石頭布"。猜拳時的設略有兩種方法。

* 猜贏之後繼續出同樣的招式 (WinningStrategy)。
* 從上一次出的招式，以機率分配方式求出下一個招式的機率 (ProbStrategy)。

<script src="https://gist.github.com/twmht/93e49c329294c68aa552.js"></script>

####Strategy 參與者
規定使用戰略之介面的參與者。例如 Strategy 介面。
#### ConcreteStrategy 參與者
實作 Strategy 參與者之介面的參與者。這裡會實際編寫有關具體戰略的程式。例如 WinningStrategy 類別和 ProbStrategy 類別。
#### Context (文法) 參與者
利用 Strategy 參與者的參與者。它有 ConcreteStrategy 參與者的物件個體，如有必要時則可使用 (最多只能呼叫 Strategy 參與者的介面)。例如 Player 類別。

###優點
我們比較習慣把實作運算法則這個部份結合到方法裡面。但是 Strategy Pattern 則故意把運算法則的部份跟其他部份分開。只規定跟運算法則有關的介面的部份，然後再從程式這邊以委讓的方式來利用運算法則。

假設現在我們想改良運算法則提高速度，只需要注意不要去修改到 Strategy 的介面，然後再改 ConcreteStrategy 就行。而且它所使用的委讓又是說分就分的關係，所以很容易就切換運算法則。舉例來說，假設想比較一下原始運算法則跟改良後的運算法則兩者的速度時，只要動手切換一下就能測得出來。

即使這個程式是一個象棋遊戲，只要使用 Strategy Pattern 的話，還能配合使用者選擇的參與者切換思考模式等級。

####執行時也能切換
可在程式執行中直接切換 ConcreteStrategy。例如若電腦記憶體不夠時，就切換為節省記憶的 Strategy，若足夠時，則切換為較快但較耗費記憶體的 Strategy。

當然也可以用甲方的運算法則來**驗算**乙方的運算法則。假設現在想用一個試算表軟體的除錯版，進行高複雜度的運算。此時，只要手邊同時有**可能還有 bug 的高速運算法則**和**可保證計算正確的低速運算法則**，就可能利用後者去驗算前者。

###問題
####1. 建立一個隨便決定下一個猜拳手勢的 RandomStrategy 類別。

<script src="https://gist.github.com/twmht/35e6dc1700439247ab23.js"></script>

####2. 以下程式為進行字串排序的類別與介面。使用的是 insertion sort。請配合 Sorter 的介面，建立一個可表示其他運算法則的類別。

<script src="https://gist.github.com/twmht/96fcf5fb58e784695574.js"></script>

可加入 QuickSort。

<script src="https://gist.github.com/twmht/2a9f59f054e0935de7e1.js"></script>



