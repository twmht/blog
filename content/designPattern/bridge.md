Title: Bridge Pattern -- 分成功能階層和實作階層
Slug: bridge
Category: Design Pattern
Author: twmht

###用的時間點
bridge 是 **橋樑** 的意思。就像現實社會裡的橋樑擔負著連接河川兩岸的重責大任一樣，Bridge Pattern 也是負責連接兩個不同位置的參與者。
###如何設計
Bridge Pattern 居間溝通的兩個位置是指 **功能的類別階層** 和 **實作的類別階層**。

####想要新增功能時
假設現在有一個類別 Something，如果想對 Something 新增其它功能時(例如，想多加一個新方法)，首先要建立 SomethingGood 類別作為 Something 的子類別 (子類別、衍生類別或擴充類別)。這就是一個小型的類別階層。
這個階層是為了新增功能而建立:

* 基本功能放在父類別
* 新功能則新增到子類別

又稱為 **功能的類別階層**。
假設現在又想對 SomethingGood 類別新增另一個功能時。此時，要建立 SomethingBetter 類別作為 SomethingGood 類別的子類別。如此一來，功能的類別階層又往下延伸一層。

如欲追加新功能時，找出類別階層中最接近目的的類別，然後建立一個子類別、建立一個有該功能的新類別...。這就是一個功能的類別階層。基本上，類別階層也最好不要建立太多層。

####想要新增實作時
在 Template Method Pattern 中，抽象類別把一連串的方法群組宣告成抽象方法，再規定介面。然後由子類別實際實作這個抽象方法。父類別的作用是利用抽象方法來規定介面，子類別的作用則是進行實作。這樣把讓父類別扮演好參與者分工，可以建立出高零組件價值(可更換性)的類別。

這裡也有類別階層的影子，假設實作父類別 AbstractClass 的抽樣方法的子類別是 ConcreteClass，則可建立起一個小型類別階層。不過這裡的類別階層並不是為了新增功能，因為類別階層沒有追加新功能的目的。這個類別階層有下列的參與者分工:

* 父類別使用抽象方法來規定介面
* 子類別使用具體方法來實作此介面

這樣的類別階層就稱為 **實作的類別階層**。
假設現在要建立另一個 AbstractClass 的實作，若其子類別為 AnotherConcreteClass，則實作的階層會有一點變化。總之，如果要建立一個新的實作，必須建立 AbstractClass 的子類別，然後實作抽象方法，這就是實作的類別階層。

####類別階層的同處一室和獨立分離
當我們有一個念頭 **好，現在要做一個子類別**的時候，請先確認清楚自己想要完成的內容 **這個動作是要新增功能?還是要進行實作?**。如果類別階層只有一個的話，功能的類別階層和實作的的類別階層就會放在同一個階層構造裡。這樣可能會讓類別階層變得太複雜，而且不容易預測後面的發展。因為自己在建立子類別時，常常會搞不清楚應該放在類別階層的哪個位置。

既然如此，那就把 **功能的類別階層** 和 **實作的類別階層** 分成兩個獨立的類別階層吧。如果一分為二可能會弄的支離破碎，所以必須在兩個類別階層之間建立一座溝通的橋樑 (bridge)。

###程式範例
用來 **列印內容** 的程式。

<script src="https://gist.github.com/twmht/bdf3a8e71e7f4d11192e.js"></script>

####Abstraction (抽象化) 參與者
位於 **功能的類別階層** 最上層的類別，利用 Implementor 的方法只記載基本功能的類別。這個物件個體是保持住 Implementor。例如 Display 類別。
#### RefinedAbstraction (改良後的抽象化) 參與者
對 Abstraction 參與者新增功能的參與者。例如 CountDisplay 類別。
#### Implementor (實作者) 參與者
位於 **實作的類別階層** 最上層的類別，規定要實作 Abstraction 參與者之介面的方法。例如 DisplayImpl 類別。
#### ConcreteImplementor (具體的實作者) 參與者
具體實作 Implementor 參與者的介面。例如 StringDisplayImpl 類別。

###優點
如果想新增功能的話，就在功能的類別階層追加類別。這時候根本不需要修改實作的類別階層，而且所有新增加的功能都可以利用**所有實作**來使用。
在 Display 類別中使用了委讓。實作的物件個體被保留在 Display 的 impl 欄位中，所以會**輪流**:

* 若執行 open 時，則呼叫 impl.rawOpen()
* 若執行 print 時，則呼叫 impl.rawPrint()
* 若執行 close 時，則呼叫 impl.rawClose()

