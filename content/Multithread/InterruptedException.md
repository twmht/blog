Title: InterruptedException
Tags: thread, java
Slug: InterruptedException
Category: Multithread
Author: twmht

呼叫 interrupt 方法後，可以中斷掉執行緒。有下面其中一種結果：

* 執行緒變成中斷狀態。
* 丟出 InterruptedException，只有在執行緒是 sleep、wait 或是 join 時才會發生，而且這個時候不會變成中斷狀態。

####從中斷狀態到丟出 InterruptedException 例外

**若執行緒是中斷狀態，就丟出 InterruptedException**，可以像下面這樣寫。

    :::java
    if(Thread.interrupted()){
        throw new InterruptedException();
    }

#####哪個執行緒來檢查 interrupted 方法
Thread.interrupted 方法會檢查 Thread.currentThread() 的中斷狀態。也就是說，上面的 if 敘述無論寫在哪個類別的哪個方法，都是檢查執行 if 敘述的執行緒的中斷狀態。
#####不想清楚中斷狀態的時候
呼叫 Thread.interrupted 方法後，執行緒就不再是中斷狀態了。也就是說，只要呼叫一次 Thread.interrupted 方法後，中斷狀態就會被清除。

如果不想清除中斷狀態，要使用 isInterrupted 方法:

    :::java
    if(Thread.currentThread().isInterrupted()){
        
    }
####丟出 InterruptedException 例外再轉換為中斷狀態
當我們這樣寫的時候，

    :::java
    try{
        Thread.sleep(1000);
    }catch(InterruptedException e){
        
    }

可由 Thread.sleep 丟出 InterruptedException。

不過，這樣寫的話，並不會變成中斷狀態。

如果想要變成中斷狀態，就必須這樣寫。

    :::java
    try{
        Thread.sleep(1000);
    }catch(InterruptedException e){
        Thread.currentThread().interrupt();
        
    }
####延後拋出 InterruptedException

收到的 InterruptedException，可以晚點再拋。

    :::java
    InterruptedException savedException = null;
    try{
        Thread.sleep(1000);
    }catch{InterruptedException e){
        savedException = e;
    }
    //do something
    if(savedException != null){
        throw savedException;
    }

