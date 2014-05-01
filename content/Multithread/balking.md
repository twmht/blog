Title: Balking Pattern
Slug: balking
Category: Multithread
Author: twmht

如果現在不需要做這個動作，就直接return，Balking Pattern一般來說不會進入wait set，而是直接放棄不做。

換句話說，不一定要執行。

現在來寫一個在文書處理器上面經常提供的<font color=blue>自動儲存功能</font>

ServerThread會不斷地去儲存資料，而ClientThread則會不斷地修改資料並且儲存資料。

<font color=red> 當發現資料已經有儲存的時候，就不重複儲存，直接離開。</font>

表示資料的類別，Data.java

    :::java
    import java.io.IOException;
    import java.io.FileWriter;
    import java.io.Writer;

    public class Data {
        private final String filename;  // 儲存時的檔名
        private String content;         // 資料的內容
        private boolean changed;        // 修改後的內容還沒儲存的話，值為true

        public Data(String filename, String content) {
            this.filename = filename;
            this.content = content;
            this.changed = true;
        }

        // 修改資料內容
        public synchronized void change(String newContent) {
            content = newContent;
            changed = true;
        }

        // 若資料有修改，就儲存到檔案裡
        public synchronized void save() throws IOException {
            if (!changed) {
                //如果已經儲存過了，直接離開
                return;
            }
            doSave();
            changed = false;
        }

        // 實際將資料儲存到檔案裡用的方法
        private void doSave() throws IOException {
            System.out.println(Thread.currentThread().getName() + " calls doSave, content = " + content);
            Writer writer = new FileWriter(filename);
            writer.write(content);
            writer.close();
        }
    }

用來定期儲存資料的ServerThread類別，ServerThread.java

    :::java
    import java.io.IOException;

    public class SaverThread extends Thread {
        private Data data;
        public SaverThread(String name, Data data) {
            super(name);
            this.data = data;
        }
        public void run() {
            try {
                while (true) {
                    data.save();            // 儲存資料
                    Thread.sleep(1000);     // 休息約1秒
                }
            } catch (IOException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

用來修改以及儲存資料的ChangerThread類別,ChangerThread.java

    :::java
    import java.io.IOException;
    import java.util.Random;

    public class ChangerThread extends Thread {
        private Data data;
        private Random random = new Random();
        public ChangerThread(String name, Data data) {
            super(name);
            this.data = data;
        }
        public void run() {
            try {
                for (int i = 0; true; i++) {
                    data.change("No." + i);             // 修改資料
                    Thread.sleep(random.nextInt(1000)); // 模擬去做別的事
                    data.save();                        // 明確地要求存檔
                }
            } catch (IOException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            Data data = new Data("data.txt", "(empty)");
            new ChangerThread("ChangerThread", data).start();
            new SaverThread("SaverThread", data).start();
        }
    }

###gardede timed的實作###
除了balk離開或者是等待條件成立為止(Guarded Suspension Pattern)，還有一種折衷的作法，也就是等待一段的時間，如果條件還是不成立，就balk離開。

將timeout視為取消的一種，TimeoutException.java

    :::java
    public class TimeoutException extends InterruptedException {
        public TimeoutException(String msg) {
            super(msg);
        }
    }

具有Timeout的host類別。

    :::java
    public class Host {
        private final long timeout; // timeout值
        private boolean ready = false; // 如果可以執行方法的話則為true

        public Host(long timeout) {
            this.timeout = timeout;
        }

        // 更改狀態
        public synchronized void setExecutable(boolean on) {
            ready = on;
            notifyAll();
        }                                                           

        // 評斷狀態後執行之
        public synchronized void execute() throws InterruptedException, TimeoutException {
            long start = System.currentTimeMillis(); // 開始時刻
            while (!ready) {
                long now = System.currentTimeMillis(); // 現在時刻
                long rest = timeout - (now - start); // 剩下的等待時間
                if (rest <= 0) {
                    //等待時間已經到了，表示timeout
                    throw new TimeoutException("now - start = " + (now - start) + ", timeout = " + timeout);
                }
                //在wait set中等待rest時間之後，回來取得鎖定。
                wait(rest);
            }
            doExecute();
        }

        // 實際的處理動作
        private void doExecute() {
            System.out.println(Thread.currentThread().getName() + " calls doExecute");
        }
    }

Main.java
    
    :::java
    public class Main {
        public static void main(String[] args) {
            //timeout設定為10秒
            Host host = new Host(10000);
            try {
                System.out.println("execute BEGIN");
                host.execute();
            } catch (TimeoutException e) {
                e.printStackTrace();
            } catch (InterruptedException e) {
                e.printStackTrace();
            }
        }
    }

因為故意都沒有改變ready的狀態，所以一定會發生timeout。

###所有參與者
####GuardedObject 參與者
與 Guarded Suspension Pattern 不同，當防衛條件不成立時，就不執行實際動作，而直接離開。

在程式範例中，Data 類別就是 GuardedObject 參與者。save 方法與 change 方法則分別是 guardedMethod 與 stateChangingMethod。

範例程式的防衛條件是<b>changed 欄位的值為 true</b>。

###重點整理
####何時使用
什麼情況下，我們會想在動作前 balk 呢？
#####不需要刻意去執行的時候
範例程式中，當 content 欄位的內容沒有改變，就在 save 方法裡 balk 住了。

balk 的原因是 content 的內容已經寫在檔案裡了，沒有必要大費工夫再去寫一次。

像這樣<b>不需要刻意去執行</b>，就可以使用 Balking Pattern，在這裡 balk 的原因，是為了提高程式的執行效率。
#####不想等待防衛條件成立時
Balking Pattern 的特徵是<b>不等待</b>。當防衛條件不成立時，就馬上離開，進入下一個工作。
#####防衛條件只有第一次成立時
例如底下的 Something 類別，在這裡先用 initialized 欄位來表示是否已經初始化。呼叫 init 方法時，會先去檢查 initialized 欄位。

當 initialized 欄位的值為 true 時，表示已經初始化了，所以就直接 return 離開（就是 balk，設計成 throw 出例外也可以）。

當 initialized 欄位為 false 時，以 doInit 方法進行實際的初始化，接下來就設定 initialized 為 true，表示初始化動作已經處理完了（這相當於沒有 stateChangingMethod 方法的情況）

這種例子經常出現在實體的初始化及終結處理等<b>無法執行兩次以上的動作</b>中。

像 Something 類別的 initialized 這種<b>狀態只會變化一次的變數</b>，我們有時候稱為 latch。這個 latch，只有一鎖上就不會再打開了。

    :::java
    public class Something {
        private boolean initialized = false;
        public synchronized void init() {
            //防衛條件不成立之後，就絕對不會再次成立
            if (initialized) {
                return;
            }
            doInit();
            initialized = true;
        }
        private void doInit() {
            // 實際的初始化動作
        }
    }


