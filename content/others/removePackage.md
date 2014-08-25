Title: 完整移除 package
Tags: ubuntu
Slug: removePackage
Category: Others
Author: twmht

[參考](http://blog.lyhdev.com/2013/01/ubuntu-linux-apt-get.html)

在 ubuntu 中，利用 dpkg -l 可以看到套件的狀態。

總共有三個欄位。

    :::bash
    Desired=Unknown/Install/Remove/Purge/Hold                                     
    | Status=Not/Inst/Conf-files/Unpacked/halF-conf/Half-inst/trig-aWait/Trig-pend
    |/ Err?=(none)/Reinst-required (Status,Err: uppercase=bad) 

第一個欄位為 desired package state ("selection state")。

* u ... unknown
* i ... install
* r ... remove/deinstall
* p ... purge (remove including config files)
* h ... hold

第二個欄位為 current package state。

* n ... not-installed
* i ... installed
* c ... config-files (only the config files are installed)
* u ... unpacked
* f ... half-configured (configuration failed for some reason)
* h ... half-installed (installation failed for some reason)
* w ... triggers-awaited (package is waiting for a trigger from another package)
* t ... triggers-pending (package has been triggered)

第三個欄位為 error state (you normally should not see a thrid letter)。
* r ... reinst-required (package broken, reinstallation required)

一般來說用 <code>apt-get remove</code> 無法完全移除套件。

因此若出現<code>rc</code>的狀態時，表示套件沒有完全被移除掉，還保有一些設定檔。

如果想要完整移除套件的話，最好是用<code>apt-get purge</code>

當想要完整移除所有狀態為<code>rc</code>的套件時，可以這樣做。

    :::bash
    sudo apt-get purge `dpkg -l | grep ^rc | awk '{ print $2 }'`
