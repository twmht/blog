Title: Producer-Consumer Pattern
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
