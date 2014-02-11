Title: Decorator Pattern -- 對裝飾和內容一視同仁
Slug: decorator
Category: Design Pattern
Author: twmht

###用的時間點
海綿蛋糕、鮮奶油蛋糕、草莓奶油蛋糕或生日蛋糕的原型其實都是海綿蛋糕，只不過運用了各種修飾技巧，能符合不同目的而改變。
###如何設計
物件也很像是蛋糕的多變化，首先建立一個像是海綿蛋糕的核心物件，再一層層加上裝飾用的功能，就可以完全符合所需的物件。
###程式範例
在字串周圍加上裝飾外框後再列印出來的程式。裝飾外框是指以-,+,| 等字元組成的框線。

<script src="https://gist.github.com/twmht/74632b289d5d81ac90d2.js"></script>

####Component 參與者
新增功能的核心參與者。在蛋糕的比喻說明中，相當於裝飾前的海綿蛋糕。Component 只規定海綿蛋糕的介面。例如 Display 類別。
#### ConcreteComponent 參與者
實作 Component 介面的具體海綿蛋糕。例如 StringDisplay 類別。
#### Decorator (裝飾者) 參與者
具有跟 Component 參與者相同的介面，另外還有 Decorator 要修飾的 Component。這個參與者是 "早就知道" 自己要去修飾的對象。例如 Border 類別。
#### ConcreteDecorator 參與者
具體的 Decorator 參與者，例如 SiderBorder 和 FullBorder 類別。

###優點
####可穿透的介面
對裝飾外框與內容一視同仁。例如**裝飾外框**的 **Border** 類別是表示**內容**的 **Display** 類別的子類別，這就是一視同仁。換句話說，Border 類別以及其子類別具有跟表示**內容**的 Display  類別相同的介面。

即使用裝飾外框把內容包起來，也不能隱藏介面，gelColumns,getRows,getRowText, 以及 show 這幾個方法並沒有被隱藏起來，還是可以從其他類別看得到。這個特性就稱為**可穿透性**的介面。

如 **b4** 所示，即使用了再多的裝飾外框，介面本身仍然沒有受到影響。

因為介面具有可穿透性，所以 Decorator Pattern 就有跟 Composite Pattern 很像的遞迴架構。也就是說，這個架構是**裝飾外框所儲存的內容實際上是另外一個裝飾外框**。兩者很像，但目的不同，Decorator Pattern 的目的是為了新增功能。

####可新增功能但內容不變
在 Decorator Pattern 當中，裝飾外框和內容具有共用的介面。雖然介面是共用，但功能逐漸一一新增進去的話，外面就一層層愈包愈多。如果是用 SiderBorder 來包 Display 的話，列印時可以設定在左右兩邊加入新的裝飾字元; 如果是用 FullBorder 來包，整個外圍都要加上裝飾外框。你並不需要去修改它的包裝方式，因為它**不需要換掉被包起來的主體，就能新增其他功能**。

Decorator Pattern 有使用到**委讓**。所有對裝飾外框的要求都會推到**內容**去。例如 SiderBorder 的 getColumns 會呼叫 display.getColumns()。

####可新增動態功能
Decorator Pattern 所使用的委讓並沒有緊密結合類別，所以不需要修改框架的原始碼就能建立一個改變物件關係的新物件。

####即使只有簡單的種類規劃，也可增加多種功能
利用 Decorator Pattern 可以新增多種不同的功能，因為只要有準備好多種具體裝飾外框，就能隨意組合成新物件。各個外框就算很簡單也無所謂。

###實例
java.io 是一個管理 input/output 的 package。

首先，可建立一個從檔案讀入資料的物件個體，例如：

Reader reader = new FileReader("datafile.txt");

而從檔案讀入資料時，會需要做 buffering。

Reader reader = new BufferedReader(new FileReader("datafile.txt"));

如此一來，如果要建立 BufferedReader 類別的物件個體時，就會指定 FileReader 類別的物件個體作為實際上資料被讀入的位置。

接著，還有行號管理的部份。

Reader reader = new LineNumberReader(new BufferedReader(new FileReader("datafile.txt")));

Reader 類別的物件個體及其子類別的物件個體可傳遞給 LineNumberReader 或 BufferedReader 的建構子。

有時候不一定會做緩衝處理，例如

Reader reader = new LineNumberReader(new FileReader("datafile.txt"));

###缺點
彼此類似的小類別一不小心就愈建愈多。

###問題

####1.請新增一個 UpDownBorder 類別，讓它能列印出上下的裝飾字元。

<script src="https://gist.github.com/twmht/8bf5d472e352942dd2b3.js"></script>

####2.請新增一個 ConcreteComponent 參與者，假設它是可列印多個字串的 MultiStringDisplay 類別。

<script src="https://gist.github.com/twmht/5a18ece53156e565e125.js"></script>
