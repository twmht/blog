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

#### ConcreteFactory 參與者
ConcreteFactory 實作 AbstractFactory 的介面：

* listfactory package --- ListFactory 類別
* tablefactory package --- TableFactory 類別

###優點
####新增具體工廠很容易
因為要建立哪些類別以及該實作哪些方法一清二楚，當然就簡單許多。

假設現在想新增其他的具體工廠。固定動作不外乎就是建立 Factory, Link, Tray, Page 的子類別，實作各個抽象方法。換句話說，就是要讓含有 factory package 的類別的抽象部份全部具體化。

此時，無論新增幾個具體工廠(或修改具體工廠的 bug)，都不需要再去修改抽象工廠或 Main 的部份。

###新增零件就很有難度
假設現在想要在 factory package 新增一個顯示影像的 Picture 零件。此時，所有已經存在的具體工廠都要修改成有支援 Picture。以 listfactory package 為例，要修改的動作包括：

* 在 ListFactory 類別新增 createPicture 方法
* 新增一個 ListPicture 類別

已經完工的具體工廠愈多，修改動作就愈多。

###問題
####1. 在 Tray 類別中，tray 欄位被定義為 protected。如果改成 private，優缺點為何?

優點是其子類別(實作 Tray 的類別)跟 tray 不會有依存關係。缺點則是不能直接參照，必須另外寫一個取得 tray 欄位的方法。

####2. 假設現在想在 Factory 類別中定義一個 **可產生只有 Yahoo 鏈結的網頁的具體方法**，也就是 **public page createYahooPage()**， 網頁作者和標題都是 Yahoo，此時具體工廠和具體零件要如何修改?

只有 Factory 類別和 Main 類別需要修改。

<script src="https://gist.github.com/twmht/93b775cdf35af47cf826.js"></script>

####3. Page 類別的作用和 Tray 類別很像，為什麼不乾脆把 Page 類別寫成是 Tray 類別的子類別呢?

因為 Page 不能 add 到 Tray (HTML 語法不合)。如果把 Page 類別設為 Tray 類別的子類別，則 Page 也是 Item 的子類別，故也可以 add。

但是必須在 Page 類別宣告 makeHTML。若如下建立一個含有 makeHTML 方法的 java 的介面的 HTMLLable，修改由 Item 類別和 Page 類別 implements HTMLLable，則可讓整個程式更加嚴謹。

    :::java
    public interface HTMLLable{
        public abstract String makeHTML();
    }
