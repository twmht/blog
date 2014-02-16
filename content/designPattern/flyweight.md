Title: Flyweight Pattern
Slug: flyweight
Category: Design Pattern
Author: twmht

###用的時間點
當想要節省記憶體空間的時候使用。

###如何設計
儘量共用物件個體，不做無謂的new。

###程式範例
輸出大型文字。

<script src="https://gist.github.com/twmht/aa42efa98d66a87a5271.js"></script>

####Flyweight 參與者
表示以一般處理會讓程式變重，因此選擇共用較佳的參與者。例如BigChar類別。
####Flyweight FlyweightFactory 參與者
產生Flyweight 參與者的工廠。利用這個工廠來產生 Flyweight 參與者，即可共用物件個體。　例如BigCharFactory類別。
####Client 參與者
利用 FlyweightFactory 參與者產生並使用 Flyweight 參與者。例如 BigString 類別。

###問題
####1. 在 BigString 中新增如下的建構子。BigString(String string, boolean shared)，若 shared 為 true 則共用 BigChar;若為 false 則不共用。

若不共用 BigChar，則不使用 BigCharFactory 而改用 new 的方式。

<script src="https://gist.github.com/twmht/6436cb19bd60c33d194e.js"></script>

####2. 利用上一個問題所修改的 BigString 類別，比較共用和不共用 BigChar 的物件個體時的記憶體使用量。

結果的確是共用的話，記憶體耗用較少。

    :::java
    public class Main {
        public static void main(String[] args) {
            if (args.length == 0) {
                System.out.println("Usage: java Main digits");
                System.out.println("Example: java Main 1212123");
                System.exit(0);
            }
            BigString bs;
            bs = new BigString(args[0], false);     // 不共用
            bs.print();
            bs = new BigString(args[0], true);      // 共用
            bs.print();
        }
    }

####3. 在 BigCharFactory 類別中，getBigChar 是 synchronized 方法。如果不設為 synchronize，會出現什麼問題?

在多個 Thread 呼叫時，可能會有重複 new 的情形。
