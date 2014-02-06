Title: Builder Pattern -- 組合複雜的物件個體
Slug: builder
Category: Design Pattern
Author: twmht

###用的時間點
所謂萬丈高樓平地起，大樓首先得打穩地基並搭建骨架，再由上而下一層層蓋上去。一般來說，如果搭建的結構愈複雜就愈難一氣呵成。

###如何設計
你得先把整個架構分成幾個部份，等到個別部份都完成了之後再依序組合起來才行。

###程式範例
設計一個建立**文件**的程式吧!

* 含有一個標題
* 含有一些字串
* 含有一些有項目符號的項目

Builder 類別規定組成文件的方法，而 Director 類別利用這個方法才能產生一份文件具體的文件。

Builder 類別是抽象類別，不含實際的處理內容，僅宣告抽象方法而已。決定產生文件的具體處理內容則是 Builder 類別的子類別。

以下幾個類別為 Builder 類別的子類別。

* TextBuilder 類別
* HTMLBuilder 類別

Director 若使用 TextBuilder 則可產生一般格式的文件，如果使用 HTMLBuilder 則可產生 HTML 格式的文件。

<script src="https://gist.github.com/twmht/763c4db0a1d41388d333.js"></script>

####Builder 參與者
Builder 規定產生物件個體的介面。包括有產生物件個體各個部份的方法和取得最後結果的方法。例如 Builder 類別。
####ConcreteBuilder 參與者
ConcreteBuilder 是實作 Builder 介面的類別。在實際產生物件個體時所呼叫的方法就是在這裡定義。例如 TextBuilder 以及 HTMLBuilder。
####Director 參與者
Director 利用 Builder 的介面產生物件個體。設計程式必須注意不要被 ConcreteBuilder 牽著鼻子走。為了讓 ConcreteBuilder 無論在什麼情形之下都能正常發揮功能，所以只使用 Builder 的方法。例如 Director 類別。
####Client 參與者
利用 Builder Pattern 的參與者，例如 Main 類別。
