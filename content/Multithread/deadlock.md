Title: DeadLock
Slug: deadlock
Category: Multithread
Author: twmht

所謂的死結，是指兩個執行緒分別取得了鎖定，互相等待另外一個執行緒解除鎖定的現象，發生死結的時候，哪個執行緒都無法繼續執行下去，這時候程式就會不斷等待。

假設有兩個人(Alice and Boddy)在用餐，餐具只有兩個，分別是spoon以及fork，Alice的習慣是左手拿spoon，接著右手拿fork才會開始用餐;Boddy的習慣是左手拿spoon，接著右手拿fork之後才開始用餐。
現在寫一個程式去模擬整個過程，一個不小心可能會出現一個情況：Alice左手拿了spoon，等待fork，但Boddy左手已經拿了fork，等待spoon，這樣互相等待共享資源的情況，就會產生deadlock。

以下是會產生deadlock的程式。

建立shared resource，如下的Tool.java

    :::java
    public class Tool {
        private final String name;
        public Tool(String name) {
            this.name = name;
        }
        public String toString() {
            return "[ " + name + " ]";
        }
    }

Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            System.out.println("Testing EaterThread, hit CTRL+C to exit.");
            Tool spoon = new Tool("Spoon");
            Tool fork = new Tool("Fork");
            new EaterThread("Alice", spoon, fork).start();
            new EaterThread("Bobby", fork, spoon).start();
        }
    }

EaterThread.java

    :::java
    public class EaterThread extends Thread {
        private String name;
        private final Tool lefthand;
        private final Tool righthand;
        public EaterThread(String name, Tool lefthand, Tool righthand) {
            this.name = name;
            this.lefthand = lefthand;
            this.righthand = righthand;
        }
        public void run() {
            while (true) {
                eat();
            }
        }
        public void eat() {
            //Alice拿起了spoon,在還沒拿到fork之前，bob已經拿到了fork
            synchronized (lefthand) {
                System.out.println(name + " takes up " + lefthand + " (left).");
                //兩個人都在等對方的資源
                synchronized (righthand) {
                    System.out.println(name + " takes up " + righthand + " (right).");
                    System.out.println(name + " is eating now, yam yam!");
                    System.out.println(name + " puts down " + righthand + " (right).");
                }
                System.out.println(name + " puts down " + lefthand + " (left).");
            }
            }
        }

要怎麼解決deadlock的問題？當然就是改寫程式囉！

##要先了解deadlock會發生在下列三種情況都成立的時候:##

* 具有多個shared resource，例如上述的spoon以及fork。
* 執行緒鎖定一個shared resource時，還沒解除鎖定就想去鎖定另外一個shared resource。
* 取得shared resource的順序不固定，例如先拿spoon再拿fork以及先拿fork再拿spoon。

只要打破其中一種條件，就能解除deadlock。

現在來打破第三個條件，讓拿resource的順序可以一致。

修改Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            System.out.println("Testing EaterThread, hit CTRL+C to exit.");
            Tool spoon = new Tool("Spoon");
            Tool fork = new Tool("Fork");
            //修改順序
            new EaterThread("Alice", spoon, fork).start();
            new EaterThread("Bobby", spoon, fork).start();
        }
    }

這樣就可以打破死結。

第二個條件比較難打破，因為必須同時拿兩個工具才能開始吃東西。

現在來試著打破第一個條件，我們可以試著把spoon以及fork合併在一起。

定義一個Pair.java

    :::java
    public class Pair {
        private final Tool lefthand;
        private final Tool righthand;
        public Pair(Tool lefthand, Tool righthand) {
            this.lefthand = lefthand;
            this.righthand = righthand;
        }
        public String toString() {
            return "[ " + lefthand + " and " + righthand + " ]";
        }
    }

修改Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            System.out.println("Testing EaterThread, hit CTRL+C to exit.");
            Tool spoon = new Tool("Spoon");
            Tool fork = new Tool("Fork");
            Pair pair = new Pair(spoon, fork);
            new EaterThread("Alice", pair).start();
            new EaterThread("Bobby", pair).start();
        }
    }

這時候EaterThread.java也就可以被修改成只存取一個resource。

    :::java
    public class EaterThread extends Thread {
        private String name;
        private final Pair pair;
        public EaterThread(String name, Pair pair) {
            this.name = name;
            this.pair = pair;
        }
        public void run() {
            while (true) {
                eat();
            }
        }
        public void eat() {
            //只鎖定pair這個shared resource
            synchronized (pair) {
                System.out.println(name + " takes up " + pair + ".");
                System.out.println(name + " is eating now, yam yam!");
                System.out.println(name + " puts down " + pair + ".");
            }
        }
    }

deadlock是個很有趣且在Multithread上經常會碰到的問題，但只要打破三個條件中的其中一個就可以讓deadlock不成立。
