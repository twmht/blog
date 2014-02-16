Title: State Pattern
Slug: state
Category: Design Pattern
Author: twmht

###用的時間點
用類別來表示 "狀態" 。

###如何設計
以類別來表示狀態之後，只要切換類別就能表現 "狀態變化"，而且在必須新增其它狀態時，也很清楚該編寫哪個部份。

###程式範例
假設現在有一個會隨著時間改變警備狀態的金庫保全系統：

* 有一個金庫
* 金庫有跟保全中心連線
* 金庫有警鈴和一般通話用的電話
* 金庫有時鐘，監視目前的時間
* 白天是9:00-16:59，晚間為17:00-23:59以及0:00-8:59
* 只有白天才能使用金庫
* 在白天使用金庫時，保全中心會保留使用紀錄
* 若晚間使用金庫時，保全中心會接到發生異常現象的通知
* 警鈴是24小時都可以使用
* 一旦使用警鈴，保全中心會接收到警鈴通知
* 一般通話用的電話是24小時都可以使用(但晚間只有答錄機服務)
* 在白天使用電話時，就會呼叫保全中心
* 若晚間使用電話時，則會呼叫保全中心的答錄機

<script src="https://gist.github.com/twmht/a04e437a923e01314421.js"></script>

####State 參與者
State 表示狀態。規定不同狀態下做不同處理的介面。這個介面等於是一個不同狀態所做處理的所有方法的集合。例如 State 介面。
####ConcreteState 參與者
ConcreteState 是表示具體的不同狀態，具體實作在 State 所規定的介面。例如 DayState 以及 NightState 類別。
####Context 參與者
Context 具有表示現在狀態的 ConcreteState，而且還規定 State Pattern 的利用者所需要的介面。例如 Context 介面以及 SafeFrame 類別。
Context 介面負責規定介面的部份，SafeFrame 類別則負責具有 ConcreteState 參與者的部份。

###優點
####Divide and Conquer
State Pattern 是以**類別**來表示**狀態**。利用不同的類別分別表示各種具體狀態的動作就是在分割問題。當在寫某一個 ConcreteState 時，可以讓自己以為沒有其他類別，彷彿獨立開來一樣。

如果不用這個 Pattern 的話，使用金庫時所呼叫的方法就得根據現在的狀態進行處理。狀態種類愈多，條件判斷就愈多;況且所有發生時所呼叫的所有方法都要寫同樣的條件判斷處理。

因為 State Pattern 是用類別來表示系統**狀態**，所以才能細細分割一個龐大複雜的程式。
####有該狀態才會有的處理
SafeFrame 類別的 setClock 方法是被 Main 類別呼叫出來。Main 類別呼叫 setClock 方法說*請設定時間*。在 setClock 方法中，這個處理委讓給 state，也就是說，設定時間被當作一個**有現在的狀態才會有的處理**。

不只是 doClock 方法，State 介面所宣告的方法都是**有該狀態才會有的處理**，其實就是**因狀態而異的處理**。

可以以下面兩點為基礎設計:

* 宣告成抽象方法，作為介面
* 實作成具體方法，作為不同的類別

####不會有自我矛盾
如果不用這個 Pattern，改以多個變數之值的集合來表示系統狀態，這時候變數值之間不能有自我矛盾或不一致的情形。

State Pattern 中，表示現在狀態的變數只有一個(SafeFrame 類別中的 state 變數)。因此不會有自我矛盾的情形。

####新增狀態很容易
新增狀態非常簡單。不過，如果想在已經完成的 State Pattern 中新增一個**有狀態才會有的處理**就沒那麼容易。因為這個新增的動作代表了要在 State 參與者的介面新增其他方法的意思，而且所有的 ConcreteState 都要新增這個處理。

雖然這個動作有點困難，但卻不用擔心會不小心忘記新增，因為編譯器會自動報錯。比起不用State Pattern，而用大量的 if 條件敘述要好用的多。

###多樣的物件個體
SafeFrame 類別中出現了下面兩種敘述：

* 在 SafeFrame 建構子內: buttonUse.addActionListener(this);
* 在 actionPerformed 方法內: state.doUse(this)

