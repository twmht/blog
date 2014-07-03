Title: Future  -- 先給您這張提貨卷
Tags: thread,java
Slug: future
Category: Multithread
Author: twmht

假設有一個執行起來需要花一些時間的方法，我們就不要等待執行結果出來了，而取得一張替代的提貨卷。因為取得提貨卷不需要花時間，這時這個提貨卷就是 Future 參與者。

取得 Future 的執行緒，會在事後再去取得執行結果。如果已經有結果了，就可以馬上到資料。如果執行結果還沒好，則繼續等到執行結果出現為止。

與 Thread-Per-Message Pattern 比較的話，送出請求的方法是有回傳值的，而回傳值剛好就是 Future 參與者。

程式範例：
<script src="https://gist.github.com/twmht/7cb126892ed724326e9c.js"></script>

###所有參與者
####Client
Client 會向 Host 發出 Request。Client 會馬上得到 VirtualData (Future)，作為這個 Request 的結果。例如 Main 類別。
####Host
Host 會建立新的執行緒，開始建立 RealData。另外，會對 Client 回傳 Future。例如 Host 類別。新的執行緒建立出 RealData，會對 Future 設定 RealData。
####VirtualData
VirtualData 是用來讓 Future 以及 RealData 可視為一種東西的參與者。例如 Data 介面。
####RealData
RealData 用來表示實際的資料，建立這個物件需要花一些時間。例如 RealData 類別。

####Future
Future 是 Host 傳給 Client，當作是 RealData 的提貨卷的參與者。

Future 相對於 Client 而言，可以進行 VirtualData 的行為。實際上 Client 對 Future 進行操作時，若 RealData 還沒建立好，執行緒會以 wait 等待。如果 RealData 已經建立好了的話，就不會等待了。Future 會將操作委託給 Client。

###重點
####Future 的變形
有些時候我們會希望重複設定 Future 的回傳值。

例如，假設現在要從網路取得圖片，一開始要取得圖片的長跟寬，接下來取得概略的模糊圖片，最後再取得清晰的圖片。這種時候就適合使用會變化的 Future。

####再利用性
RealData 並沒有考慮到多執行緒，與多執行緒有關的部份，都是在 Host 與 FutureData 中解決，對 RealData 沒有影響。因為這一點，可以將現有的類別套用 Future Pattern。

####Callback
處理完畢後，由 Host 所啟動的執行緒去呼叫 Client 的方法。不過這樣做的話，Client 也必須考慮到多執行緒了。

####非同步執行
Future Pattern 可以模擬出非同步執行的結果。首先建立出一個與處理結果具有相同介面的 Future。接著，在開始處理時，先把 Future 當作傳回值回傳。直到其他執行緒處理完以後，才將真正的結果設定給 Future。Client 可透過 Future 得到處理的結果。

而 getContent 方法也可能設計成非同步的。但不是在 getContent 方法裡面建立出新的執行緒。而是使用 Balking Pattern，如果還沒好，就馬上離開。既然 RealData 的實體還沒做好，就先回去，稍微做一些自己的工作之後，再呼叫一次 getContent 的方法試試看。

使用這個 Pattern，可使回應性不降低，並能即使得到想要的處理結果。

###問題
####1. 套用 Future Pattern。以下是一支指定 URL 以從網路上取得文件的程式。請將這支程式改成使用多執行緒的版本。首先，建立出可以取得 Yahoo! 網頁的 Retriever 類別。<code>Content content = Retriever.retriever("http://www.yahoo.com/");</code>。接下來，可以透過 <code>byte[] bytes = content.getBytes();</code> 取得 content。現在的 Retriever 類別使用 SyncContentImpl 類別以單執行緒取得文件。請修改成多執行緒的版本。具體來說，就是建立出 AsyncContentImpl 類別，將 Retriever 類別改寫成可以使用 AsyncContentImpl 類別的版本。其它類別則保持不動。

<script src="https://gist.github.com/twmht/f0feba9797631af9a1ba.js"></script>

首先，修改 Retriever 類別，使其傳回 AsyncContentImpl 類別的實體。之後，建立 AsyncContentImpl 類別，AsyncContentImpl 是 Future 參與者，SyncContentImpl 類別則是 RealData 參與者。

<script src="https://gist.github.com/twmht/6b1507d8e01ac719bfbd.js"></script>

####2. 在 Future Pattern 處理例外。以下程式，會由啟動的新的執行緒拋出 NegativeArraySizeException。無論我們怎麼在 request 方法與 getContent 方法裡面 try catch，都無法捕捉到這個例外。程式會卡住不動，因為 main 執行緒在 getContent 時 wait 住了。

Main 類別。

    :::java
    public class Main {
        public static void main(String[] args) {
            try {
                System.out.println("main BEGIN");
                Host host = new Host();

                Data data = host.request(-1, 'N');

                System.out.println("data = " + data.getContent());

                System.out.println("main END");
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }

修改的具體的步驟如下：

* 修改 Host 類別，讓 RealData 的實體在製作時如果發生例外，會將該例外設定到 FutureData 類別。
* 將設定例外的方法 setException 新增到 FutureData 類別中。
* 為了將發生的例外包起來，使用例外<code>java.lang.reflect.InvocationTarget Exception</code>。
* 還要讓 getContent 方法丟出 InvocationTargetException。

換句話說，要讓例外延遲發生，直到要從 Future 獲得必要的值。

<script src="https://gist.github.com/twmht/bcc56ac7a9ddea702d7f.js"></script>
