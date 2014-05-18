Title: Thread-Per-Message Pattern -- 這個工作交給你了
Slug: ThreadPerMessage
Category: Multithread
Author: twmht

對每個命令或請求，配置一個執行緒，由這個執行緒執行工作，這就是 Thread-Per-Message Pattern。

在範例程式中，Main 類別會委託 Host 類別顯示文字。Host 類別會啟動一個執行緒，來處理這項委託的工作。啟動的執行緒，會使用 Helper 類別實際進行顯示動作。 無論 Helper 類別的 handle 方法多花時間，Main 類別的 request 方法都不會等待 handle 方法執行完畢，而會馬上離開。

<script src="https://gist.github.com/twmht/2eea75686a221a8d57b8.js"></script>

###參與者
####Client
Client 對 Host 送出請求。Client 並不知道 Host 會如何實現這個請求。例如 Main 類別。
####Host
當 Host 收到 Client 的請求，會建立新的執行緒並啟動它。這個新的執行緒，會使用 Helper，處理這個請求。例如 Host 類別。
####Helper
Helper 會對 Host 提供處理請求的功能。Host 所建立的執行緒，會使用 Helper。例如 Helper 類別。

###重點
####提升回應性，降低延遲時間
當 handle 的動作很花時間時，或是 handle 的動作需要等待 I/O 時，效果會很好。為了降低啟動執行緒所需要的時間，可以使用 Worker Pattern。
####適合在動作順序無所謂時使用
handle 方法執行的順序，並不一定是呼叫 request 方法的順序，所以當動作順序有意義時，不適合使用這個 Pattern。
####不需要傳回值的時候
request 方法不會等待 handle 方法執行結束。也就是說，request 方法拿不到 handle 方法的傳回值。所以，這個 Pattern 只能在不需要傳回值的情況下使用，例如，通知事件的發生等等。

需要得知處理結果時，可使用 Future Pattern。
####應用在伺服器的製作
為了使伺服器可以處理多數的請求，可以使用這個 Pattern。客戶端送達的請求，由主執行緒來接收。而實際處理該請求，則交給其它執行緒來處理，伺服器則回到原本的狀態繼續等待其他客戶端的請求。

###問題
####1.改寫範例程式的 Host 類別，改寫成沒使用 inner class 的版本。

第一個版本，將 HelperThread 類別宣告為 Top Level 類別。
<script src="https://gist.github.com/twmht/cd3aa6a546f0a305f422.js"></script>
第二個版本，將 HelperThread 類別宣告為非匿名的 inner class。Helper 以及 HelperThread 的兩個類別可以表現出與 Host 類別的確關係密切。
<script src="https://gist.github.com/twmht/a450190fae7992b6c127.js"></script>

####2.以下程式中，Swing 的 framework 會去呼叫 actionPerformed 方法，在 actionPerformed 方法裡面，會呼叫 Service 類別的 service 方法。
然後，因為 service 方法很花時間，這麼一來要從 actionPerformed 方法離開，要花上一段時間。請改寫 Service 類別，提高這個類別的回應性。
<script src="https://gist.github.com/twmht/6882c7254792e288b586.js"></script>

這裡提出4個解答，這4個解答的不同之處在於使用者連續按下按鍵時的處理方式。

第一個版本，使用 Thread-Per-Message  Pattern，這個解答在使用者連續按下按鍵時，會同時執行好幾個執行緒 doService。

    :::java
    public class Service {
        public static void service() {
            new Thread() {
                public void run() {
                    doService();
                }
            }.start();
        }
        private static void doService() {
            System.out.print("service");
            for (int i = 0; i < 50; i++) {
                System.out.print(".");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                }
            }
            System.out.println("done.");
        }
    }
第二個版本，使用 Thread-Per-Message Pattern 以及 Single Threaded Execution Pattern，這個解答在使用者連續按下按鍵時，同時執行 doService 方法的執行緒只會有一個。

    :::java
    public class Service {
        public static void service() {
            new Thread() {
                public void run() {
                    doService();
                }
            }.start();
        }
        private static synchronized void doService() {
            System.out.print("service");
            for (int i = 0; i < 50; i++) {
                System.out.print(".");
                try {
                    Thread.sleep(100);
                } catch (InterruptedException e) {
                }
            }
            System.out.println("done.");
        }
    }

