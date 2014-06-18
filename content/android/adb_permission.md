Title: adb devices 顯示 no permissions
Slug: adb_permission
Tags: adb, android
Category: android
Author: twmht

解決方法如下，這使得任何使用 adb 的使用者都是以 root 的權限來使用：

    :::bash
    sudo chown root:root adb
    sudo chmod a+x adb
    sudo chmod a+s adb
    adb kill-server
    adb start-server
