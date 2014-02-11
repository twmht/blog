Title: Singleton Pattern -- 唯一的物件個體
Slug: singleton
Category: Design Pattern
Author: twmht

###用的時間點
通常我們在啟動程式時，就會產生許多物件個體。拿代表字串的 java.lang.String 類別物件個體來說，每個字串都會相對產生一個，所以如果某個程式內含 1000 個字串，就會產生 1000 個物件個體。

不過，有時候難免會有 **讓這個類別的物件個體只產生一個** 的需要，像是用程式來表現在程式中絕對是獨一無二的某個部份。好比說，表現電腦的類別或是表現視窗系統的類別等等就是最經典的例子。

###如何設計
Singleton 是指只有一個元素的集合，就是因為它只會有一個物件個體。

###程式範例
設計一個只有一個物件個體的類別。

<script src="https://gist.github.com/twmht/3339031996aa824bc3c4.js"></script>

####Singleton 參與者
Singleton Pattern 只出現一個 Singleton 參與者。 Singleton 的參與者具有 static 方法可取得唯一的物件個體。這個方法永遠都會傳回同一個物件個體。

###優點
在很多情況下，如果有一個以上的物件個體時，由於物件個體彼此之間的影響，可能會發展成出乎意料的 bug。Singleton Pattern 確保程式設計師不會不小心多產生物件。

###問題

####1.將Singleton Pattern 套用到 TicketMaker 類別。

    :::java
    public class TicketMaker {
        private int ticket = 1000;
        public int getNextTicketNumber() {
            return ticket++;
        }
    }

目的是為了只保有唯一的一個 TicketMaker。

<script src="https://gist.github.com/twmht/9dd80369fcd5aafa4453.js"></script>

####2.請自製一個物件個體數目只能有3個的類別 Triple。假設所有物件個體都要加上編號，且利用 getInstance(int id)可取得編號 id 的物件個體。

重點是做一個 static array。

<script src="https://gist.github.com/twmht/7dc40041251e218d94f0.js"></script>

####3.以下嚴格來說不能算是一個 Singleton Pattern，為什麼?

    :::java
    public class Singleton {
        private static Singleton singleton = null;
        private Singleton() {
            System.out.println("已產生物件個體。");
        }
        public static Singleton getInstance() {
            if (singleton == null) {
                singleton = new Singleton();
            }
            return singleton;
        }
    }


因為在多執行緒的狀態下，呼叫 getInstance 可能會產生多個物件。
例如：
<script src="https://gist.github.com/twmht/f14ef82669d41b855546.js"></script>

在 getInstance 方法前加上 synchronized 即可解決。

