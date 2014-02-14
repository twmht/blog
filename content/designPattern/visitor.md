Title: Visitor Pattern -- 在結構中穿梭還同時做事
Slug: visitor
Category: Design Pattern
Author: twmht

###用的時間點
資料結構裡儲存了很多個元素，假設現在要對所有元素進行一項 **處理**。那麼，這項 **處理** 的程式碼應該寫在哪裡？以常理來判斷，應該要寫在表示資料結構的類別裡面，不過如果這項 **處理** 的動作不只一個的話，該怎麼辦? 每次要做新處理的時候，就必須修改資料結構的類別。
###如何設計
Visitor Pattern 把 **資料結構** 和 **處理** 兩者分開，另外寫一個表示在資料結構內穿梭來去的主體 **訪客** 的類別，然後把處理交給這個類別來進行。如此一來，如果想追加新的處理動作時，只要再建立一個新的訪客即可。而在資料結構這邊，也只要能接受來敲門的訪客就能完成動作。

###程式範例
這個程式是訪客穿梭在由檔案和目錄組成的資料結構內，以列印檔案總覽。

<script src="https://gist.github.com/twmht/4ff936559e5bf100a3d1.js"></script>

####Visitor (訪客) 參與者
Visitor 是對每個資料結構中的具體元素 (ConcreteAcceptor) 宣告 **已經去找過XXXX** 的 visit(XXXX) 方法。visit(XXXX) 是處理 XXXX 的方法，實際原始碼則寫在 ConcreteVisitor 那裡。例如 Visitor 類別。
#### ConcreteVisitor 參與者
ConcreteVisitor 是實作 Visitor 的介面。它實作 visit(XXXX) 格式的方法，然後敘述各個 ConcreteAcceptor 的處理。 在前面的程式範例中，扮演這個角色的是 ListVisitor 類別。就像 ListVisitor 的 currentdir 欄位之值會發生變化一樣，在處理 visit(XXXX) 的過程中，ConcreteVisitor 的內部狀態也會有變化。
#### Acceptor 參與者
Acceptor 是表示 Visitor 訪問對象的參與者。宣告接受訪客的 accept 方法。Visitor 則被傳遞給 accept 方法的引數。例如 Acceptor 介面。
#### ConcreteAcceptor 參與者
ConcreteAcceptor 實作 Acceptor 的介面，例如 File 以及 Directory 類別。

###優點
**把處理從資料結構分出來**。通常 ConcreteVisitor 可以單獨開發，不必跟 File 類別或 Directory 類別雜在一起;換句話說，Visitor Pattern 能提高 File 類別和 Directory 類別的**零件獨立性**。假設現在想要把一個處理動作設計成 File 類別和 Directory 類別的方法，每次想新增**處理**功能時就得去修改 File 類別和 Directory 類別，反而會變得麻煩。
####新增 ConcreteVisitor 很容易
因為具體的處理可以直接丟給 ConcreteVisitor 去做，不需要為了這個處理就去修改 ConcreteAcceptor。

###雙重調度
Visitor Pattern 的方法呼叫可整理如下:

* accept 方法的呼叫為: acceptor.accept(visitor)
* visit 方法的呼叫為: visitor.visit(acceptor)

兩者剛好站在相反的立場。Visitor Pattern 由 ConcreteAcceptor 和 ConcreteVisitor 來決定實際的處理。一般成為雙重調度(double dispatch)。

###The Open-Closed Principle
這個原則是主張類別應該:

* 擴充(extension)時要開放(open)
* 修改(modification)時要封閉(closed)

除非有特殊理由，否則程式設計師在設計類別時都應該容許以後繼續擴充該程式。若無正當理由，就不應該禁止後人擴充程式。這就是擴充時要開放。

但是，如果每次擴充程式時還要去修改現有類別的話，那就太麻煩。所以，在擴充程式時沒有修改現有類別的需要正是**修改時要關閉**的真正意義。

總之，就是**在不修改現有類別的原則下就可以擴充**。


