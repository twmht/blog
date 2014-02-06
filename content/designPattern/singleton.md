Title: Singleton Pattern -- 唯一的物件個體
Slug: singleton
Category: Design Pattern
Author: twmht

###用的時間點
通常我們在啟動程式時，就會產生許多物件個體。拿代表字串的 java.lang.String 類別物件個體來說，每個字串都會相對產生一個，所以如果某個程式內含 1000 個字串，就會產生 1000 個物件個體。

不過，有時候難免會有 "讓這個類別的物件個體只產生一個" 的需要，像是用程式來表現在程式中絕對是獨一無二的某個部份。好比說，表現電腦的類別或是表現視窗系統的類別等等就是最經典的例子。

###如何設計
Singleton 是指只有一個元素的集合，就是因為它只會有一個物件個體。

###程式範例
設計一個只有一個物件個體的類別。

<script src="https://gist.github.com/twmht/3339031996aa824bc3c4.js"></script>

####Singleton 參與者
Singleton Pattern 只出現一個 Singleton 參與者。 Singleton 的參與者具有 static 方法可取得唯一的物件個體。這個方法永遠都會傳回同一個物件個體。
