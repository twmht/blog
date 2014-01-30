Title: Memento Pattern
Slug: memento
Category: Design Pattern
Author: twmht

###用的時間點
在文書軟體的操作環境下，即使不小心誤刪除了某些文字內容，只要利用 undo 功能就能救回被刪除前的內容。有些文書軟體甚至支援一次以上的還原動作。
物件導向程式如果要執行復原，必須預先儲存物件個體的狀態。但是又不能只做儲存的動作，否則無法以儲存的情報將物件的個體復原的原始的狀態。
必須要能自由存取物件個體內部的情報，才能還原物件個體。不過如果對存取動作毫不設限，又會讓高度依賴類別內部結構的程式碼分散到程式各處，增加修改類別時的困擾。這稱為封裝式破壞。

###如何設計
加入表示物件個體狀態的功能，而能在執行儲存以及復原時不發生封裝性破壞。它會讓某個時間點的物件個體狀態紀錄儲存起來，等到以後再讓物件個體復原到當時的狀態。例如:

1. undo (復原)
2. redo (重複)
3. history (產生操作紀錄)
4. snapshot (儲存目前狀態)

###程式範例
模擬一個收集水果的骰子遊戲，遊戲規則很簡單:

* 遊戲會自動進行
* 遊戲的主人翁丟骰子，根據骰子的結果
* 出現好的點數，則金錢增加。
* 出現不好的點數，則金錢減少。
* 出現很好的點數，可額外得到一個水果。
* 玩到沒錢時，遊戲結束。


為了後面能不受影響繼續進行，程式中儲存金錢的位置有建立一個 Memento 類別的物件個體，用來儲存 "目前的狀態"。裡面儲存的是現階段有的金錢和水果。利用預先儲存起來的 Memento 物件個體可以回復到原先的狀態，避免如果一直輸到沒有錢的時候會結束程式。

<script src="https://gist.github.com/twmht/3bb699572e0c4e9333d3.js"></script>

####Originator (產生者) 參與者
Originator 參與者是在想儲存本身目前狀態時產生一個 Memento 參與者。當 Originator 參與者又接收到以前的 Memento 參與者時，變進行恢復到產生 Memento 參與者時狀態的處理。例如 Gamer 類別。
#### Memento (紀念品) 參與者
Memento 參與者是整合 Originator 參與者的內部資訊。Memento 參與者雖然有 Originator 參與者的內部資訊，但並不會隨便把資訊公開出去。
共有以下兩種介面:
* wide interface: Memento 參與者所提供的 "wide interface" 是一個可取得物件狀態恢復原狀時之必要資訊的所有方法的集合。wide interface 會洩漏 Memento 參與者的內部狀態，所以只有 Originator 參與者能使用它。
* narrow interface: Memento 參與者所提供的 "narrow interface" 是給外部 Carataker 參與者看的。narrow interface 能力有限，可預防內部狀態公開給外部的危險。

視情況使用這兩種不同介面可以避免物件封裝化遭破壞。
扮演的角色例如 Memento 類別。

#### Carataker (照料的人) 參與者
如想儲存目前 Originator 參與者的狀態時，Carataker 參與者會把這個情形告訴 Originator 參與者。Originator 參與者接收這個訊息後就產生 Memento 參與者，然後傳遞給 Carataker 參與者。Carataker 為了將來可能會需要使用，因此要預先儲存這個 Memento。例如 Main 類別就是一個Carataker。
但是 Carataker 只能使用 Memento 的 narrow interface，所以不能存取 Memento 的內部資訊。 它只會把別人產生出來的 Memento 照單全收儲存起來，當作是一塊未知區域。
Originator 和 Memento 的結合相當緊密，但 Carataker 跟 Memento 的結合較為鬆散。Memento 會對 Carataker 隱藏資訊。
