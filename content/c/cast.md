Title:C++中的幾種cast
Slug: cast
Category: C/C++
Author: twmht

* static_cast

比較不安全。例如把子類別指標轉成父類別指標，這是可以的。但是把父類別指標轉成子類別指標，會很危險。

*dynamic_cast

有回傳值，透過檢查回傳值的方式來提高安全性。
