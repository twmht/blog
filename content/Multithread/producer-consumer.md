Title: Producer-Consumer Pattern -- 我來做，你來用
Slug: producer-consumer
Category: Multithread
Author: twmht

Producer-Consumer Pattern是架構在之前的Guarded Suspension Pattern上，例如Producer就是Client，負責發出request，而Consumer就是Server，負責接收request。
<font color=red>而重要的的地方在於存放Data的資料結構在Producer-Consumer Pattern會有Capacity的限制</font>，如果Capacity是無限大的話，若是Producer速度很快，但是Consumer速度很慢，則Data會不斷地產生出來，那麼記憶體就會很快耗盡。

以下舉一個廚師（Producer）跟客人（Consumer)的例子，廚師會不停地做蛋糕放到桌上（Table)，而客人會不停地拿蛋糕起來吃。桌子最多可以放三個蛋糕，若滿了，廚師就要等，若空了，客人就要等，Capacity大小可以調整兩邊的速度。

廚師，MakerThread.java

    :::java
    import java.util.Random;
    public class MakerThread extends Thread {
        private final Random random;
        private final Table table;
        private static int id = 0; // 蛋糕的流水號(所有廚師共通)
        public MakerThread(String name, Table table, long seed) {
            super(name);
            this.table = table;
            this.random = new Random(seed);
        }
        public void run() {
            try {
                while (true) {
                    Thread.sleep(random.nextInt(1000));
                    String cake = "[ Cake No." + nextId() + " by " + getName() + " ]";
                    table.put(cake);
                }
            } catch (InterruptedException e) {
            }
        }
        private static synchronized int nextId() {
            return id++;
        }
    }

客人，EaterThread.java

    :::java
    import java.util.Random;

    public class EaterThread extends Thread {
        private final Random random;
        private final Table table;
        public EaterThread(String name, Table table, long seed) {
            super(name);
            this.table = table;
            this.random = new Random(seed);
        }
        public void run() {
            try {
                while (true) {
                    String cake = table.take();
                    Thread.sleep(random.nextInt(1000));
                }
            } catch (InterruptedException e) {
            }
        }
    }

桌子，Table.java
    
    :::java
    public class Table {
        private final String[] buffer;
        private int tail;  // 下一個put的地方
        private int head;  // 下一個take的地方
        private int count; // buffer內的蛋糕數
        public Table(int count) {
            this.buffer = new String[count];
            this.head = 0;
            this.tail = 0;
            this.count = 0;
        }
        // 放置蛋糕
        public synchronized void put(String cake) throws InterruptedException {
            System.out.println(Thread.currentThread().getName() + " puts " + cake);
            while (count >= buffer.length) {
                wait();
            }
            buffer[tail] = cake;
            tail = (tail + 1) % buffer.length;
            count++;
            notifyAll();
        }
        // 取得蛋糕
        public synchronized String take() throws InterruptedException {
            while (count <= 0) {
                wait();
            }
            String cake = buffer[head];
            head = (head + 1) % buffer.length;
            count--;
            notifyAll();
            System.out.println(Thread.currentThread().getName() + " takes " + cake);
            return cake;
        }
    }

Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            Table table = new Table(3);     // 建立可以放置3個蛋糕的桌子
            new MakerThread("MakerThread-1", table, 31415).start();
            new MakerThread("MakerThread-2", table, 92653).start();
            new MakerThread("MakerThread-3", table, 58979).start();
            new EaterThread("EaterThread-1", table, 32384).start();
            new EaterThread("EaterThread-2", table, 62643).start();
            new EaterThread("EaterThread-3", table, 38327).start();
        }
    }

