Title: Chain of Responsibility Pattern -- 責任轉送
Slug: chainOfResponsibility
Category: Design Pattern
Author: twmht

###用的時間點
什麼是 "轉送" 呢? 假設現在要到某家公司去取文件，跟櫃台小姐說明來意後，他會告訴你應該到 "業務窗口" 去處理。當你走到業務窗口後，那邊又告訴你這份文件目前由 "客戶服務部" 負責;因此你得再到客戶服務部去一趟，找到客戶服務部後，小姐還是很客氣的說文件應該要到 "文管中心" 去拿。像這樣子把自己的要求傳送下去，一直找到適當的人選或地點就是 "轉送"。
###如何設計
例如，現在產生一個要求，但無法直接決定處理該要求的物件。這時候，可以把一個以上的物件串聯成鎖鏈狀，依序走過這個連鎖物件再決定最後目的地的物件。
如果使用這個 Pattern，可以降低 "要求端" 和 "處理端" 之間的結合性，讓它們個別成為獨立的零件。另外，還可支援有需依發生狀況改變處理要求的物件的程式。
先對人產生一個要求，如果這個人有處理的能力就處理掉;如果不能處理的話，就把要求轉送給 "第二個人"。同樣的，如果第二個人有處理能力的話就處理掉，不能處理的話，就繼續轉送給第三個人，以此類推。

###程式範例
這個程式會產生問題以及決定解決問題的人。例如一開始先是 Bob 在努力解決問題，但無法解決的時候就換成 Diana 接手。在這個過程中，都沒有發現 Alice 的蹤影，因為 Alice 只負責轉送所有問題。

<script src="https://gist.github.com/twmht/7eeb3b146fbdc6fd0ef9.js"></script>

####Handler (處理者) 參與者
Handler 是規定處理要求的介面的參與者。它會維持住 "下一個人"，萬一出現自己無法處理的要求時，再轉送過去。當然， "下一個人" 也是 Handler。例如 Support 類別。處理要求的方法則是 support 方法。
#### ConcreteHandler 參與者
ConcreteHandler 是具體處理要求的參與者。例如NoSupport、LimitSupport、OddSupport 以及 SpecialSupport 這幾個類別。
#### Client (要求者) 參與者
Client 是對第一個 ConcreteHandler 發出要求的參與者，例如 Main 類別。
