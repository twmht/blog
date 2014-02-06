Title: Adapter Pattern -- 換個包裝再度利用
Slug: adapter
Category: Design Pattern
Author: twmht

###用的時間點
例如將直流電換成交流電，轉換器的功能是介入既有內容和需要結果之間，作為溝通的橋樑。

如果既有內容無法直接利用時，通常需要先轉換成必要的型態後再使用。具有填平**既有內容**和**需要結果**兩者間的**落差**就是 **Adapter Pattern**。

###如何設計
設計wrapper，將既有內容包裝之後，重新再利用。

###程式範例(繼承)

改變輸出字串的外框，採用繼承。

<script src="https://gist.github.com/twmht/3576c41a962cb0ef2671.js"></script>

###程式範例(委讓)
改變輸出字串的外框，採用繼承。

<script src="https://gist.github.com/twmht/d89785e518eab0bf410e.js"></script>


####Target (對象) 參與者
決定現在需要什麼方法的參與者，例如筆記型電腦必須要有直流電才能動。例如 Print 介面。
#### Client 參與者
利用 Target 的方法來做事的參與者，例如有直流電 12V 才能用的比較型電腦。例如 Main 類別。
#### Adaptee (被動符合) 參與者
具有既有方法的參與者，也就是交流電 110V 的交流電電源。例如 Banner 類別。

如果擔任 Adaptee 參與者的方法與 Target 參與者的方法有相符時(即電源不需要轉換)，那就不需要 Adapter 參與者了。
#### Adapter 參與者
利用 Adaptee 的方法努力滿足 Target 的要求。例如，把交流電 110V 轉換成直流電 12V 的轉換器。例如 PrintBanner 類別。

如果是類別的 Adapter Pattern，Adapter 要透過**繼承**的方式來利用 Adaptee。而換到物件個體時，就要改以**委讓**來利用 Adaptee。
