Title: Abstract Factory Pattern -- 把相關零件組合成產品
Slug: abstractFactory
Category: Design Pattern
Author: twmht

###用的時間點
所謂的**抽象**，意思是指**不考慮要如何具體進行實作**，只注意介面的部份。抽象工廠把各種抽象零件組合成產品。
###如何設計
處理的重點是在**介面**而不是零件的具體實作。只利用介面就能把零件組合成產品。

###程式範例
將一個階層結構的相關網站鏈結做成HTML檔。

包含下列三個 package 的類別群組:

* factory --- 含抽象工廠、零件和產品
* 含 Main 的預設package
* listfactory --- 含具體工廠、零件和產品

<script src="https://gist.github.com/twmht/c98ac2b197d3c3ed7a48.js"></script>

####AbstractProduct 參與者
AbstractProduct 規定由 AbstractFactory 所產生的抽象零件及產品的介面。例如 Link、Tray 和 Page 類別。
#### AbstractFactory 參與者
AbstractFactory 規定用來產生 AbstractProduct 的物件個體的介面。例如 Factory 類別。
#### Client 參與者
Client 是一個只使用 AbstractFactory 和 AbstractProduct 的介面來完成工作的參與者。Client 並不知道具體零件、產品和工廠。例如 Main 類別。
#### ConcreteProduct 參與者
ConcreteProduct 是實作 AbstractProduct 的參與者:

* listfactory package --- ListLink、ListTray 以及 ListPage 等類別。
* tablefactory package --- TableLink、TableTray 以及 TablePage 等類別。
