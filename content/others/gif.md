Title: 如何在ubuntu中製作gif檔
Slug: gif
Category: Others
Author: twmht
在ubuntu上面製作gif檔的話，可以安裝[ImageMagick](http://www.imagemagick.org/script/index.php)

假設把所有的image file放到gif資料夾中，注意檔名最好排序過，例如001.png, 002.png, and 003.png...

    :::bash
    #delay的值*10ms為delay的秒數，loop為0表示infinite loop
    convert -delay 100 -loop 0 gif/* output.gif
