Title: Bridge Pattern -- 分成功能階層和實作階層
Slug: bridge
Category: Design Pattern
Author: twmht

###用的時間點
bridge 是 "橋樑" 的意思。就像現實社會裡的橋樑擔負著連接河川兩岸的重責大任一樣，Bridge Pattern 也是負責連接兩個不同位置的參與者。
###如何設計
Bridge Pattern 居間溝通的兩個位置是指 "功能的類別階層" 和 "實作的類別階層"。

####想要新增功能時
假設現在有一個類別 Something，如果想對 Something 新增其它功能時(例如，想多加一個新方法)，首先要建立 SomethingGood 類別作為 Something 的子類別 (子類別、衍生類別或擴充類別)。這就是一個小型的類別階層。
這個階層是為了新增功能而建立:

* 基本功能放在父類別
* 新功能則新增到子類別

又稱為 "功能的類別階層"。
假設現在又想對 SomethingGood 類別新增另一個功能時。此時，要建立 SomethingBetter 類別作為 SomethingGood 類別的子類別。如此一來，功能的類別階層又往下延伸一層。

如欲追加新功能時，找出類別階層中最接近目的的類別，然後建立一個子類別、建立一個有該功能的新類別...。這就是一個功能的類別階層。基本上，類別階層也最好不要建立太多層。

####想要新增實作時
在 Template Method Pattern 中，抽象類別把一連串的方法群組宣告成抽象方法，再規定介面。然後由子類別實際實作這個抽象方法。父類別的作用是利用抽象方法來規定介面，子類別的作用則是進行實作。這樣把讓父類別扮演好參與者分工，可以建立出高零組件價值(可更換性)的類別。

這裡也有類別階層的影子，假設實作父類別 AbstractClass 的抽樣方法的子類別是 ConcreteClass，則可建立起一個小型類別階層。不過這裡的類別階層並不是為了新增功能，因為類別階層沒有追加新功能的目的。這個類別階層有下列的參與者分工:

* 父類別使用抽象方法來規定介面
* 子類別使用具體方法來實作此介面

這樣的類別階層就稱為 "實作的類別階層"。
假設現在要建立另一個 AbstractClass 的實作，若其子類別為 AnotherConcreteClass，則實作的階層會有一點變化。總之，如果要建立一個新的實作，必須建立 AbstractClass 的子類別，然後實作抽象方法，這就是實作的類別階層。

####類別階層的同處一室和獨立分離
當我們有一個念頭 "好，現在要做一個子類別"的時候，請先確認清楚自己想要完成的內容 "這個動作是要新增功能?還是要進行實作?"。如果類別階層只有一個的話，功能的類別階層和實作的的類別階層就會放在同一個階層構造裡。這樣可能會讓類別階層變得太複雜，而且不容易預測後面的發展。因為自己在建立子類別時，常常會搞不清楚應該放在類別階層的哪個位置。

既然如此，那就把 "功能的類別階層" 和 "實作的類別階層" 分成兩個獨立的類別階層吧。如果一分為二可能會弄的支離破碎，所以必須在兩個類別階層之間建立一座溝通的橋樑 (bridge)。

###程式範例
用來 "列印內容" 的程式。

<script src="https://gist.github.com/twmht/bdf3a8e71e7f4d11192e.js"></script>

####Abstraction (抽象化) 參與者
位於 "功能的類別階層" 最上層的類別，利用 Implementor 的方法只記載基本功能的類別。這個物件個體是保持住 Implementor。例如 Display 類別。
#### RefinedAbstraction (改良後的抽象化) 參與者
對 Abstraction 參與者新增功能的參與者。例如 CountDisplay 類別。
#### Implementor (實作者) 參與者
位於 "實作的類別階層" 最上層的類別，規定要實作 Abstraction 參與者之介面的方法。例如 DisplayImpl 類別。
#### ConcreteImplementor (具體的實作者) 參與者
具體實作 Implementor 參與者的介面。例如 StringDisplayImpl 類別。

