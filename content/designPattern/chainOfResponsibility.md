Title: Chain of Responsibility Pattern -- 責任轉送
Slug: chainOfResponsibility
Category: Design Pattern
Author: twmht

###用的時間點
什麼是 "轉送" 呢? 假設現在要到某家公司去取文件，跟櫃台小姐說明來意後，他會告訴你應該到 "業務窗口" 去處理。當你走到業務窗口後，那邊又告訴你這份文件目前由 "客戶服務部" 負責;因此你得再到客戶服務部去一趟，找到客戶服務部後，小姐還是很客氣的說文件應該要到 "文管中心" 去拿。像這樣子把自己的要求傳送下去，一直找到適當的人選或地點就是 "轉送"。
###如何設計
例如，現在產生一個要求，但無法直接決定處理該要求的物件。這時候，可以把一個以上的物件串聯成鎖鏈狀，依序走過這個連鎖物件再決定最後目的地的物件。
如果使用這個 Pattern，可以降低 "要求端" 和 "處理端" 之間的結合性，讓它們個別成為獨立的零件。另外，還可支援有需依發生狀況改變處理要求的物件的程式。
先對人產生一個要求，如果這個人有處理的能力就處理掉;如果不能處理的話，就把要求轉送給 "第二個人"。同樣的，如果第二個人有處理能力的話就處理掉，不能處理的話，就繼續轉送給第三個人，以此類推。

###程式範例
這個程式會產生問題以及決定解決問題的人。例如一開始先是 Bob 在努力解決問題，但無法解決的時候就換成 Diana 接手。在這個過程中，都沒有發現 Alice 的蹤影，因為 Alice 只負責轉送所有問題。

<script src="https://gist.github.com/twmht/7eeb3b146fbdc6fd0ef9.js"></script>

####Handler (處理者) 參與者
Handler 是規定處理要求的介面的參與者。它會維持住 "下一個人"，萬一出現自己無法處理的要求時，再轉送過去。當然， "下一個人" 也是 Handler。例如 Support 類別。處理要求的方法則是 support 方法。
#### ConcreteHandler 參與者
ConcreteHandler 是具體處理要求的參與者。例如NoSupport、LimitSupport、OddSupport 以及 SpecialSupport 這幾個類別。
#### Client (要求者) 參與者
Client 是對第一個 ConcreteHandler 發出要求的參與者，例如 Main 類別。

###優點
####讓要求跟處理要求兩者間的結合關係不會太緊密
Client 直接把要求丟給第一個人，接下來這個要求就會被送往進行連鎖處理，由適合的處理者來處理要求。

如果不想使用這個 Pattern 的話，就必須採取中央集權式的管理，也就是要由其中一個人掌握**這個要求該由哪個人處理**的訊息。這個訊息最好不要交給**發出要求的人**，因為如果發出要求的人還要了解處理者個別作用能力的話，反而會降低零件的獨立性。

####機動性改變連鎖狀態
支援小組從 Alice 到 Fred 的排列順序都沒有改變。但是，程式也有可能需要機動性改變物件(處理要求的 ConcreteHandler)之間的關係。此時，只要像 Chain of Responsibility Pattern 這樣利用委讓來轉送，就能根據狀況變化重組 ConcreteHandler。

萬一程式沒有利用 Chain of Responsibility Pattern，把**如果是A要求，則由甲處理者處理**的對應關係寫死的話，要想在跑程式的時候改成其他的處理者就很麻煩。

####能專心工作在自己的崗位上
所有 ConcreteHandler 都只看著自己有能力處理的工作，如果自己處理不了，就當機立斷送出去。如此一來，應該寫在各個 ConcreteHandler 的處理就會鎖定是在該 ConcreteHandler 的固定內容。

假設現在不用這個 Pattern，那就要採取找**一個出來帶頭，讓它決定要由誰來處理不同的要求的方法**;或者是讓所有 ConcreteHandler 都要負責**工作分配**，也就是**如果自己無法處理時，要交給某甲。如果某甲也不行，就交給某乙。如果系統出現 A 狀況，就交給某丙的方法。**

###轉送會造成處理速度變慢？
如果有預先確定由誰處理哪個要求，可以讓處理者立即動手處理，相較之下，Chain of Responsibility Pattern 的處理速度本來就會稍慢。

如果說要求跟處理者的關係很固定，而且又講究速度時，可能不使用這個 Pattern 會較有利。

###問題
####1. 視窗系統使用 Chain of Responsibility Pattern 的頻率很高。 視窗上有很多種元件，當按下滑鼠左鍵時所產生的事件是如何轉送出去?轉送位置(next)又出現在哪裡?

通常是在元件所在的父視窗為 next 的情況下，傳遞給元件的要求如果不是由該元件處理，則會傳過去給父視窗。

###2. Support 類別中，support 方法設為 public，但 resolve 方法卻是 protected。為什麼？

因為當其他類別要求 Support 類別的物件個體幫忙解決問題時，必須要使用 support 方法，而不是 resolve 方法。

###3. 原本以遞迴呼叫的 suppot 方法，請改成迴圈吧！

    :::java
    public abstract class Support {
        private String name;                  // 問題解決者的名稱
        private Support next;                 // 轉送位置
        public Support(String name) {         // 產生問題解決者
            this.name = name;
        }
        public Support setNext(Support next) {  // 設定轉送位置
            this.next = next;
            return next;
        }
        public final void support(Trouble trouble) {          
            for (Support obj = this; true; obj = obj.next) {
                if (obj.resolve(trouble)) {
                    obj.done(trouble);
                    break;
                } else if (obj.next == null) {
                    obj.fail(trouble);
                    break;
                }
            }
        }
        public String toString() {              // 列印字串
            return "[" + name + "]";
        }
        protected abstract boolean resolve(Trouble trouble); // 解決的方法
        protected void done(Trouble trouble) {  // 已解決
            System.out.println(trouble + " is resolved by " + this + ".");
        }
        protected void fail(Trouble trouble) {  // 尚未解決
            System.out.println(trouble + " cannot be resolved.");
        }
    }