兩個 this 都是 SafeFrame 類別的物件個體。因為只會產生一個 SafeFrame 的物個體，因此這兩個 this 為同值。

在傳遞給 addActionListener 方法時，這個物件個體被視為**實作 ActionListener 介面之類別的物件個體**。因為 addActionListener 方法的引數是 ActionListener 型態。在 addActionListener 方法中，引數的使用範圍是在**ActionListener 介面所規定的方法的範圍之內**。傳遞過來做為引數的是不是 SafeFrame 的物件個體根本不重要。

而在傳遞給 doUse 方法的時候，同樣的物件個體卻被視為**實作 Context 介面之類別的物件個體**。因為 doUse 方法的引數是 Context 型態。在 doUse 方法中，**引數的使用範圍是在 Context 介面所規定方法的範圍之內**。

###問題
####1. 理論上，Context 應該要設成抽象類別而非介面，而 state 欄位應該要規類到 Context 類別才符合 Pattern 的主旨，但是程式範例卻把 Context 設成介面，而 state 欄位則是放在 SafeFrame 類別，為什麼?

由於 Java 是單一繼承，因此如果以類別表示 Context 的話，就不能再把已經是 Frame 的子類別之 SafeFrame 類別設為 Context 類別的子類別。

如果要做的話，應該要另外作一個 Context 類別的子類別，將其物件個體儲存在 SafeFrame 的欄位，用委讓的方式去做。

####2. 如果想把範例程式中的白天改成 8:00-20.59，而晚間改成 21:00~23:59 和 0:00~7:59。該如何修改?

需要修改 DayState 和 NightState 類別的 doClock 方法。

如果一開始先在 SafeFrame 類別建立 isDay 方法和 isNight 方法，預先準備好檢查目前時間是白天還是夜晚的方式，就能把具體的時間範圍放到 SafeFrame 類別之內。這樣之後就只要修改 SafeFrame 類別即可。

####3. 請加入 **午餐時間**(12:00~12:59) 這個新狀態。若午餐時間使用金庫，則保全中心會接到發生異常狀態的通知;若使用警鈴，則保全中心會接到警鈴通知，若使用電話，則會呼叫保全中心的答錄機。

新增一個 NoonState 類別。

    :::java
    public class NoonState implements State {
        private static NoonState singleton = new NoonState();
        private NoonState() {                                // 建構子為private
        }
        public static State getInstance() {                 // 取得唯一的個體
            return singleton;
        }
        public void doClock(Context context, int hour) {    // 設定時間
            if (hour < 9 || 17 <= hour) {
                context.changeState(NightState.getInstance());
            } else if (9 <= hour && hour < 12 || 13 <= hour && hour < 17) {
                context.changeState(DayState.getInstance());
            }
        }
        public void doUse(Context context) {                // 使用金庫
            context.callSecurityCenter("異常：午餐時間使用金庫！");
        }
        public void doAlarm(Context context) {              // 警鈴
            context.callSecurityCenter("警鈴(午餐時間)");
        }
        public void doPhone(Context context) {              // 一般通話
            context.recordLog("午餐時間的通話錄音");
        }
        public String toString() {                          // 輸出字串
            return "[午餐時間]";
        }
    }

DayState 的 doClock 方法都要修改。

    :::java
    public class DayState implements State {
        private static DayState singleton = new DayState();
        private DayState() {                                // 建構子為private
        }
        public static State getInstance() {                 // 取得唯一的個體
            return singleton;
        }
        public void doClock(Context context, int hour) {    // 設定時間
            if (hour < 9 || 17 <= hour) {
                context.changeState(NightState.getInstance());
            } else if (12 <= hour && hour < 13) {                   
                context.changeState(NoonState.getInstance());       
            }                                                       
        }
        public void doUse(Context context) {                // 使用金庫
            context.recordLog("使用金庫(白天)");
        }
        public void doAlarm(Context context) {              // 警鈴
            context.callSecurityCenter("警鈴(白天)");
        }
        public void doPhone(Context context) {              // 一般通話
            context.callSecurityCenter("一般的通話(白天)");
        }
        public String toString() {                          // 輸出字串
            return "[白天]";
        }
    }

