# -*- coding: utf-8 -*-
import os, sys, unittest

class GobbletGobblers():
    def __init__(self):
        print("Common Field GAME!")
        self.__field = [0] * 9 
        self.__pieces = [[0,0,1,1,2,2],[0,0,1,1,2,2]]
        self.__winner = None        

    def getField(self):
        return self.__field.copy()

    def render(self,mode=None):
        if mode is None:
            print("----------")
            for i in range(3):
                line = "|"
                for j in range(3):
                    line += "{:2d}|".format(self.__field[i*3+j])                
                print(line)
                print("----------")            
            for i in [0,1]:                        
                print("player {} : {}".format(i,self.getPieces(i)))        
            return
        elif mode == 'row':
            print("----------------------")
            for i in range(3):
                line = "|"
                for j in range(3):
                    line += "{:06b}|".format(self.__field[i*3+j])                
                print(line)
                print("----------------------")
        
            for i in [0,1]:                        
                print("player {} : {}".format(i,self.getPieces(i)))        
            return
        elif mode == 'No':
            print("----------")
            for i in range(3):
                line = "|"
                for j in range(3):
                    line += "{:2d}|".format(i*3+j)                
                print(line)
                print("----------")            
        elif mode =='owner':
            print("----------")
            for i in range(3):
                line = "|"
                for j in range(3):
                    if self.getOwner(i*3+j) == -1:
                        line += "  |"
                    else:
                        line += "{:2d}|".format(self.getOwner(i*3+j))                
                print(line)
                print("----------")            
            for i in [0,1]:                        
                print("player {} : {}".format(i,self.getPieces(i)))    

    def getPieces(self,side):
        # 指定サイドのエラーチェック
        if side not in [0,1]:
            print("sideで[0,1]以外を指定した [{}]".format(side))
            return None       
        return self.__pieces[side]

    def putPiece(self,side,size,pos):        
        # 試合中であることの確認
        if self.__winner is not None:
            print("試合が終了しています")
            return False

        # 指定サイドのエラーチェック
        if side not in [0,1]:
            print("sideで[0,1]以外を指定した [{}]".format(side))
            return False

        # sizeの指定チェック
        if size not in [0,1,2]:
            print("sizeを[0,1,2]以外を指定した [{}]".format(size))
            return False

        # 指定位置のエラーチェック
        if pos not in range(9):
            print("posを[0〜8]以外を指定した [{}]".format(pos))
            return False    
        
        # 持ち駒に含まれているかのチェック
        if size not in self.getPieces(side):
            print("そのサイズは持ち駒にありません [side : / size : / pieces : {}]".format(side,size,self.getPieces(side)))
            return False

        # おける位置かどうかのチェック
        if not self.chk_pos(size,pos):
            print("そのサイズのコマを置けない位置です [size: {} / pos {}]".format(size,pos))            
            return False

        # サイズを6bitへ変換
        tmp = self.size2state(side,size)

        self.__field[pos] += tmp            # 場に追加
        self.__pieces[side].remove(size)    # 持ち駒から削除
        self.judge()
        return True

    def movePiece(self,side,fromPos,toPos):        
        # 試合中であることの確認
        if self.__winner is not None:
            print("試合が終了しています")
            return False
            
        # 指定サイドのエラーチェック
        if side not in [0,1]:
            print("sideで[0,1]以外を指定した [{}]".format(side))
            return False

        # 指定位置のエラーチェック
        if fromPos not in range(9):
            print("fromPos[0〜8]以外を指定した [{}]".format(fromPos))
            return False    
        if toPos not in range(9):
            print("toPos[0〜8]以外を指定した [{}]".format(toPos))
            return False    
        if fromPos == toPos:
            print("同じ位置への移動を指定した [{}->{}]".format(fromPos,toPos))
            return False

        # fromPosの最大のコマが自分のコマかどうかの確認
        if self.getOwner(fromPos) != side:
            print("所持していない位置からは移動できない [{} : {}]".format(fromPos,self.getOwner(fromPos)))
            return
        
        if side == 0:
            state = self.__field[fromPos] >> 3
        else:
            state = self.__field[fromPos] & 0b000111
        if state >> 2 == 1:
            size = 2
        elif state >> 1 == 1:
            size = 1
        else:
            size = 0
        
        print(size)

        # fromPosのコマをtoPosにおけるかの確認
        self.chk_pos(size,toPos)
        
        # サイズを6bitへ変換
        tmp = self.size2state(side,size)

        # fromPos/toPosのコマの状態を変更
        self.__field[fromPos] -= tmp
        self.__field[toPos] += tmp

        self.judge()

        return True

    def chk_pos(self,size,pos):
        # 指定したposに指定したsize以上のコマが存在するかどうかを確認する
        
        # 指定した位置のコマの状態
        pos_state = self.__field[pos]
        # chk_b : 指定したsize以上の大きさのコマを示すbit
        if size == 0:
            chk_b = 0b111111
        elif size == 1:
            chk_b = 0b110110
        elif size == 2:
            chk_b = 0b100100

        # pos_state と chk_b のビットごとのAND演算をして、すべて0ならおける
        return (pos_state & chk_b) == 0

    def chk_move(self,side,pos):
        # 指定したposの最大のコマが自分のコマかどうかを確認する
        pos_state = self.__field[pos]
        
    def size2state(self,side,size):        
        if side == 0:
            tmp = 0b001000 << size
        elif side == 1:
            tmp = 0b000001 << size
        return tmp

    def getOwner(self,pos):
        player_0 = (0b111000 & self.__field[pos]) >> 3
        player_1 = 0b000111 & self.__field[pos]
        # print("{:06b} {:03b} {:03b}".format(self.__field[pos],player_0,player_1))        
        if player_0 > player_1:
            return 0
        elif player_0 < player_1:
            return 1
        else:
            return -1

    def judge(self):
        # 縦の並びを調べる
        for c in range(3):            
            r0 = self.getOwner(c)
            r1 = self.getOwner(c + 3)
            r2 = self.getOwner(c + 6)
            if (r0 == r1) and (r1 == r2) and(r2==r0) and r0 != -1:                
                self.__winner = r0                
            
        # 横の並びを調べる                
        for r in range(3):
            c0 = self.getOwner(3*r + 0)
            c1 = self.getOwner(3*r + 1)
            c2 = self.getOwner(3*r + 2)
            if (c0 == c1) and (c1 == c2) and(c2==c0) and c0 != -1:                
                self.__winner = c0                
            
        # 斜めの並びを調べる
        tmp0 = self.getOwner(0);    tmp2 = self.getOwner(2)    
        tmp4 = self.getOwner(4)    
        tmp6 = self.getOwner(6);    tmp8 = self.getOwner(8)
        if ((tmp0 == tmp4) and (tmp4 == tmp8) and (tmp8 == tmp0) and tmp4 != -1)or ((tmp2 == tmp4) and (tmp4 == tmp6) and (tmp6 == tmp2) and tmp4 != -1):            
            self.__winner = tmp4            
        

        if self.__winner == None:
            # self.render('owner')
            print("Continue...")
            return False
        else:
            # self.render('owner')            
            print("Winner is side {}".format(self.__winner))
            return True

    def isEnd(self):
        return self.__winner is not None

    def getWinner(self):
        if not self.isEnd():
            print("まだ試合終了していません")
            return -1
        return self.__winner

