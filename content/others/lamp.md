Title: 如何在ubuntu中安裝LAMP
Slug: lamp
Category: Others
Author: twmht

    :::bash
    #install apache
    sudo apt-get install apache2

    #install php
    sudo apt-get install libapache2-mod-php5 php5
    sudo /etc/init.d/apache2 restart
    #install mysql
    sudo apt-get install mysql-server libapache2-mod-auth-mysql php5-mysql
    #test mysql
    mysql -u root -p
    #install phpmyadmin(not necessary)
    #一開始會問你要不要自動幫你設定phpmyadmin，選擇yes。之後會問你mysql server中root的密碼。
    #最後會問你進入phpmyadmin的密碼。
    sudo apt-get install phpmyadmin

如果 `http://localhost/phpmyadmin` 不能開的話，可以這樣做。

    :::bash
    #打開/etc/apache2/apache2.conf，在最後面加上以下的code
    Include /etc/phpmyadmin/apache.conf
    #或者也可以用下面這個方法
    sudo ln -s /usr/share/phpmyadmin /var/www

###Enable userdir Apache module###

    :::bash
    sudo a2enmod userdir
    vim /etc/apache2/mods-enabled/userdir.conf
    #找到下面這段，改成這樣。
    <IfModule mod_userdir.c>
            UserDir public_html
            UserDir disabled root
     
            <Directory /home/*/public_html>
            AllowOverride All
            Options MultiViews Indexes SymLinksIfOwnerMatch
            <Limit GET POST OPTIONS>
                    Order allow,deny
                    Allow from all
            </Limit>
            <LimitExcept GET POST OPTIONS>
                    Order deny,allow
                    Deny from all
            </LimitExcept>
            </Directory>
    </IfModule>

接著修改php的設定。

    vim /etc/apache2/mods-available/php5.conf
    #找到下面這段，改成這樣
    <IfModule mod_php5.c>
        <FilesMatch "\.ph(p3?|tml)$">
        SetHandler application/x-httpd-php
        </FilesMatch>
        <FilesMatch "\.phps$">
        SetHandler application/x-httpd-php-source
        </FilesMatch>
        # To re-enable php in user directories comment the following lines
        # (from <IfModule ...> to </IfModule>.) Do NOT set it to On as it
        # prevents .htaccess files from disabling it.
        #<IfModule mod_userdir.c>
        #    <Directory /home/*/public_html>
        #        php_admin_value engine Off
        #    </Directory>
        #</IfModule>
    </IfModule>

最後別忘記重新啟動apache。

    :::bash
    service apache2 restart
    #之後就可以在家目錄建立public_html
    mkdir /home/$USER/public_html
