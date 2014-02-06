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
