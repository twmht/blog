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
