Title:用macro的技巧
Slug: macro
Category: C/C++
Author: twmht

關於macro的介紹，有一個還不錯的[網站](http://www.cprogramming.com/tutorial/cpreprocessor.html)。

在debug的時候很常用printf來debug，並且會註明這是哪一個變數名稱，用macro可以很容易作到。

    :::C
    #define print_var(var)  printf("%s: %s\n", #var, var)
    //也可以這樣
    #define PRINT_TOKEN(token) printf(#token " is %d", token)
    char s[] = "aaa";
    //s: aaa
    print_var(s);
    int a = 5;
    //a is 5
    PRINT_TOKEN(a);

如果想要一次印出多個變數，可以這樣做。

    :::C
    #define print_var(var)     do {         printf("%s: %s\n", #var, var);     } while (0)
    #define print_three_var(var) do { \
             print_var(var); \
             print_var(var##2); \
             print_var(var##3); \
         } while (0)
    int s = 10;
    int s2 = 20;
    int s3 = 30;
    print_three_var(s);
    //印出s: 10
    //    s2: 20
    //    s3 :30

也可以印出struct裡面的變數。

    :::C
    #define BUILD_FIELD(field) my_struct.inner_struct.union_a.##field
    //會被展開成
    my_struct.inner_struct.union_a.field1

使用macro會有一些陷阱

    :::C
    #define MULT(x, y) x * y
    #define ADD_FIVE(a) (a) + 5
    MULT(1+1,2+2); //會被展開成1+1*2+2，結果不對。
    ADD_FIVE(3)*3 //會被展開成(3)+5*3，結果不對。

上述的結果有誤，可以改成

    :::C
    #define MULT(x,y) (x)*(y)
    #define ADD_FIVE(a) ((a) + 5)
    MULT(1+1,2+2); //會被展開成(1+1)*(2+2)，結果正確。
    ADD_FIVE(3)*3 //會被展開成((3)+5)*3，結果正確。

經驗法則是最好每個element都把它包起來。

一個SWAP的trick。

    :::C
    //可以試著驗證看看
    #define SWAP(a, b)  do {a ^= b; b ^= a; a ^= b; } while(0)//最好把它包起來，不然的話會很容易不小心把後兩句給排除掉。加上do while是為了有分號。
    if (a>0)
        SWAP(a,b);
    else
        SWAP(a,b);

注意不要搭配side-effect服用，像這樣。

    :::C
    #define MAX(a, b) ((a) < (b) ? (b) : (a))
    int x = 5, y = 10;
    //因為macro是直接展開，並不是x++,y++做完之後才展開。
    int z = MAX(x++, y++);
    //所以會變成int z = (x++ < y++ ? y++ : x++)

如果不想寫多行的話要怎麼做?

    :::C
    //用一個slash表示接到下一行
    #define SWAP(a, b)  {                   \
                        a ^= b;         \
                        b ^= a;         \ 
                        a ^= b;         \
                    } 

