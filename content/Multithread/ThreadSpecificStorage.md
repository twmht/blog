Title: Thread-Specific Storage  -- 每個執行緒的保管箱
Tags: thread,java
Slug: ThreadSpecificStorage
Category: Multithread
Author: twmht

Thread-Specific Storage Pattern 是只有一個路口，但內部會對每個執行緒提供特有儲存空間的 Pattern。

通常會用 <code>java.lang.ThreadLocal</code> 來管理每個執行緒的特有儲存空間。

###程式範例(沒有使用 <code>java.lang.ThreadLocal</code>)：
以下是只有一個執行緒的情況。在檔案留下 Log 紀錄。
<script src="https://gist.github.com/twmht/1f281eefc25c87ac41b6.js"></script>
###程式範例(有使用 <code>java.lang.ThreadLocal</code>)：
以下是多執行緒的情況。每個執行緒會各自保留一份 Log 紀錄。
程式能夠自動區分執行緒，將字串寫入正確的 Log 中。
<script src="https://gist.github.com/twmht/43b8f32370766e40ad86.js"></script>

###所有參與者
####Client
Client 會將工作委託給 TSObjectProxy。一個 TSObjectProxy 可由多個 Client 一起使用。例如 ClientThread 類別。 
####TSObjectProxy
TSObjectProxy 會處理多個 Client 委託的工作。
首先，TSObjectProxy 會使用 TSObjectCollection，取得 Client 所對應的 TSObject。並將工作委託給TSObject。例如 Log 類別。
####TSObjectCollection
TSObjectCollection 擁有 Client 與 TSObject 的對照表。當 getTSObject 被呼叫時，就檢查對照表，傳回 Client 參與者所對應的 TSObject。而 setTSObject 被呼叫時，則在對照表裡設定 Client 與 TSObject 的組合。
####TSObject
TSObject 存放有執行緒特有的資訊。TSObject 由 TSObjectCollection 所管理。TSObject 的方法只會由單一執行緒呼叫。例如 TSLog 類別。

###重點
####使用時機點
手邊有一個假定單一執行緒作為執行環境的物件。現在我們想將這個物件放在多執行緒環境下執行。這時，我們又不想修改使用端的執行緒，也不能改變物件的介面。

但是，要對執行緒進行共用互斥，以支援多執行緒，是很困難的。一不小心就可能使物件喪失安全性，或是發生死結使執行緒喪失生命性。

這時就使用 Thread-Specific Storage Pattern。在此將目的物件作為 TSObject，並建立與 TSObject 具有相同介面的 TSObjectProxy。另外，為了管理 **Client->TSObject **的對照表，又加上了 TSObjectCollection。TSObjectProxy 會使用 TSObjectCollection，取得現在的執行緒所對應的 TSObject。而將這個工作委託給 TSObject。

像這樣，不需要修改使用端的執行緒，也不需要修改物件的介面。而且，TSObject 一定會由特定的執行緒呼叫，這個部份也不需要互斥控制。關於多執行緒的部份，則隱藏在 TSObjectCollection。
####Actor-based 與 Task-based
設計使用到執行緒的程式時，會因為重點放在主體與客體不同，出現兩種開發方式：

* Actor-based 著重於主體
* Task-based 著重於客體

一般來說，會同時出現兩種開發方式，會是 **task 在一群 actor 之間傳遞** 的狀況。
#####Actor-based
Actor-based 著重在**執行緒**。

Actor-based 的開發方式中，代表執行緒的實體，會擁有進行工作所需要的資訊(狀態)。這麼一來，可降低執行緒之間需要傳遞的資訊。每個執行緒會使用其他執行緒所傳來的資訊進行處理，改變自己的內部狀態。這種執行緒通常稱為 actor。

    :::java
    class Actor extends Thread{
        //actor 的內部狀態
        public void run(){
            
        }
    }
#####Task-based
Task-based 著重在**偏重於工作**的開發方式。

就是不將資訊(狀態)，放到執行緒裡面。而是把資訊放在執行緒之間傳遞的實體裡。並不是只有資料，包括用來執行工作的方法，也放在這個實體裡面。這種實體又可以稱為 **task**，它包含了足夠的資訊，所以 task 可以由任何執行緒來進行。這種開發方式，可以使巨大的工作能在輕巧的執行緒之間往來。

最典型的應用就是 Worker Thread Pattern。

    :::java
    class Task implements Runnable{
        //執行工作所需的資訊
        public void run(){
            //執行工作所需的處理內容
        }
    }

<code>java.util.TimerTask</code> 就是一個 task-based 的類別。這個類別實作了 <code>java.lang.Runnable</code> 介面，可由 <code>java.util.Timer</code> 類別呼叫。<code>java.util.TimerTask</code> 中可以記載在一定時間後要做的事，或是定期要執行的動作。

###問題
####執行緒的終止處理。在 ClientThread 類別裡，請修改成可以不需要明確地執行<code>Log.close();</code>。執行緒在結束時，就會自己關閉掉 log 檔。
<script src="https://gist.github.com/twmht/ec997f42d19e45fa28ea.js"></script>
