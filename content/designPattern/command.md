Title: Command Pattern -- 將命令寫成類別
Slug: command
Category: Design Pattern
Author: twmht

###用的時間點
當類別在執行作業時，會呼叫自己類別或其他類別的方法，呼叫方法之後的結果會反應在物件狀態上，但卻不會留下任何作業紀錄。

遇到這種情形的時候，要是有一個類別能表現"請執行這項作業"的"命令"時就方便多了。因為如此一來便可以用一個"表示命令的類別物件個體"來代表要執行的作業，而不需要採用"呼叫方法"之類的動態處理。如想管理相關紀錄時，只需要管理該物件個體的集合即可。而若預先將命令的集合儲存起來，還可以再執行同一個命令;或者是把多個命令結合成一個新命令供再利用。

###如何設計
這樣的Pattern叫作Command Pattern，有時也稱為"Event"，跟"Event driven"中的Event是同一個意思。一旦發生事件(例如按下滑鼠左鍵，或按下右鍵)，則先將該事件變成物件個體，按照發生順序排入queue中。接著，再依序處理所有排列等候的事件。

###程式範例
設計一個簡單的繪圖軟體，移動滑鼠的時候，便會自動產生一個個紅點，按下clear即可清除。
當使用者移動滑鼠的時候，就會產生"在這裡畫一個點"的command。把這個物件個體儲存起來，需要用的時候就可以繼續畫紅點。

<script src="https://gist.github.com/twmht/613b2636b333ca809e86.js"></script>

####Command 參與者
定義command的API。例如Command Interface。
#### ConcreteCommand 參與者
實際上實作Command參與者的API，例如MacroCommand以及DrawCommand等類別。
#### Receiver 參與者
Command 參與者執行命令時的動作對象，也可以稱為受命者。例如接受DrawCommand命令的是DrawCanvas類別。
#### Client 參與者
在產生ConcreteCommand參與者時，分配Receiver的參與者。例如Main類別，它是配合滑鼠移動而產生 DrawCommand 的物件個體，不過同時也傳遞 DrawCommand 的物件個體給建構子，作為Receiver 參與者。
#### Invoker 參與者
開始執行命令的參與者，呼叫Command所定義的API。例如Main和DrawCanvas等類別都是呼叫 Command Interface 的 execute 方法。

####命令應該要有的資訊是什麼
命令應該要有哪些資訊會因為目的而有所不同。前面的 DrawCommand 類別只有畫點位置的資訊，而沒有點的大小或色彩等資訊。

假設 DrawCommand 有一個該事件發生的時間點，如此一來，在畫的時候，可以重現出使用者滑鼠移動的快慢情形。

DrawCommand 類別還有一個表示繪製對象的欄位 (drawable)。在程式中的 DrawCanvas 的物件個體只有一個，所有繪製當然都是針對它，所以這個 drawable 欄位反而沒有太大意義。
但是如果有多個繪製對象 (也就是 Receiver)，這個欄位就很有用。因為 ConcreteCommand 本身<b>知道</b> Receiver，所以不管是誰在管理或是擁有 ConcreteCommand，都可以做 execute 的動作。

####儲存紀錄
程式用 MacroCommand 的物件個體 (history) 來表示繪製的紀錄，因為這個物件個體擁有目前為止的所有繪製相關資訊。這意思是說，只要確實將這個物件個體儲存成檔案，就能儲存繪製記錄。

####轉換器
Main 類別共實作3個介面，但實際使用到的介面的方法卻只是其中一小部份。舉例來說，MouseMotionListener 中，也只有用到 mouseDragged 方法。而 WindowListener 也只有用到 windowClosing 方法。

為了簡化整個程式，在 java.awt.event 裡面有一個轉換器。例如，對應 MouseMotionListener 介面的是 MouseMotionAdapter 類別; 對應 WindowListener 介面的是 WindowAdapter 類別。

以 MouseMotionAdapter 類別來講的話，這個類別會實作 MouseMotionListener 介面，所有該介面要求的方法都會實作到，不過，這個實作都是空的，所以只要產生 MouseMotionAdapter 類別的子類別並且實作必要的方法就能達到目的。

可以利用 inner class 的結構來使用轉換器。

###問題
####1. 新增一個設定色彩的功能。另外建立一個 ColorCommand 類別，來表示設定色彩的命令。

1. 在 drawer package 中新增一個表示設定色彩的命令的 ColorCommand 類別。
2. 在 Drawable 介面新增一個更改色彩的方法 setColor。
3. 新增後並實作 DrawCanvas 類別。
4. 在 Main 類別新增可更改色彩的變色按鍵。

<script src="https://gist.github.com/twmht/eb33fe5e8beac2fdd351.js"></script>

####2. 新增一個刪除最後畫的點的復原功能。

1. 新增復原鍵
2. 按下復原鍵時，則呼叫 history.undo 重畫。

command package 及 drawer package 都不需要改。
<script src="https://gist.github.com/twmht/685e4c86859b4fabb7c7.js"></script>

####3. 修改 Main 類別，利用 MouseMotionAdapter 以及 WindowAdapter 來取代 MouseMotionListener 介面和 WindowListener 介面。
<script src="https://gist.github.com/twmht/0b585df6c2e35c68e58d.js"></script>
