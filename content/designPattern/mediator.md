Title: Mediator Pattern -- 只要面對一個顧問
Slug: mediator
Category: Design Pattern
Author: twmht

###用的時間點
一個小組裡10個同樣立場的成員共同進行作業，但卻各自為政。每個成員都對別人發出指令，讓整個作業亂成一團。而且還有干擾其他成員的作業方式、不斷發生指令相左的情形。這時候如果有一個立場超然的 **顧問** 站出來說： **請各位成員把所有狀況回報給我這個顧問，我會整體做出考量後發給各位適當的指示。但是我不會插手管各位手上工作的細節**。所有成員同意顧問的提議，於是達成共識。
###如何設計
**每個成員都只對顧問提出報告，也只有顧問會發出指令給各個成員**。成員彼此之間也不會去探問目前狀況如何，或亂發指令給其他成員。mediator 就是一個顧問，如果有困難就告訴顧問、發生什麼會影響到整個小組的事情也要告訴顧問。對於顧問提出的要求事項要確實執行。所有小組成員都不可以擅自跟其他成員溝通意見做判斷，必須透過顧問才能進行到下一個動作。而顧問則根據小組成員所提出的報告做整體性判斷，對各個成員發出指令。

###程式範例
設計一個要求輸入姓名和密碼的系統登入對話方塊的 GUI 應用軟體。這個對話方塊的使用規則如下：

* 選擇訪客 (Guest) 登入或用戶 (Login) 登入
* 若為用戶登入，則輸入用戶名稱和密碼
* 選擇登入則按OK，放棄登入則按 Cancel。

有以下限制:

*　若選擇訪客登入，則用戶名稱和密碼要設為不可使用，無法輸入字串。
*　若選擇用戶登入，則用戶名稱可以使用，可輸入字串。
*　若用戶名稱的位置沒輸入任何字元時，則密碼為不可使用。
*　只要用戶名稱的位置有輸入字元，則密碼為可以使用 (若為訪客登入，則密碼當然就是不可使用)
*　若用戶名稱和密碼這兩個位置都有輸入字元時，則 OK 鍵為可使用，但若任何一個位置是空白的時候，則 OK 無法按下。(若為訪客登入，則 OK 當然永遠可以使用)
*　Cancel 隨時都可以按下。

像這樣需要協調多個物件的時候，就是 Mediator Pattern 的使用時機。不要讓物件彼此直接溝通，另設一個 **出面幫忙的顧問**，每個物件都只跟這個顧問溝通聯絡。當然，畫面輸出控制的邏輯就只要寫在顧問裡面即可。

<script src="https://gist.github.com/twmht/9277f7bbc0685c070997.js"></script>

####Mediator (正面) 參與者
Mediator 是跟 Colleague 進行溝通，規定調整的介面。例如 Mediator 介面。
#### ConcreteMediator 參與者
ConcreteMediator 是實作 Mediator 的介面，進行實際的調整。例如 LoginFrame 類別。
#### Colleague 參與者
Colleague 是規定與 Mediator 溝通的介面。例如 Colleague 介面。
#### ConcreteColleague 參與者
ConcreteColleague 實作 Colleague 的介面。例如 ColleagueButton、ColleagueTextField 及 ColleagueCheckbox 等幾個類別。

###優點
####解決分散處理時所帶來的困擾
因為所有的邏輯處理都放在 mediator 身上，因此只需要注意 mediator 即可。如果邏輯分散在各個元件身上，會變得很麻煩。
###哪些可以再利用
ConcreteColleague 容易再利用，因為與處理邏輯獨立分開。但 ConcreteMediator 反而就不容易再利用。

###問題
####1. 將程式修改成當用戶登入時，需要用戶名稱和密碼兩者輸入字元都超過4個字元，OK鍵才可以使用。

只需要將 LoginFrame 類別的 userpassChanged 方法的條件判斷修改如下：

    :::java
    if(textUser.getText().length() >= 4 && textPass.getText().length() >= 4){
            //statement here
    }

####2. ConcreteColleague 都有 mediator 欄位，而且 setMediator 方法的內容也相同。請在 Colleague 介面加入 mediator 欄位，讓它實作 setMediator 方法。

無法實作，因為介面不能有物件個體欄位，而且也無法實作具體方法。

同時也無法將 Colleague 介面設為類別。例如，假設把它設為類別，則 ColleagueButton 就沒辦法再繼承 Button 類別，因為 Java 只允許單繼承。
