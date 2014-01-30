Title: Observer Pattern
Slug: observer
Category: Design Pattern
Author: twmht

###用的時間點
observer是觀察的人，也就是觀察者的意思。
當被Observer Pattern列入觀察名單的狀態發生變化，就會通知觀察者。在寫一些跟狀態變化有關的處理時，Observer Pattern是很好用的工具。

###如何設計
重點在於設計Observer Interface以及有具體實作的Observer類別。另外，也需要設計被觀察者。

###程式範例
觀察者觀察產生多個數值的物件，然後輸出該值，輸出方式因觀察者而異。在這個範例中，有用數字來輸出的觀察者以及用長條圖來輸出的觀察者。

在 Observer Interface 中，呼叫 update 方法的是產生數值的 NumberGenerator ( generator 是 "產生器" "產生設備" 的意思)。update 方法是 NumberGenerator 用來告訴 Observer 說 "我的內容已經更新過了，請你也更新你的輸出內容" 的方法。


<script src="https://gist.github.com/twmht/3fd90157d2327707922e.js"></script>

####Subject (被觀察者) 參與者
表示被觀察的一方。Subject 參與者具有登錄或刪除 Observer 參與者的方法。另外也有宣告了 "取得目前狀態" 的方法。例如 NumberGenerator 類別。
#### ConcreteSubject 參與者
表示實際 "被觀察的一方" 的參與者。一旦狀態有變化，就會立刻通知已登錄的 Observer 參與者。例如 RandomNumberGenerator 類別。
#### Observer 參與者
被 Subject 參與者通知 "狀態有變化" 的參與者。通知的方法是 update。例如 Observer 介面。
#### ConcreteObserver 參與者
實際的 Observer。一呼叫 update 方法時，即可從該方法取得 Subject 參與者的目前狀態。 例如 DigitalObserver 類別和 GraphObserver 類別。
