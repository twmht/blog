Title: 如何備份mysql database
Slug: backupmysql
Category: Others
Author: twmht

有時候換環境的時候，會想要連同資料庫一起移動過去，假設要備份一個database叫做library。

    :::bash
    mysqldump -u root -p --databases library > library.sql

到新的環境中如何重新載入library.sql呢？
    
    :::bash
    mysql -u root -p < library.sql