###所有參與者
####Data 參與者
Data 參與者由 Producer 參與者所建立，並由 Consumer 參與者所使用。
例如 String 類別(蛋糕)。
####Producer 參與者
Producer 參與者會建立 Data 參與者，傳遞給 Channel 參與者。例如 MakerThread。
####Consumer 參與者
Consumer 參與者會從 Channel 參與者取得 Data 參與者。例如 EaterThread。
####Channel 參與者
Channel 參與者會從 Producer 參與者處接收 Data 參與者，並保管起來。並應 Consumer 參與者的要求，將 Data 參與者傳送出去。為了確保安全性，Producer 參與者與 Consumer 參與者要對存取進行共用排斥。

當 Producer 將 Data 傳給 Channel 時，若 Channel 的狀態無法接受 Data 時，這時 Producer 會在 Channel 的狀態變成可接受之前，保持等待狀態。

當 Consumer 從 Channel 取得 Data 的時候，若 Channel 沒有 Data 可以給 Consumer 時，這時候 Consumer 在 Channel 可以傳送 Data 之前，保持等待狀態。

當存在多個 Producer 與 Consumer 時，為了使處理不互相干涉，Channel 也要進行共用互斥。

像這樣，Channel 介於 Producer 以及 Consumer 之間，擔任傳送 Data 之中繼站的角色。

例如 Table 類別。

###重點整理
####提高 Channel 的再利用性
範例程式中，Table 類別的 put 方法與 take 方法都使用 Guarded Suspension Pattern。但 MakerThread 類別與 EaterThread 類別都不相依於 Table 類別的詳細實作。也就是說，MakerThread 不必理會其它執行緒，只要呼叫 put 方法即可 ; 而 EaterThread 也是只要會呼叫 take 方法就好了。使用 synchronized、wait、notifyAll 這些考慮到多執行緒動作的程式碼，全部隱藏在 Channel 參與者裡面。
####直接傳遞的差別？
接下來要來比較直接呼叫方法與透過 Channel 的情況。
#####直接呼叫方法
Consumer 想要取得 Data，通常是想要利用 Data 做一些處理。如果 Producer 直接呼叫 Consumer 的話，就相當於對 Data 進行處理的是 Producer 執行緒，而不是 Consumer 執行緒。

直接呼叫對方的方法，就好像廚師製作蛋糕直接交給客人，等客人吃完再做下一個，這樣太浪費了。
#####透過 Channel 傳遞
Producer 將 Data 交給 Channel 之後，不用等待 Consumer，而可以馬上開始至坐下一個 Data。Producer 的動作不會受到 Consumer 的進度的左右。
####Channel 的負荷
範例程式中，廚師最多可以擺上三個蛋糕，如果要擺第四個以上，就必須要等待到客人拿走蛋糕才行。如果客人吃的很慢，那廚師也要等很久。

也就是說，桌上的蛋糕數量，會直接影響到緩衝 MakerThread 與 EaterThread 間處理速度的落差。而如果提高 Channel 可容許的數量，如果客人吃的很慢，則蛋糕會愈積愈多，一段時間之後還是會達到上限。

像 Guarded Suspension Pattern 的範例程式，使用 java.util.LinkedList，就可以實作出沒有儲存量上限的 Channel 了。但是這樣做，還是會因為 EaterThread 平均速度較慢的情況下，最後還是會因為記憶體不足，無法配置存放蛋糕的實體。
####以什麼順序傳遞 Data
當 Channel 有多個 Data 時，要以什麼順序傳遞給 Consumer 呢？
#####Queue -- 最先收到的先傳
先進先出。
#####Stack -- 最後收到的先傳
後進先出。
#####Priority Queue -- 優先的東西先傳
給予 Data 優先順序，優先性高的先傳。
####共用互斥
思考執行緒的共用互斥的問題時，把觀察切入點放在*保護著什麼*上面，會比較容易找到問題的癥結。可以得到下面兩個口訣。

1. 執行緒的合作要想*放在中間的東西*
2. 執行緒的互斥要想*應該保護的東西*

合作與互斥是表裡一體的。執行緒為了協調合作，所以必須進行共用互斥，使共用的東西不會毀損。而執行緒的共用互斥，也是為了讓執行緒合作才進行的。

