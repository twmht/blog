Title: Iterator Pattern
Slug: iterator
Category: Design Pattern
Author: twmht

###Iterator Pattern是指依序掃描並且處理多個數字或變數。本身也是反覆的意思，又可以稱為迭代器。

現在要寫一個程式，可以把書籍放到書架上，並且依序印出來。

Aggregate Interface，實作此Interface的類別就變成類似<font color=red>陣列（多個數字或變數的集合)</font>。

    :::java
    public interface Aggregate {
        //一個可對應聚合的iterator
        public abstract Iterator iterator();
    }

如果要掃描整個聚合時，利用iterator方法即可建立一個實作Iterator介面的類別物件個體。

    :::java
    public interface Iterator {
        //有沒有下一個元素
        public abstract boolean hasNext();
        //下一個元素
        public abstract Object next();
    }

Book類別。

    :::java
    public class Book {
        private String name = "";
        public Book(String name) {
            this.name = name;
        }
        public String getName() {
            return name;
        }
    }

BookShelf類別就是一個聚合(放書)的實體，實作Aggregate Interface。

    :::java
    public class BookShelf implements Aggregate {
        private Book[] books;
        private int last = 0;
        public BookShelf(int maxsize) {
            this.books = new Book[maxsize];
        }
        public Book getBookAt(int index) {
            return books[index];
        }
        public void appendBook(Book book) {
            this.books[last] = book;
            last++;
        }
        public int getLength() {
            return last;
        }
        public Iterator iterator() {
            return new BookShelfIterator(this);
        }
    }

BookShelfIterator實作Iterator Interface。

    :::java
    public class BookShelfIterator implements Iterator {
        private BookShelf bookShelf;
        private int index;
        public BookShelfIterator(BookShelf bookShelf) {
            this.bookShelf = bookShelf;
            this.index = 0;
        }
        public boolean hasNext() {
            if (index < bookShelf.getLength()) {
                return true;
            } else {
                return false;
            }
        }
        public Object next() {
            Book book = bookShelf.getBookAt(index);
            index++;
            return book;
        }
    }

Main類別，完成整個程式。

    :::Java
    public class Main {
        public static void main(String[] args) {
            BookShelf bookShelf = new BookShelf(4);
            bookShelf.appendBook(new Book("Around the World in 80 Days"));
            bookShelf.appendBook(new Book("Bible"));
            bookShelf.appendBook(new Book("Cinderella"));
            bookShelf.appendBook(new Book("Daddy-Long-Legs"));
            //我們只有用到Iterator的方法，實際上BookShelf內部怎麼實作的我們不管。
            //如果今天BookShelf把陣列改成vector，下面的程式碼還是不會變動。
            Iterator it = bookShelf.iterator();
            while (it.hasNext()) {
                Book book = (Book)it.next();
                System.out.println("" + book.getName());
            }
        }
    }

要多加利用Abstract class以及Interface來設計程式。

####Iterator 參與者
決定依序掃描元素的介面。它決定取得是否有下一個元素的相關資訊的 **hasNext** 方法，以及取得下一個元素的 **next** 方法。例如 Iterator 介面。
####ConcreteIterator 參與者
實際上實作 Iterator 所決定的介面，例如 BookShelfIterator 類別。必須掌握掃描時的必要資訊，例如 BookShelf 類別件個體儲存 bookShelf 欄位，目前該書則儲存在 index 欄位。
####Aggregate 參與者
決定建立 Iterator 的介面。這裡的介面是指建立**能依序掃描出現在持有元素的人**的方法。例如 Aggregate 介面，它決定了 Iterator 方法。
####ConcreteAggregate 參與者
實際上實作 Aggregate 所決定的介面，它是建立實際的 Iterator 參與者，也就是 ConcreteIterator 的物件個體。例如 BookShelf 類別，它實作了 Iterator 方法。

###優點
####無論實作結果如何，都能使用 Iterator
利用 Iterator 可以跟實作分開，單獨進行遞增。請看以下的程式碼。

    :::java
    while(it.hasNext()){
        Book book = (Book)it.next();
        System.out.println(""+book.getName());
    }

這裡指使用到 hasNext 和 next 這兩個 Iterator 的方法，並沒有使用到 BookShelf 實作時所使用的方法。換句話說，這裡的**while 迴圈不會受到 BookShelf 實作的影響**。

假設原先有實作了 BookShelf，但現在不想再利用陣列管裡書籍，打算把程式修改成能使用 java.util.Vector。無論 BookShelf 修改成怎樣，BookShelf 仍然還有 iterator 方法，只要能回傳正確的 Iterator(即有傳回正常實作 hasNext 及 next 方法的類別的物件個體)，**上面的　while 迴圈即使一字不改也能正常運作**。

從這個角度來看，就可以了解為什麼在 Main 類別中我們把　iterator 方法的回傳值指定給  Iterator 型態變數，而不是 BookShelfIterator　型態變數。因為我們不是利用 BookShelfIterator 的方法來寫程式，而只是打算利用 Iterator 的方法來寫程式而已。

####一個以上的 Iterator
**把遞增的架構放在 Aggregate 之外**是 Iterator Pattern 的特徵之一。利用這個特點可以對一個 ConcreteAggregate 建立出一個以上的 ConcreteIterator。

###習慣抽象類別及介面
如果對如何使用抽象類別和介面還不太清楚的話，很容易一腳栽進去用 ConcreteAggregate 或　ConcreteIterator　來寫程式的壞習慣，就再也脫不了身回來用 Aggregate 介面或　Iterator 介面。因為只要用具體類別就能解決所有問題的感覺會讓人不知不覺上癮。

為了提高再利用性，因此必須引進抽象類別和介面的觀念。

### Aggregate 與　Iterator 的對應
BookShelfIterator 非常了解 BookShelf 整個實作過程，也因為它了解實作，所以才能呼叫用來取得**下一本書**的方法　getBookAt。

由於如果 BookShelf 的實作整個被改變，而且連 getBookAt 方法這個介面也有變動的話，就必須修改 BookShelfIterator。

###問題
####在 BookShelf 類別中，若書籍數量超過最先設定的書架大小，就無法繼續把書放上去。請利用 java.util.Vector 取代陣列，把程式改成即使已經超過書架容量也能繼續新增書籍。

如下。不需要修改 Main 的 while 迴圈。

    :::java
    import java.util.Vector;

    public class BookShelf implements Aggregate {
        private Vector books;   
        public BookShelf(int initialsize) {         
            this.books = new Vector(initialsize);   
        }
        public Book getBookAt(int index) {
            return (Book)books.get(index);
        }
        public void appendBook(Book book) {
            books.add(book);
        }
        public int getLength() {
            return books.size();                    
        }
        public Iterator iterator() {
            return new BookShelfIterator(this);
        }
    }
