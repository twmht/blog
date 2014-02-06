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
輸出字串，固定的字串(Template)，卻有不同的輸出方式(外框不同)。

<script src="https://gist.github.com/twmht/b29a5df581fcd2090243.js"></script>

####AbstractClass (抽象類別) 參與者
AbstractClass 實作範本方法，還有宣告 Template Method 所使用的抽象方法。這個抽象方法則由子類別 ConcreteClass 負責實作。例如 AbstractClass 類別。
####ConcreteClass (具象類別) 參與者
具體實作 AbstractClass 所定義的抽象方法，這裡所實作的方法是從 AbstractClass 的範本方法呼叫出來。例如 CharDisplay 和 StringDisplay 類別。
