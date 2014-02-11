Title: Adapter Pattern -- 換個包裝再度利用
Slug: adapter
Category: Design Pattern
Author: twmht

###用的時間點
例如將直流電換成交流電，轉換器的功能是介入既有內容和需要結果之間，作為溝通的橋樑。

如果既有內容無法直接利用時，通常需要先轉換成必要的型態後再使用。具有填平**既有內容**和**需要結果**兩者間的**落差**就是 **Adapter Pattern**。

###如何設計
設計wrapper，將既有內容包裝之後，重新再利用。

###程式範例(繼承)

改變輸出字串的外框，採用繼承。

<script src="https://gist.github.com/twmht/3576c41a962cb0ef2671.js"></script>

###程式範例(委讓)
改變輸出字串的外框，採用委讓。

<script src="https://gist.github.com/twmht/d89785e518eab0bf410e.js"></script>


####Target (對象) 參與者
決定現在需要什麼方法的參與者，例如筆記型電腦必須要有直流電才能動。例如 Print 介面。
#### Client 參與者
利用 Target 的方法來做事的參與者，例如有直流電 12V 才能用的比較型電腦。例如 Main 類別。
#### Adaptee (被動符合) 參與者
具有既有方法的參與者，也就是交流電 110V 的交流電電源。例如 Banner 類別。

如果擔任 Adaptee 參與者的方法與 Target 參與者的方法有相符時(即電源不需要轉換)，那就不需要 Adapter 參與者了。
#### Adapter 參與者
利用 Adaptee 的方法努力滿足 Target 的要求。例如，把交流電 110V 轉換成直流電 12V 的轉換器。例如 PrintBanner 類別。

如果是類別的 Adapter Pattern，Adapter 要透過**繼承**的方式來利用 Adaptee。而換到物件個體時，就要改以**委讓**來利用 Adaptee。

###優點
####就算沒有原始碼也無妨
Adapter Pattern 可以把過去使用過的類別換個包裝重新建立出需要的類別。因為可以確定既有類別 (Adaptee 參與者) 沒有問題，所以只要重點式地檢查 Adapter 參與者的類別即可。

Adapter Pattern 只要知道既有類別的規格，就能建立其它新的類別。
####版本更新與相容性
凡是軟體都會需要做版本更新，當你在做軟體的版本更新時最常碰到的問題應該是**與舊版本的相容性**。利用 Adapter Pattern 可讓新舊版本共存，維護更容易。

假設現在完成版本更新後，就只著重在新版本而不想再維護舊版本的部份。此時，把新版本視為 Adaptee 參與者，舊版本則為 Target ，接下來只要建立一個擔任 Adapter 參與者的類別，讓它利用新版本的類別來實作舊版本即可。

如果 Adaptee 與 Target 功能相差太多的話，當然就不能使用 Adapter Pattern 了。

###問題

java.util.Properties類別是用來管理 key 和相對應 value （即內容），如：

* year=2000 
* month=11 
* day=20

java.util.Properties類別有下面幾個方法可從資料束（stream）讀取內容或反向寫入到 資料束。

* void load(InputStream in) throws IOException 從InputStream讀取內容的集合。
* void store(OutputStream out, String header) throws IOException 把內容的集合寫入到OutputStream。header是註解字串。 


請利用Adapter Pattern建立一個把內容的集合儲存成檔案的FileProperties類別。

假設在此是以FileIO介面（Target角色）宣告把內容的集合儲存成檔案的方
法，FileProperties類別則是實作這個FileIO介面。

執行前和執行後的file.txt、newfile.txt（若該行字首是#，則為java.util.Properties類別自動產生的註解）。

**如果有FileProperties類別，就算不知道java.util.Properties類別的方法，只要知道FileIO介面的方法就能處理內容。**

以電源來比喻的話，java.util.Properties類別是既有的交流電110V、FileIO介面是現在需要的直流電12V，而FileProperties類別則為轉接器。 

**實際上這個問題主要是要把本來的 java.util.Properties 包裝成 FileProperties 類別。**

<script src="https://gist.github.com/twmht/dd1521c8d1fcf6e16d4f.js"></script>
