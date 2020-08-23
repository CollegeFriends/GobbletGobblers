import sys
import os 
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from PyGobbletGobblers import GobbletGobblers as Game

import random

class randomBot():
    def __init__(self,Game,side):
        self.game = Game
        self.side = side
    
    def showPieces(self):
        print("side : {}\t{}".format(self.side,self.game.getPieces(self.side)))
    
    def act(self):
        # コマを置けるか確認
        pieces = self.game.getPieces(self.side)
        
        ownPos = []
        for i,owner in enumerate(self.game.getOwnersList()):
            if owner == self.side:
                ownPos.append(i)

        if len(pieces) > 0 and len(ownPos) > 0:
            # 動かすことも置くこともできる = 2択で決める            
            s = random.randint(0,1)            

            if s == 0:
                self.randomPut()
            else:
                self.randomMove()


        if len(pieces) == 0:
            # 手駒がない＝コマを動かすことしかできない            
            self.randomMove()

        elif len(ownPos) == 0:
            # 所持しているマスがない＝コマを置くことしかできない
            self.randomPut()
            
     
        
    def randomPut(self):
        # 手駒リストを取得
        pieces = self.game.getPieces(self.side)

        # 各手駒がおける場所を探す            
        pos_list = []
        for piece in pieces:
            pos_tmp = []            
            for i in range(9):
                if self.game.chk_pos(piece,i):
                    pos_tmp.append(i)
            pos_list.append(pos_tmp)

        # 置ける場所がない手駒は手駒リストから消す
        tmp = []
        for i in range(len(pieces)):
            if len(pos_list[i]) == 0:
                tmp.append(i)        
        tmp_pieces = []
        tmp_pos_list = []
        for i in range(len(pieces)):
            if i not in tmp:
                tmp_pieces.append(pieces[i])
                tmp_pos_list.append(pos_list[i])
        
        pieces = tmp_pieces
        pos_list = tmp_pos_list
        
        # 置ける手駒がないときは、randomMoveを実施
        if len(pieces) == 0:                    
            return self.randomMove()

        # ランダムに手駒を選ぶ                  
        i = random.randint(0,len(pieces)-1)  
        p = pieces[i]

        # 選んだ手駒の置ける場所一覧から、ランダムに場所を決める
        pos = pos_list[i][random.randint(0,len(pos_list[i])-1)]

        # 選んだ手駒を選んだ場所に置く
        result = self.game.putPiece(self.side,p,pos)       
        if not result:
            raise Exception("randomPutでエラーが発生")
    
    def randomMove(self):
        # 盤面上のコマで動かせる位置を取得
        fromPos_list = []
        for i,owner in enumerate(self.game.getOwnersList()):
            if owner == self.side:
                fromPos_list.append(i)
        
        # fromPos_listの各マスで動かせるコマの大きさを取得する
        fromPosSize_list = []
        for fromPos in fromPos_list:
            fromPosSize_list.append(self.game.getPieceSize(fromPos))

        # 各fromPos_listの位置のコマを動かせる先を取得する
        toPos_list = []
        for i in range(len(fromPos_list)):
            toPos_tmp = []
            for j in range(9):
                if j == fromPos_list[i]:
                    continue
                if self.game.chk_pos(fromPosSize_list[i],j):
                    toPos_tmp.append(j)
            toPos_list.append(toPos_tmp)
        
        # 動かせる先のないコマを選択肢から消す
        tmp = []
        for i in range(len(fromPos_list)):
            if len(toPos_list[i]) == 0:
                tmp.append(i)

        tmp_fromPos_list = []
        tmp_toPos_list = []
        for i in range(len(fromPos_list)):
            if i not in tmp:
                tmp_fromPos_list.append(fromPos_list[i])
                tmp_toPos_list.append(toPos_list[i])
        
        fromPos_list = tmp_fromPos_list
        toPos_list = tmp_toPos_list

        # 動かせるコマがないときは、randomPutを実施
        if len(fromPos_list) == 0:
            return self.randomPut()

        # 動かすコマを選ぶ
        i = random.randint(0,len(fromPos_list)-1)
        fromPos = fromPos_list[i]

        # 動かす先を選ぶ
        toPos = toPos_list[i][random.randint(0,len(toPos_list[i])-1)]

        result = self.game.movePiece(self.side,fromPos,toPos)
        if not result:
            raise Exception("randomMoveでエラーが発生")
    
