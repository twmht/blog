Title: Introduction to Multithread
Slug: Introduction
Category: Multithread
Author: twmht

講到多執行緒時，我們常常在講concurrent(並行)與parallel(平行)，在單核的情況下，只會出現concurrent，因為concurrent表示的是一段時間只會有一個執行緒在動作;但是在雙核以上的情況下，則會出現parallel的情形，表示同一段時間可能會有多個執行緒在動作。
##不管是concurrent或者是parallel，都要考慮到thread-safe的問題。##

一般來說，在java中可以透過兩種方式建立thread。

* 繼承Thread類別，建立PrintThread.java

        :::java
        public class PrintThread extends Thread {
            private String message;
            public PrintThread(String message) {
                this.message = message;
            }
            public void run() {
                for (int i = 0; i < 10000; i++) {
                    System.out.print(message);
                }
            }
        }
Main.java

        :::java
        public class Main {
            public static void main(String[] args) {
                new PrintThread("Good!").start();
                new PrintThread("Nice!").start();
            }
        }

* 實作Runnable界面,建立Printer.java

        :::java
        public class Printer implements Runnable {
            private String message;
            public Printer(String message) {
                this.message = message;
            }
            public void run() {
                for (int i = 0; i < 10000; i++) {
                    System.out.print(message);
                }
            }
        }
Main.java

        :::java
        public class Main {
            public static void main(String[] args) {
                new Thread(new Printer("Good!")).start();
                new Thread(new Printer("Nice!")).start();
            }
        }

###接下來要來介紹synchronized方法。###
建立Bank.java

    :::java
    public class Bank {
        private int money;
        private String name;
        public Bank(String name, int money) {
            this.name = name;
            this.money = money;
        }
        public synchronized void deposit(int m) {
            money += m;
        }
        public synchronized boolean withdraw(int m) {
            if (money >= m) {
                money -= m;
                check();
                return true;
            } else {
                return false;
            }
        }
        public String getName() {
            return name;
        }
        private void check() {
            if (money < 0) {
                System.out.println("可用餘額為負數 ! money = " + money);
            }
        }
    }

ClientThread.java

    :::java
    public class ClientThread extends Thread {
        private Bank bank;
        public ClientThread(Bank bank) {
            this.bank = bank;
        }
        public void run() {
            while (true) {
                boolean ok = bank.withdraw(1000);
                if (ok) {
                    bank.deposit(1000);
                }
            }
        }
    }

Main.java

    :::java
    public class Main {
        public static void main(String[] args) {
            Bank bank = new Bank("A Good Bank", 1000);
            new ClientThread(bank).start();
            new ClientThread(bank).start();
        }
    }

當一個執行緒在執行Bank實體的deposit方法時，表示它已經取得鎖定，其它執行緒就不能執行同一個實體的deposit方法或withdraw方法，必須排隊取得鎖定。
換句話說，一個實體只會有一個鎖定。而且，只有取得鎖定的執行緒才能夠執行synchronized方法。

如果不想要讓整個方法都被synchronized保護，則可以用部份保護的方式。

    :::java
    void method(){
        //something
        synchronized(variable){
            
        }
    }

假設現在有一個加上synchronized的方法

    :::java
    synchronized void method(){
        //something
    }

它等價於

    :::java
    void method(){
        synchronized(this){

        }
    }
相當於取得this的鎖定。

另一方面，synchronized類別方法又有不同

    :::java
    class something{
        static synchronized void method(){
            //something
        }
    }

其等價於

    :::java
    class something{
        start void method(){
            synchronized(something.class){
                //something
            }
        }
    }
注意到了嗎?取得的是something這個類別的鎖定。

###最後介紹wait set的觀念###
*每個實體都會有一個wait set*，wait set是一個在執行該實體的wait方法時，動作所停止的執行緒的集合。
一執行wait方法時，該執行緒便會暫時停止動作，進入wait set這個集合，除非發生下列其中一種情形，否則該thread會永遠被留在wait set裡。

* 有其他執行緒呼叫notify方法，可以從wait set中叫醒一個執行緒出來，不能保證是哪一個。
* 有其他執行緒呼叫notifyAll方法，叫醒所有正在wait set中的執行緒。
* 有其他執行去呼叫Interrupt方法
* wait方法已到期

要執行wait或notify方法，*執行緒必須先取得鎖定*，進入wait set後，才會釋放鎖定。

一般來說，會設計成這樣。

    :::java
    synchronized void method1(){
        //something
        wait(); //或是this.wait()
        //something
    }
    synchronized void method2(){
        //something
        notify(); //或是this.notify()
        //something
    }
被叫醒後的執行緒，要繼續排隊取得鎖定，之後會執行wait()後的敘述。
