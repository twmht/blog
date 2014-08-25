Title: clone submodule
Slug: gitCloneSubmodules
Category: Others
Author: twmht

連同 project 一同 clone 下來：

    :::bash
    git clone --recursive git://github.com/foo/bar.git

假設 project 已經存在:

    :::bash
    git submodule update --init --recursive


