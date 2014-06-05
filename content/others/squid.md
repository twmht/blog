Title: 利用 squid 及 pam module 建立 proxy server
Slug: squid_proxy
Category: Others
Author: twmht

以下是 squid3 的設定方式

1. 首先修改 <b>/etc/squid3/squid.conf</b>，找到下面這幾行，把註解取消掉，有些則是要自行加入。

在 auth_param section 中:

    :::bash
    auth_param basic program /usr/lib/squid/pam_auth
    auth_param basic children 5
    auth_param basic realm Squid proxy-caching web server
    auth_param basic credentialsttl 2 hours

在 acl section 中：

    :::bash
    acl pam proxy_auth REQUIRED
    acl password proxy_auth REQUIRED

在 http_access 中：

    :::bash
    http_access allow pam


2. 接下來修改 <b>/etc/pam.d/squid</b>，加入以下這兩行。

    :::bash
    #先找出 pam_unix.so 的路徑
    #updatedb && locate pam_unix.so
    auth required path_to_pam_unix.so
    account required path_to_pam_unix.so

3. 重新啟動 squid

    :::bash
    service squid restart

4. 若驗證有問題，則可能是權限問題。

    :::bash
    sudo chmod u+s /usr/lib/squid3/pam_auth
