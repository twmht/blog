Title: 轉換字幕編碼
Tags: encoding
Slug: videoEncoding
Category: Others
Author: twmht

看影片時常常外掛字幕會有問題，因此需要用<code>iconv -f source -t target filename</code> 來轉換編碼(source to target)。通常 target 會指定 <code>utf8</code> 的編碼。

但是常常會不知道 source 是什麼編碼，這時候可以下載[MadEdit](http://sourceforge.net/projects/madedit/)，打開檔案之後右下角會自動顯示檔案的編碼(source)。