第三個版本，使用 Thread-Per-Message Pattern 以及 Balking Pattern。
在使用者連續按按鍵多次時，保證執行 doService 方法的只有第一個執行緒。在此，使用 Balking Pattern，將同時想要執行 doService 的執行緒給 balk 起來。

    :::java
    public class Service {
        private static volatile boolean working = false;
        public static synchronized void service() {
            System.out.print("service");
            if (working) {
                System.out.println(" is balked.");
                return;
            }
            working = true;
            new Thread() {
                public void run() {
                    doService();
                }
            }.start();
        }
        private static void doService() {
            try {
                for (int i = 0; i < 50; i++) {
                    System.out.print(".");
                    try {
                        Thread.sleep(100);
                    } catch (InterruptedException e) {
                    }
                }
                System.out.println("done.");
            } finally {
                working = false;
            }
        }
    }

第四個版本，連續按按鍵多次時就將執行中的處理予以取消。使用者連續按下按鍵多次時，會取消 doService 方法。

    :::java
    public class Service {
        private static Thread worker = null;
        public static synchronized void service() {
            // 如果處理在執行中，可用interrupt取消 
            if (worker != null && worker.isAlive()) {
                worker.interrupt();
                try {
                    worker.join();
                } catch (InterruptedException e) {
                }
                worker = null;
            }
            System.out.print("service");
            worker = new Thread() {
                public void run() {
                    doService();
                }
            };
            worker.start();
        }
        private static void doService() {
            try {
                for (int i = 0; i < 50; i++) {
                    System.out.print(".");
                    Thread.sleep(100);
                }
                System.out.println("done.");
            } catch (InterruptedException e) {
                System.out.println("cancelled.");
            }
        }
    }

####3. 以下是一個 Web 伺服器，每隔1秒倒數1，直到0為止。這個伺服器都是單一執行緒在運作，所以同時只能應付一個瀏覽器請求，在十秒之間，所有其他瀏覽器的請求只能等待。
請使用Thread-Per-Message Pattern，將他修改成可以同時應付所有瀏覽器的伺服器。
<script src="https://gist.github.com/twmht/efe608d3db233e04035f.js"></script>

只要修改 MiniServer 類別即可。

    :::java
    import java.net.Socket;
    import java.net.ServerSocket;
    import java.io.IOException;

    public class MiniServer {
        private final int portnumber;
        public MiniServer(int portnumber) {
            this.portnumber = portnumber;
        }
        public void execute() throws IOException {
            ServerSocket serverSocket = new ServerSocket(portnumber);
            System.out.println("Listening on " + serverSocket);
            try {
                while (true) {
                    System.out.println("Accepting...");
                    final Socket clientSocket = serverSocket.accept();
                    System.out.println("Connected to " + clientSocket);
                    new Thread() {
                        public void run() {
                            try {
                                Service.service(clientSocket);
                            } catch (IOException e) {
                                e.printStackTrace();
                            }
                        }
                    }.start();
                }
            } catch (IOException e) {
                e.printStackTrace();
            } finally {
                serverSocket.close();
            }
        }
    }

####4. 針對以下程式，嘗試寫出 magic 方法。

    :::java
    public class Main {
        public static void main(String args[]) {
            System.out.println("BEGIN");
            Object obj = new Object();
            Blackhole.enter(obj);
            System.out.println("END");
        }
    }

不會印出 Step 3。

    :::java
    public class Blackhole {
        public static void enter(Object obj) {
            System.out.println("Step 1");
            magic(obj);
            System.out.println("Step 2");
            synchronized (obj) {
                System.out.println("Step 3 (never reached here)");  //不會執行這裡
            }
        }

            （magic方法請您來完成） 

    }

1. 因為顯示了 Step 2，所以 magic 方法不會丟出例外。
2. Step 3 或 End 不會被顯示出來，因此執行緒不會從 enter 方法回來。
3. Step 3 沒有被顯示出來是因為執行緒沒有取得 obj 的鎖定就被阻擋起來。

因此，magic 方法的工作中，就是取得引數 obj。
但是，若想要取得鎖定，單純使用 synchronized 也是不行的。在從 magic 方法回來的時候，就從 synchronized 跳出，是因為鎖定被解開的緣故。我們可以知道，在這樣的情況下，只要進行如下處理。

1.magic 方法中，啟動新的執行緒，讓這個執行緒取得 obj 的鎖定。
2.新的執行緒永遠保持取得 obj 的鎖定的狀態。
3.新的執行緒啟動，取得 obj 的鎖定為止，原來的執行緒不能從 magic 方法中回來。(可以使用 Guarded Suspension Pattern)


第一個版本，使用 notifyAll。
<script src="https://gist.github.com/twmht/744d970cfddea5b7dd05.js"></script>

第二個版本，使用 notify。
<script src="https://gist.github.com/twmht/29c0791baff4cdb2985b.js"></script>
