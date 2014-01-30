Title: Interpreter Pattern
Slug: interpreter
Category: Design Pattern
Author: twmht

###用的時間點
Design Pattern 的目的之一就是要提高類別的可再用性。 可再用性是指已經產生的類別不需要多做修改或是儘量不修改就能多次使用的意思。

Interpreter Pattern 是用簡單的"迷你語言"來表現程式要解決的問題，以迷你語言寫成"迷你程式"而表現具體的問題。迷你程式本身無法獨自啟動，必須先用Java語言寫另一個負責翻譯的程式(直譯器)。當能解決的問題發生變化時，要修改迷你程式來對應處理，而不是修改直譯器(儘量避免去修改)。

###如何設計
當問題發生改變時，儘可能不去修改到直譯器（以Java寫成）。

###程式範例
首先來定義我們的問題，我們要用迷你語言來操控玩具車。玩具車基本動作有 go, right, left　以及 repeat。
