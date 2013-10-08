Title: 解決ubuntu上面麥克風沒聲音的問題
Slug: skypemic
Category: Others
Author: twmht
在ubuntu上面使用skype的話，有時候會發生麥克風沒有聲音的問題。
這時候可以使用

    :::bash
    alsamixer
或者是

    :::bash
    gnome-alsamixer
來調整麥克風的聲音。
如果再不行的話，就使用

    :::bash
    gstreamer-properties
調整input或者是output。
