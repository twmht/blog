Title: Two-Phase Termination Pattern -- 快把玩具收拾好，去睡覺吧
Tags: thread, java
Slug: twoPhaseTermination
Category: Multithread
Author: twmht

Two-Phase Termination Pattern 是用來確實地進行結束的動作後，再結束掉執行緒。

我們將執行緒進行平常的處理的狀態稱為**作業中**。當希望結束這個執行緒時，則送出**中止請求**。接著這個執行緒，並不會馬上結束，而會開始進行必要的善後工作。這個狀態稱為**終止處理中**。從**作業中**改變成**終止處理中**是第一階段。

**終止處理中**的狀態並不會進行平常的動作。雖然執行緒還在運行，但進行的是終止處理。直到**終止處理中**結束後，才真正結束執行緒。**終止處理中**的動作結束，是第二階段。

先從**作業中**進入**終止處理中**狀態，再真正結束掉執行緒。主要考慮的關鍵如下：

* 安全地結束(安全性)
* 一定會進行終止處理(生命性)
* 收到終止請求後，要盡快開始終止處理(回應性)

###範例程式
有一條執行緒會在每隔約 500 毫秒將計數遞增 1，而我們要在約 10 秒後結束程式。

<script src="https://gist.github.com/twmht/2a703442a85a40338bad.js"></script>

###參與者
####TerminationRequest
TerminationRequest 對 Terminator 送出終止請求。例如 Main 類別。
####Terminator
Terminator 會接受終止請求，實際進行終止處理。Terminator 提供有用來提出終止請求的 shutdownRequest 方法。我們沒必要對 shutdownRequest 方法使用 Single Threaded Execution Pattern。

當 shutdownRequest 方法被呼叫，Terminator 就會在考慮到安全性的情況下，自己進入**終止處理中**的狀態。接著在終止處理執行完畢後，執行緒正式結束。

Terminator 有一個 flag 來表示自己是否已經收到終止請求。並在可以安全地開始進行終止處理的地方，檢查這個 flag。如果檢查 flag 的動作很頻繁，那從收到終止請求，直到真正進入**終止處理中**狀態所間隔的時間，就可以縮短。例如 CountupThread 類別。

###重點
####不可以使用 Thread 類別的 stop 方法
<code>java.lang.Thread</code>中的 stop 方法，會強制將正在執行 critical section 的執行緒結束掉，因此缺乏資料安全性。
####只檢查 flag 也不夠
shutdownRequest 方法除了將 flag 設定為 true 之外，也呼叫了 interrupt 方法，原因在於說執行緒可能正在 sleep 或者是 wait，因此需要呼叫 interrupt 來改變執行緒的狀態。
####進行繁重的處理之前，先檢查終止請求
為了使收到終止請求前，能儘快開始終止處理，故每當要開始繁重的處理前，應該先檢查 shutdownRequested flag，或是呼叫 isShutdownRequested 方法。這樣一來，可使程式的**回應性**提高。
####程式的結束與 addShutdownHook 方法
<code>java.lang.Runtime</code>的 addShutdownHook。可在程式結束時，呼叫所指定的 thread 的 start 方法。

    :::java
    public class Main {
        public static void main(String[] args) {
            System.out.println("main:BEGIN");

            // 設定shutdown hook
            Runtime.getRuntime().addShutdownHook(
                new Thread() {
                    public void run() {
                        System.out.println("*****");
                        System.out.println(Thread.currentThread().getName() + ": SHUTDOWN HOOK!");
                        System.out.println("*****");
                    }
                }
            );

            System.out.println("main:SLEEP...");

            // 約3秒後強制結束程式
            try {
                Thread.sleep(3000);
            } catch (InterruptedException e) {
            }

            System.out.println("main:EXIT");

            // 在這裡強制結束
            System.exit(0);

            // 不會執行到這裡
            System.out.println("main:END");
        }
    }

###問題
####1.中斷狀態的變化。以下程式沒有檢查 shutdownRequested 這個 flag，但是仍然可以正常結束。請把它修改成無法正常結束。

拿掉 flag 之後的 CountThread 類別。

    :::java
    public class CountupThread extends Thread {
        // 計數器的值
        private long counter = 0;


        // 終止請求
        public void shutdownRequest() {
            interrupt();
        }

        // 動作
        public void run() {
            try {
                while (!isInterrupted()) {
                    doWork();
                }
            } catch (InterruptedException e) {
            } finally {
                doShutdown();
            }
        }

        // 作業
        private void doWork() throws InterruptedException {
            counter++;
            System.out.println("doWork: counter = " + counter);
            Thread.sleep(500);
        }

        // 終止處理
        private void doShutdown() {
            System.out.println("doShutdown: counter = " + counter);
        }
    }

因為 sleep 方法會丟出 InterruptedException。因此只要忽略這個 InterruptedException，就可以使程式無法正常被執行。

    :::java
    public class CountupThread extends Thread {
        // 計數器的值
        private long counter = 0;

        // 終止請求
        public void shutdownRequest() {
            interrupt();                    
        }                                   

        // 動作
        public void run() {
            try {
                while (!isInterrupted()) {
                    doWork();
                }
            } catch (InterruptedException e) {
            } finally {
                doShutdown();
            }
        }

        // 作業
        private void doWork() throws InterruptedException {
            counter++;
            System.out.println("doWork: counter = " + counter);
            try {
                Thread.sleep(500);
            } catch (InterruptedException e) {
                //在這裡先抓下來，直接忽略掉
            }
        }

        // 終止處理
        private void doShutdown() {
            System.out.println("doShutdown: counter = " + counter);
        }
    }

