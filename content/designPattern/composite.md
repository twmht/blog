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
