Title: 避免更新特定套件
Tags: ubuntu
Slug: preventUpdate
Category: Others
Author: twmht

因為自己編譯了 vim，而往後必須要避免系統自動去更新 vim，除了透過  <code>Synaptic Package Manager</code> 之外，也可以透過以下[方式](http://askubuntu.com/questions/18654/how-to-prevent-updating-of-a-specific-package)。

* using dpkg

如下，

    :::bash
    echo "vim hold" | sudo dpkg --set-selections
    echo "vim install" | sudo dpkg --set-selections
    #display the status
    dpkg --get-selections | grep "vim"

* using apt

如下，

    :::bash
    sudo apt-mark hold vim
    sudo apt-mark unhold vim

* using aptitude

如下，

    :::bash
    sudo aptitude hold vim
    sudo aptitude unhold vim

