Title: Interpreter Pattern -- 以類別來表達文法規則
Slug: interpreter
Category: Design Pattern
Author: twmht

###用的時間點
Design Pattern 的目的之一就是要提高類別的可再用性。 可再用性是指已經產生的類別不需要多做修改或是儘量不修改就能多次使用的意思。

Interpreter Pattern 是用簡單的"迷你語言"來表現程式要解決的問題，以迷你語言寫成"迷你程式"而表現具體的問題。迷你程式本身無法獨自啟動，必須先用Java語言寫另一個負責翻譯的程式(直譯器)。當能解決的問題發生變化時，要修改迷你程式來對應處理，而不是修改直譯器(儘量避免去修改)。

###如何設計
當問題發生改變時，儘可能不去修改到直譯器（以Java寫成）。

###程式範例
首先來定義我們的問題，我們要用迷你語言來操控玩具車。玩具車基本動作有 go, right, left　以及 repeat。go 表示前進，right 表示向右轉，left 表示向左轉，repeat 像是一個迴圈，後面接上若干個命令。
以下是幾個範例：

1. program go right right go end
2. program repeat 4 go right end end # repeat 結尾要加上 end，就像右大括號一樣

定義 BNF 如下：

1. &#60;program&#62; ::= program &#60;command list&#62;
2. &#60;command list&#62; ::=  &#60;command&#62;* end
3. &#60;command&#62; ::= &#60;repeat command&#62; | &#60;primitive command&#62;
4. &#60;repeat command&#62; ::= repeat &#60;number&#62; &#60;command list&#62;
5. &#60;primitive command&#62; ::= go | right | left

根據每一條語法設計一個類別，語法看到哪裡，類別就設計到哪裡。要注意的是，<b>到這個方法時，記號要讀取到哪裡 ; 離開這個方法時，記號又該讀取到哪裡</b>。

<script src="https://gist.github.com/twmht/72c8581377623688e342.js"></script>

如果有出現 [..] 包起來的內容，表示 interpreter 確實有解讀到該行程式。

### Interpreter Pattern 的所有參與者
#### AbstractExpression 參與者
規定樹狀剖析之節點的共用介面。例如 Node 類別，定義了 parse 方法。
#### TerminalExpression 參與者
表示不能被展開的節點，例如 PrimitiveCommandNode 類別。
#### NonterminalExpression 參與者
可以被展開的節點，例如 ProgramNode、CommandNode、RepeatCommandNode、CommandListNode 等類別。
####Context 參與者
提供 interpreter 進行文法解析時所需要的資訊的參與者，例如 Context 類別。
####Client 參與者
呼叫 TerminalExpression 以及 NonterminalExpression，以建立樹狀剖析的參與者。例如 Main 類別。

###問題
####請修改範例程式，讓它能夠執行所收到的內容，例如，可以寫出 GUI 來執行。

這裡是把跟 GUI 有關的部份放在 turtle package 中，讓 language package 裡面沒有 GUI。只要建立一個能在其他 package 裡執行 Executor 和 ExecutorFactory 介面的類別，不必修改 language package 就能另外建立一個可以<b>執行</b>相同程式的新程式。
<script src="https://gist.github.com/twmht/e0e92d0edf9dbe73aa4b.js"></script>