###問題
####1. 請在 Table 類別加上偵錯用的輸出，使執行緒是否有在進行 wait 等待能更加一目了然。
<script src="https://gist.github.com/twmht/d8d42a6677ce01aca943.js"></script>
####2.請在 Table 類別中，加上用來清除桌上所有蛋糕的 clear 方法。
<script src="https://gist.github.com/twmht/5540391d88534e7baaa4.js"></script>
####3.更改 Main 類別，使程式能再開始執行約 10 秒後結束掉所有執行緒，然後程式就此結束。
<script src="https://gist.github.com/twmht/47ba4c032e296b49677a.js"></script>
####4. Host 類別的 execute 方法，會依照參數 count 指定的次數，連續呼叫 doHeavyJob 方法。doHeavyJob 是很繁重的工作，而且還取消不掉。當 count 參數傳入的數字一大，執行緒光是要離開 execute 方法，就要執行很久。請改寫 execute 方法，使它可以中途取消。

    :::java
    public class Host {
        public static void execute(int count) {
            for (int i = 0; i < count; i++) {
                doHeavyJob();
            }
        }
        private static void doHeavyJob() {
            // 下面的程式碼
            // 是用來取代「無法取消的繁重工作」
            // （停留約10秒的迴圈）
            System.out.println("doHeavyJob BEGIN");
            long start = System.currentTimeMillis();
            while (start + 10000 > System.currentTimeMillis()) {
                // busy loop
            }
            System.out.println("doHeavyJob END");
        }
    }

改寫後如下。
<script src="https://gist.github.com/twmht/08996bc6ec3bd377f593.js"></script>

####5. 以下程式改寫 Table 類別，將 notifyAll 改成 notify，使用這個類別，有可能出現蛋糕無法傳遞的情況。
請思考原因並寫出程式證明想法：

    :::java
    public class Table {
        private final String[] buffer;
        private int tail;  // 下一個put的地方
        private int head;  // 下一個take的地方
        private int count; // buffer內的蛋糕數
        public Table(int count) {
            this.buffer = new String[count];
            this.head = 0;
            this.tail = 0;
            this.count = 0;
        }
        // 放置蛋糕
        public synchronized void put(String cake) throws InterruptedException {
            System.out.println(Thread.currentThread().getName() + " puts " + cake);
            while (count >= buffer.length) {
                wait();
            }
            buffer[tail] = cake;
            tail = (tail + 1) % buffer.length;
            count++;
            notify();
        }
        // 取得蛋糕
        public synchronized String take() throws InterruptedException {
            while (count <= 0) {
                wait();
            }
            String cake = buffer[head];
            head = (head + 1) % buffer.length;
            count--;
            notify();
            System.out.println(Thread.currentThread().getName() + " takes " + cake);
            return cake;
        }
    }

notify 方法只會從在 waitset 中等待的執行緒中呼叫一個。因此無關的執行緒進入 waitset 時若碰上 notify 引發該執行緒時，notify 所要進行的通知就沒意義了。

LazyThread 類別雖然在 Table 的實體上進行 wait，但卻是什麼都不做。Main 類別內混進 LazyThread 的執行緒並且予以執行的話，程式執行到一半會停下來。

這是由於為了呼叫 LazyThread，而隨便濫用 notify 方法只故。如果我們使用 notifyAll 而不是 notify 的話，即使參雜了 LazyThread 的執行緒，程式也不會停止而繼續執行。
<script src="https://gist.github.com/twmht/ed269955633cde7b11c6.js"></script>

####6. Something 類別宣告一個 method 方法，請問這個方法有什麼功能？

    :::java
    public class Something {
        public static void method(long x) throws InterruptedException {
            if (x != 0) {
                Object object = new Object();
                //外部沒有辦法獲得這個實體，因此不會被 notify 或 notifyAll。
                synchronized (object) {
                    object.wait(x);
                }
            }
        }
    }

Something.method(long) 相當於 Thread.sleep(long)。
