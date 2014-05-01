Title: Guarded Suspension Pattern -- 要等到我準備好喔
Slug: guarded-suspension
Category: Multithread
Author: twmht

當光靠synchronized已經沒有辦法保護shared resource的時候，通常表示存取shared resource的時候需要條件，這時候就要設計Guarded Suspension Pattern。

最常見的例子是client端以及server端的溝通，client端會不斷地送request給server，而server會不停地去收request，假設我們用queue去儲存request，那麼server就不能在queue為empty的時候去接收request，這個就是<font color=blue>存取的條件</font>---<font color = red>queue不能是empty</font>。

Request.java

    :::java
    public class Request {
        private final String name;
        public Request(String name) {
            this.name = name;
        }
        public String getName() {
            return name;
        }
        public String toString() {
            return "[ Request " + name + " ]";
        }
    }

RequestQueue.java，採用LinkedList來存放Request

    :::java
    import java.util.LinkedList;
    public class RequestQueue {
        private final LinkedList queue = new LinkedList();
        public synchronized Request getRequest() {
            while (queue.size() <= 0) {
                try {                                   
                    //當條件不滿足的時候，進入wait set
                    wait();
                    //當被喚醒的時候，只有拿到鎖定的server thread才能執行下一個敘述
                } catch (InterruptedException e) {      
                }                                       
            }                                           
            return (Request)queue.removeFirst();
        }
        public synchronized void putRequest(Request request) {
            queue.addLast(request);
            //當條件滿足的時候，喚醒所有的server thread
            notifyAll();
        }
    }

ClientThread.java，不斷呼叫putRequest，並且呼叫在RequestQueue中的wait set中server thread。

    :::java
    import java.util.Random;
    public class ClientThread extends Thread {
        private Random random;
        private RequestQueue requestQueue;
        public ClientThread(RequestQueue requestQueue, String name, long seed) {
            super(name);
            this.requestQueue = requestQueue;
            this.random = new Random(seed);
        }
        public void run() {
            for (int i = 0; i < 10000; i++) {
                Request request = new Request("No." + i);
                System.out.println(Thread.currentThread().getName() + " requests " + request);
                requestQueue.putRequest(request);
                try {
                    Thread.sleep(random.nextInt(1000));
                } catch (InterruptedException e) {
                }
            }
        }
    }

ServerThread.java，檢查queue是否empty，不是empty才能存取，不然就進去wait set中。

    :::java
    import java.util.Random;

    public class ServerThread extends Thread {
        private Random random;
        private RequestQueue requestQueue;
        public ServerThread(RequestQueue requestQueue, String name, long seed) {
            super(name);
            this.requestQueue = requestQueue;
            this.random = new Random(seed);
        }
        public void run() {
            for (int i = 0; i < 10000; i++) {
                Request request = requestQueue.getRequest();
                System.out.println(Thread.currentThread().getName() + " handles  " + request);
                try {
                    Thread.sleep(random.nextInt(1000));
                } catch (InterruptedException e) {
                }
            }
        }
    }

Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            RequestQueue requestQueue = new RequestQueue();
            new ClientThread(requestQueue, "Alice", 3141592L).start();
            new ServerThread(requestQueue, "Bobby", 6535897L).start();
        }
    }


###參與者
####GuardedObject 參與者
GuardedObject 參與者是一個擁有被防衛的方法 (guardedMethod) 的類別。當執行緒執行 guardMethod 時，只要滿足防衛條件，就會馬上執行。但防衛條件不成立的時候，就要開始等待。防衛條件的成立與否，會隨 GuardedObject 的狀態變化。

GuardedObject 除了 guardedMethod 以外，可能還會有用來更改實體狀態（特別是用來更改防衛條件） 的方法（stateChangingMethod）。

在 Java 中，是使用 while 敘述與 wait 方法  來實作 guardedMethod 的。 而使用 notify 或 notifyAll 方法來實作 stateChangingMethod。

在程式中，RequestQueue 類別就是 GuardedObject 參與者。setRequest 方法與 putRequest 方法則分別是 guardedMethod 與 stateChagingMethod。

