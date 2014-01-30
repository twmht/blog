Title: Command Pattern
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
