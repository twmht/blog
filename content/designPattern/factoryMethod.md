Title: Factory Method Pattern -- 建立物件個體可交給子類別
Slug: FactoryMethod
Category: Design Pattern
Author: twmht

###用的時間點
把 Template Method Pattern 應用在建立物件個體上面。
###如何設計
在父類別規定物件個體的建立方法，但並沒有深入到較具體的類別。所有具體的完整內容都放在子類別。根據這個原則，我們可以大致分成產生物件個體的大綱和實際產生物件個體的類別兩方面。

###程式範例
建立一個生產身份證的 factory。Product 類別和 Factory 類別屬於 framework 這個 package。負責建立產生物件個體大綱。

IDCard 類別和 IDCardFactory 類別則處理實際的內容，屬於 idcard 這個 package。

<script src="https://gist.github.com/twmht/bb3f738c08ff7891be19.js"></script>

####Product (產品) 參與者
框架的部份。這個抽象類別是規定此 Pattern 所產生的物件個體應有的介面，具體內容則由子類別的 ConcreteProduct 規定。例如 Product 類別。
####Creater (生產者) 參與者
框架的部份。這是產生 Product 的抽象類別。具體內容則有子類別的 ConcreteCreater 決定。例如 Factory 類別。
####ConcreteProduct (實際產品) 參與者
實際處理內容的部份。規定具體的產品樣式。例如 IDCard 類別。
####ConcreteCreater (實際生產者) 參與者
實際處理內容的部份。規定製造實際製品的類別。例如 IDCardFactory 類別。
