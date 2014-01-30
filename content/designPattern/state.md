Title: State Pattern
Slug: state
Category: Design Pattern
Author: twmht

###用的時間點
用類別來表示 "狀態" 。

###如何設計
以類別來表示狀態之後，只要切換類別就能表現 "狀態變化"，而且在必須新增其它狀態時，也很清楚該編寫哪個部份。

###程式範例
假設現在有一個會隨著時間改變警備狀態的金庫保全系統：

* 有一個金庫
* 金庫有跟保全中心連線
* 金庫有警鈴和一般通話用的電話
* 金庫有時鐘，監視目前的時間
* 白天是9:00-16:59，晚間為17:00-23:59以及0:00-8:59
* 只有白天才能使用金庫
* 在白天使用金庫時，保全中心會保留使用紀錄
* 若晚間使用金庫時，保全中心會接到發生異常現象的通知
* 警鈴是24小時都可以使用
* 一旦使用警鈴，保全中心會接收到警鈴通知
* 一般通話用的電話是24小時都可以使用(但晚間只有答錄機服務)
* 在白天使用電話時，就會呼叫保全中心
* 若晚間使用電話時，則會呼叫保全中心的答錄機

<script src="https://gist.github.com/twmht/a04e437a923e01314421.js"></script>

####State 參與者
State 表示狀態。規定不同狀態下做不同處理的介面。這個介面等於是一個不同狀態所做處理的所有方法的集合。例如 State 介面。
####ConcreteState 參與者
ConcreteState 是表示具體的不同狀態，具體實作在 State 所規定的介面。例如 DayState 以及 NightState 類別。
####Context 參與者
Context 具有表示現在狀態的 ConcreteState，而且還規定 State Pattern 的利用者所需要的介面。例如 Context 介面以及 SafeFrame 類別。
Context 介面負責規定介面的部份，SafeFrame 類別則負責具有 ConcreteState 參與者的部份。
