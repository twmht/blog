Title: Template Method Pattern -- 實際處理交給子類別
Slug: templateMethod
Category: Design Pattern
Author: twmht

###用的時間點
就像在塑膠版上挖空，然後用色筆塗滿挖空的部份，所表現出來的是固定的字型，但顏色卻因所使用的色筆顏色而異。所挖空的部份我們稱為 Template。
###如何設計
將作為 Template 的方法定義在父類別，而方法的定義中則使用到抽象方法。因此如果只看父類別部份的程式，根本不知道到底結果會是怎樣的處理內容，最多只能了解該如何呼叫抽象方法而已。

實際實作抽象方法的是子類別。要在子類別實作方法，才能決定具體的處理動作。理論上，如果在不同的子類別執行不同的實作，應該就能發展出不同的處理內容。不過，無論在哪個子類別執行任何一種實作，處理的大致流程都還是要依照父類別所制定的方法。

像這樣在**在父類別指定大綱並且在子類別規定具體內容**，就稱為 Template Method Pattern。

###程式範例
輸出字串，同樣流程的display，卻有不同的輸出方式(字串或字元)。

<script src="https://gist.github.com/twmht/b29a5df581fcd2090243.js"></script>

####AbstractClass (抽象類別) 參與者
AbstractClass 實作範本方法，還有宣告 Template Method 所使用的抽象方法。這個抽象方法則由子類別 ConcreteClass 負責實作。例如 AbstractClass 類別。
####ConcreteClass (具象類別) 參與者
具體實作 AbstractClass 所定義的抽象方法，這裡所實作的方法是從 AbstractClass 的範本方法(display 方法)呼叫出來。例如 CharDisplay 和 StringDisplay 類別。

###實際例子
在java.io.InputStream 的子類別進行實作的方法是 java.io.InputStream 的 read() 方法。read() 方法則被 java.io.InputStream 的範本方法 read(byte[] b,int off,int len) 反覆呼叫出來。

換句話說，**讀取1 byte** 這個處理的具體內容是交給子類別，在java.io.InputStream 這端則產生 **將指定 byte 讀入到陣列的指定位置**之處理的範本方法。

**Template Method Pattern**不容許使用介面，因為介面是全部方法都是抽象，而抽象類別允許部份方法抽象。

###優點
####邏輯可共用
因為在父類別的範本方法已經敘述了演算法則，所以子類別這邊就不需要重新逐一敘述演算法則。

假設現在故意不用 Template Method Pattern，只利用編輯器的剪貼功能來建立多個 ConcreteClass 參與者。可是後來發現其中一個 ConcreteClass 有一個 bug 時，只修改一個 bug 並沒有辦法反應到所有的 ConcreteClass 上。

從這個角度來看，如果利用 Template Method Pattern 來寫程式的話，當你發現範本方法裡面有錯誤時，只要修改這個範本方法即可。
####父類別跟子類別的連續動作
在 Template Method Pattern 中，父類別跟子類別之間的聯絡互動相當緊密。因此如果要在子類別實際實作一個已經在父類別宣告過的抽象方法時，必須先了解應該在哪個時間點呼叫這個抽象方法。要是沒有父類別的原始程式碼，恐怕子類別的實作會是一個高難度的跳戰。
####子類別應視同父類別
例如 CharDisplay 的物件個體和 StringDisplay 的物件個體都先指定到 AbstractClass 型態的變數，然後才呼叫 display 範本方法。

假設現在有一個父類別型態的變數，子類別的物件個體也被指定到該變數。此時，程式最好利用 instanceof 等寫成無論子類別種類為何，程式都能正常運作。

無論父類別型態的變數指定哪一個子類別的物件個體都能正常動作的原則稱為 **The Liskov Substituion Principle**，LSP 是繼承相關的一般性原則。

###類別階層與抽象類別
####父類別對子類別的要求
我們在學習類別階層時，通常都是從子類別的角度來思考:

* 在子類別可利用父類別中所定義的方法
* 子類別只要寫一點點方法就可以新增其他功能
* 在子類別 override 方法就能修改程式動作

在這裡可以改變一下觀點，從父類別的角度來想。假設現在父類別已經宣告了抽象方法。此時，這個方法的實作要**全權交給子類別**。也就是說，當你在宣告抽象方法時，事實上是在程式中表示：

* 期待子類別會實作這個方法
* 要求子類別要實作這個方法

你也可以把它解釋成子類別產生一個需要實作在父類別所宣告的抽象方法的責任。這稱為 subclass responsibility。
####抽象類別的意義
因為抽象方法裡面沒有方法的主體，所以無法得知具體的處理內容。但是，它可以決定方法名稱並且利用範本方法來敘述處理的內容。實際的處理內容當然要留給子類別確定，**不過在抽象類別的階段就先抓出處理流程的型態也很重要**。
####父類別跟子類別之間的協調
在設計一個程式時，必須不斷協調父類別和子類別兩邊。如果增加父類別這邊的敘述，就可以減輕在子類別的負擔，但是相對地也會降低子類別自由發揮的空間。反過來，如果減少父類別的敘述時，子類別這邊的敘述就會比較棘手，可能會發生不同子類別出現同樣處理的敘述內容。

Template Method Pattern 則是在父類別敘述處理的骨架，把具體的外觀肉體留給子類別來做。至於應該怎麼分配，則是程式設計師的工作了。