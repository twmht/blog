Title: Mutex
Slug: mutex
Category: Multithread
Author: twmht

如果可以不要用syncronized來做到thread-safe，那麼可以考慮使用mutex。

現在來修改在[Single Threaded Execution Pattern](http://twmht.github.io/blog/posts/2013/10/multithread/Introduction.html)所用到的Gate類別。

    :::java
    public class Gate {
        private int counter = 0;
        private String name = "Nobody";
        private String address = "Nowhere";
        private final Mutex mutex = new Mutex();
        public void pass(String name, String address) { // 並非synchronized
            mutex.lock();
            try {
                this.counter++;
                this.name = name;
                this.address = address;
                check();
            } finally {
                mutex.unlock();
            }
        }
        public String toString() { // 並非synchronized
            String s = null;
            mutex.lock();
            try {
                s = "No." + counter + ": " + name + ", " + address;
            } finally {
                mutex.unlock();
            }
            return s;
        }
        private void check() {
            if (name.charAt(0) != address.charAt(0)) {
                System.out.println("***** BROKEN ***** " + toString());
            }
        }
    }

問題是，Mutex這個類別要如何設計?
    我們設計一個lock方法，並且在其中設定一個busy欄位，表示目前是不是已經釋放鎖定了。同時也設定一個unlock方法，釋放鎖定。

ok，現在來設計一個simple mutex，建立Mutex.java

    :::java
    public final class Mutex {
        private boolean busy = false;
        //必須設定成syncronized,因為busy是一個shared resource
        public synchronized void lock() {
            while (busy) {
                try {
                    //當還沒拿到鎖定的時候，先進入wait set
                    wait();
                } catch (InterruptedException e) {
                }
            }
            busy = true;
        }
        public synchronized void unlock() {
            busy = false;
            //叫醒其它在wait set中的執行緒。
            notifyAll();
        }
    }

但是這樣設計並不好，雖然在Gate類別運作良好，但假設有某個執行緒連續呼叫兩次lock，則會變成在還沒釋放鎖定之前就把自己關到wait set中。
另外，即使是沒有獲得鎖定的執行緒，也可以呼叫unlock方法，邏輯上會變得很奇怪。

以下是一個改良過後的Mutex.java。利用locks紀錄目前的lock數量，當然lock數量只會有一個，並且紀錄一個owner來紀錄誰呼叫了這個lock。

    :::java
    public final class Mutex {
        private long locks = 0;
        private Thread owner = null;
        public synchronized void lock() {
            Thread me = Thread.currentThread();
            while (locks > 0 && owner != me) {
                try {
                    //若被叫醒回來發現lock大於0的話，則再回去wait set。
                    wait();
                } catch (InterruptedException e) {
                }
            }
            // locks == 0 || owner == me
            owner = me;
            locks++;
        }
        public synchronized void unlock() {
            Thread me = Thread.currentThread();
            if (locks == 0 || owner != me) {
                return;
            }
            // locks > 0 && owner == me
            locks--;
            if (locks == 0) {
                owner = null;
                notifyAll();
            }
        }
    }
