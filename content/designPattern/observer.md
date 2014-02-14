Title: Observer Pattern
Slug: observer
Category: Design Pattern
Author: twmht

###用的時間點
observer是觀察的人，也就是觀察者的意思。
當被Observer Pattern列入觀察名單的狀態發生變化，就會通知觀察者。在寫一些跟狀態變化有關的處理時，Observer Pattern是很好用的工具。

###如何設計
重點在於設計Observer Interface以及有具體實作的Observer類別。另外，也需要設計被觀察者。

###程式範例
觀察者觀察產生多個數值的物件，然後輸出該值，輸出方式因觀察者而異。在這個範例中，有用數字來輸出的觀察者以及用長條圖來輸出的觀察者。

在 Observer Interface 中，呼叫 update 方法的是產生數值的 NumberGenerator ( generator 是 "產生器" "產生設備" 的意思)。update 方法是 NumberGenerator 用來告訴 Observer 說 "我的內容已經更新過了，請你也更新你的輸出內容" 的方法。


<script src="https://gist.github.com/twmht/3fd90157d2327707922e.js"></script>

####Subject (被觀察者) 參與者
表示被觀察的一方。Subject 參與者具有登錄或刪除 Observer 參與者的方法。另外也有宣告了 "取得目前狀態" 的方法。例如 NumberGenerator 類別。
#### ConcreteSubject 參與者
表示實際 "被觀察的一方" 的參與者。一旦狀態有變化，就會立刻通知已登錄的 Observer 參與者。例如 RandomNumberGenerator 類別。
#### Observer 參與者
被 Subject 參與者通知 "狀態有變化" 的參與者。通知的方法是 update。例如 Observer 介面。
#### ConcreteObserver 參與者
實際的 Observer。一呼叫 update 方法時，即可從該方法取得 Subject 參與者的目前狀態。 例如 DigitalObserver 類別和 GraphObserver 類別。

###優點
####讓類別再利用
RandomNumberGenerator 類別並不知道現在在觀察自己的到底是 DigitalObserver 還是 GraphObserver 的物件個體。但是儲存在 observers 欄位的物件個體知道有實作 Observer 介面。因為這些物件個體是以 addObserver 新增而來，所以一定會實作 Observer 介面，也絕對能呼叫 update 方法。

而 DigitalObserver 類別也不會去注意自己所觀察的是 RandomNumberGenerator 還是其它 XXXXNumberGenerator 的物件個體。不過仍然知道這是 NumberGenerator 的子類別的物件個體，而且具有 getNumber 方法。

只要設計如下，就能達到以上的效果：

* 先利用抽象類別和介面從實際類別抽出抽象方法
* 當以引數傳遞物件個體或將物件個體儲存在欄位時，把它設成抽象類別或介面的型別，不要寫成實際的型別

###當Observer 的行為會影響 Subject 的時候
Subject 發生變化，然後通知 Observer，Observer 再呼叫 Subject 的方法。這是 Observer Pattern 一般的情況，假設 Observer 呼叫 Subject 的方法時，同時也會影響到 Subject 的狀態，那麼又要再通知 Observer，然後再...，這樣反而會一直在呼叫方法。解決方式就是在 Observer 中加一個旗標變數來表示**目前是否有 Subject 的通知**即可。

###通知的意義重於觀察
雖然 observer 是叫作**觀察者**，但實際上它是被動等待 Subject 的通知。Observer Pattern 又可稱為 Publish-Subscribe Pattern。

###問題
####1. 建立一個子類別 IncrementalNumberGenerator，讓它擴充 NumberGenerator 類別並逐一加計數值的功能。其建構子有下列三個引數:

* 開始的數值
* 結束的數值
* 增加幅度

另外，要讓　DigitalObserver 及　GraphObserver 類別觀察其動作。

    :::java
    public class IncrementalNumberGenerator extends NumberGenerator {
        private int number;                     // 目前數值
        private int end;                        // 結束數值（不含此值）
        private int inc;                        // 增加若干
        public IncrementalNumberGenerator(int start, int end, int inc) {
            this.number = start;
            this.end = end;
            this.inc = inc;
        }
        public int getNumber() {                // 取得數值
            return number;
        }
        public void execute() {
            while (number < end) {
                notifyObservers();
                number += inc;
            }
        }
    }

Main 類別。

    :::java
    public class Main {
        public static void main(String[] args) {
            NumberGenerator generator = new IncrementalNumberGenerator(10, 50, 5); 
            Observer observer1 = new DigitObserver();
            Observer observer2 = new GraphObserver();
            generator.addObserver(observer1);
            generator.addObserver(observer2);
            generator.execute();
        }
    }

####2. 新增一個　ConcreteObserver 參與者。

建立一個圓餅圖的 ConcreteObserver。

<script src="https://gist.github.com/twmht/1fd95a6801c7f161f21b.js"></script>
