Title: Flyweight Pattern
Slug: flyweight
Category: Design Pattern
Author: twmht

###用的時間點
當想要節省記憶體空間的時候使用。

###如何設計
儘量共用物件個體，不做無謂的new。

###程式範例
輸出大型文字。

<script src="https://gist.github.com/twmht/aa42efa98d66a87a5271.js"></script>

####Flyweight 參與者
表示以一般處理會讓程式變重，因此選擇共用較佳的參與者。例如BigChar類別。
####Flyweight FlyweightFactory 參與者
產生Flyweight 參與者的工廠。利用這個工廠來產生 Flyweight 參與者，即可共用物件個體。　例如BigCharFactory類別。
####Client 參與者
利用 FlyweightFactory 參與者產生並使用 Flyweight 參與者。例如 BigString 類別。
