Title: Merge 多個 commit 成為一個 commit
Slug: gitRebase
Category: Others
Author: twmht

[參考](http://stackoverflow.com/questions/2563632/how-can-i-merge-two-commits-into-one)

假設有兩個 commit (順序分別是先 a 後 b )要合併在一起

    :::bash
    git rebase -i


此時把最新的 commit (也就是b) 標記為 s(squash)，然後存檔，接著會跳出 commit message 讓你修改，此時只保留一個 changeID 即可。
