Title: C++的Class中的一些重點整理
Slug: class
Category: C/C++
Author: twmht

<font color=red> class與struct有很明顯的的差別是，class可以定義member function，但struct不行。另外，class預設的member權限是private，而struct預設則是public。 </font>

以下是我看螞蟻書的重點整理。另外，也有參考[這篇](https://www.google.com.tw/url?sa=t&rct=j&q=&esrc=s&source=web&cd=2&ved=0CD0QFjAB&url=http%3A%2F%2Fdisp.ee.ntu.edu.tw%2Fclass%2FC%2B%2B%25E7%2589%25A9%25E4%25BB%25B6%25E5%25B0%258E%25E5%2590%2591%25E5%258F%258A%25E5%25A2%259E%25E9%2580%25B2%25E6%2595%2588%25E7%258E%2587%25E7%25A8%258B%25E5%25BC%258F%25E6%258A%2580%25E5%25B7%25A7&ei=VgtpUujrMIGHlAXL4YHQDg&usg=AFQjCNE6jeVtMAQtoRa7e1_ycplTZ6Vmtw&sig2=lqmcR3rmQmWj79H-W_q8DQ)。

* friend function:
簡單來說就是你在class裡面定義了一個friend function，這個function是在class的外面，同時這個function可以修改private data。
* const function:
在function後面如果加了const的話，就表示它不會修改任何的menber data，所以，const object不能夠呼叫non const function。

以下講權限範圍，如果沒有定義的話，則預設表示private。其實跟java很類似，差別在於java沒有friend class，而且java的預設權限是package scope。

* private: 只有自己或者是friend class看得到。
* protected: 只有自己，friend class或者子類別才可以看得到。
* public: 任何可以看到這個class的地方都可以使用。

建構子跟解構子也很重要，以前不太清楚解構子可以幹嘛，只知道物件被回收的時候解構子會自動被呼叫。
以下這個例子我覺得很好，應該是說當物件內部有動態配置的時候，可以一起把動態配置的記憶體回收掉，我想應該是這個物件被回收的的時候，不會一起把內部動態配置的member data一起free掉的原因，可以看[這裡](http://stackoverflow.com/questions/11288358/does-dynamically-allocated-memory-for-data-members-of-a-c-class-frees-when-cla)。

    :::cpp-objdump
    // example on constructors and destructors rect area: 12
    #include <iostream.h> rectb area: 30
    class CRectangle {
    int *width, *height;
    public:
    //overloading
    CRectangle ();
    CRectangle (int,int);
    ~CRectangle ();
    //實作內容定義在class以內的有機會被編譯器視為inline function，編譯器會自己作判斷
    //inline function會直接將程式碼展開來，與macro非常類似
    //程式碼很短，只有return statement，用inline較有效率
    int area (void) {return (*width * *height);}
    };
    CRectangle::CRectangle () {
    width = new int;
    height = new int;
    *width = 5;
    *height = 6;
    }
    CRectangle::CRectangle (int a, int b) {
    width = new int;
    height = new int;
    *width = a;
    *height = b;
    }
    CRectangle::~CRectangle () {
    delete width;
    delete height;
    }
    int main () {
    //若不傳參數，則不需要括弧，java則需要
    CRectangle rect (3,4), rectb (5,6),rectc;
    cout << "rect area: " << rect.area() << endl;
    cout << "rectb area: " << rectb.area() << endl;
    return 0;
    }

實際上,當我們定義一個 class 而沒有定義建構子的時候,編譯器會自動假設兩
個重載的建構子 (預設建構子"default constructor" 和複製建構子"copy
constructor")，又與java類似，只是在java中我沒聽過copy constructor。

    :::cpp-objdump
    class CExample {
    public:
    //沒有定義建構子
    int a,b,c;
    void multiply (int n, int m) { a=n; b=m; c=a*b; };
    };

因此defalut constructor以及copy constructor會被自動定義，copy constructor是一個只有一個參數的建構子,該參數是這個 class 的一個物件,這個函數的功能是將被傳入的物件(object)的所有<font color=red>非靜態</font> (non-static)成員變數的值都複製給自身這個 object。

    :::cpp-objdump
    //default constructor
    CExample::CExample () { };
    //copy constructor
    //一定要pass by reference，否則會導致遞迴呼叫copy constructor而形成無窮迴圈。
    //若是有用到指標，則copy constructor預設只會複製指標的address，所以一定要視情況改寫
    CExample::CExample (const CExample& rv) {
    a=rv.a;
    b=rv.b;
    c=rv.c;
    }

為什麼copy constructor一定要pass by reference?，這個問題我大一的時候有想過，去問了ptt的版友之後終於恍然大悟。
問題點出在<font color=red>pass by value</font>的時候並不是直接用等號來作assignment，而是會先呼叫copy constructor。

假設有一個function foo長這樣

    :::cpp-objdump
    //pass by reference
    foo(Bar bar)

當有人要呼叫foo()

    :::cpp-objdump
    Bar mybar;
    foo(mybar)

進入 foo 之前, 因為是 pass by value, 所以要生成一個 myBar 的 copy. 要怎樣生成呢? compiler 會利用 copy constructor 生成一個 myBar 的複製品, 然後供 foo() 裡面使用。

要是Bar這個class的copy constructor 是 pass-by-value 的話, 比如

    :::cpp-objdump
    Bar myBar;
    Bar barCopy(myBar);

生成 barCopy 的時候, 因為 myBar 是 pass by value, 所以 compiler
要生成一個 myBar 的複製品 (假設叫 tmpBarA) 才傳進去生成 barCopy.

但生成 tmpBarA, 也是利用 copy ctor, 即是 compiler 是在做
Bar tmpBarA(myBar);
由於是 pass-by-val, 那麼要生成 tmpBarA, 其實傳進去的是 myBar 的一個
複製品 (tmpBarB).

要生成 tmpBarB......(遞迴呼叫，無窮迴圈)，<font color=red>而如果是copy by reference，則不會呼叫copy constructor。</font>