###新增ConcreteAcceptor 較為困難
假設要新增一個 Entry 類別的子類別，叫作 Device 類別。此時，必須先在 Visitor 類別建立一個 visit(Device) 方法。然後還要在 Visitor 的所有子類別都要實作這個 visit(Device) 方法。

###Visitor 要怎樣做才能進行處理
Acceptor 必須公開足夠的資訊給 Visitor。例如，visit(Directory)裡面對每個目錄進入點都有執行 accept。如果想要做這樣的處理動作，Directory 必須提供**能取得所有目錄進入點**的 iterator 方法。

訪客很努力從資料結構取得必要的資訊。如果不能取得必要的資訊情報，訪客就不能發揮百分之百的功能。但是萬一把另外不應該公開的資訊公開出來，反而也會增加以後的維護困難。

###問題

####1.請新增一個類別，叫作 FileFindVistor 類別。這個類別是找出符合指定副檔名的檔案。

不需要修改 File 類別 或 Directory 類別。以抓出所有 html 為例。

<script src="https://gist.github.com/twmht/ae21ccbca4d0d47b98f1.js"></script>

####2.Directory 類別的 getSize 方法是進行**取得目錄容量的處理**。請把這個方法改寫成**取得容量大小**的 SizeVisitor 類別。

就是把該**處理**獨立開來。

修改 Directory 類別。

    :::java
    import java.util.Iterator;
    import java.util.Vector;

    public class Directory extends Entry {
        private String name;                    // 目錄名稱
        private Vector dir = new Vector();      // 目錄進入點的集合
        public Directory(String name) {         // 建構子
            this.name = name;
        }
        public String getName() {               // 取得名稱
            return name;
        }
        public int getSize() {                  // 取得目錄容量
            SizeVisitor v = new SizeVisitor();  
            accept(v);                          
            return v.getSize();                 
        }
        public Entry add(Entry entry) {         // 新增進入點
            dir.add(entry);
            return this;
        }
        public Iterator iterator() {
            return dir.iterator();
        }
        public void accept(Visitor v) {
            v.visit(this);
        }
    }

新增 SizeVisitor 類別。

    :::java
    import java.util.Iterator;

    public class SizeVisitor extends Visitor {
        private int size = 0;
        public int getSize() {
            return size;
        }
        public void visit(File file) {
            size += file.getSize();
        }
        public void visit(Directory directory) {
            Iterator it = directory.iterator();
            while (it.hasNext()) {
                Entry entry = (Entry)it.next();
                entry.accept(this);
            }
        }
    }

####3.請在 java.util.Vector 建立一個具有 Acceptor 介面功能的 AcceptorVector 類別。讓它能對 AcceptorVector 的物件個體 add Directory 和 File 的物件個體，而且也能 accept ListVisitor 的物件個體。

AcceptorVector 類別是 java.util.Vector 的子類別，被定義要實作 Acceptor。add 方法是繼承自 Vector，不需要另外定義。

    :::java
    import java.util.Vector;
    import java.util.Iterator;

    class AcceptorVector extends Vector implements Acceptor {
        public void accept(Visitor v) {
            Iterator it = iterator();
            while (it.hasNext()) {
                Acceptor a = (Acceptor)it.next();
                a.accept(v);
            }
        }
    }

Main 如下。

    :::java
    import java.util.Iterator;

    public class Main {
        public static void main(String[] args) {
            try {
                Directory root1 = new Directory("root1");
                root1.add(new File("diary.html", 10));
                root1.add(new File("index.html", 20));

                Directory root2 = new Directory("root2");
                root2.add(new File("diary.html", 1000));
                root2.add(new File("index.html", 2000));

                AcceptorVector vec = new AcceptorVector();
                vec.add(root1);
                vec.add(root2);
                vec.add(new File("etc.html", 1234));

                vec.accept(new ListVisitor());
            } catch (FileTreatmentException e) {
                e.printStackTrace();
            }
        }
    }
