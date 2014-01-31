Title: Decorator Pattern -- 對容器和內容一視同仁
Slug: decorator
Category: Design Pattern
Author: twmht

###用的時間點
海綿蛋糕、鮮奶油蛋糕、草莓奶油蛋糕或生日蛋糕的原型其實都是海綿蛋糕，只不過運用了各種修飾技巧，能符合不同目的而改變。
###如何設計
物件也很像是蛋糕的多變化，首先建立一個像是海綿蛋糕的核心物件，再一層層加上裝飾用的功能，就可以完全符合所需的物件。
###程式範例
在字串周圍加上裝飾外框後再列印出來的程式。裝飾外框是指以-,+,| 等字元組成的框線。

<script src="https://gist.github.com/twmht/74632b289d5d81ac90d2.js"></script>

####Component 參與者
新增功能的核心參與者。在蛋糕的比喻說明中，相當於裝飾前的海綿蛋糕。Component 只規定海綿蛋糕的介面。例如 Display 類別。
#### ConcreteComponent 參與者
實作 Component 介面的具體海綿蛋糕。例如 StringDisplay 類別。
#### Decorator (裝飾者) 參與者
具有跟 Component 參與者相同的介面，另外還有 Decorator 要修飾的 Component。這個參與者是 "早就知道" 自己要去修飾的對象。例如 Border 類別。
#### ConcreteDecorator 參與者
具體的 Decorator 參與者，例如 SiderBorder 和 FullBorder 類別。

