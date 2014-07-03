Title: Swing 的 Event-Dispatching Thread
Slug: eventDispatchingThread
Category: Multithread
Author: twmht

####Event-Dispatching Thread
當按下按鈕時，會產生 <code>java.awt.event.ActionEvent</code> 這個類別的實體，移動滑鼠的時候，會產生 <code>java.awt.event.MouseEvent</code> 的類別實體。這些實體放在 Swing 的 event queue 中。

如果提到 Worker Thread 的話，那麼產生的 event 可以對應到 Request，event queue 就是 Channel，而 Client 就是對應到管理滑鼠及鍵盤等事件來源的部份。event-dispatching thread 就是 worker。

event-dispatching thread 會從 event queue 中取出一個 event，並執行這個 event。執行結束後，再回來 event queue 取出下一個 event。如果 event queue 中沒有任何 event， 則 event-dispatching thread 就會停下來等待新的 event。整個過程就是一個 Worker Thread Pattern。

而 event-dispatching thread 只有一條，因此可以省略共用互斥的問題，速度快很多。

####Event-dispatching Thread 會呼叫 Listener

event-dispatching thread 會去執行事件，接下來要具體思考的是要怎麼執行。

event-dispatching thread 進行的動作之一，是呼叫各種 Listener 的方法。

例如，按下按鈕的時候，<code>java.awt.event.ActionEvent</code> 的實體會被放進 event queue 中，當 event-dispatching thread 取得這個實體，會去呼叫用來處理 ActionEvent 實體的物件(Listener) 的 actionPerformed 方法。Event-dispatching thread 其實不知道這個方法會做什麼事情，它只是單純去呼叫這個方法而已。

#####登錄 Listener 的意義

例如，當要登錄 Listener 的時候，會呼叫 addActionListener 或 addMouseListener。對元件登錄 Listener，其實就是對元件設定當 event 發生時，event-dispatching thread 所要呼叫的方法所在的實體。

#### Event-dispatching thread 也處理畫面的重繪

event-dispatching thread 除了呼叫 Listener 的方法以外，還會呼叫重繪的方法。

當我們想要重繪畫面的時候，會去呼叫 repaint 方法，但呼叫 repaint 方法，其實並不會馬上開始重畫。repaint 方法只會在內部紀錄要重畫的區域，實際上，重畫的動作還是由 event-dispatching thread 另外處理的。

####Java.swing.SwingUtilities 類別
#####invokeAndWait 方法
這個方法會執行參數中傳入的 Runnable 物件。不過，執行這個物件的，是 event-dispatching thread。也就是說，使用 invokeAndWait 方法，可以將任意動作塞進 Swing 的 event queue。

invokeAndWait 是啟動並等待的意思。如同其名，這個方法會等待參數中傳入的 Runnable 物件執行完畢。也就是說，要等到呼叫 invokeAndWait 方法的時間點，event queue 中已經存放的所有事件都執行完，並且參數傳入的 Runnable 物件的 run 方法也執行完畢以後，才會從 invokeAndWait 方法離開。

如果我們建立額外的執行緒去呼叫元件的方法，其實是危險的。如果無論如何都想要呼叫元件的方法的話，就該將要執行的動作的內容建立成 Runnable 物件，使用 invokeAndWait 方法(或是 invokeLater 方法)交給 event-dispatching thread 來呼叫。

#####invokeLater 方法
invokeLater 方法類似 invokeAndWait 方法，不過它不會等待 Runnable 物件執行完，而是塞入 event queue 後就馬上離開。

#####isEventDispatchThread 方法
使用這個方法可以檢查目前的執行緒是不是 event-dispatching thread。

####The single-thread rule
當 Swing 元件一旦被實現，可能改變元件狀態的程式碼或只是相依於狀態的程式碼，都必須交由 event-dispatching thread 執行。所謂元件被 realized (實現)，是指元件處在已經可以呼叫 paint 的狀態。具體來說，就是這個元件的 <code>setVisible(true)</code> 方法、<code>show()</code> 方法或者是 <code>pack()</code> 方法已經被呼叫，或是這個元件是已經被實現的子元件。

簡單來說，當元件還在準備時，由其他的執行緒呼叫也沒有關係，可是，一旦顯示出來以後(設定為可顯示以後)，元件的方法就只能從 event-dispatching thread 執行。


