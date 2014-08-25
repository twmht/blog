Title: 快速更換 java 的預設路徑
Tags: java
Slug: multipleJava
Category: Others
Author: twmht

在安裝多個版本的 java 的情況下，如果想要快速切換系統預設的版本的話，可以這樣做。

    :::java
    sudo update-alternatives --config java
    sudo update-alternatives --config javac

這樣會建立一個 <code>/etc/alternatives/java(javac)</code> 的 symbolic link。
