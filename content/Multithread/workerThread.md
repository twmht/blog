Title: Worker Thread Pattern -- 等到工作來，來了就工作
Tags: thread,java
Slug: workerThread
Category: Multithread
Author: twmht

在 Worker Thread Pattern 中，worker thread 會依序抓一件工作來執行。當沒有工作時，worker thread 會停下來等待新的工作過來。

worker thread 也有人稱為 Background Thread。也有人把視點放在管理 worker thread 的地方，稱之為 thread pool。

程式範例：
<script src="https://gist.github.com/twmht/32e3250dc6035a60ed94.js"></script>

###所有參與者
####Client
Client 會建立 Requset，傳給 Channel。例如 ClientThread 類別。
####Channel
Channel 從 Client 取得 Request，傳給 Worker。例如 Channel 類別。
####Worker
Worker 會從 Channel 取得 Request，並執行這份工作。當工作結束以後，會去拿取下一個 Request。例如 WorkerThread 類別。
####Request
Request 用來表示工作，存放這份工作所需要的資料。例如 Request 類別。

###重點
####啟動執行緒也需要花時間
Worker Thread 重複使用執行緒，不像 Thread-Per-Message Pattern，它不會一直去建立新的執行緒。
####控制承載量
提高 Worker 的數量，可以提高並行處理的工作量。但如果準備的 Worker 數量比同時間的工作還要多，有些 worker 也派不上用場。所以有必要配合實際的需要，來調整 worker 的數量。

worker 的數量，可以有機動性變化：

* 最先從某個一定量的 worker 開始
* 當工作量增加時，增加 worker 數量
* 不過增加太多會用光記憶體，所以到達某個上限要停止增加
* 相反地，工作減少時(也就是待命中的 worker 增加時)，就結束掉一些 worker。

#### Request 的數量
增加 Channel 可以存放的 Request 數量，可緩衝 Client 與 Worker 的處理速度差，但是如果儲存太多 Request，也會佔用大量記憶體資源。

####Invocation 與 Execution 的分離
在 Worker Thread Pattern 與 Thread-Per-Message Pattern 中，將方法的啟動與執行分開，這也是 Command Pattern 的應用。有以下好處：

* 提高回應性
* 控制優先順序(可控制 Request 的處理優先順序)
* 可取消，可重複執行(雖然呼叫了，但是沒有執行。只要產生 Request，就可以重複執行)
* 分散處理的第一步(呼叫跟執行可以在不同的電腦上執行，相當於 Request 可以透過網路傳送到另外一台電腦上)

####增加工作的種類
可以藉由建立 Request 的子類別，來增加工作的種類，Channel 以及 Worker 都不需要修改，即使增加工作的種類，Worker 都只是呼叫 Request 的 execute 方法而已。

####如果只有一個 worker
那就不需要共用互斥了。

###問題
####1. 改寫 Channle 類別，使得請求傳進來時，就產生一個新的執行緒來處理請求。

改寫後的 Channel 類別。

    :::java
    public final class Channel {
        public Channel(int threads) {
        }
        public void startWorkers() {
        }
        public void putRequest(final Request request) {
            new Thread() {
                public void run() {
                    request.execute();
                }
            }.start();
        }
    }

####2. 以下的 GUI 程式中，預期結果是每秒之後的 label 會遞增顯示新的數字。但是結果是十秒之後直接顯示 9。請修改程式達成預期結果。

<script src="https://gist.github.com/twmht/ce69641ee03d614f6d64.js"></script>

原因就在於說 event-dispatching thread 要離開 actionPerformed 方法之後才會更新畫面。

採取 Thread-Per-Message 解決這個問題，在 countUp 方法中，啟動 invokerThread 執行緒。這個執行緒執行實際的累算動作。呼叫出 CountUp 的執行緒(Event Dispatching Thread) 啟動 invokerThread，馬上就從 countUp 方法回來。

invokerThread 當中，會從 0 開始進行累算，再以 sleep 方法休息約一秒。invokerThread 並非 event-dispatching thread。為了讓 event-dispatching thread 執行 setText 方法，就要使用 <code>SwingUtilities.invokeLater(executor)</code>，其中 executor 是一個 Runnable 物件，它執行了 setText 方法。

<script src="https://gist.github.com/twmht/4ab2c19e70bc0cb5aa7d.js"></script>

####3. 為了使程式在 5 秒內結束，將 Main 類別做了修改，請做出下列的其他修改。

* 在 Channel 類別加上 stopAllWorker 方法。這個方法可以用來結束掉所有 Channel 類別所管理的 WorkerThread 的執行緒。

* 在 ClientThread 類別加上 stopThread 方法，這個方法可以用來結束掉 ClientThread 的執行緒。

修改後的 Main 類別。

    :::java
    public class Main {
        public static void main(String[] args) {
            Channel channel = new Channel(5);   // 工人執行緒個數
            channel.startWorkers();
            ClientThread alice = new ClientThread("Alice", channel);
            ClientThread bobby = new ClientThread("Bobby", channel);
            ClientThread chris = new ClientThread("Chris", channel);
            alice.start();
            bobby.start();
            chris.start();

            try {
                Thread.sleep(5000);
            } catch (InterruptedException e) {
            }
            alice.stopThread();
            bobby.stopThread();
            chris.stopThread();
            channel.stopAllWorkers();
        }
    }



我們不去用 Thread 類別的 stop 方法，這是因為 stop 方法即使是對鎖定的執行緒，也能讓它結束，所以較不安全。

採取 Two Phase Termination Pattern 來解決此問題。

<script src="https://gist.github.com/twmht/dab196e0d01c2f986db8.js"></script>
