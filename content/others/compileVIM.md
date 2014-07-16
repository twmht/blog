Title: 手動 compile vim
Tags: vim
Slug: compileVIM
Category: Others
Author: twmht

[參考](https://github.com/Valloric/YouCompleteMe/wiki/Building-Vim-from-source)下載到字型。

先安裝以下這些 dependency。

    :::bash
    sudo apt-get install libncurses5-dev libgnome2-dev libgnomeui-dev \
    libgtk2.0-dev libatk1.0-dev libbonoboui2-dev \
    libcairo2-dev libx11-dev libxpm-dev libxt-dev python-dev ruby-dev mercurial

移除系統的 vim。

    :::bash
    sudo apt-get purge vim vim-runtime gvim vim-tiny vim-common vim-gui-common

如果系統有安裝 <code>pythonbrew</code>，建議先把它關掉，同時把相關的 <code>.bashrc</code>的設定註解掉。

在下<code>./configure</code>時，會讀取 cache，其中的 <code>python path</code> 一定要是系統目錄的，這樣編譯才會正常。通常如果有裝<code>pythonbrew</code>的話，都會出現問題。因此最好編譯之前把 <code>src/auto/config.cache</code> 移除掉，讓系統讀到最新的 path。

    :::bash
    ./configure --with-features=huge \
                --enable-multibyte \
                --enable-rubyinterp \
                --enable-pythoninterp \
                --with-python-config-dir=$(/usr/bin/python2.7-config --configdir) \
                --enable-perlinterp \
                --enable-luainterp \
                --enable-gui=gtk2 --enable-cscope --prefix=/usr


產生 makefile 之後，開始編譯。

    :::bash
    make VIMRUNTIMEDIR=/usr/share/vim/vim74

最後下 checkinstall。

    :::bash
    sudo checkinstall

最好讓系統不要自動更新 vim。

    :::bash
    sudo aptitude hold vim