class GobbletGobblersTest(unittest.TestCase):
    CLS_VAL='none'

    # テストクラスが初期化される際に一度だけ呼ばれる (python2.7以上)
    @classmethod
    def setUpClass(cls):
        if sys.flags.debug: print('> setUpClass method is called.')
        # テストの準備するための重い処理のメソッドを実行
        cls.CLS_VAL = '> setUpClass : initialized!'
        if sys.flags.debug: print(cls.CLS_VAL)

    # テストクラスが解放される際に一度だけ呼ばれる (python2.7以上)
    @classmethod
    def tearDownClass(cls):
        if sys.flags.debug: print('> tearDownClass method is called.')
        # setUpClassで準備したオブジェクトを解放する
        cls.CLS_VAL = '> tearDownClass : released!'
        if sys.flags.debug: print(cls.CLS_VAL)

    # テストメソッドを実行するたびに呼ばれる
    def setUp(self):
        if sys.flags.debug: print(os.linesep + '> setUp method is called.')
        # テストの準備をするための軽い処理を実行
        self.game = GobbletGobblers()

    # テストメソッドの実行が終わるたびに呼ばれる
    def tearDown(self):        
        if sys.flags.debug: print(os.linesep + '> tearDown method is called.')
        # setUpで準備したオブジェクトを解放する
        self.game = None

    def test_initialize(self):
        expected = [0,0,0,0,0,0,0,0,0]
        actual = self.game.getField()
        self.assertEqual(expected,actual)

    def test_put(self):
        self.game.putPiece(0,0,3)        
        self.game.putPiece(0,1,3)
        self.game.putPiece(0,2,3)        
    
    def test_put_on(self):
        self.game.putPiece(0,0,3)        
        self.game.putPiece(0,1,3)
        self.game.putPiece(1,0,3)        
        self.game.putPiece(1,1,3)
        self.game.putPiece(1,2,3)
        self.game.render(mode='row')
    
    def test_render(self):
        self.game.render()
        self.game.render(mode='row')
        self.game.render(mode='No')

    def test_judge(self):
        self.game.putPiece(0,0,0)
        self.game.judge()        
        self.game.putPiece(0,0,1)
        self.game.judge()
        self.game.putPiece(0,1,2)
        self.game.judge()

    
if __name__ == '__main__':
    unittest.main()

