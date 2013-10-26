Title:用macro的技巧
Slug: macro
Category: C/C++
Author: twmht

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

