Title: Composite Pattern -- 對容器和內容一視同仁
Slug: composite
Category: Design Pattern
Author: twmht

###用的時間點
舉例來說，目錄和檔案都可以放在目錄底下，因此可以一視同仁。
###如何設計
可以把目錄想成是容器，檔案想成是內容，容器底下可能是內容，也可能是更小一號的容器。
###程式範例
以模擬方式表示檔案和目錄的程式。表示檔案的類別是 File 類別、表示目錄的是 Directory 類別，兩者合併起來就是父類別 Entry 類別。Entry 類別是表示目錄進入點的類別，對 File 和 Directory 一視同仁的類別。

<script src="https://gist.github.com/twmht/3aa67b2bb2be40cd03ca.js"></script>

####Leaf 參與者
表示內容的參與者。不可以放入其他東西。例如 File 類別。
#### Composite 參與者
表示容器的參與者。可放入 Leaf 或 Composite。例如 Directory 類別。
#### Component 參與者
對 Leaf 和 Component 一視同仁的參與者。Component 是 Leaf 和 Composite 共用的父類別。例如 Entry 類別。
#### Client 參與者
利用 Composite Pattern 的人，例如 Main 類別。

###實例
[Kent Beck Testing Framework](http://www.objectclub.jp/community/memorial/homepage3.nifty.com/masarl/article/testing-framework.html)
[Simple Smalltalk Testing: With Patterns](http://www.xprogramming.com/testfram.htm)
###優點
####單複數的一視同仁
Composite Pattern 對容器和內容一視同仁，這也可以稱為單複數的一視同仁。也就是說，**把複數個物體集中在一起，可像是在處理一個整體**。就以程式的測試動作為例，假設 Test1 是鍵盤輸入的輸入測試，Test2 是檔案匯入的輸入測試，Test3 是網路匯入的輸入測試。如果現在想把 Test1, Test2, Test3 這三個整合成一個**輸入測試**，利用 Component Pattern 就能辦到。先把複數個測試集中起來設為 **輸入測試**，再建立一個包含其他測試的**輸出測試**，最後兩者合起來便成為**輸出/輸入測試**。

###細節
####add 要放在哪裡?
我們在 Entry 類別定義 add 方法，然後再丟出例外。實際上能使用 add 方法的也只有 Directory 類別而已。add 方法的擺放及實作有幾種可能：
#####在 Entry 類別進行實作並且設為程式錯誤
這是程式範例的作法。在實際能使用 add 方法的 Directory 類別則重新寫入 Entry 類別的 add，置換成有意義的實作。

由於 File 類別從 Entry 類別繼承到 add 方法，所以可以做 add。但會丟出例外。
#####在 Entry 類別進行實作，沒有任何動作
也就是主體為空。
#####在 Entry 類別有宣告，但沒實作
在 Entry 類別把 add 方法設為抽象方法，如果有必要則另外在子類別加以定義，無此必要則設為程式錯誤，這也是一種作法。好處是可以統一處理，不過如此一來就必須在 File 類別實作根本不需要的 add。
#####只放在 Directory 類別
這種作法是不把 add 方法放在 Entry 類別，只有真正有必要的 Directory 類別才放。但是若採取這種作法時，如果 add 到 Entry 型態變數(其實際內容為 Directory 的物件個體)，就必須一個個強迫轉型成 Directory 型態。

###問題
####如果現在想在程式範例中新增一個能從 Entry 的物件個體(其子類別的物件個體)取得**全路徑**的功能，例如想從 File 的物件個體取得字串 "/root/usr/yuki/Composite.java"，該修改哪個類別?

把 parent 欄位保留在 Entry。在根目錄時，則 parent 為 null。從接收到的物件個體往上回溯到 parent 欄位，則可以建立出全路徑。要修改的是 Entry 類別和 Directory 類別。在Directory 類別則用 add 方法修改 parent 欄位。

<script src="https://gist.github.com/twmht/5afae2a800526ac9f1fc.js"></script>
