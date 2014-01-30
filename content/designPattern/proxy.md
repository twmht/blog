Title: Proxy Pattern
Slug: proxy
Category: Design Pattern
Author: twmht

###用的時間點
proxy就是代理人的意思，不需要本人親自去做的事情，就交給代理人去做。代理人是代替忙到無法自己動手的本人去處理工作。

###如何設計
代理人以及本人都是物件。

###程式範例
這次的範例是一個把字串輸出到畫面上的列表機。由 Main 類別產生 PrinterProxy 類別的物件個體。 該物件命名為 Alice，並將此名稱輸出到畫面上。 然後改名為Bob， 且輸出該新名稱。 在命名和取得名稱的階段都還沒有產生真正的 Printer 類別(就是本人個體)，命名和取得名稱的部份由 PrinterProxy 代理執行，最後呼叫 print 方法進入真正執行列印的階段，才由 PrinterProxy 類別產生 Printer 類別的物件個體。

PrinterProxy 以及 Printer 類別要一視同仁，故須定義 Printable Interface。

這個程式範例的前提要件是產生 Printer 類別的物件個體會花很多時間。 為了表現出費時的感覺，所以從建構子故意呼叫 heavyJob 方法。

<script src="https://gist.github.com/twmht/1672d63393eb403671f0.js"></script>

####Subject 參與者
規定對 Proxy 參與者和 RealSubject 參與者 一視同仁的API。因為已經有 Subject 參與者，所以 Client 參與者不需要去注意 Proxy 參與者跟 RealSubject 參與者有什麼差異。 例如 Printable Interface。
#### Proxy 參與者
Proxy 參與者會盡量處理 Client 參與者的要求。當自己無法單獨處理時，Proxy 參與者便會把工作交給 RealSubject 參與者。 要等到真正需要用到 RealSubject 參與者時， Proxy 參與者才會產生 RealSubject 參與者。 Proxy 參與者是實作 Subject 參與者規定的 API。 例如 PrinterProxy 類別。
#### RealSubject 參與者
當代理人束手無策的時候，就輪到本人 RealSubject 自己上場。這個參與者跟 Proxy 參與者同樣都要實作 Subject 參與者規定的 API。例如 Printer 類別。
#### Client 參與者
利用 Proxy Pattern 的參與者，例如 Main 類別。