####2.改寫 CountupThread 類別定義的 doShutdown 方法，將呼叫 doShutdown 方法時，counter 欄位的值會存到檔案 counter.txt 裡面。

如下，

    :::java
    import java.io.IOException;
    import java.io.FileWriter;

    public class CountupThread extends Thread {
        // 計數器的值
        private long counter = 0;

        // 已經送出終止請求則為true
        private volatile boolean shutdownRequested = false;

        // 終止請求
        public void shutdownRequest() {
            shutdownRequested = true;
            interrupt();
        }

        // 判斷終求請求是否已經送出
        public boolean isShutdownRequested() {
            return shutdownRequested;
        }

        // 動作
        public void run() {
            try {
                while (!shutdownRequested) {
                    doWork();
                }
            } catch (InterruptedException e) {
            } finally {
                doShutdown();
            }
        }

        // 作業
        private void doWork() throws InterruptedException {
            counter++;
            System.out.println("doWork: counter = " + counter);
            Thread.sleep(500);
        }

        // 終止處理
        private void doShutdown() {
            System.out.println("doShutdown: counter = " + counter);
            System.out.println("doShutdown: Save BEGIN");
            try {
                FileWriter writer = new FileWriter("counter.txt");
                writer.write("counter = " + counter);
                writer.close();
            } catch (IOException e) {
                e.printStackTrace();
            }
            System.out.println("doShutdown: Save END");
        }
    }

####3. Template Method Pattern。請改寫 CountupThread 類別，使其成為 GracefulThread 類別的子類別。

    :::java
    public class GracefulThread extends Thread {
        // 已經送出終止請求則為true
        private volatile boolean shutdownRequested = false;

        // 終止請求
        public final void shutdownRequest() {
            shutdownRequested = true;
            interrupt();
        }

        // 判斷終止請求是否已經送出
        public final boolean isShutdownRequested() {
            return shutdownRequested;
        }

        // 動作
        public final void run() {
            try {
                while (!shutdownRequested) {
                    doWork();
                }
            } catch (InterruptedException e) {
            } finally {
                doShutdown();
            }
        }

        // 作業
        protected void doWork() throws InterruptedException {
        }

        // 終止處理
        protected void doShutdown() {
        }
    }

以父類別的方法來組成處理的架構，將該方法呼叫出來的方法用子類別來實作，稱為 Template Method Pattern。

    :::java
    public class CountupThread extends GracefulThread {
        // 計數器的值
        private long counter = 0;

        // 作業
        protected void doWork() throws InterruptedException {
            counter++;
            System.out.println("doWork: counter = " + counter);
            Thread.sleep(500);
        }

        // 終止處理
        protected void doShutdown() {
            System.out.println("doShutdown: counter = " + counter);
        }
    }

####4. 現在寫一支 GUI 程式，按下之後會逐漸顯示 50 個句點。可以按 Cancel 鈕取消顯示。

繼承 GracefulThread 類別，建立 ServerThread 類別。從 Service 類別啟動 ServiceThread 類別。這就是 Thread-Per-Message Pattern。

連續按 Execute 按鈕時，採用 Balking Pattern 進行 balk。

<script src="https://gist.github.com/twmht/ac95da9ad1f9626b7162.js"></script>

####5. 改善回應性。以下是一隻河內塔程式，在 10 秒後送出終止請求，但是程式卻延遲了 7681 毫秒後才呼叫 doShutdown 方法。請改寫之，使其能夠縮短延遲的時間。

<script src="https://gist.github.com/twmht/8e817762af3ddb042e5d.js"></script>

在 dowork 方法裡面檢查 showdownRequested 這個 flag，如果有就馬上丟出 InterruptedException。

    :::java
    public class HanoiThread extends Thread {
        // 已經送出終止請求則為true
        private volatile boolean shutdownRequested = false;
        // 送出終止請求的時刻
        private volatile long requestedTimeMillis = 0;

        // 終止請求
        public void shutdownRequest() {
            requestedTimeMillis = System.currentTimeMillis();
            shutdownRequested = true;
            interrupt();
        }

        // 判斷終止請求是否已經送出
        public boolean isShutdownRequested() {
            return shutdownRequested;
        }

        // 動作
        public void run() {
            try {
                for (int level = 0; !shutdownRequested; level++) {
                    System.out.println("==== Level " + level + " ====");
                    doWork(level, 'A', 'B', 'C');
                    System.out.println("");
                }
            } catch (InterruptedException e) {
            } finally {
                doShutdown();
            }
        }

        // 作業
        private void doWork(int level, char posA, char posB, char posC) throws InterruptedException {
            if (level > 0) {
                if (shutdownRequested) {
                    throw new InterruptedException();
                }
                doWork(level - 1, posA, posC, posB);
                System.out.print(posA + "->" + posB + " ");
                doWork(level - 1, posC, posB, posA);
            }
        }

        // 終止處理
        private void doShutdown() {
            long time = System.currentTimeMillis() - requestedTimeMillis;
            System.out.println("doShutdown: Latency = " + time + " msec.");
        }
    }