###重點整理
####有條件的 synchronized
Guarded Suspension Pattern 是附加條件的 Single Threaded Execution Pattern。也就是<b>有條件的 synchronized</b>。
####多執行緒板的 if
一般來說，單一執行緒的程式，防衛條件會使用 if 敘述處理。從這個角度來看，Guarded Suspension Pattern 就像是<b>多執行緒版的 if</b>。
####忘記更改狀態與生命性
如果程式寫錯，忘記修改 GuardedObject 的狀態，那防衛條件無論經過多久都不會成立。這種時候，執行緒永遠都不會前進，程式就失去生命性。

所以我們可能會想將 wait 之後經過一段很長的時間還沒有被 notify 或 notifyAll 的現象，認定為一種錯誤，而想要中斷程式運作，想要在一定時間後中斷動作時，我們可以在呼叫 wait 方法時，在引數裡指定 timeout 的時間。
####再利用性
在程式中，會發現只有 RequestQueue 類別有用到 wait 及 notifyAll。之所以這樣做的原因是因為，使用 RequestQueue 類別的一方，並不需要考慮 wait 以及 notifyAll 的問題，只要呼叫 getRequest 方法與 putRequest 方法就行了。
####各式各樣的稱呼
Guarded Suspension Pattern 共通的特徵有下面三點：

1. 有迴圈的存在
2. 有條件的測試
3. 因為某種原因在<b>等待</b>

##### guarded wait
意義是被阻擋而等待。大致上是執行緒使用 wait 等待，等到被 notify 及 notifyAll 以後再次測試條件的實作方法。使用 wait 等待的時間，其實是停止在等待區裡停止執行，所以不會浪費到 JVM 的處理時間。

一般來說，在接收端(server)的設計會是這樣。

    :::java
    synchronized void receive(){
        while(!ready){
            //釋放鎖定，進到wait set中。
            wait()
        }
        //do something
    }

而在發送端(client)的設計會是這樣

    :::java
    synchronized void send(){
        //do something
        ready = True
        //wake up all receivers
        notifyAll()
    }

#####busy wait
執行緒不使用 wait 等待，而使用 yield （儘量把優先權交給其它執行緒），並且不斷測試條件。因為等待中的執行緒也持續運作，所以會浪費 JVM 的時間。
    :::java
    //Thread.yield()不會解除鎖定，所以不可以寫在 synchronized 裡面。
    //ready 必須宣告成 volatile。
    void receive(){
        while(!ready){
            Thread.yield();
        }
    }

而在發送端(client)的設計會是這樣

    :::java
    synchronized void send(){
        //do something
        ready = True
    }
#####spin lock
spin lock 有時意思與 guarded wait 相同，有時與 busy wait 相同。另外，有時候則是指一開始使用 busy wait，之後再切換成 guarded wait 的方式。另外，有些以硬體實作的同步機制，也稱為 spin lock。

#####polling
反覆檢查某個事件是否發生，當發生時，就進行對應處理的方式。

###問題
####1. 請在 RequestQueue 類別加上偵錯輸出，使我們可以一目瞭然程式是否有照我們的期待運作。
<script src="https://gist.github.com/twmht/77d734c9de468249de36.js"></script>
####2. 請嘗試不更改 Main 類別，而試著修改其它類別，讓程式在約十秒後能夠真的結束。
雖然 Main 類別呼叫 interrupt 方法，執行緒還是不停下來，是因為 sleep 方法與 wait 方法在呼叫時，沒有顧慮到 InterruptedException 的緣故。

修正 RequestQueue 類別，準備讓 getRequest 方法丟出 InterruptException。

此外，修正 ClientThread 類別與 ServerThread 類別，在 InterruptedException 被丟出後，就跳出 fot 敘述之外。

如果沒有修正 ReQuestQueue 類別的話，則假設 interrupt 方法被呼叫時執行緒正在 sleep，程式就可以正常結束。但是如果執行緒正在 wait，程式就不會結束，這是因為沒有顧慮到 InterruptException 的緣故。也就是說，這個程式每執行幾次就會有一次無法正常結束。

<script src="https://gist.github.com/twmht/3a3424dd062a37afaa7d.js"></script>
