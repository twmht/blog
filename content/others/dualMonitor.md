Title: Lubuntu 底下設定雙螢幕
Slug: dual_monitor
Category: Others
Author: twmht

以下是 lubuntu 的設定方式。

如果想進入桌面之後就執行，必須要去修改<code>.config/lxsession/Lubuntu/autostart</code>。

加入

    :::bash
    @xrandr --auto --output VGA-1 --right-of DVI-I-1

接著會在<code>.config/autostart/lxrandr-autostart.desktop</code>看到相關設定。
