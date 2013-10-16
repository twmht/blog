Title: 如何在ubuntu中加入新的字型
Slug: addFont
Category: Others
Author: twmht
在ubuntu上面使用字型的話，有三種方式，假設現在要安裝myfont.ttf。

* 使用gnome-font-viewer 

        :::bash
        sudo gnome-font-viewer myfont.ttf

* 直接在myfont.ttf上面點兩下直接安裝。

* 適合一次安裝大量字型檔

        :::bash
        cd /usr/local/share/fonts/truetype
        sudo mkdir myfonts && cd myfonts
        cp /path/to/fonts/*.ttf ./
        sudo chown root *.ttf #可能不需要
        fc-cache

可以在[這邊]( http://www.exljbris.com/fontin.html)下載到字型。
