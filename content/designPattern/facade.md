Title: Facade Pattern -- 單一窗口
Slug: facade
Category: Design Pattern
Author: twmht

###用的時間點
程式這個東西往往愈做愈大，許多類別彼此間的影響讓關係更加錯綜複雜。因此在使用類別時，要確實了解類別之間的關係，正確依序呼叫方法。
利用大型程式進行資料處理時，必須精確控制相關的類別。既然如此，就乾脆設個處理專用的"窗口"，如此一來就不需要個別控制類別，只要把要求丟給"窗口"即可。
###如何設計
Facade Pattern 能整合錯綜複雜的來龍去脈，提供較為高級的介面。Facade 參與者則是讓系統外埠看到較簡單的介面。而且 Facade 參與者還會兼顧系統內部各類別功能和互動關係，以最正確的順序利用類別。

###程式範例
設計一個產生使用者 Web 網頁的程式。
以三個類別的簡單系統為例，這個系統中包含有利用郵件信箱取得姓名的資料庫(Database)、產生 HTML 檔的類別(HtmlWriter)以及提供較高級介面的類別(PageMaker，也就是 Facade 參與者)。

<script src="https://gist.github.com/twmht/2df294dc66cd9a1008ce.js"></script>

####Facade (正面) 參與者
構築成系統的其他參與者之"單一窗口"。Facade 對系統外部提供較高級且單一的介面。例如 PageMaker 類別。
#### 構築成系統的其他參與者
其他林林種種的參與者則各司其職，Facade 參與者的存在並不會有任何影響。它們乖乖的聽從 Facade 的呼叫出來做事，但不會反過來呼叫 Facade。例如 Database 及 HtmlWriter 類別。
#### Client 參與者
利用 Facade Pattern 的參與者。例如 Main 類別。
