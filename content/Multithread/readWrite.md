Title: Read-Write Lock Pattern -- 大家想看就看吧，不過看的時候不能寫喔
Slug: readWrite
Category: Multithread
Author: twmht

Read-Write Lock Pattern 主要是分成讀跟寫的執行緒，當讀跟讀之間的執行緒不需要共用互斥時，而且讀的頻率很高的時候，使用這個 Pattern 效率會很好。這個 Pattern 的重點在於，他沒有 read-read conflict，但是其他三種組合會有 conflict，例如 read-write conflict，因此需要做共用互斥。

在範例程式碼中，preferWriter 欄位就是用來讓 ReaderThread 以及 WriterThread 可以輪流執行。
<script src="https://gist.github.com/twmht/a4b92735f01b4efdc3c3.js"></script>

###所有參與者
####Reader
Reader 會對 SharedResource 進行 read。例如 ReaderThread 類別。
####Writer
Writer 會對 SharedResource 進行 write。例如 WriterThread 類別。
####SharedResource
SharedResource 代表 Reader 與 Writer 所共享的資源。SharedResource 會提供不會改變內部狀態的動作 (read)，與會改變內部狀態的動作 (write)，例如 Data 類別。
####ReadWriteLock
ReadWriteLock 提供了對 SharedResource 進行 read 動作與 write 動作時所需要的鎖定。為了達成 read 動作，提供了 readLock 與 readUnlock，為了達成 write 動作，提供了 writeLock 與 writeUnlock。例如 ReadWriteLock 類別。

###重點
####鎖定的意義
使用 synchronized 可以取得實體的鎖定，java 中的每一個實體都有一個鎖定，同一個實體的鎖定無法由兩個以上的執行緒所取得，這是*物理*上的鎖定。
而 ReadWriteLock 裡面所定義的讀取的鎖定以及寫入的鎖定，是屬於邏輯上的鎖定，由程式設計師來實作。 但實際上實作時，也用到了一個物理性的鎖定，也就是 ReadWriteLock 實體的鎖定。
####Before/After Pattern
程式範例中的 Data 類別使用了 Before/After pattern，通常會像下面這樣寫：

    :::java
    before();
    try{
        execute();
    }finally{
        after();
    }

呼叫 execute 方法之前一定會呼叫 before 方法，並且能確保 after 方法也一定會被呼叫到。而 before 方法在 try 之外，就表示*如果在 before 的執行過程中發生例外，就不執行 execute 與 after。例如，從 before 中丟出 InterruptedException，就可以想成是 before 的中斷，如果 before 放在 try 裡面的話，即使中斷 before 的執行，也會呼叫 after。

###問題
####關於程式再利用性，有下列問題，請修改之。

1. Data 類別包含實際進行讀寫的動作。若要進行其他的讀寫動作，需要建立新的類別，進行與 Data 類別一樣的同步處理動作。
2. ReadWriteLock 類別包含了防衛條件。當想要更改防衛條件的原則時，還需要建立新的類別，進行與 Data 類別一樣的讀寫動作。
3. ReadWriteLock 類別的方法都是 public，有被 Data 以為的類別呼叫的危險。

為了解決 1 跟 2，可以使用 Strategy Pattern。關於讀寫處理的 policy 以 ReadWriteStrategy 表示，Guard 條件相關的 policy 則以 GuardStrategy 介面表現。之後，再建立 Data 類別的實體時，設定表示各自 policy 的 ConcreteStrategy，在執行時將處理交給對方處理。如果 policy 未被設定，則預設的 policy 如 DefaultReadWriteStrategy 類別及 DefaultGuardStrategy 類別會成為 Data 類別的 inner class。

為了解決 3，將 ReadWriteLock 類別當成 Data 類別的 inner class。

將 ReadWriteStrategy  介面與 GuardStrategy 介面與 Data 類別整合到 readwritelock package 中。

只要先走這一步，就可以切換讀寫處理與 Guard 條件的 policy。但是，這個方法也會有使得類別和介面增加，導致管理困難。
<script src="https://gist.github.com/twmht/7895d5c4fe69736d0bdf.js"></script>
