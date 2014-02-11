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
框架的部份。這是產生 Product 的抽象類別。具體內容則有子類別的 ConcreteCreater 決定。例如 Factory 類別。Creator 對於實際產生的 ConcreteProduct 完全一無所知。Creator 唯一知道的是只要呼叫出 Product 和產生物件個體的方法，就能產生 Product。例如 createProduct 方法是產生物件個體的方法。**如果用 new 的實際產生物件個體來取代產生物件個體的方法呼叫，則可解除實際類別名稱對父類別的約束。**
####ConcreteProduct (實際產品) 參與者
實際處理內容的部份。規定具體的產品樣式。例如 IDCard 類別。
####ConcreteCreater (實際生產者) 參與者
實際處理內容的部份。規定製造實際製品的類別。例如 IDCardFactory 類別。

###優點
####框架與內容
再範例程式中，framework 屬於框架，而 idcard 屬於內容。假設現在想要利用同一個框架建立不同的**產品**和**工廠**，例如產品 Television 類別以及電視機工廠　TelevisionFactory 類別。這時候當然要建立另外一個有 import framework　的　package television。

我們可以不必修改 package framework 就能建立完全不同的*產品*和*工廠*的地方。

package framework 並沒有 import package idcard。Product 類別和 Factory 類別也沒有任何具體的類別名稱（如 IDCard 及 IDCardFactory)。因此，如果要用同一個框架產生新類別時，完全不需要做任何修改。

###產生物件個體的方法的實作方式
在程式範例中，Factory 類別的 createProduct 方法是抽象方法。也就是說，這個方法需要在子類別進行實作。createProduct 方法的敘述方式有下列三種：
####寫成抽象方法
如果當作抽象方法，子類別就一定要實作這個方法。要是沒有實作的話，編譯的時候一定會檢查出來。
    
    :::java
    abstract class Factory{
        public abstract Product createProduct(string name);
        //...
    }

####另外準備預設的實作
萬一遇到子類別沒有進行實作的時候，就會使用這個實作。

    :::java
     class Factory{
        public Product createProduct(string name){
            return new Product(name);
        }
        //...
    }

不過這時候它是直接對 Product 類別做 new 的動作，所以不能把　Product 類別設為抽象類別。

####設為錯誤
當子類別沒有進行實作時，程式一執行就會發生錯誤（如果有程式錯誤時，就表示沒有進行實作）。

    :::java
     class Factory{
        public Product createProduct(string name){
            throw new FactoryMethodRuntimeException();
        }
        //...
    }

但是這種方式只限於另外還有一個 FactoryMethodRuntimeException　的情形。

###Pattern 利用與程式開發工程師之間的溝通
如果只看一個類別的話，根本無法確實掌握動作的方向。除了深入理解父類別的動作骨架並且找出其中的抽象方法之外，還要去看實際實作該抽象方法的類別的原始碼。

一般來說，利用設計 Pattern 設計類別群組時，一定要完整地把設計理念傳達給後續負責維護的人。

###問題
把 IDCard 類別加上卡片的流水號碼，讓 IDCardFactory 類別有一個持有人和流水編號的對照表。

不需要修改 framework.Product 類別、framework.Factory 類別或 Main 類別。即使要修改 IDCard 類別和 IDCardFactory 類別，也不用動到框架端的原始程式碼。

修改 IDCard 類別。

    :::java
    package idcard;
    import framework.*;

    public class IDCard extends Product {
        private String owner;
        private int serial;
        IDCard(String owner, int serial) {
            System.out.println("建立" + owner + "(" + serial + ")" + "的卡。");
            this.owner = owner;
            this.serial = serial;
        }
        public void use() {
            System.out.println("使用" + owner + "(" + serial + ")" + "的卡。");
        }
        public String getOwner() {
            return owner;
        }
        public int getSerial() {
            return serial;
        }
    }

修改 IDCardFactory 類別。

    :::java
    package idcard;
    import framework.*;
    import java.util.*;

    public class IDCardFactory extends Factory {
        private Hashtable database = new Hashtable();
        private int serial = 100;
        protected synchronized Product createProduct(String owner) {
            return new IDCard(owner, serial++);
        }
        protected void registerProduct(Product product) {
            IDCard card = (IDCard)product;
            database.put(card.getOwner(), new Integer(card.getSerial()));
        }
        public Hashtable getDatabase() {
            return database;
        }
    }
