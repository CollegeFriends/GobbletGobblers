from READ_ONLY.PyGobbletGobblers import GobbletGobblers as Game

import numpy as np
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
            print(self.side,p,pos)
            print("{:06b}".format(self.game.getField()[pos]))
            raise Exception("randomMoveでエラーが発生")
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
            print(self.side,fromPos,toPos)
            print("{:06b} {:06b}".format(self.game.getField()[fromPos],self.game.getField()[toPos]))
            raise Exception("randomMoveでエラーが発生")

class Agent():
    def __init__(self,game,side):
        self.env = game
        self.side = side

    # ある手を選択した場合のその後の結果の予想を返す(simulationをする)
    def predict_act(self,action_no):
        playground = self.env.copy()

        if action_no < 3*9:
            size = int(action_no / 3)
            pos = action_no % 9
            res = playground.putPiece(self.side,size,pos)
        elif action_no < 3*9+9*9:
            tmp = action_no - 3*9
            fromPos = int(tmp / 9)
            toPos = tmp%9
            res = playground.movePiece(self.side,fromPos,toPos)        

        return playground.getField(), res

if __name__ == '__main__':
    
    NUM_EPISODES = 10000

    for i in range(NUM_EPISODES):
        env = Game()        
        agent = randomBot(env,side=0)
        enemy_lv0 = randomBot(env,side=1)        
        while not env.isEnd():  

            # 有効な手を打てるまでその場で学習
            res = False    
            # while not res:
            #     action = random.randint(0,3*9+9*9-1)

            #     if action < 3*9:
            #         # 置くパターン
            #         size = int(action/9)
            #         pos = action % 9
            #         res = env.putPiece(agent_side,size,pos)
            #     elif action < 3*9 + 9*9:
            #         # 動かすパターン
            #         tmp = action - 27
            #         fromPos = int(tmp/9)
            #         toPos = tmp % 9
            #         res = env.movePiece(agent_side,fromPos,toPos)
            #     else:
            #         raise Exception("Range Error")

            #     if res is None:
            #         res = False

            #     # 使用できないコマンドを送ると、報酬は負の値
            #     try:
            #         if res:                
            #             reward = 0
            #         else:
            #             reward = -1
            #     except:
            #         reward = -1
            #         res = False
            #     # 勝つと+１
            #     terminal = env.isEnd()
            #     if terminal:
            #         reward += 1

            agent.act()                
            # 終了判定
            if not env.isEnd():                
                # 相手の手番なので相手に打たせる
                enemy_lv0.act()            
        print(i)            


            





        