NightState 類別的 doClock 方法都要修改。

    :::java
    public class NightState implements State {
        private static NightState singleton = new NightState();
        private NightState() {                              // 建構子為private
        }
        public static State getInstance() {                 // 取得唯一的個體
            return singleton;
        }
        public void doClock(Context context, int hour) {    // 設定時間
            if (9 <= hour && hour < 17) {
                context.changeState(DayState.getInstance());
            } else if (12 <= hour && hour < 13) {                   
                context.changeState(NoonState.getInstance());       
            }                                                       
        }
        public void doUse(Context context) {                // 使用金庫
            context.callSecurityCenter("異常：晚間使用金庫！");
        }
        public void doAlarm(Context context) {              // 警鈴
            context.callSecurityCenter("警鈴(晚間)");
        }
        public void doPhone(Context context) {              // 一般通話
            context.recordLog("晚間的通話錄音");
        }
        public String toString() {                          // 輸出字串
            return "[晚間]";
        }
    }

####3. 請加入**緊急**這個新狀態。當按下警鈴時，無論任何時間，狀態立刻切換到緊急狀態。若緊急狀態時使用金庫，則保全中心接到緊急狀況通知;若使用警鈴，則保全中心會接到警鈴通知;若使用電話，則會呼叫保全中心。

這個規格的問題在於發生異常之後，沒有可以回到原來狀態的方式。

新增一個 UrgentState 類別。

    :::java
    public class UrgentState implements State {
        private static UrgentState singleton = new UrgentState();
        private UrgentState() {                                // 建構子為private
        }
        public static State getInstance() {                 // 取得唯一的個體
            return singleton;
        }
        public void doClock(Context context, int hour) {    // 設定時間
            // 設定時間的部分不做處理
        }                                                                   
        public void doUse(Context context) {                // 使用金庫
            context.callSecurityCenter("異常：異常使用金庫！");
        }
        public void doAlarm(Context context) {              // 警鈴
            context.callSecurityCenter("警鈴(異常)");
        }
        public void doPhone(Context context) {              // 一般通話
            context.callSecurityCenter("一般的通話(異常)");
        }
        public String toString() {                          // 輸出字串
            return "[異常]";
        }
    }

修改 DayState 類別的 doAlarm 方法。

    :::java
    public class DayState implements State {
        private static DayState singleton = new DayState();
        private DayState() {                                // 建構子為private
        }
        public static State getInstance() {                 // 取得唯一的個體
            return singleton;
        }
        public void doClock(Context context, int hour) {    // 設定時間
            if (hour < 9 || 17 <= hour) {
                context.changeState(NightState.getInstance());
            }
        }
        public void doUse(Context context) {                // 使用金庫
            context.recordLog("使用金庫(白天)");
        }
        public void doAlarm(Context context) {              // 警鈴
            context.callSecurityCenter("警鈴(白天)");
            context.changeState(UrgentState.getInstance()); 
        }
        public void doPhone(Context context) {              // 一般通話
            context.callSecurityCenter("一般的通話(白天)");
        }
        public String toString() {                          // 輸出字串
            return "[白天]";
        }
    }

修改 NightState 的 doAlarm 方法。

    :::java
    public class NightState implements State {
        private static NightState singleton = new NightState();
        private NightState() {                              // 建構子為private
        }
        public static State getInstance() {                 // 取得唯一的個體
            return singleton;
        }
        public void doClock(Context context, int hour) {    // 設定時間
            if (9 <= hour && hour < 17) {
                context.changeState(DayState.getInstance());
            }
        }
        public void doUse(Context context) {                // 使用金庫
            context.callSecurityCenter("異常：晚間使用金庫！");
        }
        public void doAlarm(Context context) {              // 警鈴
            context.callSecurityCenter("警鈴(晚間)");
            context.changeState(UrgentState.getInstance()); 
        }
        public void doPhone(Context context) {              // 一般通話
            context.recordLog("晚間的通話錄音");
        }
        public String toString() {                          // 輸出字串
            return "[晚間]";
        }
    }