只要一聲該做事了，就會**交給 impl 辦**。

繼承是一種牢不可分的關係，若要修改類別關係，則要修改原始碼。但委讓是說分手就分手。因為它的對象是跟在產生 Display 類別的物件個體的階段時傳遞給引數的內容。例如 Main 類別產生 Display 和 CountDisplay 的物件個體時，就把 StringDisplayImpl 的物件個體傳遞給引數。

如果還有一個非 StringDisplayImpl 類別的 ConcreteImplementor 參與者傳遞給 Display 或者是 CountDisplay，則實作會很乾脆的切換過去。只要修改 Main 類別，不需要動到 Display 或 DisplayImpl 等程式碼。

### 問題

#### 1.假設要新增一個類別，讓它有**列印隨機次數**的處理能力。此時應該要擴充哪個類別？(假設列印的方法是 void randomDisplay(int times)，只有遇到大於0但小於 times 的時候才列印隨機次數)

這是屬於**功能**，則新增在**功能的類別階層**中。

    :::java
    import java.util.Random;

    public class RandomCountDisplay extends CountDisplay {
        private Random random = new Random();
        public RandomCountDisplay(DisplayImpl impl) {
            super(impl);
        }
        public void randomDisplay(int times) {
            multiDisplay(random.nextInt(times));
        }
    }

#### 2.假設要新增一個類別，讓它有**輸出文字檔內容**的處理能力。此時應該要擴充哪個類別？

擴充的是 **實作階層類別**，原先是利用 standard output，現在則新增一個實作類別輸出到檔案。

    :::java
    import java.io.*;

    public class FileDisplayImpl extends DisplayImpl {
        private String filename;
        private BufferedReader reader;
        private final int MAX_READAHEAD_LIMIT = 4096;   // 可反覆列印的上限（緩衝器容量）
        public FileDisplayImpl(String filename) {
            this.filename = filename;
        }
        public void rawOpen() {
            try {
                reader = new BufferedReader(new FileReader(filename));
                reader.mark(MAX_READAHEAD_LIMIT);
            } catch (IOException e) {
                e.printStackTrace();
            }
            System.out.println("=-=-=-=-=-= " + filename + " =-=-=-=-=-="); // 花邊
        }
        public void rawPrint() {
            try {
                String line;
                reader.reset(); // 捲回到mark的位置
                while ((line = reader.readLine()) != null) {
                    System.out.println("> " + line);
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        public void rawClose() {
            System.out.println("=-=-=-=-=-= "); // 花邊
            try {
                reader.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }

修改 Main 類別。

    :::java
    public class Main {
        public static void main(String[] args) {
            CountDisplay d = new CountDisplay(new FileDisplayImpl("star.txt"));
            d.multiDisplay(3);
        }
    }

#### 3.假設要新增一個列印結果: 列印第一個字元->列印多個裝飾字元->列印結束字元並且換行。反覆執行多行，裝飾字元數量會隨著反覆次數而增加。

在**功能類別階層**中，新增一個表示輸出內容逐漸增加次數的類別。

    :::java
    public class IncreaseDisplay extends CountDisplay {
        private int step; // 增加次數
        public IncreaseDisplay(DisplayImpl impl, int step) {
            super(impl);
            this.step = step;
        }
        public void increaseDisplay(int level) {
            int count = 0;
            for (int i = 0; i < level; i++) {
                multiDisplay(count);
                count += step;
            }
        }
    }

在**實作類別階層**中，新增一個表示輸出成字元的類別。

    :::java
    public class CharDisplayImpl extends DisplayImpl {
        private char head;
        private char body;
        private char foot;
        public CharDisplayImpl(char head, char body, char foot) {
            this.head = head;
            this.body = body;
            this.foot = foot;
        }
        public void rawOpen() {
            System.out.print(head);
        }
        public void rawPrint() {
            System.out.print(body);
        }
        public void rawClose() {
            System.out.println(foot);
        }
    }

只要修改 Main 類別即可。

    :::java
    public class Main {
        public static void main(String[] args) {
            IncreaseDisplay d1 = new IncreaseDisplay(new CharDisplayImpl('<', '*', '>'), 1);
            IncreaseDisplay d2 = new IncreaseDisplay(new CharDisplayImpl('|', '#', '-'), 2);
            d1.increaseDisplay(4);
            d2.increaseDisplay(6);
        }
    }
