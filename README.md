# 環境構築

Anacondaを使用して、下記の環境で実施    
（ipykernelは挙動を試すために使用した)  
```
conda create -n GobbletGobblers python=3.8.5 
conda install ipykernel                         # Jupyter
````

適当なフォルダ下でターミナルで書きコマンドを実行することで、ダウンロードできる  
```
git clone git@github.com:CollegeFriends/GobbletGobblers.git
```

# PyGobbletGobblers.py
このゲームのメインクラス
ルール等を反映したものである

下記のようにimportして使用することを想定している

```python
from PyGobbletGobblers import PyGobbletGobblers as Game
```

# ルール
基本的には 3x3(9マス) で行う三目並べ (Tic Tac Toe)と同じ。
ただし、コマは大中小の3種類を2つずつ保持する。

1. 3列並べたら勝ち
2. 手番は交互
**3. プレイヤーは毎ターン必ず「コマを盤面に置く」「盤面上の自分のコマを動かす」のいずれかをする**

# main.py

python main.pyで実行すると、ゲームを遊べる。  
コマンドラインで動作コマンドを数値で入力することで、遊べる。  
ただし、先手・後手のいずれも手動で動かす。


## 変数の説明

side : 先手と後手.....先手 = 0 | 後手 = 1

size : コマの大きさ...大 = 2 | 中 = 1 | 小 = 0

pos  : 盤面上の位置...上段は左から0,1,2...の順

## 関数

### ゲームの開始
game = Game()      

### putPiece()

手番(=side)のコマ(大きさ=size)をposの位置に置く関数  

例] game.putPiece(side=0,size=2,pos=1)


戻り値はその操作が可能かどうか (True/False)  

例えば、side=2とした場合や中コマ(size=1)がおいてある位置へ小コマ(size=0)を置こうとすると、

盤面を変化させず、Falseを返す


### movePiece()

手番(side)が位置(fromPos)のコマにおいてあるコマで、最も大きなコマを位置(toPos)へと移動させる

例] game.movePiece(side=0,fromPos=0,toPos=8)

戻り値はその操作が可能かどうか (True/False)  

例えば、side=2とした場合や自分のコマがおいてないマスからの移動をさせようとすると、

盤面を変化させず、Falseを返す

### getField()

盤面の状態を示した配列を返す

例えば、盤面の中央のマス(4のマス)は、

```
state = game.getField()
print(state[4])
```

で表示できる。

各状態は6bitの数値であり、上位ビットから、先手の大,中,小,後手の大,中,小のコマがおいてあるかどうかを示している。


例] 先手の大、小と後手の中が重ねておいてあるマス :　0b101010 = 42       


    先手の中と後手の小が重ねておいてあるマス     :　0b010001 = 17

### getOwner()

指定したマスで一番大きなコマを持っている手番を返す

戻り値は、0：先手　1:後手　-1:先手も後手もコマを置いていない　のいずれかである

### isEnd()

現在の盤面で、終了している（どちらかの手番が勝っている）かどうかを返す。

戻り値はTrue/Falseの２パターン

### getWinner()

試合に勝った手番を返す

戻り値は　0:先手 / 1:後手　/ None:まだ試合が終わっていない　の3パターン

### render()

盤面を表示する

引数を指定することで、下記の3通りの表示が可能  
引数なし        : 各マスの状態を数値で表示  
mode='raw'      : 各マスの状態を6bitの値で表示  
mode='owner'    : 各マスの所有者（最大のコマをおいている手番）を表示　※どちらもコマをおいてないマスは空欄になる

### getPieces()

引数で指定したsideの手駒（盤面上に置いていないコマ）の一覧を取得する

```python
print(game.getPices(0))
> [0,0,1,1,2,2]
```