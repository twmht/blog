Title: Guarded Suspension Pattern
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
