Title:Single Threaded Execution Pattern
Slug: single-thread-execution
Category: Multithread
Author: twmht

##Single Threaded Execution Pattern
是指我們的方法限定一次只能由一個執行緒所執行。 


假設我們有一個*Gate*，一次只能夠限定一個人通過，現在我們有多個人（多個thread)要通過這個門，每次通過之後*Gate*會顯示通過的人的*name*以及*address*，同時*Gate*會用一個*counter*來紀錄目前有多少人通過。

Gate.java

    :::java
        public class Gate {
        private int counter = 0;
        private String name = "Nobody";
        private String address = "Nowhere";
        //加入synchronized限制一次只能由一個thread來執行這個pass
        public synchronized void pass(String name, String address) {
            this.counter++;
            this.name = name;
            this.address = address;
            check();
        }
        public synchronized String toString() {
            return "No." + counter + ": " + name + ", " + address;
        }
        private void check() {
            if (name.charAt(0) != address.charAt(0)) {
                //表示shared resource有同時讓不同的thread更改過，同時也代表這不是thread-safe
                System.out.println("***** BROKEN ***** " + toString());
            }
        }
    }

Main.java

    :::java
        public class Main {
        public static void main(String[] args) {
            System.out.println("Testing Gate, hit CTRL+C to exit.");
            Gate gate = new Gate();
            new UserThread(gate, "Alice", "Alaska").start();
            new UserThread(gate, "Bobby", "Brazil").start();
            new UserThread(gate, "Chris", "Canada").start();
        }
    }

UserThread.java

    :::java
        public class UserThread extends Thread {
        private final Gate gate;
        private final String myname;
        private final String myaddress;
        public UserThread(Gate gate, String myname, String myaddress) {
            this.gate = gate;
            this.myname = myname;
            this.myaddress = myaddress;
        }
        public void run() {
            System.out.println(myname + " BEGIN");
            while (true) {
                gate.pass(myname, myaddress);
            }
        }
    }

Single Thread Execution Pattern的概念較為簡單，我們把Gate當作SharedResource，在一般情況下，SharedResource會被多個執行緒所存取，SharedResource會有一些方法，這些方法又可以分為safeMethod以及unsafeMethod。

* safeMethod: 讓多個執行緒同時存取也不會有問題。
* unsafeMethod: 讓多個執行緒同時存取會有問題，因此可以考慮加上synchronized，讓unsafeMethod只能同時被一個執行緒所存取。我們又可以稱加上synchronized的方法為critical section。

至於為什麼check()這一個方法不需要加上synchronized，因為check()在pass()中被呼叫，而pass()又是synchronized的方法，因此可以保證同時只會有一個執行緒去執行check()。
