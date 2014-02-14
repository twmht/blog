Title: Facade Pattern -- 單一窗口
Slug: facade
Category: Design Pattern
Author: twmht

###用的時間點
程式這個東西往往愈做愈大，許多類別彼此間的影響讓關係更加錯綜複雜。因此在使用類別時，要確實了解類別之間的關係，正確依序呼叫方法。
利用大型程式進行資料處理時，必須精確控制相關的類別。既然如此，就乾脆設個處理專用的"窗口"，如此一來就不需要個別控制類別，只要把要求丟給"窗口"即可。
###如何設計
Facade Pattern 能整合錯綜複雜的來龍去脈，提供較為高級的介面。Facade 參與者則是讓系統外埠看到較簡單的介面。而且 Facade 參與者還會兼顧系統內部各類別功能和互動關係，以最正確的順序利用類別。

###程式範例
設計一個產生使用者 Web 網頁的程式。
以三個類別的簡單系統為例，這個系統中包含有利用郵件信箱取得姓名的資料庫(Database)、產生 HTML 檔的類別(HtmlWriter)以及提供較高級介面的類別(PageMaker，也就是 Facade 參與者)。

<script src="https://gist.github.com/twmht/2df294dc66cd9a1008ce.js"></script>

####Facade (正面) 參與者
構築成系統的其他參與者之"單一窗口"。Facade 對系統外部提供較高級且單一的介面。例如 PageMaker 類別。
#### 構築成系統的其他參與者
其他林林種種的參與者則各司其職，Facade 參與者的存在並不會有任何影響。它們乖乖的聽從 Facade 的呼叫出來做事，但不會反過來呼叫 Facade。例如 Database 及 HtmlWriter 類別。
#### Client 參與者
利用 Facade Pattern 的參與者。例如 Main 類別。

####優點
###減少介面
Facade 讓複雜的內容看起來很單純。躲在背後工作的那些類別間的關係和用法相當複雜，Facade 可以把這些複雜的方法組合隱藏在背後，讓 Client 只專注在 Facade 上面。

這部份的重點就在**減少介面**。看了太多的類別和方法，只會讓程式設計師猶豫不知道該使用哪一個才對，而且還得注意呼叫順序不能搞錯。要注意的事情愈多，就愈是容易弄錯。所以不如**把精神放在介面較少的 Facade 上**，反而比較有效率。

###Facade Pattern 的遞迴應用
假設現在有數個內含 Facade 的類別集合，這時候當然可以新增一個整合所有集合的 Facade。換句話說，就是遞迴應用 Facade Pattern。

如果是面對大型系統有大量的類別和 package 時，在適當的位置使用 Facade Pattern 會很方便。

###問題
####請在 PageMaker 類別新增一個 makeLinkPage 方法，這個方法可產生使用者郵件信箱的相關鏈結。

    :::java
    package pagemaker;

    import java.io.FileWriter;
    import java.io.IOException;
    import java.util.Properties;
    import java.util.Enumeration;

    public class PageMaker {
        private PageMaker() {   // 不建立物件個體，所以宣告private
        }
        public static void makeWelcomePage(String mailaddr, String filename) {
            try {
                Properties mailprop = Database.getProperties("maildata");
                String username = mailprop.getProperty(mailaddr);
                HtmlWriter writer = new HtmlWriter(new FileWriter(filename));
                writer.title("Welcome to " + username + "'s page!");
                writer.paragraph("歡迎來到" + username + "的網頁。");
                writer.paragraph("等你來信喔！");
                writer.mailto(mailaddr, username);
                writer.close();
                System.out.println(filename + " is created for " + mailaddr + " (" + username + ")");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
        public static void makeLinkPage(String filename) {          
            try {
                HtmlWriter writer = new HtmlWriter(new FileWriter(filename));
                writer.title("Link page");
                Properties mailprop = Database.getProperties("maildata");
                Enumeration en = mailprop.propertyNames();
                while (en.hasMoreElements()) {
                    String mailaddr = (String)en.nextElement();
                    String username = mailprop.getProperty(mailaddr, "(unknown)");
                    writer.mailto(mailaddr, username);
                }
                writer.close();
                System.out.println(filename + " is created.");
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
