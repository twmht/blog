Title: Visitor Pattern -- 在結構中穿梭還同時做事
Slug: visitor
Category: Design Pattern
Author: twmht

###用的時間點
資料結構裡儲存了很多個元素，假設現在要對所有元素進行一項 "處理"。那麼，這項 "處理" 的程式碼應該寫在哪裡？以常理來判斷，應該要寫在表示資料結構的類別裡面，不過如果這項 "處理" 的動作不只一個的話，該怎麼辦? 每次要做新處理的時候，就必須修改資料結構的類別。
###如何設計
Visitor Pattern 把 "資料結構" 和 "處理" 兩者分開，另外寫一個表示在資料結構內穿梭來去的主體 "訪客" 的類別，然後把處理交給這個類別來進行。如此一來，如果想追加新的處理動作時，只要再建立一個新的訪客即可。而在資料結構這邊，也只要能接受來敲門的訪客就能完成動作。

###程式範例
這個程式是訪客穿梭在由檔案和目錄組成的資料結構內，以列印檔案總覽。

<script src="https://gist.github.com/twmht/4ff936559e5bf100a3d1.js"></script>

####Visitor (訪客) 參與者
Visitor 是對每個資料結構中的具體元素 (ConcreteAcceptor) 宣告 "已經去找過XXXX" 的 visit(XXXX) 方法。visit(XXXX) 是處理 XXXX 的方法，實際原始碼則寫在 ConcreteVisitor 那裡。例如 Visitor 類別。
#### ConcreteVisitor 參與者
ConcreteVisitor 是實作 Visitor 的介面。它實作 visit(XXXX) 格式的方法，然後敘述各個 ConcreteAcceptor 的處理。 在前面的程式範例中，扮演這個角色的是 ListVisitor 類別。就像 ListVisitor 的 currentdir 欄位之值會發生變化一樣，在處理 visit(XXXX) 的過程中，ConcreteVisitor 的內部狀態也會有變化。
#### Acceptor 參與者
Acceptor 是表示 Visitor 訪問對象的參與者。宣告接受訪客的 accept 方法。Visitor 則被傳遞給 accept 方法的引數。例如 Acceptor 介面。
#### ConcreteAcceptor 參與者
ConcreteAcceptor 實作 Acceptor 的介面，例如 File 以及 Directory 類別。

